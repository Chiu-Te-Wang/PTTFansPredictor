import json
import sys
import time
# boardName	pageNum	indexNewest
# Baseball	5000	5183
# Elephants	3500	3558
# Monkeys	3500	3672
# Lions	3300	3381
# Guardians	3500	3542

boardNameList = ["Baseball", "Elephants", "Monkeys", "Lions", "Guardians"]
def loadData(filename):
	_data = json.loads(open(filename).read())
	return _data

def buildUserDict(userDict, _data, boardName):
	#各版發文數	發文總推數	發文總噓數	發文總->數	各版推文數	各板噓文數	各版->數
	#article	article_g	article_b	article_n	g 			b 			n 			
	# userDict = dict()
	for article in _data:
		_user = article['b_作者'].split(" ")[0] 
		if not _user in userDict:
			userDict[_user] = dict()
		if not boardName in userDict[_user]:
			userDict[_user][boardName] = {'article':0,'article_g':0,'article_b':0,'article_n':0,'g':0,'b':0,'n':0}
		
		userDict[_user][boardName]['article'] += 1
		userDict[_user][boardName]['article_g'] += article['h_推文總數']['g']
		userDict[_user][boardName]['article_b'] += article['h_推文總數']['b']
		userDict[_user][boardName]['article_n'] += article['h_推文總數']['n']
		responses = article['g_推文']
		for res in responses:
			resUser = responses[res]['留言者']
			if not resUser in userDict:
				userDict[resUser] = dict()
			if not boardName in userDict[resUser]:
				userDict[resUser][boardName] = {'article':0,'article_g':0,'article_b':0,'article_n':0,'g':0,'b':0,'n':0}

			if responses[res]['狀態'] == u'噓 ':
				userDict[resUser][boardName]['b'] += 1
			elif responses[res]['狀態'] == u'推 ':
				userDict[resUser][boardName]['g'] += 1
			else:
				userDict[resUser][boardName]['n'] += 1
	return userDict
def printFeature2File(userDict, filename):
	_file = open(filename, "w")
	json.dump(userDict,_file)
	_file.close()

if __name__ == "__main__":  
	# filename = str(sys.argv[1])
	featureFileOut = str(sys.argv[1])
	dataDir = "../data/"
	filenameList = ['data-Baseball-5000-2017-06-29-03-25-05.json','data-Elephants-3500-2017-06-29-03-30-22.json',
					'data-Monkeys-3500-2017-06-29-03-31-55.json','data-Guardians-3500-2017-06-29-04-12-43.json',
					'data-Lions-3300-2017-06-29-04-11-50.json']
	#python3 extractFeatures.py ../data/userFeatureTest.json
	total_start = time.time()
	_start = time.time()
	userDict = dict()
	for index in range(len(filenameList)):
		print("Loading data from "+boardNameList[index]+" ...")
		_data = loadData(dataDir+filenameList[index])
		print("number of articles : "+str(len(_data)))
		print("Cost time : "+str(time.time()-_start)+" secs")
		_start = time.time()

		print("Building user dict...")
		boardName = boardNameList[index]
		userDict = buildUserDict(userDict, _data, boardName)
		print("Total user number : "+str(len(userDict.keys())))
		print("Cost time : "+str(time.time()-_start)+" secs")
		_start = time.time()

	print("Extract user features...")
	printFeature2File(userDict, featureFileOut)
	print("Cost time : "+str(time.time()-_start)+" secs")
	print("Total cost time : "+str(time.time()-total_start)+" secs")
	_start = time.time()
	
	# for dd in _data:
	# 	print("=====================================")
	# 	print(dd['b_作者'].split(" ")[0])
	# 	print(dd['h_推文總數']['b'])
	# 	print(dd['h_推文總數']['g'])
	# 	print(dd['h_推文總數']['all'])
	# 	res = dd['g_推文']
	# 	goodResList = list()
	# 	BooResList = list()
	# 	neutralResList = list()
	# 	for rr in res:
	# 		if res[rr]['狀態'] == u'噓 ':
	# 			BooResList.append(res[rr]['留言者'])
	# 		elif res[rr]['狀態'] == u'推 ':
	# 			goodResList.append(res[rr]['留言者'])
	# 		else:
	# 			neutralResList.append(res[rr]['留言者'])
	# 	print("噓"+str(BooResList))
	# 	print("推"+str(goodResList))
	# 	print("->"+str(neutralResList))
	# print(_data[0]['c_標題'])
	# print(_data[0]['h_推文總數'])
	# print(_data[0]['g_推文'])