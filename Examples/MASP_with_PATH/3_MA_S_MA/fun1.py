def fun1(pathToRoot, poolTypes):
	curPoolNum = pathToRoot["_pool"]
	#the return value of pathToRoot["_pool"] is a string
	pooltype = poolTypes[int(curPoolNum)-1]
	#print(pooltype)
	return pooltype

#test the function -> uncomment the print(... command in line 5 as well
#fun1({"_pool": "1"},["nb","dt"])
