def cplfun(pathToRoot, poolTypes, numComInEachPool, parent, children):
    #parent is notebooks or desktops
    #children[i] is notebook_i or desktop_i
    curPoolNum = pathToRoot["_pool"]
    curType = poolTypes[int(curPoolNum)-1]
    curNumCom = numComInEachPool[int(curPoolNum)-1]

    cplg = []
    for i in range(curNumCom):
        if curType == "nb":
            cplg.append([parent,"in1 / SPR",children[i],"in1 / SPR",""])
            cplg.append([parent,"in2 / SPR",children[i],"in2 / SPR",""])
            cplg.append([children[i],"out1 / SPR",parent,"out"+str(i+1)+" / SPR",""])
        elif curType == "dt":
            cplg.append([parent,"in1 / SPR",children[i],"in1 / SPR",""])
            cplg.append([children[i],"out1 / SPR",parent,"out"+str(i+1)+" / SPR",""])

    #print(cplg)
    return cplg

#test the function -> uncomment the print(... command in line 18 as well
#cplfun({"_pool": "1"},["nb","dt"],[2,3],"notebooks",["notebook_1","notebook_2"])
#cplfun({"_pool": "2"},["nb","dt"],[2,3],"desktops",["desktop_1","desktop_2","desktop_3"])
