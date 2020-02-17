def fun2(pathToRoot, numComInEachPool):
	curPoolNum = pathToRoot["_pool"]
	#the return value of pathToRoot["_pool"] is a string
	numCom = numComInEachPool[int(curPoolNum)-1]
	#print(numCom)
	return numCom

#test the function -> uncomment the print(... command in line 5 as well
#fun2({"_pool": "1"},[2,3])
