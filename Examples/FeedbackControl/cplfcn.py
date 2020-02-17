def cplfcn(feedforward, children):
	#children[0] is feedforwardCtrl
	#children[1] is sourceSys
	#children[2] is feedbackSys
	#children[3] is ctrlPIDSys
	#children[4] is procUnitSys
	#children[5] is sourceDist
	#children[6] is tfDist
	#children[7] is addDist
	
	cplg = []
	
	#fixed couplings
	cplg.append([children[1],"y / SPR",children[2],"u1 / SPR",""])
	cplg.append([children[2],"y / SPR",children[3],"u / SPR",""])
	cplg.append([children[4],"y / SPR",children[7],"u2 / SPR",""])
	cplg.append([children[7],"y / SPR",children[2],"u2 / SPR",""])
	cplg.append([children[5],"y / SPR",children[6],"u / SPR",""])
	cplg.append([children[6],"y / SPR",children[7],"u1 / SPR",""])
	
	#variable couplings
	if feedforward==0:
		cplg.append([children[3],"y / SPR",children[4],"u / SPR",""])
	elif feedforward==1:
		cplg.append([children[5],"y / SPR",children[0],"u1 / SPR",""])
		cplg.append([children[3],"y / SPR",children[0],"u2 / SPR",""])
		cplg.append([children[0],"y / SPR",children[4],"u / SPR",""])
	
	#return
	return cplg
