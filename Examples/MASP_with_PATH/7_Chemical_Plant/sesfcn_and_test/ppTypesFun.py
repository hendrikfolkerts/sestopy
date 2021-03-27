def ppTypesFun(pathToRoot, ppTypes):
	"""
	which type a partial plant has
	"""
	#find partial plant
	curNumPP = pathToRoot["_partialPlant"]
	#the value of curNumPP is a string
	curNumPP = int(curNumPP)
	#map to ppTypes -> type of partial plant
	typePP = ppTypes[curNumPP-1]
	return typePP
