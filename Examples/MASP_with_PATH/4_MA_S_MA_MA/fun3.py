def fun3(pathToRoot, numOfCores):
	curPoolNum = pathToRoot["_pool"]
	#the return value of pathToRoot["_pool"] is a string
	#either there are notebooks or desktops in the pool
	try:
		curComNum = pathToRoot["_notebook"]
	except:	#if there is an exception, the key does not exist -> desktop computers
		curComNum = pathToRoot["_desktop"]
	#now the current computer number is assigned
	numCores = numOfCores[int(curPoolNum)-1][int(curComNum)-1]
	#print(numCores)
	return numCores

#test the function -> uncomment the print(... command in line 11 as well
#fun3({"_pool": "1", "_desktop": "2"},[[1,2],[1,2,1]])
