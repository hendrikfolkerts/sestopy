# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *

from copy import deepcopy

#needed for pruning without the editor
from json_json import *
from te_TreeNode import *

class Flatten:

    #constructor
    def __init__(self):
        self.main = ""
        self.paths = ""
        self.nodelist = ""
        self.sespeslist = ""
        self.sesvarlist = ""

    # the main function for flattening
    def flattenMain(self, pesfile="", fpesfile="", editor=False, main=None):
        datafound = False
        # get the lists or create them
        nodelist = []
        sespeslist = []
        sesvarlist = []
        paths = []
        if editor:
            # if the prune function was called using the editor
            self.main = main

            # tree and sesvarlist (sesvarlist shall be inserted in the pruned tree)
            nodelist = deepcopy(self.main.modellist[self.main.activeTab][3].treeToList())  # make sure, it is a copy
            sespeslist = self.main.modellist[self.main.activeTab][0].outputSesPes()
            sesvarlist = self.main.modellist[self.main.activeTab][1].outputSesVarList()
            # since the editor was used for flattening the findPaths function in te_TreeManipulate can be used
            pathsOriginal = self.main.modellist[self.main.activeTab][3].findPaths()
            paths = deepcopy(pathsOriginal)

            #the necessary data was found
            datafound = True
        else:
            # the flatten function was called not using the editor
            try:
                # read the file
                f = open(pesfile, "r")
                istOkay, nodelist, sespeslist, sesvarlist, semconlist, selconlist, sesfunlist, loadtime = fromJSON(f.read())
                f.close()
                if istOkay:
                    #get the paths -> if the flattening was started not using the graphical editor the findPaths function in te_TreeManipulate.py can not be used
                    paths = self.findPathsFromNodelist(self, nodelist)
                    # convert the SES/PES into a list consisting of ses/pes and the SES comment
                    sespeslist = sespeslist[0]

                    # the necessary data was found
                    datafound = True
                else:
                    print("Error reading the file containing the SES. Maybe it was created with an old version of this editor?")
            except:
                print("Error reading the file containing the SES. Is it a file created by this editor?")

        #all data are collected, now start the flattening

        #only continue if all data was found
        if datafound:
            #check that the SES starts and ends with entity nodes in all paths
            if self.checkPesNodes(self, paths):
                print("OK - The paths of the tree were found.")
                if sespeslist[0] == "pes":
                    print("OK - It shall be a PES.")

                    #now flatten and return the nodelist
                    nodelist = self.flatten(self, nodelist, paths)
                    print("OK - The flattening is done successfully.")

                    #build the new information for the FPES -> the type is FPES and the description from the SES
                    sespes = ["fpes", sespeslist[1]]

                    # if the flatten function is called using the editor it is necessary to insert the flattened PES into a model else it has to written to a file
                    if editor:
                        #the prune function was called using the editor
                        self.insertInModel(self, nodelist, sesvarlist, [sespes], self.main)
                    else:
                        #the prune function was called not using the editor
                        filestr = toJSON(nodelist, sespes, sesvarlist, [], [], [])
                        #write
                        f = open(fpesfile, "w")
                        f.write(filestr)
                        # close
                        f.close()
                else:
                    if editor:
                        QMessageBox.information(None, "Cannot flatten", "Please make sure, that the tree represents a PES and set the radio button in the information menu to PES.", QtWidgets.QMessageBox.Ok)
                    else:
                        print("Not OK - Please make sure, that the tree represents a PES and set the radio button in the information menu to PES.")
            else:
                if editor:
                    QMessageBox.information(None, "Cannot flatten", "The tree is empty or does not end with an entity node in all paths.", QtWidgets.QMessageBox.Ok)
                else:
                    print("Not OK - The tree is empty or does not end with an entity node in all paths.")
        else:
            if editor:
                QMessageBox.information(None, "Cannot flatten", "Not all data could be read.", QtWidgets.QMessageBox.Ok)
            else:
                print("Not OK - Not all data could be read.")


    #get the paths -> if the flattening was started not using the graphical editor the findPaths function in te_TreeManipulate.py can not be used
    def findPathsFromNodelist(self, nodelistFromSave):

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

    #a PES has to start and end with entity nodes
    def checkPesNodes(self, paths):
        endWithEntity = False
        for nd in paths:
            if nd[len(nd)-1][0].typeInfo() == "Entity Node":
                endWithEntity = True
        return endWithEntity

    #insert the processed nodelist into a new model
    def insertInModel(self, nodelist, sesvarlist, sespes, main):
        while True:
            num, ok = QInputDialog.getInt(None, "Model for the FPES", "In which model different from the current model do you want to insert the FPES? Please enter an integer from 1 to 10.")
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
                reply = QMessageBox.question(None, 'Empty Model', "Are you sure you want to empty the model number " + str(num) + " in order to insert the flattened model?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    empty = self.main.emptyCurrentModel(True, (num-1))
            if empty or isemptymodel:
                self.main.modellist[(num - 1)][3].fromSave(nodelist)
                self.main.modellist[(num - 1)][0].fromSave(sespes)
                self.main.modellist[(num - 1)][1].fromSave(sesvarlist)
                #it is no PES anymore
                if sespes[0] == "fpes":
                    self.main.modellist[(num - 1)][0].rbses.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbipes.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbpes.setChecked(False)
                    self.main.modellist[(num - 1)][0].rbfpes.setChecked(True)



    #all functions for flattening---------------------------------------------------------------------------------------

    #the flattening function
    def flatten(self, nodelist, paths):

        #create a dictionary where to every uid the index of the nodelist is placed (then the nodelist does not have to be travelled for finding the corresponding index to an uid)
        uidIndexDict = {}
        for n in range(len(nodelist)):
            uidIndexDict.update({nodelist[n][0]: n})

        #find leaf nodes in nodelist -> they shall be part of the FPES
        nodesPartOfFpesIndices = []
        nodenamesPartOfFpes = []
        for pa in paths:
            nodesPartOfFpesIndices.append(uidIndexDict.get(str(pa[len(pa)-1][0].getUid())))
            nodenamesPartOfFpes.append(pa[len(pa)-1][0].name())

        #when flattening, there could be name duplicates in brothers, since the hierarchy is resolved -> valid brothers axiom would be violated -> change name by appending _number -> in couplings as well
        #the nodelist still contains all nodes that will be in the FPES, but the names of nodes being leaf nodes are found
        #-> find uid and couplings for these nodes
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set(x for x in nodenamesPartOfFpes if x in seen or seen_add(x))
        # turn the set into a list (as requested)
        duplicates = list(seen_twice)
        #for each duplicate
        uidNewnameDict = {} #dictionary containing the uid and the new name -> this can be used to adapt the couplings
        for d in duplicates:
            #delete node from nodenamesPartOfFpes
            duplicateIndices = [i for i, x in enumerate(nodenamesPartOfFpes) if x == d]
            duplicateIndices.sort(reverse=True)
            for di in duplicateIndices:
                del nodenamesPartOfFpes[di]
            #rename node in nodelist and get the uid of the node, that is changed in name -> for couplings
            numToAppend = 1
            for nd in nodelist:
                if nd[2] == d:
                    nd[2] = d + "_" + str(numToAppend)  #set new name for the node -> with _ and number
                    numToAppend += 1
                    uidNewnameDict.update({nd[0]:nd[2]})    #update the dictionary with the uid and the new name
                    nodenamesPartOfFpes.append(nd[2])       #append the new name to the list of nodes in the FPES

        #delete not needed nodes from the nodelist
        #just keep the first two nodes (in the PES the nodelist should begin with an Entity followed by an Aspect) and the leaf nodes
        #for the nodes to delete: keep couplings
        couplinglist = []
        i = len(nodelist)-1     #if deleting lower indices in the nodelist first, the upper indices would be incorrect
        while i >= 2:   #do not delete or change the first two (indices 0 and 1)
            if i not in nodesPartOfFpesIndices:
                cpl = nodelist[i][8]    #if it is not an Aspect node, the couplinglist is just empty
                if len(cpl) > 0:
                    for cp in cpl:
                        cp.append(nodelist[i][0])  #add the uid of the node the couplings stand in
                    couplinglist = cpl + couplinglist
                del nodelist[i]
            else:
                #at the leaf nodes the parent has to be corrected -> take uid from the second node in the nodelist
                nodelist[i][3] = nodelist[1][0]
                #at the leaf nodes the depth needs to be corrected
                nodelist[i][12] = "2"
            i -= 1
        #add the couplings of the second node
        if len(nodelist) > 1:
            cpl = nodelist[1][8]
            if len(cpl) > 0:
                for cp in cpl:
                    cp.append(nodelist[1][0])  #add the uid of the node the couplings stand in
                couplinglist = cpl + couplinglist
            #add the names of the first and the second node to the nodenamesPartOfFpes list (because for couplings it is important to know, which nodes will still be in the FPES)
            #nodenamesPartOfFpes.extend([paths[0][0][0].name()])
            #nodenamesPartOfFpes.extend([paths[0][1][0].name()])
            nodenamesPartOfFpes.insert(0, paths[0][1][0].name())   #insert at front -> actually order does not matter
            nodenamesPartOfFpes.insert(0, paths[0][0][0].name())   #insert at front -> actually order does not matter

            #correct nodenames in the couplinglist (that have changed because of resolving duplicates)
            for cpl in couplinglist:
                if cpl[1] in uidNewnameDict:
                    cpl[0] = uidNewnameDict.get(cpl[1])
                if cpl[4] in uidNewnameDict:
                    cpl[3] = uidNewnameDict.get(cpl[4])

            #all couplings are in the couplinglist -> now correct the couplings, since they will all be placed in the second node
            # -> using the couplinglist and the list containing the nodenames, which are part of the FPES (nodenamesPartOfFpes)
            notCompletelyCorrected = True
            t = 0   #for safety, that the while loop is definitely exited if there is a problem correcting the couplings
            while notCompletelyCorrected and t<10:   #do, until all couplings are corrected completely, but t times at maximum -> actually all should be done on the first run
                couplinglist, notCompletelyCorrected = self.correctCouplings(self, couplinglist, nodenamesPartOfFpes)
                t += 1

            #warning, if not all couplings could be corrected
            if notCompletelyCorrected:
                QMessageBox.information(None, "Cannot correct the couplings completely", "The couplings could not be corrected completely for the FPES. Please do so manually.", QtWidgets.QMessageBox.Ok)

            #place the recalculated couplings in the second node of the nodelist (the only aspect node)
            nodelist[1][8] = couplinglist

        #return the final nodelist
        return nodelist

    #correct the couplings -> the idea of the algorithm is shown in an example
    def correctCouplings(self, couplinglist, nodenamesPartOfFpes):
        """
        Example PES:

                Model-XY
                    |
                ModelDEC
                    |
                ---------
                |       |
                A       D
                |       |
               aDEC    dDEC
                |       |
            ---------   E
            |       |
            B       C

            Assuming following couplings:

            ModelDEC:
                source      sink
                A   out     D   in
                D   out     A   in

            aDEC:
                source      sink
                A   in      B   in1
                A   in      C   in
                C   out     B   in2
                B   out     A   out

            dDEC:
                source      sink
                D   in      E   in
                E   out     D   out

        The FPES would look like:

                Model-XY
                    |
                ModelDEC
                    |
            -----------------
            |       |       |
            B       C       E

            with the couplings in ModelDEC:
                source      sink
                E   out     B   in1
                C   out     B   in2
                E   out     C   in
                B   out     E   in

        The idea is:
        1) get a list with all couplings of the PES
        2) go through the list and if one part of a coupling like " A out " refers to an inner node, try to replace all occurences of " A out " with another coupling containing " A out "
            (if a node is an inner node, the name is not in the nodenamesPartOfFpes list) -> see the example for details

        For the example above:
        source      sink
        A   out     D   in
        D   out     A   in
        A   in      B   in1
        A   in      C   in
        C   out     B   in2
        B   out     A   out
        D   in      E   in
        E   out     D   out
                |
        Take the first coupling, " A out " is identified as inner coupling (on the source side) -> try to replace all occurrences of " A out "
        Found in the 6th coupling, replace with " B out " -> Keep in mind, that a source should stay a source and a sink should stay a sink,
        so the replacement for " A out " should be found on the source side (and " A out " in the replacement coupling pair is then on the sink side like in the 6th coupling).
        Remove the used 6th couplings from the list.
                |
        source      sink
        B   out     D   in
        D   out     A   in
        A   in      B   in1
        A   in      C   in
        C   out     B   in2
        D   in      E   in
        E   out     D   out
                |
        The node D will not be in the FPES, so " D in " and " D out " are inner couplings, which need to be replaced.
        " D in " can be replaced with the 6th coupling. Remove the used 6th coupling.
                |
        source      sink
        B   out     E   in
        D   out     A   in
        A   in      B   in1
        A   in      C   in
        C   out     B   in2
        E   out     D   out
                |
        " D out " can be replaced with the 6th coupling. Remove the 6th coupling.
                |
        source      sink
        B   out     E   in
        E   out     A   in
        A   in      B   in1
        A   in      C   in
        C   out     B   in2
                |
        " A in " will not be in the FPES, but it is twice in the third and fourth coupling -> therefore " A in " is replaced by " E out " and the 2nd coupling is deleted.
                |
        source      sink
        B   out     E   in
        E   out     B   in1
        E   out     C   in
        C   out     B   in2
                |
        The correct couplings are evaluated for the FPES.

        The following algorithm works like that, only all sourcenodes are travelled first, afterwards all sinknodes are travelled. The couplinglist is split into source- and sinkcouplings therefore.
        """

        #split the couplings in sourcecouplings and sinkcouplings
        sourcecpl = []
        sinkcpl = []
        for cpl in couplinglist:
            src = cpl[0:3]
            src.append(cpl[8])
            sourcecpl.append(src)
            snk = cpl[3:6]
            snk.append(cpl[8])
            sinkcpl.append(snk)

        #go through the sourcecouplings and see, if a coupling refers to an inner node -> please see example to understand
        i = 0
        while i < len(sourcecpl):
            if sourcecpl[i][0] not in nodenamesPartOfFpes:    #coupling nodename -> check, if it will be in the FPES
                #the current coupling is an inner coupling, which needs to be replaced
                #get the listindices using the name and the port, where the same coupling as the current coupling is in the sinkcoupling
                #the sinkcouplings need to be in another descriptive node
                ind = []
                for j in range(len(sinkcpl)):
                    if sourcecpl[i][0] == sinkcpl[j][0] and sourcecpl[i][2] == sinkcpl[j][2] and sourcecpl[i][3] != sinkcpl[j][3]:
                        ind.append(j)
                #get the listindices using the name and the port, where the same coupling is in the sourcecoupling again and needs to be replaced as well, but make sure, it is not the current coupling
                #the other sourcecouplings need to be in the same descriptive node
                ind2 = []
                for j in range(len(sourcecpl)):
                    if sourcecpl[i][0] == sourcecpl[j][0] and sourcecpl[i][2] == sourcecpl[j][2] and sourcecpl[i][3] == sinkcpl[j][3] and i != j:
                        ind2.append(j)
                #check, how many times the current coupling was found in the sinkcouplings and replace
                if len(ind) > 1:
                    pass    #see example: like " A in " -> it will be replaced when going through the sinkcpl
                else:
                    if len(ind) > 0:    #replace the current coupling
                        #apply the ind[0] element from the sourcecpl to sourcecpl[i] (replace the current coupling with the sourcecoupling, which has the same coupling as the current coupling on the sink side)
                        sourcecpl[i] = sourcecpl[ind[0]]
                        #replace further occurences of the current coupling in the sourcecouplings
                        for inde in ind2:
                            sourcecpl[inde] = sourcecpl[ind[0]]
                        #remove the ind[0] element in sourcecpl and sinkcpl
                        del sourcecpl[ind[0]]
                        del sinkcpl[ind[0]]
            else:
                pass    #the node, the coupling refers to, will be in the FPES
            i += 1

        #go through the sinkcouplings and see, if a coupling refers to an inner node -> please see example to understand
        i = 0
        while i < len(sinkcpl):
            if sinkcpl[i][0] not in nodenamesPartOfFpes:    #coupling nodename -> check, if it will be in the FPES
                #the current coupling is an inner coupling, which needs to be replaced
                #get the listindices using the name and the port, where the same coupling as the current coupling is in the sourcecoupling
                #the sourcecouplings need to be in another node
                ind = []
                for j in range(len(sourcecpl)):
                    if sinkcpl[i][0] == sourcecpl[j][0] and sinkcpl[i][2] == sourcecpl[j][2] and sinkcpl[i][3] != sourcecpl[j][3]:
                        ind.append(j)
                #get the listindices using the name and the port, where the same coupling is in the sinkcoupling again and needs to be replaced as well, but make sure, it is not the current coupling
                #the other sinkcouplings need to be in the same descriptive node
                ind2 = []
                for j in range(len(sinkcpl)):
                    if sinkcpl[i][0] == sinkcpl[j][0] and sinkcpl[i][2] == sinkcpl[j][2] and sinkcpl[i][3] == sourcecpl[j][3] and i != j:
                        ind2.append(j)
                #check, how many times the current coupling was found in the sourcecouplings and replace
                if len(ind) > 1:
                    pass    #see example: like " A in " -> actually this should not happen, since it should be replaced when going through the sourcecpl
                else:
                    if len(ind) > 0:    #replace the current coupling
                        #apply the ind[0] element from the sinkcpl to sinkcpl[i] (replace the current coupling with the sinkcoupling, which has the same coupling as the current coupling on the source side)
                        sinkcpl[i] = sinkcpl[ind[0]]
                        #replace further occurences of the current coupling in the sinkcouplings
                        for inde in ind2:
                            sinkcpl[inde] = sinkcpl[ind[0]]
                        #remove the ind[0] element in sourcecpl and sinkcpl
                        del sourcecpl[ind[0]]
                        del sinkcpl[ind[0]]
            else:
                pass    #the node, the coupling refers to, will be in the FPES
            i += 1

        #build new couplinglist from the parts and check, if there are still couplings refering to a node not being in the FPES (inner couplings)
        #variable to describe if there are still couplings refering to nodes, which are not in the FPES
        stillCouplingsNodesNotInFpes = False
        couplinglist = []
        for i in range(len(sourcecpl)):
            couplinglist.append(sourcecpl[i][0:3]+sinkcpl[i][0:3]+["",""]+sourcecpl[i][3:4])
            if sourcecpl[i][0] not in nodenamesPartOfFpes:
                stillCouplingsNodesNotInFpes = True
            if sinkcpl[i][0] not in nodenamesPartOfFpes:
                stillCouplingsNodesNotInFpes = True

        return couplinglist, stillCouplingsNodesNotInFpes