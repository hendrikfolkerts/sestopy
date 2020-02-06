# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5.QtCore import QItemSelectionModel
#import copy
from copy import deepcopy

from te_TreeModel import *
from ww_ManageWindow import *
from pn_attributes import *
from pn_aspectrule import *
from pn_coupling import *
from pn_number_replication import *
from pn_specrule import *

class TreeManipulate(QtCore.QObject):   #for defining a signal the class must be inherited from QObject

    nodeDeletedSignal = pyqtSignal()
    treeChangedSignal = pyqtSignal()

    """init"""
    def __init__(self, main, tabnumber):
        super(TreeManipulate, self).__init__()  #since it is inherited from QObject, the super class must be called
        #init the tree
        self.rootNode = Node(0, "SES")

        #variables and widgets from main
        self.main = main
        self.tabnumber = tabnumber
        self.hierarchymodeltreeview = None
        self.cbnodetype = None
        self.nodeTypes = self.main.nodeTypes
        self.nodeTypeIcons = self.main.nodeTypeIcons
        self.baddsubnode = None
        self.baddsiblingnode = None
        self.bdeletenode = None
        self.bexpandall = None
        self.bcollapseall = None
        self.tbproperties = None
        self.setUiInit()

        #fill node Type field
        self.prepareCBNodeType()

        #creating and setting the models
        self.treeModel = TreeModel(self.rootNode, self.hierarchymodeltreeview)
        self.hierarchymodeltreeview.setModel(self.treeModel)
        self.treeSelectionModel = QItemSelectionModel(self.treeModel)
        self.hierarchymodeltreeview.setSelectionModel(self.treeSelectionModel)

        #ui and model signals
        self.baddsubnode.clicked.connect(self.addSubNode)
        self.baddsiblingnode.clicked.connect(self.addSiblingNode)
        self.bdeletenode.clicked.connect(self.deleteNode)
        self.bexpandall.clicked.connect(self.expandAll)
        self.bcollapseall.clicked.connect(self.collapseAll)
        self.treeSelectionModel.currentChanged.connect(self.setCbNodeTypeField)
        self.cbnodetype.currentIndexChanged.connect(self.typeChange)
        self.treeSelectionModel.selectionChanged.connect(self.setLastSelectedIndex)
        self.treeSelectionModel.selectionChanged.connect(self.readPropertiesNode)
        self.treeSelectionModel.selectionChanged.connect(self.checkAxiomsSelectionChanged) #-> not only when selection is changed, but also when the name is changed (see below)
        self.treeSelectionModel.selectionChanged.connect(self.updateUidNodenameDict)
        self.treeModel.nameChangedSignal.connect(self.checkName)
        self.treeModel.nameChangedSignal.connect(self.checkAxiomsCurrentNodeNameChanged)
        # for checks: old functions
        #self.treeModel.attributeInsertedSignal.connect(self.keepUniformityInsNodeProp)
        #self.treeModel.aspectruleInsertedSignal.connect(self.keepUniformityInsNodeProp)
        #self.treeModel.priorityInsertedSignal.connect(self.keepUniformityInsNodeProp)
        #self.treeModel.numrepInsertedSignal.connect(self.keepUniformityInsNodeProp)
        #self.treeModel.couplingInsertedSignal.connect(self.keepUniformityInsNodeProp)
        #self.treeModel.specruleInsertedSignal.connect(self.keepUniformityInsNodeProp)
        # for checks: new function
        self.treeModel.attributeInsertedSignal.connect(self.checkAxiomsCurrentNodePropertiesInserted)
        self.treeModel.aspectruleInsertedSignal.connect(self.checkAxiomsCurrentNodePropertiesInserted)
        self.treeModel.priorityInsertedSignal.connect(self.checkAxiomsCurrentNodePropertiesInserted)
        self.treeModel.numrepInsertedSignal.connect(self.checkAxiomsCurrentNodePropertiesInserted)
        self.treeModel.couplingInsertedSignal.connect(self.checkAxiomsCurrentNodePropertiesInserted)
        self.treeModel.specruleInsertedSignal.connect(self.checkAxiomsCurrentNodePropertiesInserted)

        #last selected index
        self.lastSelectedIndex = QtCore.QModelIndex()
        self.currentSelectedIndex = QtCore.QModelIndex()
        #variable telling, that the tree is read in
        self.isRestoringTree = False
        #ensure that some functions are only executed once and not being self executed
        self.doOnceNameChange = True
        self.allowTypeChange = True
        #for checks: old functions
        #self.doOnceAllowedNames = True
        #self.doOnceValidBrothers = True
        #self.doOnceStrictHierarchy = True
        #self.doOnceUniformity = True
        #self.doOnceKeepUniformity = True
        #for checks: new function
        self.doOnceChecks = True
        self.allowChecks = True
        self.allowUniformityCheck = True

        #manage the visibility of the property fields
        self.mw = ManageWindow(self.tbproperties, self.treeModel, self.treeSelectionModel, self.hierarchymodeltreeview)

        #creation of the properties_node
        self.at = Attributes(self, self.tabnumber)
        self.ar = Aspectrule(self, self.tabnumber)
        self.pr = Priority(self, self.tabnumber)
        self.nr = NumberReplication(self, self.tabnumber)
        self.cp = Coupling(self, self.tabnumber)
        self.sr = Specrule(self, self.tabnumber)

        #resize
        self.resz()

    def setUiInit(self):
        if self.tabnumber == 0:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt1
            self.cbnodetype = self.main.cbnodetypet1
            self.baddsubnode = self.main.buttonst1[0]
            self.baddsiblingnode = self.main.buttonst1[1]
            self.bdeletenode = self.main.buttonst1[2]
            self.bexpandall = self.main.buttonst1[3]
            self.bcollapseall = self.main.buttonst1[4]
            self.tbproperties = self.main.tbpropertiest1
        elif self.tabnumber == 1:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt2
            self.cbnodetype = self.main.cbnodetypet2
            self.baddsubnode = self.main.buttonst2[0]
            self.baddsiblingnode = self.main.buttonst2[1]
            self.bdeletenode = self.main.buttonst2[2]
            self.bexpandall = self.main.buttonst2[3]
            self.bcollapseall = self.main.buttonst2[4]
            self.tbproperties = self.main.tbpropertiest2
        elif self.tabnumber == 2:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt3
            self.cbnodetype = self.main.cbnodetypet3
            self.baddsubnode = self.main.buttonst3[0]
            self.baddsiblingnode = self.main.buttonst3[1]
            self.bdeletenode = self.main.buttonst3[2]
            self.bexpandall = self.main.buttonst3[3]
            self.bcollapseall = self.main.buttonst3[4]
            self.tbproperties = self.main.tbpropertiest3
        elif self.tabnumber == 3:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt4
            self.cbnodetype = self.main.cbnodetypet4
            self.baddsubnode = self.main.buttonst4[0]
            self.baddsiblingnode = self.main.buttonst4[1]
            self.bdeletenode = self.main.buttonst4[2]
            self.bexpandall = self.main.buttonst4[3]
            self.bcollapseall = self.main.buttonst4[4]
            self.tbproperties = self.main.tbpropertiest4
        elif self.tabnumber == 4:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt5
            self.cbnodetype = self.main.cbnodetypet5
            self.baddsubnode = self.main.buttonst5[0]
            self.baddsiblingnode = self.main.buttonst5[1]
            self.bdeletenode = self.main.buttonst5[2]
            self.bexpandall = self.main.buttonst5[3]
            self.bcollapseall = self.main.buttonst5[4]
            self.tbproperties = self.main.tbpropertiest5
        elif self.tabnumber == 5:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt6
            self.cbnodetype = self.main.cbnodetypet6
            self.baddsubnode = self.main.buttonst6[0]
            self.baddsiblingnode = self.main.buttonst6[1]
            self.bdeletenode = self.main.buttonst6[2]
            self.bexpandall = self.main.buttonst6[3]
            self.bcollapseall = self.main.buttonst6[4]
            self.tbproperties = self.main.tbpropertiest6
        elif self.tabnumber == 6:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt7
            self.cbnodetype = self.main.cbnodetypet7
            self.baddsubnode = self.main.buttonst7[0]
            self.baddsiblingnode = self.main.buttonst7[1]
            self.bdeletenode = self.main.buttonst7[2]
            self.bexpandall = self.main.buttonst7[3]
            self.bcollapseall = self.main.buttonst7[4]
            self.tbproperties = self.main.tbpropertiest7
        elif self.tabnumber == 7:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt8
            self.cbnodetype = self.main.cbnodetypet8
            self.baddsubnode = self.main.buttonst8[0]
            self.baddsiblingnode = self.main.buttonst8[1]
            self.bdeletenode = self.main.buttonst8[2]
            self.bexpandall = self.main.buttonst8[3]
            self.bcollapseall = self.main.buttonst8[4]
            self.tbproperties = self.main.tbpropertiest8
        elif self.tabnumber == 8:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt9
            self.cbnodetype = self.main.cbnodetypet9
            self.baddsubnode = self.main.buttonst9[0]
            self.baddsiblingnode = self.main.buttonst9[1]
            self.bdeletenode = self.main.buttonst9[2]
            self.bexpandall = self.main.buttonst9[3]
            self.bcollapseall = self.main.buttonst9[4]
            self.tbproperties = self.main.tbpropertiest9
        elif self.tabnumber == 9:
            self.hierarchymodeltreeview = self.main.hierarchymodeltreeviewt10
            self.cbnodetype = self.main.cbnodetypet10
            self.baddsubnode = self.main.buttonst10[0]
            self.baddsiblingnode = self.main.buttonst10[1]
            self.bdeletenode = self.main.buttonst10[2]
            self.bexpandall = self.main.buttonst10[3]
            self.bcollapseall = self.main.buttonst10[4]
            self.tbproperties = self.main.tbpropertiest10

    def setSesVarsFunsInTm(self):
        self.at.setSesVarsFunsInAttributes()
        self.ar.setSesVarsFunsInAspectrules()
        self.pr.setSesVarsFunsInPrio()
        self.nr.setSesVarsFunsInNrep()
        self.cp.setSesVarsFunsInCoupling()
        self.sr.setSesVarsFunsInSpecrules()

    #-----saving / opening a tree---------------------------------------------------------------------------------------

    """restore from save -> tree from list"""
    """#old function, replaced now
    def fromSave(self, nodelist, subSES=False, selconlist=""):

        subSESInsertable = False
        nameExist = True
        nodetypeOk = False

        #set the variable, telling, that the tree is being read in -> needed for node specific variables -> during reading in the tree, the write function shall not be executed due to selection change
        self.isRestoringTree = True

        #make sure that no check is made during restoring
        self.doOnceChecks = False

        # if it is a subtree which shall be inserted the parent of the first nodes must be adjusted and the depth of all
        # nodes to insert must be updated, the axiom of alternating mode must be checked
        if subSES:
            selnode = self.treeModel.getNode(self.treeSelectionModel.currentIndex())

            sameName = False
            if selnode.name() == nodelist[0][2]:
                sameName = True

            #change name of parent
            #get name of selected node
            nmesel = selnode.parent().name()
            #get parent and depth of first node
            par = nodelist[0][3]
            dep = nodelist[0][12]
            i = 0
            while i < len(nodelist):
                if nodelist[i][3] == par and nodelist[i][12] == dep:
                    nodelist[i][3] = nmesel
                i += 1

            #update depth
            #find depth of selected node
            indices = self.listAllIndices(self.treeSelectionModel.currentIndex())
            depsel = -1
            for ind in indices:
                if self.treeModel.getNode(self.treeSelectionModel.currentIndex()).parent() == self.treeModel.getNode(ind[0]):
                    depsel = ind[1]
            #update depth in nodelist
            diff = depsel - int(nodelist[0][12])
            i = 0
            while i < len(nodelist):
                nodelist[i][12] = str(int(nodelist[i][12]) + diff + 1)
                i += 1

            #check if the names of the nodes to insert already exist
            for ind in indices:
                for n in range(len(nodelist)):
                    if n>0 and self.treeModel.getNode(ind[0]).name() == nodelist[n][2]:
                        nameExist = False
                        break

            #check if the axiom of alternating mode is satisfied
            anodeType = selnode.typeInfo()
            inodeType = nodelist[0][1]

            if anodeType == inodeType:
                nodetypeOk = True

            #get new uids for the nodes and update them in the node specific properties except the specrules
            for el in range(len(nodelist)):
                #the first node is only updated, not newly inserted
                if el != 0:
                    olduid = int(nodelist[el][0])
                    newuid = self.treeModel._rootNode.findHighestUid() + el
                    # set the new uid for the nodes
                    nodelist[el][0] = str(newuid)
                    # update the uid for node specific properties
                    for ele in range(len(nodelist[el][7])):
                        if nodelist[el][7][ele][1] == str(olduid):
                            nodelist[el][7][ele][1] = str(newuid)       #<- UNTESTED
                    for ele in range(len(nodelist[el][8])):
                        if nodelist[el][8][ele][1] == str(olduid):
                            nodelist[el][8][ele][1] = str(newuid)       #<- UNTESTED

                    #update the uid for selection constraints
                    for ele in range(len(selconlist)):
                        if selconlist[ele][1] == str(olduid) and selconlist[ele][0] == nodelist[el][2]:
                            selconlist[ele][1] = str(newuid)
                        stopuids = selconlist[ele][3].split(", ")
                        stopnames = selconlist[ele][2].split(", ")
                        for ui in range(len(stopuids)):
                            if stopuids[ui] == str(olduid) and stopnames[ui] == nodelist[el][2]:
                                stopuids[ui] = str(newuid)
                                selconlist[ele][3] = ', '.join(stopuids)

            #insert the updated selection constraints
            self.main.modellist[self.main.activeTab][5].fromSave(selconlist, True)

            #update the uids in the specrules
            for el in range(len(nodelist)):
                if nodelist[el][1] == "Spec Node":
                    parentname = nodelist[el][2]
                    depth = int(nodelist[el][12]) + 1
                    #get the names
                    for ele in range(len(nodelist[el][10])):
                        name = nodelist[el][10][ele][0]
                        uid = -1
                        for elem in range(len(nodelist)):
                            if nodelist[elem][2] == name and nodelist[elem][12] == str(depth) and nodelist[elem][3] == parentname:
                                uid = nodelist[elem][0]
                                break
                        if uid != -1:
                            nodelist[el][10][ele][1] = uid

            #insertable
            subSESInsertable = sameName and nameExist and nodetypeOk

        i = 0
        while i < len(nodelist):
            #node to insert
            inodeuid = int(nodelist[i][0])
            inodetype = nodelist[i][1]
            inodename = nodelist[i][2]
            iparentnodeuid = nodelist[i][3]
            inodetextcolor = nodelist[i][4]
            inodetextbold = False
            if nodelist[i][5] == 'True':
                inodetextbold = True
            inodeattributes = nodelist[i][6]
            inodeaspectrules = nodelist[i][7]
            inodecouplings = nodelist[i][8]
            inodenumrep = nodelist[i][9]
            inodespecrules = nodelist[i][10]
            inodeprio = nodelist[i][11]
            inodedepth = int(nodelist[i][12])

            # walk through already inserted nodes and find out where to insert
            indices = self.listAllIndices(self.treeSelectionModel.currentIndex())

            nodeUidsInserted = []

            j = 0
            while j < len(indices):
                enodeuid = str(self.treeModel.getNode(indices[j][0]).getUid())
                enodedepth = indices[j][1]

                if not subSES:

                    # hinder the keepUniformity when reading an SES from file -> it would be called in the addSubNode() and addSiblingNode() functions
                    self.doOnceKeepUniformity = False

                    #first node
                    if iparentnodeuid == enodeuid and inodedepth == 0 and enodedepth == 0:
                        nodeUidsInserted.append(inodeuid)
                        self.addSubNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                        break

                    #subnodes going into depth
                    elif iparentnodeuid == enodeuid and inodedepth == (enodedepth + 1) and inodedepth > int(nodelist[i-1][12]) and inodeuid not in nodeUidsInserted:
                        # which is selected?
                        # selnode = self.treeModel.getNode(self.treeSelectionModel.currentIndex())
                        nodeUidsInserted.append(inodeuid)
                        self.addSubNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                        break

                    #node has less depth than node before
                    elif iparentnodeuid == enodeuid and inodedepth == (enodedepth + 1) and inodedepth < int(nodelist[i-1][12]):
                        #find out index of last child -> mark it for inserting sibling there
                        enodelastchild = self.treeModel.getNode(indices[j][0]).childrenlist()[-1]
                        k = 0
                        while k < len(indices):
                            if enodelastchild == self.treeModel.getNode(indices[k][0]):
                                self.treeSelectionModel.setCurrentIndex(indices[k][0], QItemSelectionModel.ClearAndSelect)
                                nodeUidsInserted.append(inodeuid)
                                self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                            k += 1
                        break

                    #siblingnodes
                    elif iparentnodeuid == enodeuid and inodedepth == (enodedepth + 1) and inodedepth == int(nodelist[i-1][12]):
                        nodeUidsInserted.append(inodeuid)
                        self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                        break

                    #allow the keepUniformity again
                    self.doOnceKeepUniformity = True

                elif subSES and subSESInsertable:   #it is a subtree which shall be inserted

                    if i == 0:
                        for l in range(len(indices)):
                            if nodelist[0][2] == self.treeModel.getNode(indices[l][0]).name():
                                #add node specific properties -> Entity Node -> Attributes
                                self.treeModel.insertNodeSpecProp(indices[l][0], nodelist[0][7], "attriblist", self.treeModel.getNode(indices[l][0]).getUid())
                    else:
                        #insert the other nodes

                        #subnodes going into depth
                        if iparentnodeuid == enodeuid and inodedepth == (enodedepth + 1) and (inodedepth > int(nodelist[i-1][12]) or i == 0):
                            # which is selected?
                            # selnode = self.treeModel.getNode(self.treeSelectionModel.currentIndex())
                            self.addSubNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)

                        #node has less depth than node before
                        elif iparentnodeuid == enodeuid and inodedepth == (enodedepth + 1) and inodedepth < int(nodelist[i-1][12]):
                            #find out index of last child -> mark it for inserting sibling there
                            enodelastchild = self.treeModel.getNode(indices[j][0]).childrenlist()[-1]
                            k = 0
                            while k < len(indices):
                                if enodelastchild == self.treeModel.getNode(indices[k][0]):
                                    self.treeSelectionModel.setCurrentIndex(indices[k][0], QItemSelectionModel.ClearAndSelect)
                                    self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                                k += 1

                        #siblingnodes
                        elif iparentnodeuid == enodeuid and inodedepth == (enodedepth + 1) and inodedepth == int(nodelist[i-1][12]):
                            self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                j += 1
            i += 1
        # resize
        self.resz()

        #allow checks again
        self.doOnceChecks = True

        #tell, that the restoring of the tree is finished
        self.isRestoringTree = False

        #return
        return subSESInsertable
    """

    """restore from save -> tree from list"""
    def fromSave(self, nodelist, subSES=False, selconlist=""):

        subSESInsertable = False
        nameExist = True
        nodetypeOk = False

        #set the variable, telling, that the tree is being read in -> needed for node specific variables -> during reading in the tree, the write function shall not be executed due to selection change
        self.isRestoringTree = True

        #make sure that no check is made during restoring
        self.doOnceChecks = False

        # if it is a subtree which shall be inserted the parent of the first nodes must be adjusted and the depth of all
        # nodes to insert must be updated, the axiom of alternating mode must be checked
        if subSES:
            selnode = self.treeModel.getNode(self.treeSelectionModel.currentIndex())

            sameName = False
            if selnode.name() == nodelist[0][2]:
                sameName = True

            #change uid of parent
            #get uid of selected node
            uidsel = selnode.parent().getUid()
            #get parent and depth of first node
            par = nodelist[0][3]
            dep = nodelist[0][12]
            i = 0
            while i < len(nodelist):
                if nodelist[i][3] == par and nodelist[i][12] == dep:
                    nodelist[i][3] = str(uidsel)
                    break
                i += 1

            #update depth
            #find depth of selected node
            indices = self.listAllIndices(self.treeSelectionModel.currentIndex())
            depsel = -1
            for ind in indices:
                if self.treeModel.getNode(self.treeSelectionModel.currentIndex()).parent() == self.treeModel.getNode(ind[0]):
                    depsel = ind[1]
            #update depth in nodelist
            diff = depsel - int(nodelist[0][12])
            i = 0
            while i < len(nodelist):
                nodelist[i][12] = str(int(nodelist[i][12]) + diff + 1)
                i += 1

            #check if the names of the nodes to insert already exist
            for ind in indices:
                for n in range(len(nodelist)):
                    if n>0 and self.treeModel.getNode(ind[0]).name() == nodelist[n][2]:
                        nameExist = False
                        break

            #check if the axiom of alternating mode is satisfied
            anodeType = selnode.typeInfo()
            inodeType = nodelist[0][1]

            if anodeType == inodeType:
                nodetypeOk = True

            #get new uids for the nodes and update them in the node specific properties
            nodeparentuidchangedindices = [0]
            oldnewuid = {}
            for el in range(len(nodelist)):
                #the first node is only updated, not newly inserted
                if el != 0:
                    olduid = int(nodelist[el][0])
                    newuid = self.treeModel._rootNode.findHighestUid() + el
                    oldnewuid.update({nodelist[el][0]: str(newuid)})
                    # set the new uid for the nodes
                    nodelist[el][0] = str(newuid)
                    #update all parent uids in the nodelist refering to the old uid
                    for ele in range(len(nodelist)):
                        if nodelist[ele][3] == str(olduid) and (ele not in nodeparentuidchangedindices):
                            nodelist[ele][3] = str(newuid)
                            nodeparentuidchangedindices.append(ele)
            #add the name and uid of the first node, since it shall not be changed
            for l in range(len(indices)):
                if nodelist[0][2] == self.treeModel.getNode(indices[l][0]).name():
                    uid = self.treeModel.getNode(indices[l][0]).getUid()
                    oldnewuid.update({nodelist[0][0]: str(uid)})

            #go through nodes and update the uids of node specific properties
            for el in range(len(nodelist)):
                if nodelist[el][1] == "Aspect Node" or nodelist[el][1] == "Maspect Node":
                    #update the uid for aspectrules
                    for ele in range(len(nodelist[el][7])):
                        try:
                            newuid = oldnewuid.get(nodelist[el][7][ele][1])
                            if newuid:
                                nodelist[el][7][ele][1] = str(newuid)
                        except:
                            pass
                    #update the uid for couplings
                    for ele in range(len(nodelist[el][8])):
                        #source node
                        try:
                            newuid = oldnewuid.get(nodelist[el][8][ele][1])
                            if newuid:
                                nodelist[el][8][ele][1] = str(newuid)
                        except:
                            pass
                        #sink node
                        try:
                            newuid = oldnewuid.get(nodelist[el][8][ele][4])
                            if newuid:
                                nodelist[el][8][ele][4] = str(newuid)
                        except:
                            pass

                if nodelist[el][1] == "Spec Node":
                    #update the uid for specrules
                    for ele in range(len(nodelist[el][10])):
                        try:
                            newuid = oldnewuid.get(nodelist[el][10][ele][1])
                            if newuid:
                                nodelist[el][10][ele][1] = str(newuid)
                        except:
                            pass

            #update the uid for selection constraints
            for ele in range(len(selconlist)):
                #for the startnode
                try:
                    newuid = oldnewuid.get(selconlist[ele][1])
                    if newuid:
                        selconlist[ele][1] = str(newuid)
                except:
                    pass
                #for the stopnodes
                try:
                    stopuids = selconlist[ele][3].split(", ")
                    newuids = []
                    for st in stopuids:
                        newuid = oldnewuid.get(st)
                        if newuid:
                            newuids.append(newuid)
                        else:
                            newuids.append("")
                    selconlist[ele][3] = ', '.join(newuids)
                except:
                    pass
            #insert the updated selection constraints
            self.main.modellist[self.main.activeTab][5].fromSave(selconlist, True)

            #insertable
            subSESInsertable = sameName and nameExist and nodetypeOk

        #now insert the nodes keeping uid and index in a dictionary
        nodesInserted = {}  #inodeuid: [QModelIndex, [childuids]]
        enodeuid = -1   #uid of the node beefore
        enodedepth = -1 #depth of the node before
        i = 0
        while i < len(nodelist):
            #for the last node to insert tell, that the restoring of the tree is finished -> so the node specific attributes are read for the last node to insert
            if i == len(nodelist)-1:
                self.isRestoringTree = False

            #node to insert
            inodeuid = int(nodelist[i][0])
            inodetype = nodelist[i][1]
            inodename = nodelist[i][2]
            iparentnodeuid = nodelist[i][3]
            inodetextcolor = nodelist[i][4]
            inodetextbold = False
            if nodelist[i][5] == 'True':
                inodetextbold = True
            inodeattributes = nodelist[i][6]
            inodeaspectrules = nodelist[i][7]
            inodecouplings = nodelist[i][8]
            inodenumrep = nodelist[i][9]
            inodespecrules = nodelist[i][10]
            inodeprio = nodelist[i][11]
            inodedepth = int(nodelist[i][12])

            if not subSES:
                # hinder the keepUniformity when reading an SES from file -> it would be called in the addSubNode() and addSiblingNode() functions
                self.doOnceKeepUniformity = False

                #first node
                if not nodesInserted:   #if no nodes are inserted yet, the dict is empty
                    ind = self.addSubNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                    #add the newly created node to the dictionary
                    nodesInserted.update({inodeuid: [ind, []]})
                    #update enode... with inode...
                    enodeuid = inodeuid
                    enodedepth = inodedepth

                #add sibling node - if the node before has the same depth, it is a sibling
                elif enodedepth == inodedepth:
                    #mark the sibling before the node to insert
                    parentind = nodesInserted.get(enodeuid)[0]
                    self.treeSelectionModel.setCurrentIndex(parentind, QItemSelectionModel.ClearAndSelect)
                    #now insert
                    ind =  self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                    #add the newly created node to the dictionary
                    nodesInserted.update({inodeuid: [ind, []]})
                    #add the newly created node as child to the parent's dictionary
                    dictlist = nodesInserted.get(int(iparentnodeuid))
                    dictlist[1].append(int(inodeuid))
                    nodesInserted.update({int(iparentnodeuid): dictlist})
                    #update enode... with inode...
                    enodeuid = inodeuid
                    enodedepth = inodedepth

                #add sub node - if the node before has a smaller depth, it goes in the depth
                elif enodedepth < inodedepth:
                    #mark the parent of the node to insert
                    parentind = nodesInserted.get(int(iparentnodeuid))[0]
                    self.treeSelectionModel.setCurrentIndex(parentind, QItemSelectionModel.ClearAndSelect)
                    #now insert
                    ind = self.addSubNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                    #add the newly created node to the dictionary
                    nodesInserted.update({inodeuid: [ind, []]})
                    #add the newly created node as child to the parent's dictionary
                    dictlist = nodesInserted.get(int(iparentnodeuid))
                    dictlist[1].append(int(inodeuid))
                    nodesInserted.update({int(iparentnodeuid): dictlist})
                    #update enode... with inode...
                    enodeuid = inodeuid
                    enodedepth = inodedepth

                #add sibling node - if the node before has a higher depth, a sibling at a node with a higher depth needs to be added
                elif enodedepth > inodedepth:
                    #mark the last child of the parent of the node to insert
                    lastchilduid = nodesInserted.get(int(iparentnodeuid))[1][-1]
                    lastchildind = nodesInserted.get(lastchilduid)[0]
                    self.treeSelectionModel.setCurrentIndex(lastchildind, QItemSelectionModel.ClearAndSelect)
                    #now insert
                    ind = self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                    #add the newly created node as child to the parent's dictionary
                    nodesInserted.update({inodeuid: [ind, []]})
                    #add the newly created node as child to the parent's dictionary
                    dictlist = nodesInserted.get(int(iparentnodeuid))
                    dictlist[1].append(int(inodeuid))
                    nodesInserted.update({int(iparentnodeuid): dictlist})
                    #update enode... with inode...
                    enodeuid = inodeuid
                    enodedepth = inodedepth

                #allow the keepUniformity again
                self.doOnceKeepUniformity = True

            elif subSES and subSESInsertable:  # it is a subtree which shall be inserted
                if i == 0:
                    #for the first node only the attributes need to be inserted since a subSES is only insertable at nodes with the same name as the first node of the subSES -> it needs to be found in the SES -> go through indices
                    for l in range(len(indices)):
                        if nodelist[0][2] == self.treeModel.getNode(indices[l][0]).name():
                            # add node specific properties -> Entity Node -> Attributes
                            self.treeModel.insertNodeSpecProp(indices[l][0], nodelist[0][7], "attriblist", self.treeModel.getNode(indices[l][0]).getUid())
                            #mark it
                            self.treeSelectionModel.setCurrentIndex(indices[l][0], QItemSelectionModel.ClearAndSelect)
                            #add the node to the dictionary -> the uid of the node in the subSES to insert so that the parent uid of the child does not need to be updated -> once inserted it is taken the uid of the node in the SES and not of the subSES
                            nodesInserted.update({int(nodelist[0][0]): [indices[l][0], []]})
                            #update enode... with inode...
                            enodeuid = inodeuid
                            enodedepth = inodedepth
                            break
                else:
                    #insert the other nodes

                    # add sibling node - if the node before has the same depth, it is a sibling
                    if enodedepth == inodedepth:
                        # mark the sibling before the node to insert
                        parentind = nodesInserted.get(enodeuid)[0]
                        self.treeSelectionModel.setCurrentIndex(parentind, QItemSelectionModel.ClearAndSelect)
                        # now insert
                        ind = self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                        # add the newly created node to the dictionary
                        nodesInserted.update({inodeuid: [ind, []]})
                        # add the newly created node as child to the parent's dictionary
                        dictlist = nodesInserted.get(int(iparentnodeuid))
                        dictlist[1].append(int(inodeuid))
                        nodesInserted.update({int(iparentnodeuid): dictlist})
                        # update enode... with inode...
                        enodeuid = inodeuid
                        enodedepth = inodedepth

                    #add sub node - if the node before has a smaller depth, it goes in the depth
                    elif enodedepth < inodedepth:
                        #mark the parent of the node to insert
                        parentind = nodesInserted.get(int(iparentnodeuid))[0]
                        self.treeSelectionModel.setCurrentIndex(parentind, QItemSelectionModel.ClearAndSelect)
                        #now insert
                        ind = self.addSubNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                        #add the newly created node to the dictionary
                        nodesInserted.update({inodeuid: [ind, []]})
                        #add the newly created node as child to the parent's dictionary
                        dictlist = nodesInserted.get(int(iparentnodeuid))
                        dictlist[1].append(int(inodeuid))
                        nodesInserted.update({int(iparentnodeuid): dictlist})
                        #update enode... with inode...
                        enodeuid = inodeuid
                        enodedepth = inodedepth

                    #add sibling node - if the node before has a higher depth, a sibling at a node with a higher depth needs to be added
                    elif enodedepth > inodedepth:
                        #mark the last child of the parent of the node to insert
                        lastchilduid = nodesInserted.get(int(iparentnodeuid))[1][-1]
                        lastchildind = nodesInserted.get(lastchilduid)[0]
                        self.treeSelectionModel.setCurrentIndex(lastchildind, QItemSelectionModel.ClearAndSelect)
                        #now insert
                        ind = self.addSiblingNode(inodeuid, inodetype, inodename, inodetextcolor, inodetextbold, inodeattributes, inodeaspectrules, inodecouplings, inodenumrep, inodespecrules, inodeprio)
                        #add the newly created node as child to the parent's dictionary
                        nodesInserted.update({inodeuid: [ind, []]})
                        #add the newly created node as child to the parent's dictionary
                        dictlist = nodesInserted.get(int(iparentnodeuid))
                        dictlist[1].append(int(inodeuid))
                        nodesInserted.update({int(iparentnodeuid): dictlist})
                        #update enode... with inode...
                        enodeuid = inodeuid
                        enodedepth = inodedepth

            i += 1
        # resize
        self.resz()

        #allow checks again
        self.doOnceChecks = True

        #tell, that the restoring of the tree is finished (actually, this should be done when the last node is about to be read in (see before), but make sure)
        self.isRestoringTree = False

        #return
        return subSESInsertable


    """tree to list"""
    def treeToList(self, subSES=False):
        treeList = []
        indices = self.listAllIndices(self.treeSelectionModel.currentIndex())
        firstNodeDepth = -1
        if subSES:
            indicestosave = []
            for ind in indices:
                node = self.treeModel.getNode(self.treeSelectionModel.currentIndex())
                if node.typeInfo() == "Entity Node":
                    #find indices which are part of the subtree by looking at the depth -> firstNodeDepth contains the depth of the first node
                    if self.treeModel.getNode(ind[0]).getUid() == node.getUid():
                        firstNodeDepth = ind[1]
                        indicestosave.append(ind)
                    elif firstNodeDepth != -1 and ind[1] > firstNodeDepth:
                        indicestosave.append(ind)
                    elif firstNodeDepth != -1 and ind[1] <= firstNodeDepth:
                        break
            indices = indicestosave
        for i in range(len(indices)):
            node = self.treeModel.getNode(indices[i][0])
            uid = str(node.getUid())
            type = node.typeInfo()
            name = node.name()
            if node.name() != 'SES' and node.parent() is not None:
                parent = str(node.parent().getUid())
            else:
                parent = 'None'
            textColor = node.color()
            bold = str(node.bold())
            attributes = []
            aspectrule = []
            coupling = []
            number_replication = '1'
            specrule = []
            priority = "1"
            if type == "Entity Node":
                attributes = node.attributes
            if type == "Aspect Node":
                aspectrule = node.aspectrule
                coupling = node.coupling
                priority = node.priority
            if type == "Maspect Node":
                aspectrule = node.aspectrule
                coupling = node.coupling
                number_replication = node.number_replication
                priority = node.priority
            if type == "Spec Node":
                specrule = node.specrule
            #if it is a subtree, make the depth of the first node to zero and adjust the depth of the subnodes
            if not subSES:    #no change in depth necessary, since it is no subtree
                depth = str(indices[i][1])
            else:
                depth = str(indices[i][1]-firstNodeDepth)  #it is a subtree, change of the depth is necessary
            # if it is a subtree, make also sure that the first node gets the parentuid "0" -> so it can be opened as SES
            if subSES and i==0:
                parent = "0"    #it is a subtree, the first node of the subtree needs to have the parent with uid 0
            treeList.append([uid, type, name, parent, textColor, bold, attributes, aspectrule, coupling, number_replication, specrule, priority, depth])
        return treeList

    #-----setting the last selected index-------------------------------------------------------------------------------

    """set the last selected index"""
    def setLastSelectedIndex(self):
        if not self.lastSelectedIndex.isValid():
            self.lastSelectedIndex = self.treeSelectionModel.currentIndex()
            self.currentSelectedIndex = self.treeSelectionModel.currentIndex()
        else:
            self.lastSelectedIndex = self.currentSelectedIndex
            self.currentSelectedIndex = self.treeSelectionModel.currentIndex()

    #-----prepare / set the field of the node types (insert all possible types)-----------------------------------------

    """prepare the node type field"""
    def prepareCBNodeType(self):
        self.cbnodetype.addItems(self.nodeTypes)
        i=0
        for icon in self.nodeTypeIcons:
            self.cbnodetype.setItemIcon(i, icon)
            i += 1

    """setting the combobox Node Type"""
    def setCbNodeTypeField(self):
        if not self.isRestoringTree:    #only do, when the tree is not restored (for the last node, self.isRestoringTree is set to False)
            #check if there are nodes at all (not needed any more)
            #if self.hierarchymodeltreeview.currentIndex().isValid():
            #find selected index
            index = self.hierarchymodeltreeview.currentIndex()
            #check if first element (index.row() is -1, if nothing is selected -> first element)
            if index.parent().row() == -1:
                if self.cbnodetype.findText("Entity Node") == -1:
                    self.cbnodetype.insertItem(1, self.nodeTypeIcons[1], "Entity Node")
                self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Entity Node"))
                self.cbnodetype.setEnabled(False)
            else:
                node = self.treeModel.getNode(index)
                type = node.typeInfo()
                if type == "Entity Node":
                    if self.cbnodetype.findText("Entity Node") == -1:
                        self.cbnodetype.insertItem(1, self.nodeTypeIcons[1], "Entity Node")
                    self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Entity Node"))
                    self.cbnodetype.setEnabled(False)
                elif type == "Descriptive Node":
                    if self.cbnodetype.findText("Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Node"))
                    if self.cbnodetype.findText("Entity Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Entity Node"))
                    if self.cbnodetype.findText("Descriptive Node") == -1:
                        self.cbnodetype.insertItem(0, self.nodeTypeIcons[2], "Descriptive Node")
                    self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Descriptive Node"))
                    self.cbnodetype.setEnabled(True)
                elif type == "Aspect Node":
                    if self.cbnodetype.findText("Entity Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Entity Node"))
                    if self.cbnodetype.findText("Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Node"))
                    if self.cbnodetype.findText("Descriptive Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Descriptive Node"))
                    self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Aspect Node"))
                    self.cbnodetype.setEnabled(True)
                elif type == "Maspect Node":
                    if self.cbnodetype.findText("Entity Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Entity Node"))
                    if self.cbnodetype.findText("Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Node"))
                    if self.cbnodetype.findText("Descriptive Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Descriptive Node"))
                    self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Maspect Node"))
                    self.cbnodetype.setEnabled(True)
                elif type == "Spec Node":
                    if self.cbnodetype.findText("Entity Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Entity Node"))
                    if self.cbnodetype.findText("Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Node"))
                    if self.cbnodetype.findText("Descriptive Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Descriptive Node"))
                    self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Spec Node"))
                    self.cbnodetype.setEnabled(True)
                else: #type == "Node"
                    if self.cbnodetype.findText("Entity Node") != -1:
                        self.cbnodetype.removeItem(self.cbnodetype.findText("Entity Node"))
                    self.cbnodetype.setCurrentIndex(self.cbnodetype.findText("Node"))
                    self.cbnodetype.setEnabled(True)

    #-----resize--------------------------------------------------------------------------------------------------------
    """resizing """
    def resz(self):
        if not self.isRestoringTree:    #only do, when the tree is not restored (for the last node, self.isRestoringTree is set to False)
            i = 1
            while i < 8:
                self.hierarchymodeltreeview.resizeColumnToContents(i)
                i += 1

    #-----adding (with alternating mode) or deleting nodes, expand or collapse tree-------------------------------------

    """Adding a SubNode"""
    """index is a QModelIndex with the member functions row() column() parent()"""
    """index.row() index.column() index.parent() index.sibling()"""
    def addSubNode(self, uid=-1, type="", name="", textColor="#000000", bold=False, attributes="", aspectrules="", couplings="", numrep="1", specrules="", priority="1"):
        index = self.hierarchymodeltreeview.currentIndex()

        #the index of the newly created node
        newind = None

        #index.row() is -1, if nothing is selected -> creation of first node
        if index.row() == -1:
            #find parent
            par = self.treeModel.index(0, 0, QtCore.QModelIndex())  #find the parent
            #find type
            if not type:
              type = self.alternatingMode(QtCore.QModelIndex(), True)
            #add item
            position = -1
            self.treeModel.insertRows(position, 1, par, uid, type, name, None, textColor, bold, attributes, aspectrules, couplings, numrep, specrules, priority)
            newind = self.treeModel.index(index.row() + 1, 0, index.parent())
            #keep uniformity not necessary, because it it the first node
            #set selection
            self.treeSelectionModel.setCurrentIndex(newind, QItemSelectionModel.ClearAndSelect)     #if the program crashes here, just have a look, which other functions are called by signals
            #resize the view
            self.hierarchymodeltreeview.resizeColumnToContents(0)
            #set the node type field
            self.setCbNodeTypeField()

        #index is valid and is selected -> index.row() != -1 -> add below selection -> creating subNodes
        else:
            #parent is variable index
            #find type
            if not type:
                type = self.alternatingMode(index, True)
            #add item
            position = 0
            self.treeModel.insertRows(position, 1, index, uid, type, name, None, textColor, bold, attributes, aspectrules, couplings, numrep, specrules, priority)
            newind = self.treeModel.index(0, 0, index)
            #keep uniformity
            self.checkAxiomsUpdate("an", "", position, newind, "su")
            #set selection
            self.treeSelectionModel.setCurrentIndex(newind, QItemSelectionModel.ClearAndSelect)     #if the program crashes here, just have a look, which other functions are called by signals
            #resize the view
            self.hierarchymodeltreeview.resizeColumnToContents(0)
            #set the node type field
            self.setCbNodeTypeField()

        # resize
        self.resz()
        # keep the uniformity
        #self.keepUniformity("an", position, index.row(), index.column(), index)
        #tree changed signal
        self.treeChangedSignal.emit()
        return newind

    """Adding a SiblingNode"""
    """index is a QModelIndex with the member functions row() column() parent()"""
    """index.row() index.column() index.parent() index.sibling()"""
    def addSiblingNode(self, uid=-1, type="", name="", textColor="#000000", bold=False, attributes="", aspectrules="", couplings="", numrep="1", specrules="", priority="1"):
        index = self.hierarchymodeltreeview.currentIndex()

        #the index of the newly created node
        newind = None

        position = -1
        #par = QModelIndex

        #index.row() is -1, if nothing is selected -> creation of first node
        if index.row() == -1:
            #self.treeModel.insertRows(-1, 1)   #we do not need it, since after creation of the first subNode one node is always selected
            QMessageBox.information(None, "Inserting not possible", "Please insert a SubNode first.", QtWidgets.QMessageBox.Ok)

        #something is selected -> index.row() != -1 -> add behind selection
        else:
            #check, if first decision knot exists
            if not (self.treeModel.getNode(index.parent()).name() == "SES" and index.row() == 0 and index.column() == 0):
                #find parent
                par = index.parent()
                #find type
                if not type:
                    type = self.alternatingMode(index)
                #add item
                position = index.row()+1
                self.treeModel.insertRows(position, 1, par, uid, type, name, None, textColor, bold, attributes, aspectrules, couplings, numrep, specrules, priority)
                newind = self.treeModel.index(index.row() + 1, 0, index.parent())
                # keep uniformity
                self.checkAxiomsUpdate("an", "", position, newind, "si")
                #set selection
                self.treeSelectionModel.setCurrentIndex(newind, QItemSelectionModel.ClearAndSelect)     #if the program crashes here, just have a look, which other functions are called by signals
                #resize the view
                self.hierarchymodeltreeview.resizeColumnToContents(0)
                #set the node type field
                self.setCbNodeTypeField()
            else:
                QMessageBox.information(None, "Inserting not possible", "Please insert a SubNode first.", QtWidgets.QMessageBox.Ok)

        # resize
        self.resz()
        # keep the uniformity
        #self.keepUniformity("an", position, index.row()+1, index.column(), par)
        #tree changed signal
        self.treeChangedSignal.emit()
        return newind

    """possible types - alternating mode (needed for inserting a sub node or a sibling node)"""
    def alternatingMode(self, index, newRank=False):
        type = ""
        if newRank:
            if not index.isValid():
                type = "Entity Node"
            elif self.treeModel.getNode(index).typeInfo() != "Entity Node":
                type = "Entity Node"
            elif self.treeModel.getNode(index).typeInfo() == "Entity Node":
                type = "Descriptive Node"
        else:
            if self.treeModel.getNode(index).typeInfo() != "Entity Node":
                type = "Descriptive Node"
            elif self.treeModel.getNode(index).typeInfo() == "Entity Node":
                type = "Entity Node"
        return type

    """Deleting a Node"""
    """index is a QModelIndex with the member functions row() column() parent()"""
    """index.row() index.column() index.parent() index.sibling()"""
    def deleteNode(self, selectall=False, indexToDel=None):
        if not selectall:
            if indexToDel == None:
                #find selected index
                index = self.hierarchymodeltreeview.currentIndex()
            else:
                #take the passed index
                index = indexToDel
        else:
            index = self.listAllIndices(self.hierarchymodeltreeview.currentIndex())[0][0]
        # make sure, no checks are executed due to focus change
        self.allowChecks = False
        #now delete
        #deletedUid = -1
        deletedName = ""
        #index.row() is -1, if nothing is selected
        if index.row() == -1:
            pass        #for deleting something has to be selected
        else:
            #something is selected -> index.row() != -1 -> delete
            #deletedUid = self.treeModel.getNode(index).getUid()
            deletedName = self.treeModel.getNode(index).name()
            self.treeModel.removeRows(index.row(), 1, index.parent())
            self.setCbNodeTypeField()
            self.mw.setDisplayNodeType()
        # resize
        self.resz()
        #send signal that node was deleted
        self.nodeDeletedSignal.emit()
        # keep the uniformity
        #self.keepUniformity("dn", -1, -1, -1, None, deletedUid)
        self.checkAxiomsUpdate("dn", "", -1, QModelIndex, "", deletedName)
        # allow checks again
        self.allowChecks = True
        #tree changed signal
        self.treeChangedSignal.emit()

    """Hierarchy Model Tree View expand all"""
    def expandAll(self):
        self.hierarchymodeltreeview.expandAll()

    """Hierarchy Model Tree View collapse all"""
    def collapseAll(self):
        self.hierarchymodeltreeview.collapseAll()

    #-----changing the type of a node-----------------------------------------------------------------------------------

    """Changing the type of a Node"""
    def typeChange(self):   #call by signal
        self.tyChange(None, False)

    def typeChangeAspect(self):   #call by context menu
        self.tyChange("Aspect Node", True)

    def typeChangeMaspect(self):   #call by context menu
        self.tyChange("Maspect Node", True)

    def typeChangeSpec(self):   #call by context menu
        self.tyChange("Spec Node", True)

    def tyChange(self, type, byContextMenu):
        #find current type shown in the node type combo box
        if type is None:
            type = self.cbnodetype.currentText()
        #find selected index in the tree
        index = self.hierarchymodeltreeview.currentIndex()
        #only if it is not the first node or an entity node -> changing the type without a node at all in the list does not have effect
        if index.parent().row() != -1 and self.treeModel.getNode(index).typeInfo() != "Entity Node":
            #only if the node type combobox has the focus (since it is an active type change then and not emitted by changing the selection) or it is invoked by the context menu
            if (self.cbnodetype.hasFocus() or byContextMenu) and self.allowTypeChange:
                #make sure, the function is only executed once
                self.allowTypeChange = False
                #make sure, no uniformity check is executed due to focus change
                self.allowUniformityCheck = False
                #get information from the old node
                oldnode = self.treeModel.getNode(index)
                insertAtRow = index.row()
                parentindex = index.parent()
                #find out if name should be taken with or maybe a name attachment shall be changed
                nty = {"Entity Node": ["ENuid", "", 0], "Descriptive Node": ["DNuid", "", 0], "Aspect Node": ["ANuid", "DEC", -3], "Maspect Node": ["MNuid", "MASP", -4], "Spec Node": ["SNuid", "SPEC", -4]}
                oV = nty[oldnode.typeInfo()]
                nV = nty[type]
                if oV[0] == oldnode.name()[0:5]:
                    nme = ""
                else:
                    nme = oldnode.name()
                if nme != "" and oV[1].lower() == nme[oV[2]:].lower():
                    nme = nme[:oV[2]] + nV[1]
                # remove the original node
                self.treeModel.removeRows(index.row(), 1, index.parent())
                # create new node of other type and place it on the position of the original node
                self.treeModel.insertRows(insertAtRow, 1, parentindex, oldnode.getUid(), type, nme, oldnode.childrenlist(), oldnode.color())
                # set selection on the new node
                newindex = self.treeModel.index(insertAtRow, 0, parentindex)
                self.treeSelectionModel.setCurrentIndex(newindex, QItemSelectionModel.ClearAndSelect)
                # expand the changed row
                self.hierarchymodeltreeview.expand(newindex)
                #make sure, all other nodes of this name are type changed either -> now part of uniformity check
                #self.typeChangeSameName(newindex, oldnode.name())
                #make sure, all other nodes with this uid are type changed as well -> by calling the axioms check
                self.checkAxiomsUpdate("tc", oldnode.name())
                #allow uniformity check again
                self.allowUniformityCheck = True
                #allow re-execution of the function
                self.allowTypeChange = True

        # resize
        self.resz()
        #tree changed signal
        self.treeChangedSignal.emit()

    """if the type of a node is changed make sure the type is changed at all nodes with the same name"""
    """ #not needed any more -> now part of uniformity check
    def typeChangeSameName(self, index, oldname):
        #get the type of the index which has to be changed
        newindexname = self.treeModel.getNode(index).name()
        newindextype = self.treeModel.getNode(index).typeInfo()
        #list all indices
        indices = self.listAllIndices(index)
        #list indices which have to be changed
        toChange = []
        for inde in indices:
            if inde[0] != index and self.treeModel.getNode(inde[0]).name() == oldname:
                toChange.append(inde[0])
        #change the type where necessary
        for inde in toChange:
            #get the old node (which type has to be changed)
            oldnode = self.treeModel.getNode(inde)
            insertAtRow = inde.row()
            parentindex = inde.parent()
            #remove the original node
            self.treeModel.removeRows(inde.row(), 1, inde.parent())
            #create new node of other type and place it on the position+1 of the original node
            self.treeModel.insertRows(insertAtRow, 1, parentindex, oldnode.getUid(), newindextype, newindexname, oldnode.childrenlist(), oldnode.color())
            #expand
            newindex = self.treeModel.index(insertAtRow, 0, parentindex)
            self.hierarchymodeltreeview.expand(newindex)

        # resize
        self.resz()
        """

    #-----checking the name of a node-----------------------------------------------------------------------------------

    def checkName(self):
        if self.doOnceNameChange:
            self.doOnceNameChange = False
            nda = self.treeModel.getNode(self.currentSelectedIndex)
            if nda.name().find("_") != -1 or nda.name().find("_") != -1:
                name = nda.name().replace("_", "-").replace(" ", "-")
                self.treeModel.setData(self.currentSelectedIndex, name)
                QMessageBox.information(None, "Letters were replaced in the name",
                                        "The underscore and / or the whitespace were replaced by a minus letter. Underscores are reserved for pruning!",
                                        QtWidgets.QMessageBox.Ok)
            self.doOnceNameChange = True


    #-----adding a subtree to a node------------------------------------------------------------------------------------

    """add a subtree to a node"""
    """Input: the subtree (childrenlist of the parent node), the QModelIndex of the parent Node of the subtree"""
    def addSubTreeToNode(self, subtree, placeindex):
        inode = self.treeModel.getNode(placeindex)
        #inode is the parent of the node which is identified as duplicate and shall get the subtree
        #if there are several children of inode, they would be replaced, since subtree does not contain them -> so merge before
        newchildrenlist = []
        for chil in inode.childrenlist():
            if chil.getUid() == subtree[0].getUid():
                newchildrenlist.append(subtree[0])
            else:
                newchildrenlist.append(chil)
        self.treeModel.insertRows(placeindex.row()+1, 1, placeindex.parent(), inode.getUid(), inode.typeInfo(), inode.name(), newchildrenlist, "#000000", False, [], [], [], "1", [], "1")
        newindex = self.treeModel.index(placeindex.row()+1, 0, placeindex.parent())
        self.hierarchymodeltreeview.expand(newindex)
        self.treeModel.removeRows(placeindex.row(), 1, placeindex.parent())
        self.treeSelectionModel.setCurrentIndex(newindex, QItemSelectionModel.ClearAndSelect)

        # resize
        self.resz()
        #tree changed signal
        self.treeChangedSignal.emit()

    #-----list all indices of a tree------------------------------------------------------------------------------------

    """lists all indices of the tree starting with the first index"""
    """INPUT: any QModelIndex of the tree"""
    """OUTPUT: list of all QModelIndex of the tree in array 0 and depth of the node in array 1"""
    def listAllIndices(self, index):

        def iterateIndices(ind, output, tabLevel=-1):
            tabLevel += 1
            output.append([ind, tabLevel])
            i=0
            while i < len(self.treeModel.getNode(ind).childrenlist()):
                ind2 = self.treeModel.index(i, 0, ind)
                iterateIndices(ind2, output, tabLevel)
                i += 1
            tabLevel -= 1
            return output

        try:
            while not (self.treeModel.getNode(index).name() == "SES" and self.treeModel.getNode(index).parent() == None):
                index = self.treeModel.parent(index)
            #index is first index now go to the right index (one deeper)
            index = self.treeModel.index(0, 0, index)

            #recursive function to list all indices
            indices = iterateIndices(index, [])
        except:
            indices = [[QtCore.QModelIndex(), -1]]

        return indices

    #-----find the node to a given uid----------------------------------------------------------------------------------

    """give an uid and find the corresponding node"""
    """INPUT: any uid of the tree"""
    """OUTPUT: node of the tree"""
    def findNodeFromUid(self, uid):
        foundnode = None
        indexlist = self.listAllIndices(self.treeSelectionModel.currentIndex())
        for index in indexlist:
            node = self.treeModel.getNode(index[0])
            nodeuid = node.getUid()
            if nodeuid == uid:
                foundnode = node
                break
        return foundnode

    #-----read the properties of the selected node----------------------------------------------------------------------

    """read the properties of the selected node"""
    def readPropertiesNode(self):
        if not self.isRestoringTree:    #only do, when the tree is not restored (for the last node, self.isRestoringTree is set to False)
            #read the properties and fill the corresponding views
            nda = self.treeModel.getNode(self.currentSelectedIndex)
            if nda.typeInfo() == "Entity Node":
                self.at.emptyAttribModel()
                self.at.readAttribList(nda.attributes)
            elif nda.typeInfo() == "Aspect Node":
                self.ar.emptyAspruleModel()
                self.ar.readAspRuleList(nda.aspectrule)
                self.cp.emptyCouplingModel()
                self.cp.readCouplingList(nda.coupling)
                self.pr.readPrio(nda.priority)
            elif nda.typeInfo() == "Maspect Node":
                self.ar.emptyAspruleModel()
                self.ar.readAspRuleList(nda.aspectrule)
                self.nr.readNumRep(nda.number_replication)
                self.cp.emptyCouplingModel()
                self.cp.readCouplingList(nda.coupling)
                self.pr.readPrio(nda.priority)
            elif nda.typeInfo() == "Spec Node":
                self.sr.emptySpecruleModel()
                self.sr.readSpecRuleList(nda.specrule)

    #-----get the paths of the tree-------------------------------------------------------------------------------------

    """find the paths of the tree"""
    def findPaths(self):
        # all nodes
        indices = self.listAllIndices(self.treeSelectionModel.currentIndex())
        nodelist = []
        for inde in indices:
            nodelist.append([self.treeModel.getNode(inde[0]), inde[1]])
        # paths
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

    #-----keep track of the uids and the names of the tree--------------------------------------------------------------
    #to keep track of uids and names in the tree is necessary for renaming nodes with the same name -> otherwise after renaming one node it would be unknown which node with the same name there is in the tree
    def updateUidNodenameDict(self):   #update this dict on selection change
        if not self.isRestoringTree:
            for ind in self.listAllIndices(self.currentSelectedIndex):
                node = self.treeModel.getNode(ind[0])
                self.main.uidNodenameDict.update({node.getUid(): node.name()})

    #-----check, if two nodes are brothers------------------------------------------------------------------------------

    """check, if two nodes are brothers taking the uid of the node"""
    def areBrothers(self, node1uid, node2uid):
        #all nodes
        indices = self.listAllIndices(self.currentSelectedIndex)
        # check for duplicates
        nodelist = []
        for inde in indices:
            nodelist.append([self.treeModel.getNode(inde[0]), inde[1]])
        node1 = self.findNodeFromUid(node1uid)
        node2 = self.findNodeFromUid(node2uid)

        inode1 = -1
        inode2 = -1
        i = 0
        while i < len(nodelist):
            if nodelist[i][0] == node1:
                inode1 = i
            if nodelist[i][0] == node2:
                inode2 = i
            i += 1

        #if the nodes are on the same layer and have the same parent they are brothers
        areBrothers = False
        if nodelist[inode1][1] == nodelist[inode2][1] and nodelist[inode1][0].parent() == nodelist[inode2][0].parent():
            areBrothers = True
        return areBrothers

    #checks and additions-----------------------------------------------------------------------------------------------

    def checkAxiomsCurrentNodeNameChanged(self):   #name or property of the node changed
        self.checkAxiomsUpdate("nc")

    def checkAxiomsSelectionChanged(self):
        self.checkAxiomsUpdate("sc")

    #uniformity shall be kept by inserting a node specific property (attribute...) into a duplicate -> it is directly inserted (current node)
    def checkAxiomsCurrentNodePropertiesInserted(self):
        self.checkAxiomsUpdate("pi")

    """
    when a selection is changed, the name is changed or the type is changed, add, change or delete the _NameOfTheNode attribute at entities following multi-aspects
    when a node is changed in name, make sure, other nodes with the old name are changed as well (have the same name, but not the same uid)
    when a node is changed in name or the selection is changed:
        check the name (no axiom)
        check for valid brothers
        check for strict hierarchy
        make uniformity
    when the type of a node is changed: make sure, identical nodes (name) are changed as well
    when properties are inserted, make sure, they are inserted in nodes with the same name as well
    when a node is appended, make sure, it is appended to all fathers with the same name
    when a node is deleted, make sure, it is deleted in all same fathers as well
    kind: "nc" = name changed: check all axioms
    kind: "sc" = selection changed: the current node is the lastSelectedIndex, because the selection was changed, check all axioms
    kind: "tc" = type changed: identical nodes (name) have to be type changed as well (uniformity), changing the type the name can have changed -> pass the name before type change
    kind: "pi" = properties inserted: keep the uniformity by inserting the properties of the original node
    kind: "an" = append node: an appended node needs to be appended to identical nodes (uniformity)
    kind: "dn" = delete node: a deleted node needs to be deleted in identical nodes as well (uniformity)
    """
    def checkAxiomsUpdate(self, kind, nameBeforeTypeChange="", positionToInsert=-1, indexOfNewChild=QModelIndex, subSibling="su", nameDeleted=""):
        if self.doOnceChecks:
            self.doOnceChecks = False

            #append an attribute _NameOfTheNode to a child entity of an multi-aspect node if it has not this attribute yet -> deal with changed names as well

            if kind == "nc" or kind == "sc" or kind == "tc":
                try:
                    wNode = self.treeModel.getNode(self.currentSelectedIndex)
                    ndlst = []
                    todo = 0
                    if kind in ["nc", "sc"] and wNode.parent() and wNode.parent().typeInfo() == "Maspect Node": #when name or selection is changed, the node is clicked -> the parent must be an maspeect (if it exists at all)
                        ndlst = [wNode]
                        todo = 1
                    elif kind == "tc" and wNode.typeInfo() == "Maspect Node":   #when type is changed, the parent is clicked -> the clicked node must be an maspeect
                        ndlst = wNode.childrenlist()
                        todo = 2
                    elif kind == "tc" and wNode.typeInfo() != "Maspect Node":   #when type is changed, the parent is clicked -> the clicked node must be an maspeect
                        ndlst = wNode.childrenlist()
                        todo = 3
                    for ndel in ndlst:
                        atlst = ndel.attributes
                        if todo == 1 and atlst and atlst[0][0].startswith("_"):
                            #attribute exists, check if the name is correct (the node could have been renamed)
                            if atlst[0][0] != "_" + wNode.name():
                                atlst[0][0] = "_" + wNode.name()
                                #updaten in the attribmodel to show changes in ui
                                index = self.at.attribmodel.index(0, 0)
                                self.at.attribmodel.setData(index, "_" + wNode.name())
                        elif todo in [1, 2]:
                            #insert the attribute
                            atlst.insert(0, ['_' + wNode.name(), '0', '', 'internal variable'])
                            self.at.attribmodel.removeRows(0, self.at.attribmodel.rowCount())   #delete all rows
                            self.at.readAttribList(atlst)   #read the new rows according to atlst
                        elif todo == 3:
                            #delete the attribute if it is an _ attribute
                            if atlst and atlst[0][0].startswith("_"):
                                del atlst[0]
                except:
                    pass

            #do the other checks / additions

            #get current node (which has just been changed) and its index (if the selection has changed, the changed node is in the lastSelectedIndex)
            currentNode = self.treeModel.getNode(self.currentSelectedIndex)
            cindex = self.currentSelectedIndex
            if kind == "sc":    #if the selection has changed, take the last selected node instead of the current selected node (since the selection is changed)
                currentNode = self.treeModel.getNode(self.lastSelectedIndex)
                cindex = self.lastSelectedIndex

            #get all QModelIndices of the tree
            indices = self.listAllIndices(self.currentSelectedIndex)

            # get a dictionary with the information: for each nodename (key) how many nodes there are, their depth and QModelIndex
            nameNodeDepthDict = {}  # dictionary with nodename as key and the node itself, the depth and the QModelIndex of the node as value
            #uidNodeDict = {}    #dictionary with uid as key and the node itself as value
            for inde in indices:
                nd = self.treeModel.getNode(inde[0])
                #fill nameNodeDict
                ndInDict = nameNodeDepthDict.get(nd.name())
                if not ndInDict:
                    nameNodeDepthDict.update({nd.name(): [[nd, inde[1], inde[0]]]})
                else:
                    ndInDict.append([nd, inde[1], inde[0]])
                    nameNodeDepthDict.update({nd.name(): ndInDict})
                #fill uidNodeDict
                #ndInDict = uidNodeDict.get(nd.getUid())
                #if not ndInDict:
                    #uidNodeDict.update({nd.getUid(): [nd]})
                #else:
                    #ndInDict.append(nd)
                    #uidNodeDict.update({nd.getUid(): ndInDict})

            #when name changed and there is already a node with the same name -> change that name too
            if kind == "nc":
                oldname = self.main.uidNodenameDict.get(currentNode.getUid())
                #the old name is received, now search for duplicates -> use the dictionary
                ndInDict = nameNodeDepthDict.get(oldname)
                #if a duplicate is found -> update
                if ndInDict:
                    #there is still one node with the same name
                    renameAll = True
                    #if this is the first node of an identical subtree, offer to rename it without renaming the node(s) with the same name
                    if len(ndInDict) > 0:
                        ndp = nameNodeDepthDict.get(ndInDict[0][0].parent().name())
                        if len(ndp) == 1:
                            #it seems to be the parent of an identical tree
                            reply = QMessageBox.question(None, "Uniformity",
                                                         "You have renamed the first node of an identical subtree due to uniformity. Do you want to rename the node without renaming nodes with the same name?",
                                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                renameAll = False
                    if renameAll:
                        for nd in ndInDict:
                            nd[0].setName(currentNode.name())
                #update uidNodenameDict with the new name
                self.main.uidNodenameDict.update({currentNode.getUid(): currentNode.name()})

            #when name changed or selection changed: the axioms need to be checked
            elif kind == "nc" or kind == "sc":
                if self.allowChecks:
                    # ------------------------------------
                    #check the name
                    nameConventionViolated = False
                    if currentNode.name().find(", ") != -1: #actually, spaces in nodenames are replaced with a minus
                        self.treeSelectionModel.setCurrentIndex(cindex, QItemSelectionModel.ClearAndSelect)
                        nameConventionViolated = True
                        QMessageBox.information(None, "The name contains illegal letters", "The name contains a comma followed by a whitespace which is illegal. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                    # ------------------------------------
                    #check, that the brothers are valid -> brothers may not have the same name
                    # brothers have the same father (and the same depth)
                    # find current node in the nameNodeDeptDict -> only if there are more than one entry for one name, it have to be checked the father and the depth
                    nameNodes = nameNodeDepthDict.get(currentNode.name())
                    validBrothersViolated = False
                    if nameNodes and len(nameNodes) > 1:    #if nameNodes is not None and ...
                        for nn in range(len(nameNodes)-1):
                            if nameNodes[nn][0].parent() == nameNodes[nn+1][0].parent() and nameNodes[nn][1] == nameNodes[nn+1][1]: #the same parent and the same depth
                                validBrothersViolated = True
                                break
                    if validBrothersViolated:
                        self.treeSelectionModel.setCurrentIndex(cindex, QItemSelectionModel.ClearAndSelect)
                        QMessageBox.information(None, "No valid brothers", "The axiom of valid brothers is violated. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                    # ------------------------------------
                    #strict hierarchy
                    #get the paths of the tree
                    paths = self.findPaths()
                    #compare every node in the path -> and break when a double is found (easier than just comparing current node)
                    strictHierarchyViolated = False
                    for pa in paths:  # pa is one path
                        for nm in pa:
                            for na in pa:
                                if na != nm and na[0].name() == nm[0].name():
                                    strictHierarchyViolated = True
                    if strictHierarchyViolated:
                        self.treeSelectionModel.setCurrentIndex(cindex, QItemSelectionModel.ClearAndSelect)
                        QMessageBox.information(None, "No strict hierarchy", "The axiom of strict hierarchy is violated. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                    # ------------------------------------
                    #uniformity -> if a node gets the same name, it shall get the same uid, properties and subtree
                    #only, if before all was good
                    if not nameConventionViolated and not validBrothersViolated and not strictHierarchyViolated:
                        #only, if the uniformity check is allowed at the moment
                        if self.allowUniformityCheck:
                            # find current node -> get the name
                            actname = ""
                            i = 0
                            for ind in indices:
                                if ind[0] == cindex:
                                    actname = self.treeModel.getNode(ind[0]).name()
                                    break
                                i += 1  #i is the position of the selected node

                            #find next duplicate (if there are more duplicates we only need one because the subtrees must be the same)
                            isdouble = False
                            j = 0
                            for ind in indices:
                                if ind[0] != cindex and self.treeModel.getNode(ind[0]).name() == actname:
                                    isdouble = True
                                    break
                                j += 1  #j is the position of the first node which shall be inserted after position i

                            #tree parts
                            if isdouble:
                                changed = []
                                doubled = []
                                ii = i
                                jj = j

                                changed.append(indices[ii])
                                while ii < len(indices)-1 and indices[ii][1] < indices[ii+1][1]:
                                    changed.append(indices[ii+1])
                                    ii += 1

                                doubled.append(indices[jj])
                                while jj < len(indices)-1 and indices[jj][1] < indices[jj+1][1]:
                                    doubled.append(indices[jj+1])
                                    jj += 1

                                if len(doubled) != len(changed):
                                    isdouble = False    #if length of subtrees does not fit they can not be identical
                                else:
                                    #compare fields
                                    k = 0
                                    while k < len(doubled) and k < len(changed):
                                        #fields to compare
                                        changednodecompare = []
                                        doublednodecompare = []
                                        changednodecompare.append(self.treeModel.getNode(changed[k][0]).name())
                                        changednodecompare.append(self.treeModel.getNode(changed[k][0]).typeInfo())
                                        doublednodecompare.append(self.treeModel.getNode(doubled[k][0]).name())
                                        doublednodecompare.append(self.treeModel.getNode(doubled[k][0]).typeInfo())

                                        if changednodecompare != doublednodecompare:
                                            isdouble = False
                                            break
                                        k += 1

                                #if node has no identical subtree
                                if not isdouble:
                                    reply = QMessageBox.question(None, "Uniformity", "You have entered a node name which already exists. Because of the axiom of uniformity nodes with the same name have to have an identical subtree. Shall I add an identical subtree? If you press the No-button please press F2 to rename the node.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                    if reply == QMessageBox.Yes:
                                        if (i == (len(indices)-1)) or (i < (len(indices)-1) and indices[i][1] >= indices[i+1][1]):   #check, that the name changed node not already has a subtree: either the name changed node is at the end of the list or it is not at the end of the list and the depth of the following node is smaller or equals the depth of the name changed node
                                            if j < (len(indices)-1) and indices[j][1] < indices[j+1][1]:     #check if the duplicate has a subtree
                                                dsubtreeo = self.treeModel.getNode(indices[j][0].parent()).childrenlist()
                                                dsubtree = deepcopy(dsubtreeo)
                                                #replace siblings of the duplicate node with the siblings of the changed node
                                                # -> remove all siblings in the duplicate node from dsubtree
                                                dnode = self.treeModel.getNode(indices[j][0])   #dnode is the node which subtree shall be taken
                                                l = 0
                                                rmind = []
                                                while l < len(dsubtree):
                                                    if dsubtree[l].getUid() != dnode.getUid():
                                                        rmind.append(l)
                                                    l += 1
                                                rmind = sorted(rmind, reverse=True)
                                                for rm in rmind:
                                                    del dsubtree[rm]
                                                # -> get the uid of the newly renamed node (the node that shall get the subtree) -> dnode in dsubtree (the first node) shall get its uid
                                                cnode = self.treeModel.getNode(indices[i][0])  # cnode is the node, which is just renamed and shall get the same subtree as dnode
                                                dsubtree[0].setUid(cnode.getUid())
                                                #get new uids for the nodes in dsubtree and keep track of the changes, so that the uids can be updated in aspectrules, specrules etc...
                                                #-> preOrder traversal of the tree without recursion
                                                namenewuid = {} #keep track of the names of the nodes with their new uid
                                                if dsubtree:    #the tree to insert shall not be empty
                                                    el = 0
                                                    # create an empty stack and push the first node to it
                                                    nodeStack = []
                                                    nodeStack.append(dsubtree[0])
                                                    highestUid = self.treeModel._rootNode.findHighestUid()

                                                    #  Pop all items. Then:
                                                    #   a) change uid
                                                    #   b) push the other children
                                                    m = 0   #the first node shall not be updated in the uid, so check if a new uid shall be given (in the loop)
                                                    while (len(nodeStack) > 0):

                                                        # Pop the top item from stack and change the uid
                                                        node = nodeStack.pop()
                                                        if m != 0:  #the uid of the first node shall not be updated
                                                            newuid = highestUid + el
                                                            node.setUid(newuid)
                                                        namenewuid.update({node.name(): node.getUid()})

                                                        el += 1
                                                        m += 1

                                                        # Push children
                                                        for chil in node.childrenlist():
                                                            nodeStack.append(chil)

                                                    #since it is a tree, there is no need to set/update a parentuid

                                                    #now go through the tree again and correct uids in properties-> again preOrder traversal of tree without recursion
                                                    nodeStack = []
                                                    nodeStack.append(dsubtree[0])

                                                    while (len(nodeStack) > 0):

                                                        # Pop the top item from stack and correct uids
                                                        node = nodeStack.pop()
                                                        try:
                                                            #for Aspect and Maspect nodes: aspectrules and couplings
                                                            if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
                                                                #correct aspectrules
                                                                asr = node.aspectrule
                                                                nodename = node.name()
                                                                changeduid = namenewuid.get(nodename)
                                                                for ar in asr:  #there is only one aspectrule per node and the rule is defined for the current node -> so no need to check if the name is right
                                                                    ar[1] = str(changeduid)
                                                                #correct couplings
                                                                cpl = node.coupling
                                                                for cp in cpl:  #couplings are between other nodes
                                                                    #source
                                                                    changeduid = namenewuid.get(cp[0])
                                                                    cp[1] = str(changeduid)
                                                                    #sink
                                                                    changeduid = namenewuid.get(cp[3])
                                                                    cp[4] = str(changeduid)
                                                            if node.typeInfo() == "Spec Node":
                                                                #correct specrules
                                                                spr = node.specrule
                                                                for sp in spr:
                                                                    changeduid = namenewuid.get(sp[0])
                                                                    sp[1] = str(changeduid)
                                                        except:
                                                            pass

                                                        # Push children
                                                        for chil in node.childrenlist():
                                                            nodeStack.append(chil)

                                                    #append the dsubtree now with new uids
                                                    if len(dsubtree) > 0:
                                                        pmindex = indices[i][0].parent()
                                                        self.addSubTreeToNode(dsubtree, pmindex)
                                            else:
                                                self.treeSelectionModel.setCurrentIndex(cindex, QItemSelectionModel.ClearAndSelect)
                                                QMessageBox.information(None, "Inserting subtree", "Inserting subtree not possible. The duplicate node has no subtree.", QtWidgets.QMessageBox.Ok)
                                        else:
                                            self.treeSelectionModel.setCurrentIndex(cindex, QItemSelectionModel.ClearAndSelect)
                                            QMessageBox.information(None, "Inserting subtree", "Inserting subtree not possible. The node which name is just changed already has a subtree. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                                    else:
                                        self.treeSelectionModel.setCurrentIndex(cindex, QItemSelectionModel.ClearAndSelect)

            #when type changed: identical nodes (have the same name) need to be changed in type as well
            elif kind == "tc":
                #nodes which have to be changed -> which shall get the new type
                nameNodes = nameNodeDepthDict.get(nameBeforeTypeChange)
                toChange = []
                if nameNodes:   #if nameNodes is not None
                    for lst in nameNodes:
                        if lst[2] != cindex:    #take indices except for the selected (modified) one
                            toChange.append(lst)
                # change the type of the nodes found
                for tc in toChange:
                    # get the old node (which type has to be changed)
                    oldnode = tc[0]
                    insertAtRow = tc[2].row()
                    parentindex = tc[2].parent()
                    # remove the original node
                    self.treeModel.removeRows(insertAtRow, 1, parentindex)
                    # create new node of other type and place it on the position+1 of the original node
                    self.treeModel.insertRows(insertAtRow, 1, parentindex, oldnode.getUid(), currentNode.typeInfo(), currentNode.name(), oldnode.childrenlist(), oldnode.color())
                    # expand
                    newindex = self.treeModel.index(insertAtRow, 0, parentindex)
                    self.hierarchymodeltreeview.expand(newindex)

            #when property inserted: identical nodes need to get inserted properties as well
            elif kind == "pi":
                #get all nodes with the name of the modified node (the modified node itself as well, since it does not function to exclude it, the model index changes somehow), then go through and apply properties of modified node
                # nodes which shall get the properties of the changed node (a list including the modified node)
                nameNodes = nameNodeDepthDict.get(currentNode.name())
                toChange = []
                if nameNodes:   #if nameNodes is not None
                    for lst in nameNodes:
                        toChange.append(lst)
                # change the properties of the nodes found
                for tc in toChange:
                    # enter the information in the node
                    #get the type of the node etc. (just to be sure)
                    ctype = tc[0].typeInfo()
                    actuid = tc[0].getUid()
                    ind = tc[2]
                    # get the properties of the current (changed) node and set it in the nodes with the same name
                    if currentNode.typeInfo() == ctype == "Entity Node":
                        self.treeModel.insertNodeSpecProp(ind, currentNode.attributes, "attriblist", actuid)
                    elif currentNode.typeInfo() == ctype == "Aspect Node":
                        self.treeModel.insertNodeSpecProp(ind, currentNode.aspectrule, "asprulelist", actuid)
                        self.treeModel.insertNodeSpecProp(ind, currentNode.coupling, "couplinglist", actuid)
                        self.treeModel.insertNodeSpecProp(ind, currentNode.priority, "prio", actuid)
                    elif currentNode.typeInfo() == ctype == "Maspect Node":
                        self.treeModel.insertNodeSpecProp(ind, currentNode.aspectrule, "asprulelist", actuid)
                        self.treeModel.insertNodeSpecProp(ind, currentNode.coupling, "couplinglist", actuid)
                        self.treeModel.insertNodeSpecProp(ind, currentNode.number_replication, "numrep", actuid)
                        self.treeModel.insertNodeSpecProp(ind, currentNode.priority, "prio", actuid)
                    elif currentNode.typeInfo() == ctype == "Spec Node":
                        self.treeModel.insertNodeSpecProp(ind, currentNode.specrule, "specrulelist", actuid)
                    else:  # Descriptive node in general
                        pass

            #when node appended: identical nodes need to have the child appended as well
            elif kind == "an":
                newInsertedChild = self.treeModel.getNode(indexOfNewChild)
                #insert in all parents
                if subSibling == "su":
                    nameNodes = nameNodeDepthDict.get(currentNode.name())
                else:
                    nameNodes = nameNodeDepthDict.get(currentNode.parent().name())
                if nameNodes and len(nameNodes) > 1:
                    for lst in nameNodes:
                        try:
                            self.treeModel.insertRows(positionToInsert, 1, lst[2], newInsertedChild.findHighestUid()+1, newInsertedChild.typeInfo(), newInsertedChild.name())
                        except:
                            pass
                    #delete the inserted child, since it was duplicated above
                    self.deleteNode(False, indexOfNewChild)

            #when node deleted: identical nodes need to have the child deleted as well
            elif kind == "dn":
                #get the deleted node
                nameNodes = nameNodeDepthDict.get(nameDeleted)
                if nameNodes:
                    for lst in nameNodes:   #if there are still nodes with the deleted name -> delete them too
                        try:
                            self.treeModel.removeRows(lst[2].row(), 1, lst[2].parent())
                        except:
                            pass

            self.doOnceChecks = True


    #old functions for axioms checks

    #calling the axioms checking functions
    """
    def checkAxioms(self):
        self.allowedNames()
        vb = self.validBrothers()
        sh = self.strictHierarchy()
        if vb and sh:
            self.uniformity()
    """

    #checking, if the names of the nodes are allowed
    """
    def allowedNames(self):
        if self.doOnceAllowedNames:
            self.doOnceAllowedNames = False
            indices = self.listAllIndices(self.treeSelectionModel.currentIndex())
            names = [self.treeModel.getNode(ind[0]).name() for ind in indices]
            namesok = True
            for na in names:
                if na.find(", ") != -1:
                    namesok = False
            if not namesok:
                self.treeSelectionModel.setCurrentIndex(self.lastSelectedIndex, QItemSelectionModel.ClearAndSelect)
                QMessageBox.information(None, "The name contains illegal letters", "The name contains a comma followed by a whitespace which is illegal. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
            self.doOnceAllowedNames = True
    """

    #checking, if valid brothers are watched
    """
    def validBrothers(self):
        if self.doOnceValidBrothers:
            self.doOnceValidBrothers = False
            #all nodes
            indices = self.listAllIndices(self.lastSelectedIndex)
            #check for duplicates
            nodelist = []
            for inde in indices:
                nodelist.append([self.treeModel.getNode(inde[0]), inde[1]])
            dbl = False
            for nd in nodelist:
                for nl in nodelist:
                    if nl != nd and nl[1] == nd[1] and nl[0].name() == nd[0].name() and nl[0].parent() == nd[0].parent():
                        dbl = True
            returnwert = True
            if dbl:
                self.treeSelectionModel.setCurrentIndex(self.lastSelectedIndex, QItemSelectionModel.ClearAndSelect)
                QMessageBox.information(None, "No valid brothers", "The axiom of valid brothers is violated. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                returnwert = False
            self.doOnceValidBrothers = True
            return returnwert
    """

    #checking if strict hierarchy is watched
    """
    def strictHierarchy(self):
        if self.doOnceStrictHierarchy:
            self.doOnceStrictHierarchy = False
            #get the paths of the tree
            paths = self.findPaths()

            #compare names in every path
            isdouble = False
            for pa in paths:    #pa is one path
                for nm in pa:
                    for na in pa:
                        if na != nm and na[0].name() == nm[0].name():
                            isdouble = True
            #return
            returnwert = True
            if isdouble:
                self.treeSelectionModel.setCurrentIndex(self.lastSelectedIndex, QItemSelectionModel.ClearAndSelect)
                QMessageBox.information(None, "No strict hierarchy", "The axiom of strict hierarchy is violated. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                returnwert = False
            self.doOnceStrictHierarchy = True
            return returnwert
    """

    #uniformity: if a node has the same name as another node -> it shall get the same subtree -> when focus is changed
    """
    def uniformity(self):
        """"""
        # correct children uids -> preOrder traversal of the tree without recursion
        def correctChildrenUids(subtree=None, uid=-1):

            # Base Case
            if subtree is None:
                return

            # create an empty stack and push the first node to it
            nodeStack = []
            nodeStack.append(subtree[0])

            #  Pop all items. Then:
            #   a) change uid
            #   b) push the other children
            while (len(nodeStack) > 0):

                # Pop the top item from stack and change the uid
                node = nodeStack.pop()
                node.setUid(uid)
                uid += 1

                # Push children
                for chil in node.childrenlist():
                    nodeStack.append(chil)
        """"""

        if self.doOnceUniformity:
            self.doOnceUniformity = False
            #all nodes
            indices = self.listAllIndices(self.lastSelectedIndex)

            #find current node -> get the name
            actname = ""
            i = 0
            for ind in indices:
                if ind[0] == self.currentSelectedIndex:
                    actname = self.treeModel.getNode(ind[0]).name()
                    break
                i += 1  #i is the position of the selected node

            #find next duplicate (if there are more duplicates we only need one because the subtrees must be the same)
            isdouble = False
            j = 0
            for ind in indices:
                if ind[0] != self.currentSelectedIndex and self.treeModel.getNode(ind[0]).name() == actname:
                    isdouble = True
                    break
                j += 1  #j is the position of the first node which shall be inserted after position i

            #tree parts
            if isdouble:
                changed = []
                doubled = []
                ii = i
                jj = j

                changed.append(indices[ii])
                while ii < len(indices)-1 and indices[ii][1] < indices[ii+1][1]:
                    changed.append(indices[ii+1])
                    ii += 1

                doubled.append(indices[jj])
                while jj < len(indices)-1 and indices[jj][1] < indices[jj+1][1]:
                    doubled.append(indices[jj+1])
                    jj += 1

                if len(doubled) != len(changed):
                    isdouble = False    #if length of subtrees does not fit they can not be identical
                else:
                    #compare fields
                    k = 0
                    while k < len(doubled) and k < len(changed):
                        #fields to compare
                        changednodecompare = []
                        doublednodecompare = []
                        changednodecompare.append(self.treeModel.getNode(changed[k][0]).name())
                        changednodecompare.append(self.treeModel.getNode(changed[k][0]).typeInfo())
                        doublednodecompare.append(self.treeModel.getNode(doubled[k][0]).name())
                        doublednodecompare.append(self.treeModel.getNode(doubled[k][0]).typeInfo())

                        if changednodecompare != doublednodecompare:
                            isdouble = False
                            break
                        k += 1

                #if node has no identical subtree
                if not isdouble:
                    reply = QMessageBox.question(None, "Uniformity", "You have entered a node name which already exists. Because of the axiom of uniformity nodes with the same name have to have an identical subtree. Should I add an identical subtree? If you press the No-button please press F2 to rename the node.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        if (i == (len(indices)-1)) or (i < (len(indices)-1) and indices[i][1] >= indices[i+1][1]):   #check, that the name changed node not already has a subtree: either the name changed node is at the end of the list or it is not at the end of the list and the depth of the following node is smaller or equals the depth of the name changed node
                            if j < (len(indices)-1) and indices[j][1] < indices[j+1][1]:     #check if the duplicate has a subtree
                                dsubtreeo = self.treeModel.getNode(indices[j][0].parent()).childrenlist()
                                dsubtree = deepcopy(dsubtreeo)
                                csubtreeo = self.treeModel.getNode(indices[i][0].parent()).childrenlist()
                                csubtree = deepcopy(csubtreeo)
                                #replace siblings of the duplicate node with the siblings of the changed node
                                # -> remove all siblings in the duplicate node from dsubtree
                                dnode = self.treeModel.getNode(indices[j][0])
                                l = 0
                                rmind = []
                                while l < len(dsubtree):
                                    if dsubtree[l].getUid() != dnode.getUid():
                                        rmind.append(l)
                                    l += 1
                                rmind = sorted(rmind, reverse=True)
                                for rm in rmind:
                                    del dsubtree[rm]
                                # -> remove the changed node from csubtree
                                cnode = self.treeModel.getNode(indices[i][0])
                                l = 0
                                rmind = []
                                while l < len(csubtree):
                                    if csubtree[l].getUid() == cnode.getUid():
                                        rmind.append(l)
                                    l += 1
                                rmind = sorted(rmind, reverse=True)
                                for rm in rmind:
                                    del csubtree[rm]
                                #now ceate the subtree that shall be appended
                                subtree = csubtree + dsubtree
                                #append the subtree
                                if len(subtree) > 0:
                                    # correct uids in subtree: uid and parent uid -> not necessary, shall not be done -> the same nodes shall have the same uid
                                    #startuid = subtree[0].findHighestUid()
                                    #correctChildrenUids(subtree, startuid)     # -> the same nodes shall have the same uid
                                    pmindex = indices[i][0].parent()
                                    #self.deleteNode(False, indices[i][0])  # -> not needed
                                    self.addSubTreeToNode(subtree, pmindex)
                            else:
                                self.treeSelectionModel.setCurrentIndex(self.lastSelectedIndex, QItemSelectionModel.ClearAndSelect)
                                QMessageBox.information(None, "Inserting subtree", "Inserting subtree not possible. The duplicate node has no subtree.", QtWidgets.QMessageBox.Ok)
                        else:
                            self.treeSelectionModel.setCurrentIndex(self.lastSelectedIndex, QItemSelectionModel.ClearAndSelect)
                            QMessageBox.information(None, "Inserting subtree", "Inserting subtree not possible. The node which name is just changed already has a subtree. Please press F2 to rename the node.", QtWidgets.QMessageBox.Ok)
                    else:
                        self.treeSelectionModel.setCurrentIndex(self.lastSelectedIndex, QItemSelectionModel.ClearAndSelect)
            self.doOnceUniformity = True
    """

    #uniformity: nodes with the same uid shall be always identical -> check it
    """
    def keepUniformityInsNodeProp(self):
        self.keepUniformity("inp")

    def keepUniformity(self, val, pos=-1, row=-1, column=-1, parent=None, deletedUid=-1):
        if self.doOnceKeepUniformity:
            self.doOnceKeepUniformity = False

            # all nodes
            indices = self.listAllIndices(self.currentSelectedIndex)

            #changed node
            try:
                cnode = self.treeModel.getNode(self.currentSelectedIndex)
                if deletedUid == -1:
                    actuid = cnode.getUid()
                else:
                    actuid = deletedUid
                actuid2 = actuid
                ctype = cnode.typeInfo()
                cname = cnode.name()

                if val == "an":
                    actuid2 = actuid
                    actuid = cnode.parent().getUid()

                # get the duplicate nodes (which have the same uid) -> which shall get the properties of the changed node
                for ind in indices:
                    #enter the information in the node
                    if self.treeModel.getNode(ind[0]).getUid() == actuid:
                        if val == "an":# and ind[0] != self.currentSelectedIndex: #a child shall be inserted -> of course not as brother of the node which is just inserted
                            self.treeModel.insertRows(pos, 1, ind[0], actuid2, ctype, cname)
                        elif val == "dn":
                            self.treeModel.removeRows(ind[0].row(), 1, ind[0].parent())
                        elif val == "inp":
                            # get the properties of the current (changed) node and set it in the nodes with the same uid (actuid)
                            if ctype == "Entity Node":
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.attributes, "attriblist", actuid)
                            elif ctype == "Aspect Node":
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.aspectrule, "asprulelist", actuid)
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.coupling, "couplinglist", actuid)
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.priority, "prio", actuid)
                            elif ctype == "Maspect Node":
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.aspectrule, "asprulelist", actuid)
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.coupling, "couplinglist", actuid)
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.number_replication, "numrep", actuid)
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.priority, "prio", actuid)
                            elif ctype == "Spec Node":
                                self.treeModel.insertNodeSpecProp(ind[0], cnode.specrule, "specrulelist", actuid)
                            else:  # Descriptive node in general
                                pass
                if val == "an":
                    # the inserted node got the same node as brother -> remove one of the identical brothers here
                    self.deleteNode(False, self.treeModel.index(row, column, parent))
            except:
                pass

            self.doOnceKeepUniformity = True
    """