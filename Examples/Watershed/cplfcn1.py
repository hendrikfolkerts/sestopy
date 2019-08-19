def cplfcn1(children,parent,NUM):
	#parent is Mountain1
	#children[0] is Estimator
	#children[1] is Areas
	#children[2] is Basin
	#children[3] is UAM2
	
	cplg = []
	
	#fixed couplings
	cplg.append([parent,"in1 / SPR",children[0],"in1 / SPR",""])
	cplg.append([parent,"in2 / SPR",children[0],"in2 / SPR",""])
	cplg.append([parent,"in3 / SPR",children[0],"in3 / SPR",""])
	cplg.append([parent,"in4 / SPR",children[2],"in1 / SPR",""])
	cplg.append([children[0],"out1 / SPR",children[1],"in1 / SPR",""])
	cplg.append([children[1],"out1 / SPR",children[2],"in2 / SPR",""])
	cplg.append([children[2],"out1 / SPR",children[3],"in1 / SPR",""])
	cplg.append([children[3],"out / SPR",parent,"out / SPR",""])
	
	#variable couplings
	if NUM==2:
		cplg.append([children[0],"out2 / SPR",children[1],"in2 / SPR",""])
		cplg.append([children[1],"out2 / SPR",children[3],"in2 / SPR",""])
	
	#return
	return cplg
