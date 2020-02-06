# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *

from copy import deepcopy
from copy import copy

from pg_SemanticConditions import *
from pn_aspectrule import *
from pn_specrule import *
from pn_attributes import *
from pn_number_replication import *
from pn_coupling import *

#needed for pruning without the editor
from json_json import *
from te_TreeNode import *

class Prune:

    #constructor
    def __init__(self):
        self.main = ""
        self.paths = ""
        self.nodelist = ""
        self.sespeslist = ""
        self.sesvarlist = ""
        self.semconlist = ""

    #the main function for pruning
    def pruneMain(self, sesfile="", sesvariableslist="", pesfile="", editor=False, main=None):
        datafound = False
        #get the lists or create them
        nodelist = []
        sespeslist = []
        sesvarlist = []
        semconlist = []
        sesfunlist = []
        paths = []
        if editor:
            # if the prune function was called using the editor
            self.main = main

            #tree and sesvarlist (sesvarlist shall be inserted in the pruned tree)
            nodelist = deepcopy(self.main.modellist[self.main.activeTab][3].treeToList())   #make sure, it is a copy
            sespeslist = self.main.modellist[self.main.activeTab][0].outputSesPes()
            sesvarlist = self.main.modellist[self.main.activeTab][1].outputSesVarList()
            semconlist = self.main.modellist[self.main.activeTab][4].outputSemCondList()
            sesfunlist = self.main.modellist[self.main.activeTab][2].outputSesFunList()
            #since the editor was used for pruning the findPaths function in te_TreeManipulate can be used
            pathsOriginal = self.main.modellist[self.main.activeTab][3].findPaths()
            paths = deepcopy(pathsOriginal)

            #the necessary data was found
            datafound = True
        else:
            #the prune function was called not using the editor
            try:
                #read the file
                f = open(sesfile, "r")
                istOkay, nodelist, sespeslist, sesvarlist, semconlist, selconlist, sesfunlist, loadtime = fromJSON(f.read())
                f.close()
                #print(istOkay)
                #print('[%s]' % ', '.join(map(str, nodelist)))
                if istOkay:
                    #get the paths -> if the pruning was started not using the graphical editor the findPaths function in te_TreeManipulate.py can not be used
                    paths = self.findPathsFromNodelist(self, nodelist)
                    #convert the SES/PES into a list consisting of ses/pes and the SES comment
                    sespeslist = sespeslist[0]
                    # convert every SES variable into a list consisting of name and value
                    for i in range(len(sesvariableslist)):
                        sesvariableslist[i] = sesvariableslist[i].split("=")
                    #replace the SES variables values if the variable exists in the model (in the sesvarlist)
                    for s in sesvariableslist:
                        for i in range(len(sesvarlist)):
                            if sesvarlist[i][0] == s[0]:
                                sesvarlist[i][1] = s[1]

                    #evaluate the replaced SES variables and functions for the semantic conditions and set it in the paths
                    sc = SemanticConditions     #create object
                    semcontfl = sc.validate(self, sesvarlist, semconlist)    #evaluate the semantic conditions with the new SES variables
                    for i in range(len(semconlist)):           #replace the result with the result for the new SES variables
                        semconlist[i][1] = semcontfl[i]
                    for i in range(len(sesvarlist)):           #make the values of the new SES variables to strings again
                        sesvarlist[i][1] = str(sesvarlist[i][1])

                    #evaluate the replaced SES variables and functions for the aspectrules and set it in the paths
                    #do NOT do if the attribute value contains PATH -> then underscore variables are accessed, which are only assigned when multi-aspects are expanded during pruning
                    for i in range(len(paths)):
                        for j in range(len(paths[i])):
                            node = paths[i][j][0]
                            if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
                                #evaluate the replaced SES variables and functions for the aspectrules
                                ar = Aspectrule     #create object
                                aspruletf = ar.validate(self, sesvarlist, sesfunlist, node, False, paths) #evaluate the aspectrules with the new SES variables
                                if aspruletf != "":
                                    elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[i][j][0].aspectrule[0][2])  #find PATH
                                    elWithQuotPath = re.findall('[\'\"]\\b' + re.escape('PATH') + '\\b[\'\"]', paths[i][j][0].aspectrule[0][2]) #find 'PATH' (with quotes -> string)
                                    #if PATH is a variable or in a function, then the result is not inserted (PATH as variable: there are more PATH than 'PATH' (with quotes -> string))
                                    if len(elWithPath) != 0 and len(elWithPath) > len(elWithQuotPath):
                                        pass
                                    else:
                                        paths[i][j][0].aspectrule[0][3] = aspruletf     #replace the result with the result for the new SES variables

                                nodelist = self.replaceSesVarFunAspr(self, node, nodelist)  #do so in the nodelist

                    for i in range(len(sesvarlist)):    # make the values of the new SES variables to strings again
                        sesvarlist[i][1] = str(sesvarlist[i][1])

                    #evaluate the replaced SES variables and functions for the specrules and set it in the paths
                    #do NOT do if the attribute value contains PATH -> then underscore variables are accessed, which are only assigned when multi-aspects are expanded during pruning
                    for i in range(len(paths)):
                        for j in range(len(paths[i])):
                            node = paths[i][j][0]
                            if node.typeInfo() == "Spec Node":
                                #evaluate the replaced SES variables and functions for the specrules
                                sr = Specrule
                                specruletfl = sr.validate(self, sesvarlist, sesfunlist, node, paths)    #evaluate the specrules with the new SES variables
                                for k in range(len(specruletfl)):
                                    elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[i][j][0].specrule[k][2])   #find PATH
                                    elWithQuotPath = re.findall('[\'\"]\\b' + re.escape('PATH') + '\\b[\'\"]', paths[i][j][0].specrule[k][2])   #find 'PATH' (with quotes -> string)
                                    #if PATH is a variable or in a function, then the result is not inserted (PATH as variable: there are more PATH than 'PATH' (with quotes -> string))
                                    if len(elWithPath) != 0 and len(elWithPath) > len(elWithQuotPath):
                                        pass
                                    else:
                                        paths[i][j][0].specrule[k][3] = specruletfl[k]        #replace the result with the result for the new SES variables

                                nodelist = self.replaceSesVarFunSpecr(self, node, nodelist) #do so in the nodelist

                    for i in range(len(sesvarlist)):    # make the values of the new SES variables to strings again
                        sesvarlist[i][1] = str(sesvarlist[i][1])

                    # the necessary data was found
                    datafound = True
                else:
                    print("Error reading the file containing the SES. Maybe it was created with an old version of this editor?")
            except:
                print("Error reading the file containing the SES. Is it a file created by this editor?")

        #now replace the SES variables and functions with their values and set it in the paths -> this has to be done when pruning using the editor or not

        #in entity nodes -> attributes
        #do NOT do if the attribute value contains PATH -> then underscore variables are accessed, which are only assigned when multi-aspects are expanded during pruning
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                node = paths[i][j][0]
                if node.typeInfo() == "Entity Node":
                    #evaluate the SES variables for the attributes
                    at = Attributes
                    attribres = at.validate(self, sesvarlist, sesfunlist, node, paths)     #evaluate the attributes (replace possible SES variables or functions)
                    for k in range(len(attribres)):
                        elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[i][j][0].attributes[k][1]) #find PATH
                        #elWithQuotPath not needed, since in attributes there is a field showing if it is a variable or a function -> attributes[k][2]
                        #if PATH is a variable or in a function, then the value is not replaced with the result
                        if len(elWithPath) != 0 and paths[i][j][0].attributes[k][2] != "":
                            pass
                        else:
                            paths[i][j][0].attributes[k][1] = attribres[k]  #replace the SES variables or functions with the result
                            paths[i][j][0].attributes[k][2] = ""    #clear the field which indicates whether this is a SES function or SES variable

                    nodelist = self.replaceSesVarFunAttr(self, node, nodelist)   #do so in the nodelist

        for i in range(len(sesvarlist)):    # make the values of the SES variables to strings again
            sesvarlist[i][1] = str(sesvarlist[i][1])

        #in aspect and maspect nodes -> priority
        #do NOT do if the attribute value contains PATH -> then underscore variables are accessed, which are only assigned when multi-aspects are expanded during pruning
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                node = paths[i][j][0]
                if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
                    #evaluate the SES variables for the priority
                    pr = Priority
                    priores, allOk = pr.validate(self, sesvarlist, sesfunlist, node, False, paths)     #evaluate the priority (replace possible SES variables or functions)
                    elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[i][j][0].priority)  #find PATH
                    elWithQuotPath = re.findall('[\'\"]\\b' + re.escape('PATH') + '\\b[\'\"]', paths[i][j][0].priority)  #find 'PATH' (with quotes -> string)
                    #if PATH is a variable or in a function, then the value is not replaced with the result (PATH as variable: there are more PATH than 'PATH' (with quotes -> string))
                    if len(elWithPath) != 0 and len(elWithPath) > len(elWithQuotPath):
                        pass
                    else:
                        #give a warning, that the priority value=1 is taken, if the value in the priority field could not be interpreted
                        if not allOk:
                            QMessageBox.information(None, "Assuming...", "The priority of the node with the name "+paths[i][j][0].name()+" (uid: "+str(paths[i][j][0].getUid())+") does not evaluate to an integer. Assuming a priority value of 1.", QtWidgets.QMessageBox.Ok)
                        paths[i][j][0].priority = priores  #replace the SES variables or functions with the result

                    nodelist = self.replaceSesVarFunPrio(self, node, nodelist)  #do so in the nodelist

        for i in range(len(sesvarlist)):    # make the values of the SES variables to strings again
            sesvarlist[i][1] = str(sesvarlist[i][1])

        #in maspect nodes -> number of replication
        #do NOT do if the attribute value contains PATH -> then underscore variables are accessed, which are only assigned when multi-aspects are expanded during pruning
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                node = paths[i][j][0]
                if node.typeInfo() == "Maspect Node":
                    #evaluate the SES variables for the number of replication
                    nr = NumberReplication
                    numrepres, allOk = nr.validate(self, sesvarlist, sesfunlist, node, False, paths)     #evaluate the number of replication (replace possible SES variables or functions)
                    elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[i][j][0].number_replication)  #find PATH
                    elWithQuotPath = re.findall('[\'\"]\\b' + re.escape('PATH') + '\\b[\'\"]', paths[i][j][0].number_replication)  #find 'PATH' (with quotes -> string)
                    #if PATH is a variable or in a function, then the value is not replaced with the result (PATH as variable: there are more PATH than 'PATH' (with quotes -> string))
                    if len(elWithPath) != 0 and len(elWithPath) > len(elWithQuotPath):
                        pass
                    else:
                        #give a warning, that the numRep value=1 is taken, if the value in the numRep field could not be interpreted
                        if not allOk:
                            QMessageBox.information(None, "Assuming...", "The number of replications of the node with the name "+paths[i][j][0].name()+" (uid: "+str(paths[i][j][0].getUid())+") does not evaluate to an integer. Assuming a number of replications value of 1.", QtWidgets.QMessageBox.Ok)
                        paths[i][j][0].number_replication = numrepres  #replace the SES variables or functions with the result

                    nodelist = self.replaceSesVarFunNumRep(self, node, nodelist)    #do so in the nodelist

        for i in range(len(sesvarlist)):    # make the values of the SES variables to strings again
            sesvarlist[i][1] = str(sesvarlist[i][1])

        #in aspect and maspect nodes -> coupling functions (if there is a function defined for the node) -> after that coupling functions can be handled like couplings defined in the list
        #do NOT do if the attribute value contains PATH -> then underscore variables are accessed, which are only assigned when multi-aspects are expanded during pruning
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                node = paths[i][j][0]
                if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node" and node.coupling and node.coupling[0][6] != "":    #node.coupling[0][6] != "" then a coupling function is defined -> it is defined in the first coupling (there is only one)
                    #if the couplings are defined at all and defined by a function
                    if node.coupling and node.coupling[0][6] != "":
                        #evaluate the SES variables for the coupling functions
                        cg = Coupling
                        coupres, allOk = cg.validate(self, sesvarlist, sesfunlist, node, paths)     #evaluate the coupling function (replace SES variables and functions)
                        elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[i][j][0].coupling[0][6])  #find PATH
                        elWithQuotPath = re.findall('[\'\"]\\b' + re.escape('PATH') + '\\b[\'\"]', paths[i][j][0].coupling[0][6])  #find 'PATH' (with quotes -> string)
                        #if PATH is a variable or in a function, then the value is not replaced with the result (PATH as variable: there are more PATH than 'PATH' (with quotes -> string))
                        if len(elWithPath) != 0 and len(elWithPath) > len(elWithQuotPath):
                            pass
                        else:
                            #give a warning, that they have to be checked again, if they are not okay
                            if not allOk:
                                QMessageBox.information(None, "Warning", "The couplings of the node with the name " + paths[i][j][0].name() + " (uid: " + str(paths[i][j][0].getUid()) + ") have to be checked again.", QtWidgets.QMessageBox.Ok)
                            paths[i][j][0].coupling = coupres   #place the result of the coupling function as if the couplings were defined by a list

                        nodelist = self.replaceSesVarFunCpl(self, node, nodelist)  #do so in the nodelist

        for i in range(len(sesvarlist)):    # make the values of the SES variables to strings again
            sesvarlist[i][1] = str(sesvarlist[i][1])

        #the data is evaluated for the (maybe new) SES variables and the SES functions -> the pruning can be done now
        #-> but the data is NOT evaluated yet, if the rule/attribute/priority/numrep/couplingfunction contains PATH
        #-> then underscore variables are needed, which are only assigned when multi-aspects are expanded during pruning

        #only continue if all data was found
        if datafound:
            #check that the SES starts and ends with entity nodes in all paths
            if self.checkSesNodes(self, paths):
                print("OK - The paths of the tree were found.")
                # check if SES variables are okay (check semantic conditions)
                if self.checkSesVar(self, semconlist):
                    print("OK - The semantic conditions are okay.")

                    #add a field to express if the node stays in the pruned tree
                    #and a field containing the original depth (make a copy of the depth since the depth can be changed by pruning an specialization node)
                    for i in range(len(nodelist)):
                        nodelist[i].append(True)
                        nodelist[i].append(copy(nodelist[i][12]))
                    #print("fields added")

                    #now prune and return the nodelist and what it is now (incompletely pruned PES or PES)
                    nodelist, sespestype = self.prune(self, nodelist, paths, sesvarlist, sesfunlist)
                    print("OK - The pruning is done successfully.")

                    #build the new information for the PES -> the type of the PES (incompletely pruned PES or PES) from the prune function and the description from the SES
                    sespes = [sespestype, sespeslist[1]]

                    #remove the disabled nodes and remove the field to indicate they are disabled
                    self.removeDisabledNodesFromNodelist(self, nodelist)

                    #remove the two fields added before
                    for i in range(len(nodelist)):
                        del nodelist[i][14]
                        del nodelist[i][13]
                    #print("fields removed")

                    # if the prune function is called using the editor it is necessary to insert the pruned SES into a model else it has to written to a file
                    if editor:
                        #the prune function was called using the editor
                        self.insertInModel(self, nodelist, sesvarlist, [sespes], self.main)
                    else:
                        #the prune function was called not using the editor
                        filestr = toJSON(nodelist, sespes, sesvarlist, [], [], [])
                        #write
                        f = open(pesfile, "w")
                        f.write(filestr)
                        # close
                        f.close()
                else:
                    if editor:
                        QMessageBox.information(None, "Cannot prune", "At least one SES variable violates the semantic conditions.", QtWidgets.QMessageBox.Ok)
                    else:
                        print("Not OK - At least one SES variable violates the semantic conditions!")
            else:
                if editor:
                    QMessageBox.information(None, "Cannot prune", "The tree is empty or does not end with an entity node in all paths. Please edit the tree.", QtWidgets.QMessageBox.Ok)
                else:
                    print("Not OK - The tree is empty or does not end with an entity node in all paths.")
        else:
            if editor:
                QMessageBox.information(None, "Cannot prune", "Not all data could be read.", QtWidgets.QMessageBox.Ok)
            else:
                print("Not OK - Not all data could be read.")

    #get the paths -> if the pruning was started not using the graphical editor the findPaths function in te_TreeManipulate.py can not be used
    def findPathsFromNodelist(self, nodelistFromSave):
        """
        #get the depth in the tree for each node and build a nodelist
        #the depth is not needed since this information is part of the nodelist
        #the path needs a list of node type objects, so this is not needed any more
        nodelist = []
        depth = 0
        for node in nodelistFromSave:
            #first node
            if depth == 0:
                nodelist.append([node, depth])
                depth += 1
            #following nodes
            elif depth >= 1:
                # go through the nodelist and find the name of the parent of the node which shall be inserted
                for nd in nodelist:
                    nodeparent = node.parent()
                    ndname = nd[0].name()
                    if nodeparent == ndname:
                        depth = nd[1] + 1
                        nodelist.append([node, depth])
                        break
        """
        #create list of node objects from nodelist
        nodelist = []
        firstnode = Node(0, "SES")

        for node in nodelistFromSave:
            nodetype = node[1]
            nodeobject = None
            try:
                depth = int(node[14])   #take the copied depth -> for the paths the original depth is relevant
            except:
                depth = int(node[12])   #for pruning without editor: paths shall be taken after reading the file, but the depth is not copied then -> so take original depth
            if nodetype == "Entity Node":
                bold = False
                if node[5] == "True":
                    bold = True
                nodeobject = EntityNode(int(node[0]), node[2], None, node[4], bold, node[6])
            elif nodetype == "Descriptive Node":  #maybe not needed since pruning can not be done with general descriptive nodes
                bold = False
                if node[5] == "True":
                    bold = True
                nodeobject = DescriptiveNode(int(node[0]), node[2], None, node[4], bold)
            elif nodetype == "Aspect Node":
                bold = False
                if node[5] == "True":
                    bold = True
                nodeobject = AspectNode(int(node[0]), node[2], None, node[4], bold, node[7], node[8], node[11])
            elif nodetype == "Maspect Node":
                bold = False
                if node[5] == "True":
                    bold = True
                nodeobject = MaspectNode(int(node[0]), node[2], None, node[4], bold, node[7], node[8], node[9], node[11])
            elif nodetype == "Spec Node":
                bold = False
                if node[5] == "True":
                    bold = True
                nodeobject = SpecNode(int(node[0]), node[2], None, node[4], bold, node[10])
            nodelist.append([nodeobject, depth])

            #now the parent node for the current node has to be set
            # first node
            if depth == 0:
                nodelist[0][0].setParent(firstnode)
            else:   #other nodes
                nodeuid = node[0]
                nodeparentuid = node[3]
                parentnode = None
                #get the parentnode
                for i in range(len(nodelist)):
                    if str(nodelist[i][0].getUid()) == nodeparentuid:
                        parentnode = nodelist[i][0]
                        break
                #set the parentnode
                for i in range(len(nodelist)):
                    if str(nodelist[i][0].getUid()) == nodeuid and parentnode != None:
                        nodelist[i][0].setParent(parentnode)
                        break

            #now the current node must be inserted as child for its parent
            for i in range(len(nodelist)):
                #if the parent of the current node equals the name of nodelist[i][0], it is a child
                if node[3] == str(nodelist[i][0].getUid()):
                    nodelist[i][0].addChild(nodeobject)

        #now find the paths
        paths = []
        while len(nodelist) > 0:
            i = 0
            while i < len(nodelist) - 1 and nodelist[i][1] < nodelist[i + 1][1]:    #nodelist[i][1] <= nodelist[i + 1][1] is the condition if brother nodes shall be seen in the same path
                i += 1
            paths.append(nodelist[0:i + 1])
            # delete the part of the tree
            toremove = []
            j = i
            while (i == len(nodelist) - 1 or nodelist[j][1] >= nodelist[i + 1][1]) and j >= 0:
                toremove.append(nodelist[j])
                j -= 1
            for rm in toremove:
                nodelist.remove(rm)
        return paths

    #aspectrules: replace the interpreted SES variables and functions in the nodelist according to the node in paths
    def replaceSesVarFunAspr(self, nd, nodelist):
        uid = nd.getUid()
        for i in range(len(nodelist)):
            if str(uid) == nodelist[i][0]:
                nodelist[i][7] = nd.aspectrule
        return nodelist

    #specrules: replace the interpreted SES variables and functions in the nodelist according to the node in paths
    def replaceSesVarFunSpecr(self, nd, nodelist):
        uid = nd.getUid()
        for i in range(len(nodelist)):
            if str(uid) == nodelist[i][0]:
                nodelist[i][10] = nd.specrule
        return nodelist

    #attributes: replace the interpreted SES variables and functions in the nodelist according to the node in paths
    def replaceSesVarFunAttr(self, nd, nodelist):
        uid = nd.getUid()
        for i in range(len(nodelist)):
            if str(uid) == nodelist[i][0]:
                nodelist[i][6] = nd.attributes
        return nodelist

    #priority: replace the interpreted SES variables and functions in the nodelist according to the node in paths
    def replaceSesVarFunPrio(self, nd, nodelist):
        uid = nd.getUid()
        for i in range(len(nodelist)):
            if str(uid) == nodelist[i][0]:
                nodelist[i][11] = nd.priority
        return nodelist

    #number of replication: replace the interpreted SES variables and functions in the nodelist according to the node in paths
    def replaceSesVarFunNumRep(self, nd, nodelist):
        uid = nd.getUid()
        for i in range(len(nodelist)):
            if str(uid) == nodelist[i][0]:
                nodelist[i][9] = nd.number_replication
        return nodelist

    #coupling: replace the interpreted SES variables and functions in the nodelist according to the node in paths
    def replaceSesVarFunCpl(self, nd, nodelist):
        uid = nd.getUid()
        for i in range(len(nodelist)):
            if str(uid) == nodelist[i][0]:
                nodelist[i][8] = nd.coupling
        return nodelist

    #an SES has to start and end with entity nodes
    def checkSesNodes(self, paths):
        endWithEntity = False
        for nd in paths:
            if nd[len(nd)-1][0].typeInfo() == "Entity Node":
                endWithEntity = True
        return endWithEntity

    #check the SES variables if they fit the semantic conditions
    def checkSesVar(self, semconlist):
        #look at the element in the second column -> has to be T or nothing (SES var not specified)
        scok = True
        for el in semconlist:
            tf = el[1]
            if tf == "F":
                scok = False
                break
        return scok

    #find nodes from paths in nodelist and remove the disabled ones
    def removeDisabledNodesFromNodelist(self, nodelist):
        indicesToRemove = []
        for i in range(len(nodelist)):
            if nodelist[i][13] == False:
                indicesToRemove.append(i)
        indicesToRemove = sorted(indicesToRemove, reverse=True)
        for i in indicesToRemove:
            del nodelist[i]

    #insert the processed nodelist and sesvarlist into a new model
    def insertInModel(self, nodelist, sesvarlist, sespes, main):
        while True:
            num, ok = QInputDialog.getInt(None, "Model for the PES", "In which model different from the current model do you want to insert the PES? Please enter an integer from 1 to 10.")
            if (num - 1) == self.main.activeTab:
                QMessageBox.information(None, "Cannot insert", "The model you selected is the current model.", QtWidgets.QMessageBox.Ok)
            if ((num - 1) != self.main.activeTab) and num >= 1 and num <= 10:
                break
            if ok == False:
                break
        #change the tab to the tab with the pruned tree
        main.tabs.setCurrentIndex(num - 1)
        if ok:
            #check if model is empty
            isemptymodel = False
            nodel = self.main.modellist[(num-1)][3].treeToList()
            svl = self.main.modellist[(num-1)][1].outputSesVarList()
            smcl = self.main.modellist[(num-1)][4].outputSemCondList()
            slcl = self.main.modellist[(num - 1)][5].outputSelConsList()
            sfl = self.main.modellist[(num - 1)][2].outputSesFunList()
            if len(nodel) == 1 and nodel[0][1] == 'Node' and nodel[0][2] == 'SES' and nodel[0][3] == 'None' and len(svl) == 0 and len(smcl) == 0 and len(slcl) == 0 and len(sfl) == 0:
                isemptymodel = True
            empty = False
            if not isemptymodel:
                reply = QMessageBox.question(None, 'Empty Model', "Are you sure you want to empty the model number " + str(num) + " in order to insert the pruned model?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    empty = self.main.emptyCurrentModel(True, (num-1))
            if empty or isemptymodel:
                self.main.modellist[(num - 1)][3].fromSave(nodelist)
                self.main.modellist[(num - 1)][0].fromSave(sespes)
                #make the sesvars to strings again, then import
                for svarl in range(len(sesvarlist)):
                    for svl in range(len(sesvarlist[svarl])):
                        sesvarlist[svarl][svl] = str(sesvarlist[svarl][svl])
                self.main.modellist[(num - 1)][1].fromSave(sesvarlist)
                #it cannot be an SES anymore
                if sespes[0] == "ipes":
                    self.main.modellist[(num - 1)][0].rbses.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbipes.setChecked(True)
                    self.main.modellist[(num - 1)][0].rbpes.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbfpes.setChecked(False)
                elif sespes[0] == "pes":
                    self.main.modellist[(num - 1)][0].rbses.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbipes.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbpes.setChecked(True)
                    self.main.modellist[(num - 1)][0].rbfpes.setChecked(False)







    #all functions for pruning------------------------------------------------------------------------------------------

    #the pruning function
    def prune(self, nodelist, paths, sesvarlist, sesfunlist):
        #go through paths and prune -> change the nodelist according to the information given in the nodes in the paths
        sespestype = "pes"
        nodeUidsPruned = [] #a list of nodeuids which are pruned already so that no node is pruned twice

        #create a dictionary where to every uid the index of the nodelist is placed (then the nodelist does not have to be travelled for finding the corresponding index to an uid)
        uidIndexDict = {}
        for n in range(len(nodelist)):
            uidIndexDict.update({nodelist[n][0]: n})

        #go through paths
        lenpaths = len(paths)
        el = 0
        while el < lenpaths:
            lenpathsel = len(paths[el]) #needed to do so since for a Maspect node the length can be changed
            nd = 0
            while nd < lenpathsel:
                nodeUidsPruned, paths, nodelist, lenpaths, changeSesPes, uidIndexDict = self.findDoPruning(self, nodeUidsPruned, paths, el, nd, nodelist, lenpaths, uidIndexDict, sesvarlist, sesfunlist)
                #if the pruning of this just taken node was not successful changeSesPes will be True saying the SES could not be pruned completely at this node
                if changeSesPes:
                    sespestype = "ipes"
                nd += 1
            el += 1

        return nodelist, sespestype

    #decide which pruning to take and do it
    def findDoPruning(self, nodeUidsPruned, paths, el, nd, nodelist, lenpaths, uidIndexDict, sesvarlist, sesfunlist):
        #set this variable to True if no decision could be made or an error occured -> so the SES cannot be pruned completely
        couldNotPrune = []
        #only if this node is not already excluded (children of the pruned nodes are not in nodeUidsPruned so this cannot be taken)
        if self.nodeInPesValue(self, paths[el][nd][0], nodelist, uidIndexDict):
            # find type
            nodetype = paths[el][nd][0].typeInfo()
            # find brothers
            pathsbrothers = self.findBrothers(self, paths[el][nd][0])
            # find brothers in the nodelist since by pruning (which is made by changing the nodelist) the brothers can have changed
            nodelistbrotherindices = self.findBrothersInNodelist(self, paths[el][nd][0].getUid(), nodelist, uidIndexDict)

            if nodetype == "Entity Node":
                # calculate attributes with PATH
                nodelist = self.calcAttWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # for an entity node no decision has to be made

            elif nodetype == "Aspect Node" and (paths[el][nd][0].getUid() not in nodeUidsPruned):
                # calculate aspectrules with PATH
                nodelist = self.calcAsrWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist, uidIndexDict)
                # calculate priority with PATH
                nodelist = self.calcPrioWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # calculate couplings with PATH
                nodelist = self.calcCoupWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # now make the decisions

                # pruning pattern 1 - if the node is an aspect node and there is no brother at all there is nothing to do, the node stays in the tree
                if len(pathsbrothers) == 1 and len(nodelistbrotherindices) == 1:  # the brothers can be of any type
                    pass
                # there are brothers (can be of any type)
                else:
                    # pruning pattern 7 - look if there are brothers of the type specialization - they have to be pruned before
                    for b in range(len(pathsbrothers)):  # go through the brothers and look whether there is a Spec Node -> if there is, prune it
                        if pathsbrothers[b].typeInfo() == "Spec Node" and (pathsbrothers[b].getUid() not in nodeUidsPruned):
                            ele, nde = self.findNodeUidInPaths(self, pathsbrothers[b].getUid(), paths)
                            paths, nodelist, noSpecruleInfo = self.pruneSpec(self, paths, ele, nde, nodelist, uidIndexDict)
                            if noSpecruleInfo:
                                couldNotPrune.append(True)
                                QMessageBox.information(None, "Cannot find a decision", "The node with the name " + paths[el][nd][0].name() + " (uid " + str(paths[el][nd][0].getUid()) + ") has no specrule. No child is taken.", QtWidgets.QMessageBox.Ok)
                            nodeUidsPruned.append(pathsbrothers[b].getUid())

                    # pruning pattern 8 (including 2) - if there are 2 or more brothers of the type aspect or maspect
                    # they have to be pruned either with pruning pattern 2 or pruning pattern 8 (priority pruning)
                    # after resolving the specnodes the number of aspect / maspect brothers can have changed -> get a new list (there are no more specnodes inside)
                    nodelistbrotherindices = self.findBrothersInNodelist(self, paths[el][nd][0].getUid(), nodelist, uidIndexDict)
                    # since all specnodes on this layer are resolved before the number of aspect and maspect brothers is the length of nodelistbrotherindices
                    numberAspectBrothers = len(nodelistbrotherindices)
                    # pruning pattern 1
                    if numberAspectBrothers == 1:  # if number of aspectbrothers == 1 there is nothing to do
                        pass
                    # pruning pattern 2 or 8
                    elif numberAspectBrothers > 1:  # if number of aspectbrothers > 1 go on -> it needs to be checked if pruning can be done by aspectrules or priority is needed
                        # look how the situation on the layer is -> how many aspectrules result to "T", to "T -> F" and to "F"
                        # and how many nodes got to this layer by resolving a specnode (the depth differs from the original depth in the SES)
                        numberAspectruleTrue = 0
                        numberAspectruleTF = 0
                        numberAspectruleFalse = 0
                        numberArOnThisLayerByResolvingSpecnode = 0
                        #create a dictionary in which the old and the new depth of a node are saved: new depth is key, old depth is value
                        newOldDepthDict = {}
                        #now go through nodes
                        for ni in nodelistbrotherindices:
                            if len(nodelist[ni][7]) != 0 and nodelist[ni][7][0][3] == "T":
                                numberAspectruleTrue += 1
                            if len(nodelist[ni][7]) != 0 and nodelist[ni][7][0][3] == "T -> F":
                                numberAspectruleTF += 1
                            if len(nodelist[ni][7]) != 0 and nodelist[ni][7][0][3] == "F":
                                numberAspectruleFalse += 1
                            if nodelist[ni][12] != nodelist[ni][14]:    #if the depth is changed -> a specnode was resolved
                                oldDepth = newOldDepthDict.get(nodelist[ni][12])    #but if aspect / multi-aspect nodes were brothers in the SES as well, they both have the same entries for old and new depth -> get the old depth of the current node
                                if not oldDepth:    #if there is no node with the entry for new depth as the current node -> make entry
                                    newOldDepthDict.update({nodelist[ni][12]: nodelist[ni][14]})
                                    numberArOnThisLayerByResolvingSpecnode += 1
                                else:   #if there is a node with the entry for the new depth as the current node, check if the old depth fit as well
                                    if oldDepth == nodelist[ni][14]:    #if old depth and new depth fit, the nodes were brothers in the SES -> not by resolving specnodes
                                        numberArOnThisLayerByResolvingSpecnode -= 1
                                    else:                               #if the old depth and new depth do not fit, they became brothers by resolving a specnode
                                        numberArOnThisLayerByResolvingSpecnode += 1

                        # prepare a text with name and uid for the nodes on one layer -> for possible error messages
                        nodesOnOnelayerText = "\n"
                        for bi in nodelistbrotherindices:
                            nodesOnOnelayerText = nodesOnOnelayerText + nodelist[bi][2] + " (uid " + nodelist[bi][0] + ")\n"

                        # decide whether it is possible to prune and if so whether to use aspectrules or priority
                        pruningPossible = False
                        pruneWithPriority = False
                        # if all nodes were on the same layer in the SES and exactly one aspectrule results to "T" -> use pruning by aspectrules (pattern 2)
                        if numberArOnThisLayerByResolvingSpecnode == 0 and numberAspectruleTrue == 1:
                            pruningPossible = True
                        # if all nodes were on the same layer in the SES and the aspectrules result to "T -> F" because more than 1 aspectrule results to "T" -> no pruning possible
                        elif numberArOnThisLayerByResolvingSpecnode == 0 and numberAspectruleTF > 0:
                            couldNotPrune.append(True)
                            QMessageBox.information(None, "Cannot find a decision", "The nodes" + nodesOnOnelayerText + "are on the same layer. A decision by aspectrules cannot be made since more than one aspectrule evaluates to true. All children are inserted.", QtWidgets.QMessageBox.Ok)
                        # if all nodes were on the same layer in the SES and the aspectrules all result to "F" -> no pruning possible
                        elif numberArOnThisLayerByResolvingSpecnode == 0 and numberAspectruleFalse == numberAspectBrothers:
                            couldNotPrune.append(True)
                            QMessageBox.information(None, "Cannot find a decision", "The nodes" + nodesOnOnelayerText + "are on the same layer. A decision by aspectrules cannot be made since the aspectrules for all children evaluate to false. All children are inserted.", QtWidgets.QMessageBox.Ok)
                        # if all nodes were on the same layer in the SES and there are not aspectrules for all nodes -> no pruning possible
                        elif numberArOnThisLayerByResolvingSpecnode == 0 and (numberAspectruleTrue + numberAspectruleTF + numberAspectruleFalse) != numberAspectBrothers:
                            couldNotPrune.append(True)
                            QMessageBox.information(None, "Cannot find a decision", "The nodes" + nodesOnOnelayerText + "are on the same layer. A decision by aspectrules cannot be made since not for all nodes on this layer an aspectrule is defined. All children are inserted.", QtWidgets.QMessageBox.Ok)
                        # if nodes got to this layer by resolving a specnode -> priority pruning
                        elif numberArOnThisLayerByResolvingSpecnode > 0:
                            pruningPossible = True
                            pruneWithPriority = True

                        # do the pruning with aspectrules (pattern 2) or priority pruning (pattern 8)
                        if pruningPossible and not pruneWithPriority:
                            # pruning pattern 2
                            nodelist = self.pruneAspect(self, paths, el, nd, nodelist, False, uidIndexDict)
                            nodeUidsPruned.append(paths[el][nd][0].getUid())
                        elif pruningPossible and pruneWithPriority:
                            # pruning pattern 8
                            nodelist, prunedUids, cannotPriorityPrune = self.pruneAspectWithPriority(self, paths, nodelist, nodelistbrotherindices, uidIndexDict)
                            if cannotPriorityPrune:
                                couldNotPrune.append(True)
                                QMessageBox.information(None, "Cannot find a decision", "The nodes" + nodesOnOnelayerText + "are on the same layer. A decision by aspectrules could not be made and the highest priority equals a brother. All children are inserted.", QtWidgets.QMessageBox.Ok)
                            nodeUidsPruned = nodeUidsPruned + prunedUids

            elif nodetype == "Spec Node" and (paths[el][nd][0].getUid() not in nodeUidsPruned):
                # calculate specrules with PATH
                self.calcSpeWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # now make the decisions

                # pruning pattern 3, 4, 5, 6
                paths, nodelist, noSpecruleInfo = self.pruneSpec(self, paths, el, nd, nodelist, uidIndexDict)
                if noSpecruleInfo:
                    couldNotPrune.append(True)
                    QMessageBox.information(None, "Cannot find a decision", "In the node with the name " + paths[el][nd][0].name() + " (uid " + str(paths[el][nd][0].getUid()) + ") no decision by specrules can be made. No child is taken.", QtWidgets.QMessageBox.Ok)
                nodeUidsPruned.append(paths[el][nd][0].getUid())

            elif nodetype == "Maspect Node" and (paths[el][nd][0].getUid() not in nodeUidsPruned):
                # calculate aspectrules with PATH
                nodelist = self.calcAsrWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist, uidIndexDict)
                # calculate priority with PATH
                nodelist = self.calcPrioWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # calculate couplings with PATH
                nodelist = self.calcCoupWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # calculate numrep with PATH
                nodelist = self.calcNrepWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist)
                # now make decisions
                # the underscore variables in PATH are assigned in the pruneMaspect function

                # pruning pattern 9
                paths, nodelist, uidIndexDict = self.pruneMaspect(self, paths, el, nd, nodelist, nodeUidsPruned, lenpaths, uidIndexDict, sesvarlist, sesfunlist)
                lenpaths = len(paths)  # new paths are added, so the variable needs to be updated
                # lenpathsel = len(paths[el])    #the existing path length are not changed, so this is not needed
                nodeUidsPruned.append(paths[el][nd][0].getUid())

        couldNotPrune = any(couldNotPrune)

        return nodeUidsPruned, paths, nodelist, lenpaths, couldNotPrune, uidIndexDict

    #calculate attributes with PATH
    def calcAttWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist):
        at = Attributes
        attribres = at.validate(self, sesvarlist, sesfunlist, paths[el][nd][0], paths)  # evaluate the attributes with the PATH (replace possible SES variables or functions)
        for k in range(len(attribres)):
            paths[el][nd][0].attributes[k][1] = attribres[k]  # replace the SES variables or functions with the result
            paths[el][nd][0].attributes[k][2] = ""  # clear the field which indicates whether this is a SES function or SES variable
        nodelist = self.replaceSesVarFunAttr(self, paths[el][nd][0], nodelist)
        return nodelist

    #calculate aspecrules with PATH
    def calcAsrWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist, uidIndexDict):
        ar = Aspectrule
        aspruletf = ar.validate(self, sesvarlist, sesfunlist, paths[el][nd][0], False, paths)  # evaluate the aspectrules with the PATH
        if aspruletf != "":
            paths[el][nd][0].aspectrule[0][3] = aspruletf  # replace the result with the calculated result
            if aspruletf == "F":
                nodelist = self.nodeNotInPes(self, paths[el][nd][0], nodelist, uidIndexDict)  # deactivate the not selected node and the children below
                nodelist = self.childrenNotInPes(self, paths[el][nd][0], paths, nodelist, uidIndexDict)
        nodelist = self.replaceSesVarFunAspr(self, paths[el][nd][0], nodelist)  # do so in the nodelist
        return nodelist

    #calculate specrules with PATH
    def calcSpeWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist):
        sr = Specrule
        specruletfl = sr.validate(self, sesvarlist, sesfunlist, paths[el][nd][0], paths)  # evaluate the specrules with the PATH
        for k in range(len(specruletfl)):
            paths[el][nd][0].specrule[k][3] = specruletfl[k]  # replace the result with the result for the new SES variables
        nodelist = self.replaceSesVarFunSpecr(self, paths[el][nd][0], nodelist)  # do so in the nodelist
        return nodelist

    #calculate priority with PATH
    def calcPrioWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist):
        pr = Priority
        priores, allOk = pr.validate(self, sesvarlist, sesfunlist, paths[el][nd][0], False, paths)  # evaluate the priority with the PATH (replace possible SES variables or functions)
        elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[el][nd][0].priority)  #find PATH, if it is still there
        if len(elWithPath) != 0:
            # give a warning, that the priority value=1 is taken, if the value in the priority field could not be interpreted
            if not allOk:
                QMessageBox.information(None, "Assuming...", "The priority of the node with the name " + paths[el][nd][0].name() + " (uid: " + str(paths[el][nd][0].getUid()) + ") does not evaluate to an integer. Assuming a priority value of 1.", QtWidgets.QMessageBox.Ok)
            paths[el][nd][0].priority = priores  # replace the SES variables or functions with the result
            nodelist = self.replaceSesVarFunPrio(self, paths[el][nd][0], nodelist)  # do so in the nodelist
        return nodelist

    #calculate couplings with PATH
    def calcCoupWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist):
        if paths[el][nd][0].coupling and paths[el][nd][0].coupling[0][6] != "": #if the couplings are defined at all and defined by a function
            cg = Coupling
            coupres, allOk = cg.validate(self, sesvarlist, sesfunlist, paths[el][nd][0], paths)  # evaluate the coupling function with the PATH (replace SES variables and functions)
            elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[el][nd][0].coupling[0][6])  # find PATH, if it is still there
            if len(elWithPath) != 0:
                # give a warning, that they have to be checked again, if they are not okay
                if not allOk:
                    QMessageBox.information(None, "Warning", "The couplings of the node with the name " + paths[el][nd][0].name() + " (uid: " + str(paths[el][nd][0].getUid()) + ") have to be checked again.", QtWidgets.QMessageBox.Ok)
                paths[el][nd][0].coupling = coupres  # place the result of the coupling function as if the couplings were defined by a list
                nodelist = self.replaceSesVarFunCpl(self, paths[el][nd][0], nodelist)  # do so in the nodelist
        return nodelist

    #calculate numRep with PATH
    def calcNrepWiPath(self, paths, el, nd, nodelist, sesvarlist, sesfunlist):
        nr = NumberReplication
        numrepres, allOk = nr.validate(self, sesvarlist, sesfunlist, paths[el][nd][0], False, paths)  # evaluate the number of replication with the PATH (replace possible SES variables or functions)
        elWithPath = re.findall('\\b' + re.escape('PATH') + '\\b', paths[el][nd][0].number_replication)  # find PATH
        if len(elWithPath) != 0:
            # give a warning, that the numRep value=1 is taken, if the value in the numRep field could not be interpreted
            if not allOk:
                QMessageBox.information(None, "Assuming...", "The number of replications of the node with the name " + paths[el][nd][0].name() + " (uid: " + str(paths[el][nd][0].getUid()) + ") does not evaluate to an integer. Assuming a number of replications value of 1.", QtWidgets.QMessageBox.Ok)
            paths[el][nd][0].number_replication = numrepres  # replace the SES variables or functions with the result
            nodelist = self.replaceSesVarFunNumRep(self, paths[el][nd][0], nodelist)  # do so in the nodelist
        return nodelist

    #prune aspectsiblings (using aspectrules)
    def pruneAspect(self, paths, el, nd, nodelist, deactivateAnyway=False, uidIndexDict=None):
        # check the aspectrule for the node in order to determine whether it is true or false and it stays in the tree or not
        if (not self.checkAspRule(self, paths[el][nd])) or deactivateAnyway:
            nodelist = self.nodeNotInPes(self, paths[el][nd][0], nodelist, uidIndexDict)
            nodelist = self.childrenNotInPes(self, paths[el][nd][0], paths, nodelist, uidIndexDict)

        return nodelist

    #prune aspectsiblings with priority
    def pruneAspectWithPriority(self, paths, nodelist, nodelistbrotherindices, uidIndexDict):
        # pruning pattern 8 -> prune with priority
        prunedUids = []
        prioritylist = []
        cannotPriorityPrune = False
        for ni in nodelistbrotherindices:
            prioritylist.append([ni, int(nodelist[ni][11])])  # prioritylist: [index in nodelist, priority]
            # sort for priority -> highest priority first
            prioritylist = sorted(prioritylist, key=lambda x: x[1], reverse=True)
            # give a warning if the two brothers with the highest priority have the same priority
            if len(prioritylist) > 1 and prioritylist[0][1] == prioritylist[1][1]:
                cannotPriorityPrune = True
            else:
                # keep all elements except for the first element since they shall be deactivated
                prioritylistwofirstel = prioritylist[1:]
                # now deactivate the nodes not taken -> prune
                for nip in prioritylistwofirstel:
                    nuid = int(nodelist[nip[0]][0])
                    ell, ndd = self.findNodeUidInPaths(self, nuid, paths)
                    nodelist = self.pruneAspect(self, paths, ell, ndd, nodelist, True, uidIndexDict)
                    prunedUids.append(nuid)

        return nodelist, prunedUids, cannotPriorityPrune

    #prune a specnode
    def pruneSpec(self, paths, el, nd, nodelist, uidIndexDict):
        # check the specrule for the node in order to determine which path is selected -> returns selected uid
        sel = self.checkSpecRule(self, paths[el][nd])
        noSpecruleInfo = False
        if sel != None:
            # deactivate node
            nodelist = self.nodeNotInPes(self, paths[el][nd][0], nodelist, uidIndexDict)
            # selected child uid
            selchilduid = int(sel)
            # change node and disable the not selected children
            # find the correct parent - if there are several specnodes below each other the first is needed
            pnode = self.goToHighestParentSpecsInPath(self, paths[el][nd][0])
            # find the selected child
            cnode = ""
            for ch in paths[el][nd][0].childrenlist():
                if ch.getUid() == selchilduid:
                    cnode = ch
                    nodelist = self.nodeNotInPes(self, ch, nodelist, uidIndexDict)  # deactivate the childnode - the information will be in the parent
                else:
                    nodelist = self.nodeNotInPes(self, ch, nodelist, uidIndexDict)  # deactivate the not selected childnodes and the children below
                    nodelist = self.childrenNotInPes(self, ch, paths, nodelist, uidIndexDict)
            #create the new name
            if cnode != "" and cnode.name().lower() != "none":  #change NONE to lowercase letters -> to recognize None / none as well
                newname = cnode.name() + "_" + pnode.name()
            else:
                newname = "NONE"
            # change the parent node in the nodelist and add the attributes of the child
            #for i in range(len(nodelist)):  # find index of parent node
                #if str(pnode.getUid()) == nodelist[i][0]:  #there is only one parent, so there is only one entry in the nodelist fitting -> now replaced by the next line
            i = uidIndexDict.get(str(pnode.getUid()))    #-> instead of going through the nodelist, just use the dictionary
            # set the new name in the nodelist
            nodelist[i][2] = newname
            # change the parent nodename in the paths so that for further children the names are set correctly
            puid = pnode.getUid()
            ele, nde = self.findNodeUidInPaths(self, puid, paths)
            paths[ele][nde][0].setName(newname)
            # check for attribute duplicates -> the child attribute should overwrite the parent attribute
            attriblist = cnode.attributes
            attribnameschild = []
            for at in cnode.attributes:
                attribnameschild.append(at[0])
            for at in pnode.attributes:
                if at[0] not in attribnameschild:
                    attriblist.append(at)
            nodelist[i][6] = attriblist
            # set the attriblist for the parentnode in the paths
            paths[ele][nde][0].attributes = attriblist

            #correct uids and names in couplings -> there are made two changes n the couplings: the father is changed in name and the child is changed in name and uid (because it is deactivated and combined with father)
            try:    #successful, if the parent of the parent of the node exists and has couplings
                pp = paths[el][nd][0].parent().parent()
                ppuid = pp.getUid()
                ppcpl = pp.coupling
                for coup in range(len(ppcpl)):
                    try:
                        if ppcpl[coup][1] == str(paths[el][nd][0].parent().getUid()):
                            ppcpl[coup][0] = newname
                            ppcpl[coup][1] = str(paths[el][nd][0].parent().getUid())  #not necessary
                    except:
                        pass
                    try:
                        if ppcpl[coup][4] == str(paths[el][nd][0].parent().getUid()):
                            ppcpl[coup][3] = newname
                            ppcpl[coup][4] = str(paths[el][nd][0].parent().getUid())  # not necessary
                    except:
                        pass
                j = uidIndexDict.get(str(ppuid))
                nodelist[j][8] = ppcpl  #set to nodelist
                elec, ndec = self.findNodeUidInPaths(self, ppuid, paths)    #set in paths
                paths[elec][ndec][0].coupling = ppcpl
            except:
                pass
            #the same for the children of the children of the node
            for chi in paths[el][nd][0].childrenlist():
                for cc in chi.childrenlist():
                    try:    #if the node has couplings at all
                        ccuid = cc.getUid()
                        cccpl = cc.coupling
                        for coup in range(len(cccpl)):
                            try:
                                if cccpl[coup][1] == str(cc.parent().getUid()):
                                    cccpl[coup][0] = newname
                                    cccpl[coup][1] = str(cc.parent().parent().parent().getUid())
                            except:
                                pass
                            try:
                                if cccpl[coup][4] == str(cc.parent().getUid()):
                                    cccpl[coup][3] = newname
                                    cccpl[coup][4] = str(cc.parent().parent().parent().getUid())
                            except:
                                pass
                        j = uidIndexDict.get(str(ccuid))
                        nodelist[j][8] = cccpl  # set to nodelist
                        elec, ndec = self.findNodeUidInPaths(self, ccuid, paths)    #set in paths
                        paths[elec][ndec][0].coupling = cccpl
                    except:
                        pass

            # for the children of the selected child set the new parent uid in the nodelist
            childchildnodes = cnode.childrenlist()
            cuids = []
            for chch in childchildnodes:
                cuids.append(chch.getUid())
            childchildnodeindices = self.findNodeUidInNodelist(self, cuids, nodelist, uidIndexDict)
            nodelist = self.changeParentUidInNodelist(self, childchildnodeindices, str(puid), nodelist)
            # for the children of the selected child set the new depth in the nodelist (new parent depth plus 1) and travel the whole list recursively (in the changeChildrenDepthInNodelist function)
            pnodeindex = self.findNodeUidInNodelist(self, [puid], nodelist, uidIndexDict)
            pdepth = int(nodelist[pnodeindex[0]][12])
            nodelist = self.changeChildrenDepthInNodelist(self, childchildnodeindices, pdepth, nodelist)
        else:  # nothing is selected in the specnode -> it shall be deactivated
            nodelist = self.nodeNotInPes(self, paths[el][nd][0], nodelist, uidIndexDict)  # deactivate the not selected node and the children below
            nodelist = self.childrenNotInPes(self, paths[el][nd][0], paths, nodelist, uidIndexDict)
            noSpecruleInfo = True

        return paths, nodelist, noSpecruleInfo

    #prune a maspectnode
    def pruneMaspect(self, paths, el, nd, nodelist, nodeUidsPruned, lenpaths, uidIndexDict, sesvarlist, sesfunlist):
        def findNextUid():
            #list all uids
            highestUid = 0
            allUids = []
            for no in nodelist:
                allUids.append(int(no[0]))
            #sort them by descending order
            allUids = sorted(allUids, reverse=True)
            #set highest uid + 1
            if allUids:    #allUids != []
                highestUid = allUids[0] + 1
            return highestUid

        #get the number of replications
        nuid = paths[el][nd][0].getUid()
        nindex = self.findNodeUidInNodelist(self, [nuid], nodelist, uidIndexDict)
        numRep = int(nodelist[nindex[0]][9])
        #get all uids for children of the maspect node
        childrenuidlist = []
        for p in range(len(paths)):
            goBelow = False
            for q in range(len(paths[p])):
                if paths[p][q][0].getUid() == nuid:
                    goBelow = True
                elif goBelow:
                    childrenuidlist.append(paths[p][q][0].getUid())
        childrenuidlist = list(set(childrenuidlist))    #remove duplicates by converting to a set and back
        # find the highest uid in the nodelist in order to know where to start giving new uids
        nextUid = findNextUid()

        #change the Maspect node to an Aspect node in the nodelist, change the name if necessary, set the numRep to 1
        nodelist[nindex[0]][1] = "Aspect Node"
        if "MASP" in nodelist[nindex[0]][2]: #change the name if necessary
            nodelist[nindex[0]][2] = nodelist[nindex[0]][2].replace("MASP", "DEC")
        nodelist[nindex[0]][9] = "1" #set numRep to 1
        #find the children of the maspect node with their subtrees in the nodelist (indices of nodelist)
        childrenindexlist = []
        for cuidl in childrenuidlist:
            childrenindexlist.append(self.findNodeUidInNodelist(self, [cuidl], nodelist, uidIndexDict)[0])
        #sort the indices descending order so removing one child will not destroy the other indices in the list
        childrenindexlist = sorted(childrenindexlist, reverse=True)
        #extract them from the nodelist
        childrenlist = []
        for ind in childrenindexlist:
            childrenlist.append(nodelist[ind])
            del nodelist[ind]
        #reverse the childrenlist (the children were added in reverse)
        childrenlist = list(reversed(childrenlist))
        #multiply them with the numRep, set new uids, correct the parent uids and correct uids in aspectrules, couplings and specrules
        #childrenlist = [i for i in childrenlist for r in range(numRep)]    #no real copy is made
        chi = len(childrenlist) #chi is the original childrenlist's length
        nR = 0
        while nR < (numRep-1):  #it exists already one time
            ch = 0
            oldnewuid = []  # a list containing the old uid and the new uid so that the new parentuid can be set correctly
            #create the new child and set new uid and parent uid
            while ch < chi:
                newchild = deepcopy(childrenlist[ch])   #make a copy of the child
                olduid = newchild[0]
                newuid = str(nextUid + ch + chi * nR)
                oldnewuid.append([olduid, newuid])  #put the old and the new uid in the list -> it is needed to set the parents uid correctly
                #set new uid
                newchild[0] = newuid
                #look at the old uid in oldnewuid and see if the parentuid has to be adjusted
                parUidOfNewchild = newchild[3]
                for onu in oldnewuid:
                    if onu[0] == parUidOfNewchild:
                        newchild[3] = onu[1]
                #begin inserting at the end of the original nodes
                childrenlist.insert(chi+ch, newchild)
                ch += 1
            #all nodes for this numRep part got the new uids -> now replace the old uids in aspectrules, couplings and specrules with the new uids for the just copied nodes
            while ch < (2*chi):     #the copied nodes are the nodes from the current ch to 2*chi since they were inserted behind the last original nodes
                # look if an aspectrule or a specrule uid has to be adjusted to the new uid
                for onu in range(len(oldnewuid)):
                    # aspectrules
                    for aspectr in range(len(childrenlist[ch][7])):
                        if childrenlist[ch][7][aspectr][1] == oldnewuid[onu][0]:
                            childrenlist[ch][7][aspectr][1] = oldnewuid[onu][1]
                    # couplings
                    for cpls in range(len(childrenlist[ch][8])):
                        if childrenlist[ch][8][cpls][1] == oldnewuid[onu][0]:
                            childrenlist[ch][8][cpls][1] = oldnewuid[onu][1]
                        if childrenlist[ch][8][cpls][4] == oldnewuid[onu][0]:
                            childrenlist[ch][8][cpls][4] = oldnewuid[onu][1]
                    # specrules
                    for specr in range(len(childrenlist[ch][10])):
                        if childrenlist[ch][10][specr][1] == oldnewuid[onu][0]:
                            childrenlist[ch][10][specr][1] = oldnewuid[onu][1]
                ch += 1

            # add a new coupling to the Maspect node (which has already been converted to an Aspect node), get the original couplings from the paths, since changes (e.g.) adding of new couplings for new children are made in the nodelist
            """ #the couplings in the Maspect node are created for the children already in the validate function of the couplings, only the uids have to be corrected (can only be done, after the new names are given to the nodes, since the couplings already contain the new names created from the validate function)
            cplnew = deepcopy(paths[el][nd][0].coupling)
            for onu in range(len(oldnewuid)):
                for cpls in range(len(cplnew)):
                    if cplnew[cpls][1] == oldnewuid[onu][0]:
                        cplnew[cpls][1] = oldnewuid[onu][1]
                    if cplnew[cpls][4] == oldnewuid[onu][0]:
                        cplnew[cpls][4] = oldnewuid[onu][1]
            for cplitem in cplnew:  #add to node
                nodelist[nindex[0]][8].append(cplitem)
            """

            #create next childrenlist to insert (if nR is not numRep-1 already)
            nR += 1

        #remove double couplings in the Maspect node
        """ #not needed any more, since the correct couplings are already created by the validate function of the couplings (so no couplings are doubled while creating the children of the Maspect node)
        cpl = nodelist[nindex[0]][8]  # get the multiplied couplings
        nodelist[nindex[0]][8] = [x for n, x in enumerate(cpl) if x not in cpl[:n]]  # remove duplicate couplings
        """

        #find and rename the direct children of the Maspect node -> they are in the childrenlist
        maspectnodeuid = paths[el][nd][0].getUid()
        childrenMaspectIndices = []
        childrenNumber = {} #dictionary containing the current number of children of one name so that the name can be set correctly, key: name, value: number
        #find the children
        chi = 0
        while chi < len(childrenlist):
            #children have the Maspect node as parent
            if int(childrenlist[chi][3]) == maspectnodeuid:
                childrenMaspectIndices.append(chi)
            chi += 1
        #now go through and rename
        uidOldNewNameDict = {}  #a dictionary containing the uid, the old and the new name, dictionary uid: [oldname, newname]
        newNameUidDict = {}     #a dictionary containing the new name give to the node as key and the uid as value, dictionary newname: uid -> it is needed for correcting the coupling uids of the Maspect node
        for ind in range(len(childrenMaspectIndices)):
            number = childrenNumber.get(childrenlist[childrenMaspectIndices[ind]][2])
            if not number:  #if the child's name is not in the childrenNumber dictionary yet, add it
                childrenNumber.update({childrenlist[childrenMaspectIndices[ind]][2]: 1})
                number = 0
            #add a number
            number += 1
            childrenNumber.update({childrenlist[childrenMaspectIndices[ind]][2]: number})
            #rename
            cuid = childrenlist[childrenMaspectIndices[ind]][0]
            oldname = childrenlist[childrenMaspectIndices[ind]][2]
            newname = childrenlist[childrenMaspectIndices[ind]][2] + "_" + str(number)
            uidOldNewNameDict.update({cuid: [oldname, newname]})
            newNameUidDict.update({newname: cuid})
            childrenlist[childrenMaspectIndices[ind]][2] = newname  #apply the new name to the node

        #change the couplings of the nodes in the childrenlist to the new name if necessary
        for ind in range(len(childrenlist)):
            for coup in range(len(childrenlist[ind][8])):
                nn = uidOldNewNameDict.get(childrenlist[ind][8][coup][1])
                if nn:  #if the name was found in the couplings
                    if childrenlist[ind][8][coup][0] == nn[0]:  #just to be very sure, actually not needed
                        childrenlist[ind][8][coup][0] = nn[1]
                nn = uidOldNewNameDict.get(childrenlist[ind][8][coup][4])
                if nn:  # if the name was found in the couplings
                    if childrenlist[ind][8][coup][3] == nn[0]:  #just to be very sure, actually not needed
                        childrenlist[ind][8][coup][3] = nn[1]

        #change the couplings of the Maspect node (changed in Aspect node) to the new name if necessary
        """ #not needed any more, since the correct couplings are already created by the validate function of the couplings
        for coup in range(len(nodelist[nindex[0]][8])):
            nn = uidOldNewNameDict.get(nodelist[nindex[0]][8][coup][1])
            if nn:  #if the name was found in the couplings
                if nodelist[nindex[0]][8][coup][0] == nn[0]:  # just to be very sure, actually not needed
                    nodelist[nindex[0]][8][coup][0] = nn[1]
            nn = uidOldNewNameDict.get(nodelist[nindex[0]][8][coup][4])
            if nn:  # if the name was found in the couplings
                if nodelist[nindex[0]][8][coup][3] == nn[0]:  # just to be very sure, actually not needed
                    nodelist[nindex[0]][8][coup][3] = nn[1]
        """

        #change the couplings of the Maspect node (changed in Aspect node) to the new uids
        for coup in range(len(nodelist[nindex[0]][8])):
            nuid = newNameUidDict.get(nodelist[nindex[0]][8][coup][0])
            if nuid:  #if the uid was found in the couplings
                nodelist[nindex[0]][8][coup][1] = nuid
            nuid = newNameUidDict.get(nodelist[nindex[0]][8][coup][3])
            if nuid:  #if the uid was found in the couplings
                nodelist[nindex[0]][8][coup][4] = nuid

        #in the childrenlist assign the underscore variables for each child
        for inde in childrenMaspectIndices:     #indices of the children in the childrenlist
            for ind in range(len(childrenlist[inde][6])):
                if childrenlist[inde][6][ind][0].startswith("_"):
                    namesplit = childrenlist[inde][2].split("_")   #name
                    childrenlist[inde][6][ind][1] = namesplit[-1]  #assign the number

        #put the childrenlist in the nodelist again (at the right index (parentindex+1+c))
        for c in range(len(childrenlist)):
            nodelist.insert(nindex[0]+1+c, childrenlist[c])
        #now that the nodelist contains all children as well, recreate the dictionary with the nodeuids and the corresponding indices in the nodelist (uidIndexDict)
        uidIndexDict = {}
        for n in range(len(nodelist)):
            uidIndexDict.update({nodelist[n][0]: n})

        """ -> now the paths are completely recreated
        #add the new nodes to the paths
        #create the paths from the nodelist again and the check for differences
        newpaths = self.findPathsFromNodelist(self, nodelist)
        for path in newpaths:
            pathInPaths = False
            #go to the last node, it defines the path
            n = len(path)-1
            luid = path[n][0].getUid()
            for path2 in paths:
                # go to the last node, it defines the path
                n2 = len(path)-1
                luid2 = path2[n2][0].getUid()
                if luid == luid2:
                    pathInPaths = True
                    break
            if not pathInPaths:
                paths.append(path)
        """

        #instead of adding new nodes to the paths simply create the paths new from the nodelist
        paths = self.findPathsFromNodelist(self, nodelist)

        #now look whether there are aspects on the same layer so a decision has to be found -> simply call the algorithm again (for this layer since el and nd stay the same)
        self.findDoPruning(self, nodeUidsPruned, paths, el, nd, nodelist, lenpaths, uidIndexDict, sesvarlist, sesfunlist)

        return paths, nodelist, uidIndexDict




    #look in the aspectrule and check whether the aspectrule for the node evaluates to true
    def checkAspRule(self, nd):
        #get the element in the fourth column -> has to be T or nothing (condition not evaluable)
        asprule = nd[0].aspectrule
        if asprule == [] or asprule[0][3] == "T" or asprule[0][3] == "":     #the node shall stay in the tree if nothing is selected
            return True
        else:
            return False

    # look in the specrule and look which child is selected and return the uid of the selected child
    def checkSpecRule(self, nd):
        # get the element in the fourth column -> has to be T or nothing (condition not evaluable)
        specrule = nd[0].specrule
        for el in specrule:
            # specrule for the uid of the selected node, if nothing is selected there is returned nothing
            if el[3] == "T":
                return el[1]

    #find the highest parent in the path - when several specnodes are in one path it is not the direct father
    def goToHighestParentSpecsInPath(self, nd):
        """
        if nd.parent().parent().typeInfo() == "Spec Node":
            nd = nd.parent().parent()
            self.goToHighestParentSpecsInPath(self, nd)
            return nd.parent()
        else:
            return nd.parent()
        """
        while nd.parent().parent().typeInfo() == "Spec Node":
            nd = nd.parent().parent()
        return nd.parent()

    #find a node uid in paths and return the indices
    def findNodeUidInPaths(self, uid, paths):
        for ell in range(len(paths)):  #find the indices
            for ndd in range(len(paths[ell])):
                if paths[ell][ndd][0].getUid() == uid:
                    return ell, ndd

    #find a node uid in the nodelist and return the index
    def findNodeUidInNodelist(self, uids, nodelist, uidIndexDict):
        indices = []
        for uid in uids:
            struid = str(uid)
            #for i in range(len(nodelist)):
                #if nodelist[i][0] == struid:
                    #indices.append(i)
            indices.append(uidIndexDict.get(struid))    #-> the dictionary replaces going through the nodelist
        return indices

    #change the parent uid of a childnode in the nodelist
    def changeParentUidInNodelist(self, indices, newparentuid, nodelist):
        for ind in indices:
            nodelist[ind][3] = newparentuid
        return nodelist

    # change the depth of all childnodes beginning with the nodes in indices in the nodelist -> recusively
    def changeChildrenDepthInNodelist(self, indices, pdepth, nodelist):
        for ind in indices:
            #change it
            newdepth = pdepth + 1
            nodelist[ind][12] = str(newdepth)
            #seek for children and apply the function again
            #get the uid -> seek in the nodelist for nodes having this uid as parent -> add the index
            struid = str(nodelist[ind][0])
            nextindices = []
            for i in range(len(nodelist)):
                if nodelist[i][3] == struid:
                    nextindices.append(i)
            #now call the function recursively
            if nextindices != []:
                self.changeChildrenDepthInNodelist(self, nextindices, newdepth, nodelist)
        #return updated nodelist
        return nodelist

    #find node in the nodelist and return the value whether ist stays in the tree or not
    def nodeInPesValue(self, nd, nodelist, uidIndexDict):
        uid = nd.getUid()
        #for i in range(len(nodelist)):
            #if str(uid) == nodelist[i][0]:
                #return nodelist[i][13]
        i = uidIndexDict.get(str(uid))
        return nodelist[i][13]

    #find brothers of a node object in the paths
    def findBrothers(self, nd):
        p = nd.parent()
        return p.childrenlist()

    #find brothers in the nodelist (brothers to an uid) if they are not deactivated
    def findBrothersInNodelist(self, uid, nodelist, uidIndexDict):
        brothernodelistindices = []
        nodelistindex = self.findNodeUidInNodelist(self, [uid], nodelist, uidIndexDict)
        #get the parentuid for the nodelistindex
        strparentuid = nodelist[nodelistindex[0]][3]
        #go through nodelist and find the brothers (same parentuid) if they are not deactivated
        for i in range(len(nodelist)):
            if nodelist[i][3] == strparentuid and nodelist[i][13] == True:
                brothernodelistindices.append(i)
        return brothernodelistindices

    #seek node in nodelist and set false to show it does not stay in the tree
    def nodeNotInPes(self, nd, nodelist, uidIndexDict):
        uid = nd.getUid()
        #for i in range(len(nodelist)):
            #if str(uid) == nodelist[i][0]:
                #nodelist[i][13] = False
        i = uidIndexDict.get(str(uid))
        nodelist[i][13] = False
        return nodelist

    #find node in nodelist and set all children to false to show they do not stay in the tree
    def childrenNotInPes(self, nd, paths, nodelist, uidIndexDict):
        uid = nd.getUid()
        #find paths in which nd is
        i=0
        j=0
        # go through all paths
        while i<len(paths):
            #go through nodelist of a path and switch off all nodes below nd
            switchoff = False
            while j<len(paths[i]):
                if switchoff:
                    nodelist = self.nodeNotInPes(self, paths[i][j][0], nodelist, uidIndexDict)
                if not switchoff and paths[i][j][0].getUid() == uid:
                    switchoff = True
                j += 1
            j = 0
            i += 1
        return nodelist