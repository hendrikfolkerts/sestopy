def cplfcn2(children, parent, NUM):
	#parent is Areas
	#children[0] is Area_1
	#children[1] is Area_2
	
	cplg = []
	
	#variable couplings
	for i in range(0,NUM):
		cplg.append([parent,"in"+str(i+1),children[i],"in",""])
		cplg.append([children[i],"out",parent,"out"+str(i+1),""])
	
	#return
	return cplg