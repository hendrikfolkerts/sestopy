def cplfcn(feedforward):
	cplg = []
	
	#fixed couplings
	cplg.append(["sourceSys","y / SPR","feedbackSys","u1 / SPR",""])
	cplg.append(["feedbackSys","y / SPR","ctrlPIDSys","u / SPR",""])
	cplg.append(["procUnitSys","y / SPR","addDist","u2 / SPR",""])
	cplg.append(["addDist","y / SPR","feedbackSys","u2 / SPR",""])
	cplg.append(["sourceDist","y / SPR","tfDist","u / SPR",""])
	cplg.append(["tfDist","y / SPR","addDist","u1 / SPR",""])
	
	#variable couplings
	if feedforward==0:
		cplg.append(["ctrlPIDSys","y / SPR","procUnitSys","u / SPR",""])
	elif feedforward==1:
		cplg.append(["sourceDist","y / SPR","feedforwardCtrl","u1 / SPR",""])
		cplg.append(["ctrlPIDSys","y / SPR","feedforwardCtrl","u2 / SPR",""])
		cplg.append(["feedforwardCtrl","y / SPR","procUnitSys","u / SPR",""])
	
	#return
	return cplg