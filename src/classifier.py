import json
import sys
import time
from sklearn import svm
from sklearn.metrics import accuracy_score

boardNameList = ["Baseball", "Elephants", "Monkeys", "Lions", "Guardians"]
fansList = ["中信兄弟","Lamigo桃猿","統一7-11獅","富邦悍將"]
# boardNameList = ["Gossiping"]
featureList = ['article','article_g','article_b','article_n','g','b','n']
emptyFeatureList = [0]*len(featureList)
def loadUserData(filename):
	_data = json.loads(open(filename).read())
	return _data

def loadTrainCase(filename):
	#user\t[0~3]
	_file = open(filename, 'r')
	caseDict = dict()
	lines = _file.readlines()
	for line in lines:
		line = line.strip().split("\t")
		caseDict[line[0]] = int(line[1])
	return caseDict

def buildTestX(userName, userDict):
	tempTest_X = list()
	if not userName in userDict:
		tempTest_X += emptyFeatureList*len(boardNameList)
		# print(userName+" not in database.")
	else:
		for board in boardNameList:
			if board in userDict[userName]:
				for feature in featureList:
					tempTest_X.append(userDict[userName][board][feature])	
			else:
				tempTest_X += emptyFeatureList
	return tempTest_X

if __name__ == "__main__":  
	userDataFile = str(sys.argv[1])
	trainCaseFile = str(sys.argv[2])
	testCaseFile = str(sys.argv[3])
	#python3 classifier.py ../data/userFeatureTest.json ../data/trainCase.txt ../data/testCase.txt
	#python3 classifier.py ../data/userFeatureTest.json ../data/trainCase.txt ../data/trainCase.txt
	total_start = time.time()
	_start = time.time()

	print("Loading data...")
	userDict = loadUserData(userDataFile)
	print("number of users : "+str(len(userDict.keys())))
	trainCaseDict = loadTrainCase(trainCaseFile)
	testCaseDict = loadTrainCase(testCaseFile)
	print("number of train cases : "+str(len(trainCaseDict.keys())))
	print("number of test cases : "+str(len(testCaseDict.keys())))
	print("Cost time : "+str(time.time()-_start)+" secs")
	_start = time.time()


	print("loading training data features...")
	train_X = list()
	train_Y = list()
	for trainCase in trainCaseDict:
		tempTrain_X = list()
		if not trainCase in userDict:
			continue

		for board in boardNameList:
			if board in userDict[trainCase]:
				for feature in featureList:
					tempTrain_X.append(userDict[trainCase][board][feature])	
			else:
				tempTrain_X += emptyFeatureList
		train_X.append(list(tempTrain_X))
		train_Y.append(trainCaseDict[trainCase])
	print("number of train cases : "+str(len(train_Y)))
	print("Cost time : "+str(time.time()-_start)+" secs")
	_start = time.time()

	print("loading testing data features...")
	test_X = list()
	test_Y = list()
	for testCase in testCaseDict:
		test_Y.append(testCaseDict[testCase])
		tempTest_X = buildTestX(testCase, userDict)
		test_X.append(tempTest_X)
	print("number of test cases : "+str(len(test_Y)))
	print("Cost time : "+str(time.time()-_start)+" secs")
	_start = time.time()

	print("Train classifier...")
	lin_clf = svm.LinearSVC()
	lin_clf.fit(train_X, train_Y)
	resultsTrain = lin_clf.predict(train_X)
	resultsTest = lin_clf.predict(test_X)
	print("Train Accuracy : "+str(accuracy_score(train_Y, resultsTrain)))
	print("Test Accuracy : "+str(accuracy_score(test_Y, resultsTest)))
	# print("Feature importance:")
	# print(lin_clf.coef_)
	print("Cost time : "+str(time.time()-_start)+" secs")
	_start = time.time()
	print("Total cost time : "+str(time.time()-total_start)+" secs")

	while 1:
		userName = input('要查詢的使用者名稱 : ')
		userName = userName.strip()
		tempTest_X = buildTestX(userName, userDict)
		result = lin_clf.predict([tempTest_X])
		print(userName+" 是 "+fansList[result[0]]+" 球迷\n")



