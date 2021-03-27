def cpNumFun(pathToRoot, ppTypes, cpNum):
	"""
	the number of chemical productions of one partial plant
	"""
	#find partial plant
	curNumPP = pathToRoot["_partialPlant"]
	#the value of curNumPP is a string
	curNumPP = int(curNumPP)
	#map to ppTypes -> type of partial plant
	typePP = ppTypes[curNumPP-1]
	#when "chemical productions" find out how many
	#single "chemical production"s
	if typePP == "cp":
		#find out which index the "cp" is in the list
		#find all occurrences of "cp" first
		all_occurrences_cp = []
		last_found_index = -1
		element_found = True
		while element_found:
			try:
				last_found_index = ppTypes.index("cp", last_found_index + 1)
				all_occurrences_cp.append(last_found_index)
			except ValueError:
				element_found = False
		#all_occurrences_cp now holds a list of the indices with "cp"
		#find out at which place in all_occurrences_cp the current curNumPP is
		indexOfCurNumPP = all_occurrences_cp.index(curNumPP-1)
		#now map to the list with the number of chemical productions cpNum
		numCP = cpNum[indexOfCurNumPP]
		return numCP
	else:
		return 1
