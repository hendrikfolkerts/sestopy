def fun(pathToRoot, poolTypes):
	curPoolNum = pathToRoot["_pool"]
	#the return value of pathToRoot["_pool"] is a string
	pooltype = poolTypes[int(curPoolNum)-1]
	#print(pooltype)
	return "MB/" + pooltype

#test the function -> uncomment the print(... command in line 5 as well
#fun({"_pool": "1"},["nb","dt"])
