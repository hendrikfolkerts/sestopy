def cplfcn(feedforward):
	cplg = []
	
	#fixed couplings
	cplg.append(["sourceSys","y","feedbackSys","u1",""])
	cplg.append(["feedbackSys","y","ctrlPIDSys","u",""])
	cplg.append(["procUnitSys","y","addDist","u2",""])
	cplg.append(["addDist","y","feedbackSys","u2",""])
	cplg.append(["sourceDist","y","tfDist","u",""])
	cplg.append(["tfDist","y","addDist","u1",""])
	
	#variable couplings
	if feedforward==0:
		cplg.append(["ctrlPIDSys","y","procUnitSys","u",""])
	elif feedforward==1:
		cplg.append(["sourceDist","y","feedforwardCtrl","u1",""])
		cplg.append(["ctrlPIDSys","y","feedforwardCtrl","u2",""])
		cplg.append(["feedforwardCtrl","y","procUnitSys","u",""])
	
	#return
	return cplg