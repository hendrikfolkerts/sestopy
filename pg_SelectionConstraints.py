# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *#QItemSelectionModel, Qt

#redefine functions from QStandarditemmodel
class SelectionConstraintsStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent):
        super(SelectionConstraintsStandardItemModel, self).__init__(parent)

    #fifth row only changable (comment)
    def flags(self, index):
        if index.column() == 5:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

class SelectionConstraints(QtCore.QObject):

    selconChangedSignal = pyqtSignal()

    def __init__(self, main, tabnumber):

        # since we inherited from QObject, we have to call the super class init
        super(SelectionConstraints, self).__init__()

        self.main = main
        self.tabnumber = tabnumber
        self.tvselectionconstraintsview = None
        self.bselectionconstraintsstart = None
        self.bselectionconstraintsstop = None
        self.bselectionconstraintsclear = None
        self.lstartnodename = None
        self.lstopnodename = None
        self.bselectionconstraintsinsert = None
        self.bselectionconstraintsdelete = None
        self.bselectionconstraintshelp = None
        self.setUiInit()
        self.helptext = self.main.selconhelp
        self.treeManipulate = None
        #build empty model for data and the selection
        self.selconsmodel = SelectionConstraintsStandardItemModel(self.tvselectionconstraintsview)
        self.selconsmodel.setHorizontalHeaderLabels(["Startnode", "uid", "Stopnode(s)", "uid(s)", "Color", "Comment"])
        self.selconsselectionmodel = QItemSelectionModel(self.selconsmodel)
        #set model to tableview
        self.tvselectionconstraintsview.setModel(self.selconsmodel)
        self.tvselectionconstraintsview.setSelectionModel(self.selconsselectionmodel)
        #signals
        self.bselectionconstraintsstart.clicked.connect(self.chooseStartNode)
        self.bselectionconstraintsstop.clicked.connect(self.chooseStopNode)
        self.bselectionconstraintsclear.clicked.connect(self.clearStartStopNode)
        self.bselectionconstraintsinsert.clicked.connect(self.addSelCon)
        self.bselectionconstraintsdelete.clicked.connect(self.deleteSelCon)
        self.bselectionconstraintshelp.clicked.connect(self.help)
        #resize
        self.resz()
        #startstopnode
        self.startnodeuid = -1
        self.stopnodeuids = []

        # hide the uid column
        #self.tvselectionconstraintsview.setColumnHidden(1, True)
        #self.tvselectionconstraintsview.setColumnHidden(3, True)

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt1
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt1
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt1
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart1
            self.lstartnodename = self.main.lstartnodenamet1
            self.lstopnodename = self.main.lstopnodenamet1
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt1
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet1
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt1
        if self.tabnumber == 1:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt2
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt2
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt2
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart2
            self.lstartnodename = self.main.lstartnodenamet2
            self.lstopnodename = self.main.lstopnodenamet2
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt2
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet2
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt2
        if self.tabnumber == 2:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt3
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt3
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt3
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart3
            self.lstartnodename = self.main.lstartnodenamet3
            self.lstopnodename = self.main.lstopnodenamet3
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt3
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet3
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt3
        if self.tabnumber == 3:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt4
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt4
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt4
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart4
            self.lstartnodename = self.main.lstartnodenamet4
            self.lstopnodename = self.main.lstopnodenamet4
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt4
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet4
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt4
        if self.tabnumber == 4:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt5
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt5
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt5
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart5
            self.lstartnodename = self.main.lstartnodenamet5
            self.lstopnodename = self.main.lstopnodenamet5
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt5
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet5
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt5
        if self.tabnumber == 5:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt6
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt6
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt6
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart6
            self.lstartnodename = self.main.lstartnodenamet6
            self.lstopnodename = self.main.lstopnodenamet6
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt6
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet6
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt6
        if self.tabnumber == 6:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt7
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt7
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt7
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart7
            self.lstartnodename = self.main.lstartnodenamet7
            self.lstopnodename = self.main.lstopnodenamet7
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt7
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet7
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt7
        if self.tabnumber == 7:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt8
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt8
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt8
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart8
            self.lstartnodename = self.main.lstartnodenamet8
            self.lstopnodename = self.main.lstopnodenamet8
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt8
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet8
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt8
        if self.tabnumber == 8:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt9
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt9
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt9
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart9
            self.lstartnodename = self.main.lstartnodenamet9
            self.lstopnodename = self.main.lstopnodenamet9
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt9
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet9
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt9
        if self.tabnumber == 9:
            self.tvselectionconstraintsview = self.main.tvselectionconstraintsviewt10
            self.bselectionconstraintsstart = self.main.bselectionconstraintsstartt10
            self.bselectionconstraintsstop = self.main.bselectionconstraintsstopt10
            self.bselectionconstraintsclear = self.main.bselectionconstraintscleart10
            self.lstartnodename = self.main.lstartnodenamet10
            self.lstopnodename = self.main.lstopnodenamet10
            self.bselectionconstraintsinsert = self.main.bselectionconstraintsinsertt10
            self.bselectionconstraintsdelete = self.main.bselectionconstraintsdeletet10
            self.bselectionconstraintshelp = self.main.bselectionconstraintshelpt10

    def setTreeManipulateInSelCon(self):
        if self.tabnumber == 0:
            self.treeManipulate = self.main.modellist[0][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 1:
            self.treeManipulate = self.main.modellist[1][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 2:
            self.treeManipulate = self.main.modellist[2][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 3:
            self.treeManipulate = self.main.modellist[3][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 4:
            self.treeManipulate = self.main.modellist[4][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 5:
            self.treeManipulate = self.main.modellist[5][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 6:
            self.treeManipulate = self.main.modellist[6][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 7:
            self.treeManipulate = self.main.modellist[7][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 8:
            self.treeManipulate = self.main.modellist[8][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)
        if self.tabnumber == 9:
            self.treeManipulate = self.main.modellist[9][3]
            self.treeManipulate.bdeletenode.clicked.connect(self.updateSelConDelete)
            self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateSelConNameChanged)

    """restore from save"""
    def fromSave(self, sc, subSES=False):
        if not subSES:
            for row in range(len(sc)):
                itema = QStandardItem(sc[row][0])
                itemau = QStandardItem(sc[row][1])
                itemo = QStandardItem(sc[row][2])
                itemou = QStandardItem(sc[row][3])
                itemcol = QStandardItem(sc[row][4])
                itemcom = QStandardItem(sc[row][5])
                self.selconsmodel.appendRow([itema, itemau, itemo, itemou, itemcol, itemcom])
                modin = self.selconsmodel.index(self.selconsmodel.rowCount()-1, 4)
                color = QtGui.QColor()
                color.setNamedColor(sc[row][4])
                self.selconsmodel.setData(modin, color, QtCore.Qt.TextColorRole)
        else:
            selcoli = self.outputSelConsList()
            for row in range(len(sc)):
                if [sc[row][0], sc[row][1], sc[row][2], sc[row][3], sc[row][4]] in selcoli:  # the same exists
                    pass
                else:
                    itema = QStandardItem(sc[row][0])
                    itemau = QStandardItem(sc[row][1])
                    itemo = QStandardItem(sc[row][2])
                    itemou = QStandardItem(sc[row][3])
                    itemcol = QStandardItem(sc[row][4])
                    itemcom = QStandardItem(sc[row][5])
                    self.selconsmodel.appendRow([itema, itemau, itemo, itemou, itemcol, itemcom])
                    modin = self.selconsmodel.index(self.selconsmodel.rowCount()-1, 4)
                    color = QtGui.QColor()
                    color.setNamedColor(sc[row][4])
                    self.selconsmodel.setData(modin, color, QtCore.Qt.TextColorRole)
        self.resz()

        # hide the uid column
        #self.tvselectionconstraintsview.setColumnHidden(1, True)
        #self.tvselectionconstraintsview.setColumnHidden(3, True)

    """output"""
    def outputSelConsList(self, subSES=False, nodelistSubSES=""):
        selConsList = []
        ok = []
        if not subSES:
            for row in range(self.selconsmodel.rowCount()):
                inda = self.selconsmodel.item(row, 0)
                indau = self.selconsmodel.item(row, 1)
                indo = self.selconsmodel.item(row, 2)
                indou = self.selconsmodel.item(row, 3)
                indc = self.selconsmodel.item(row, 4)
                indcom = self.selconsmodel.item(row, 5)
                var = [inda.data(QtCore.Qt.DisplayRole), indau.data(QtCore.Qt.DisplayRole), indo.data(QtCore.Qt.DisplayRole), indou.data(QtCore.Qt.DisplayRole), indc.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                selConsList.append(var)
        else:
            for row in range(self.selconsmodel.rowCount()):
                inda = self.selconsmodel.item(row, 0)
                indo = self.selconsmodel.item(row, 2)
                indc = self.selconsmodel.item(row, 4)
                indcom = self.selconsmodel.item(row, 5)
                indau = self.selconsmodel.item(row, 1).data(QtCore.Qt.DisplayRole)
                indou = self.selconsmodel.item(row, 3).data(QtCore.Qt.DisplayRole)
                indouu = indou.split(", ")
                uidsSubSES = []
                for n in nodelistSubSES:
                    uidsSubSES.append(n[0])
                toCheck = False
                if indau in uidsSubSES:
                    toCheck = True
                for el in indouu:
                    if el in uidsSubSES:
                        toCheck = True
                if toCheck:
                    for n in nodelistSubSES:
                        if n[0] == indau:
                            ok.append(True)
                    for n in nodelistSubSES:
                        for u in indouu:
                            if n[0] == u:
                                ok.append(True)
                    if len(ok) == (len(indouu) + 1):
                        var = [inda.data(QtCore.Qt.DisplayRole), indau, indo.data(QtCore.Qt.DisplayRole), indou, indc.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                        selConsList.append(var)
                    else:
                        var = ["", "", "", "", "", ""]
                        QMessageBox.information(None, "Saving not possible", "Only some nodes of a selection constraint would be saved.", QtWidgets.QMessageBox.Ok)
                        selConsList.append(var)
                else:
                    var = [inda.data(QtCore.Qt.DisplayRole), indau, indo.data(QtCore.Qt.DisplayRole), indou, indc.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                    selConsList.append(var)
        return selConsList

    """resize"""
    """
    def resz(self):
        self.tvselectionconstraintsview.setColumnWidth(0, self.tvselectionconstraintsview.width() * 0.3)
        self.tvselectionconstraintsview.setColumnWidth(1, self.tvselectionconstraintsview.width() * 0.1)
        self.tvselectionconstraintsview.setColumnWidth(2, self.tvselectionconstraintsview.width() * 0.3)
        self.tvselectionconstraintsview.setColumnWidth(3, self.tvselectionconstraintsview.width() * 0.1)
        header = self.tvselectionconstraintsview.horizontalHeader()
        header.setStretchLastSection(True)
    """
    def resz(self):
        i = 0
        while i < 5:
            self.tvselectionconstraintsview.resizeColumnToContents(i)
            i += 1
        header = self.tvselectionconstraintsview.horizontalHeader()
        header.setStretchLastSection(True)

    """choose startnode"""
    def chooseStartNode(self):
        index = self.treeManipulate.currentSelectedIndex
        startnode = self.treeManipulate.treeModel.getNode(index)
        if self.startnodeuid == -1:
            if not startnode.getUid() in self.stopnodeuids:
                if startnode.typeInfo() == "Entity Node" or startnode.typeInfo() == "Aspect Node":
                    self.startnodeuid = startnode.getUid()
                    self.lstartnodename.setText(startnode.name())
                else:
                    QMessageBox.information(None, "Selecting not possible", "The startnode must be an entity node or an aspect node.", QtWidgets.QMessageBox.Ok)
            else:
                QMessageBox.information(None, "Selecting not possible", "Please select a node which does not equal one of the stopnodes.", QtWidgets.QMessageBox.Ok)
        else:
            QMessageBox.information(None, "Selecting not possible", "You can not select another startnode. Please clear the selection first.", QtWidgets.QMessageBox.Ok)

    """choose stopnode"""
    def chooseStopNode(self):
        #start selection
        if self.startnodeuid != -1:     #a startnode must be selected
            index = self.treeManipulate.currentSelectedIndex
            stopnode = self.treeManipulate.treeModel.getNode(index)

            otherBranch = self.isOtherBranch(self.treeManipulate.findNodeFromUid(self.startnodeuid), stopnode)
            areBrothersStartStop = self.treeManipulate.areBrothers(self.startnodeuid, stopnode.getUid())
            areBrothersStopStop = False
            for sn in self.stopnodeuids:
                if self.treeManipulate.areBrothers(sn, stopnode.getUid()):
                    areBrothersStopStop = True
            #isBetweenDecisionNode = self.isBetweenDecisionNode(self.treeManipulate.findNodeFromUid(self.startnodeuid), stopnode)   #for explanation see the commented out function
            if (not stopnode.getUid() in self.stopnodeuids) and (self.startnodeuid != stopnode.getUid()):
                if otherBranch and not areBrothersStartStop and not areBrothersStopStop:
                    if True:#isBetweenDecisionNode: #for explanation see the commented out function
                        startnodetype = self.treeManipulate.findNodeFromUid(self.startnodeuid).typeInfo()
                        stopnodetype = stopnode.typeInfo()
                        startnodeisentity = {"Entity Node", "Aspect Node", "Maspect Node"}
                        startnodeisaspect = {"Entity Node", "Maspect Node"}
                        if (startnodetype == "Entity Node" and stopnodetype in startnodeisentity) or (startnodetype == "Aspect Node" and stopnodetype in startnodeisaspect):
                            self.stopnodeuids.append(stopnode.getUid())
                            self.lstopnodename.setText(self.createStopnodeString())
                        else:
                            QMessageBox.information(None, "Selecting not possible", "If the startnode is an entity node, the stopnode must be an entity node, an aspect node or a maspect node. If the startnode is an aspect node, the stopnode must be an entity node or a maspect node.", QtWidgets.QMessageBox.Ok)
                    else:
                        #QMessageBox.information(None, "Selecting not possible", "You selected a startnode and a stopnode without an aspect node as a father between them.", QtWidgets.QMessageBox.Ok)
                        pass    #for explanation see the commented out function
                else:
                    QMessageBox.information(None, "Selecting not possible", "Please select a node which does not lie in the same branch as the startnode and is no brother of the startnode or one of the stopnodes.", QtWidgets.QMessageBox.Ok)
            else:
                QMessageBox.information(None, "Selecting not possible", "Please select a node which does not equal the startnode and is not already selected as stopnode.", QtWidgets.QMessageBox.Ok)
        else:
            QMessageBox.information(None, "Selecting not possible", "Please select a startnode first.", QtWidgets.QMessageBox.Ok)

    """check if the startnode and the stopnodes are in different branches of the tree"""
    def isOtherBranch(self, sa, so):
        # get the paths of the tree
        paths = self.treeManipulate.findPaths()

        # compare
        isOtherBranch = False

        # find start node
        safound = []
        sofoundsamepath = False
        pa = 0
        while pa < len(paths):
            nda = 0
            while nda < len(paths[pa]):
                if paths[pa][nda][0] == sa:
                    safound.append(pa)
                    break
                nda += 1
            pa += 1

        # we found the path of the startnode, now look if the stopnode can be found in the same path as the startnode
        for pa in safound:
            ndo = 0
            while ndo < len(paths[pa]):
                if paths[pa][ndo][0] == so:
                    sofoundsamepath = True
                    break
                ndo += 1

        # compare
        if safound and not sofoundsamepath:
            isOtherBranch = True
        return isOtherBranch

    """
    Thought so, but found other examples -> disable
        look if the startnode and the stopnode are between decision knots
        the startnode and the stopnode have to be in different paths which are below an
         aspect decision node
        in both paths to the root must be at least one common aspect node (the entity nodes below this node are brothers)
    """
    """
    def isBetweenDecisionNode(self, sa, so):
        isBetweenDecisionNode = False
        #get the paths of the tree
        paths = self.treeManipulate.findPaths()

        #seek for brothers
        #find start node
        safound = []
        pa = 0
        while pa < len(paths):
            nda = 0
            while nda < len(paths[pa]):
                if paths[pa][nda][0] == sa:
                    safound.append(pa)
                    break
                nda += 1
            pa += 1
        #find stop node
        sofound = []
        po = 0
        while po < len(paths):
            ndo = 0
            while ndo < len(paths[po]):
                if paths[po][ndo][0] == so:
                    sofound.append(po)
                    break
                ndo += 1
            po += 1

        #startnode: go from behind until the father is an aspect node
        #take first path from safound (it can be taken any path since we are looking for the parents)
        safound = safound[0]
        #take first path from sofound (it can be taken any path since we are looking for the parents)
        sofound = sofound[0]
        #look for brother nodes in the path with the startnode and the path for the stopnodes
        brothersnotfound = True
        sfa = len(paths[safound]) - 1   #get the length of the path
        while sfa >= 0 and brothersnotfound:
            sfo = len(paths[sofound]) - 1   #get the length of the paths
            while sfo >= 0 and brothersnotfound:
                if self.treeManipulate.areBrothers(paths[safound][sfa][0].getUid(), paths[sofound][sfo][0].getUid()):
                    brothersnotfound = False
                sfo -= 1
            sfa -= 1
        #check type of father (either startnode or stopnode needed since they are brothers and have the same father)
        if paths[safound][sfa][0].typeInfo() == "Aspect Node":
            isBetweenDecisionNode = True

        return isBetweenDecisionNode
    """

    """clear selection"""
    def clearStartStopNode(self):
        self.startnodeuid = -1
        self.stopnodeuids = []
        self.lstartnodename.setText("start")
        self.lstopnodename.setText("target(s)")

    """insert the selection constraints"""
    def addSelCon(self):
        #check if selected nodes still exist
        startnodeexists = False
        stopnodesexist = True
        if self.treeManipulate.findNodeFromUid(self.startnodeuid) is not None:
            startnodeexists = True
        for snuid in self.stopnodeuids:
            if self.treeManipulate.findNodeFromUid(snuid) is None:
                stopnodesexist = False
                break

        self.stopnodeuids.sort()    #sort to be able to check if the same condition is already inserted
        if self.startnodeuid == -1 or len(self.stopnodeuids) == 0:
            QMessageBox.information(None, "Inserting not possible", "Please insert a hierarchical model first and select a startnode and a targetnode.", QtWidgets.QMessageBox.Ok)
        elif not startnodeexists or not stopnodesexist:
            QMessageBox.information(None, "Inserting not possible", "After selection you deleted at least one of the nodes you want to insert. ", QtWidgets.QMessageBox.Ok)
        else:
            if len(self.selconsmodel.findItems(str(self.startnodeuid), QtCore.Qt.MatchExactly, 1)) == 0 and len(self.selconsmodel.findItems(self.createStopnodeUidString(), QtCore.Qt.MatchExactly, 3)) == 0:    #check for duplicates of variable name
                colorDialog = QColorDialog
                #color = QtGui.QColor()  #constructs invalid color
                color = colorDialog.getColor(QtCore.Qt.white)
                if color.isValid():
                    itemsecosta = QStandardItem(self.treeManipulate.findNodeFromUid(self.startnodeuid).name())
                    itemsecostau = QStandardItem(str(self.startnodeuid))
                    itemsecosto = QStandardItem(self.createStopnodeString())
                    itemsecostou = QStandardItem(self.createStopnodeUidString())
                    itemcolor = QStandardItem(color.name())
                    itemcomment = QStandardItem("")     #empty comment
                    self.selconsmodel.appendRow([itemsecosta, itemsecostau, itemsecosto, itemsecostou, itemcolor, itemcomment])
                    modin = self.selconsmodel.index(self.selconsmodel.rowCount()-1, 4)
                    #self.selconsmodel.setData(modin, color, QtCore.Qt.BackgroundColorRole) #for background
                    self.selconsmodel.setData(modin, color, QtCore.Qt.ForegroundRole)        #for text
                    #self.lstartnodename.setText("start")
                    #self.lstopnodename.setText("target(s)")
                    #self.startnode = ""
                    #del self.stopnodeuids[:]    #empty list
                    #setting the color of the nodes
                    self.colorNodesInTreeModel()
                    self.clearStartStopNode()
            else:
                QMessageBox.information(None, "Inserting not possible", "The selection constraint exists already.", QtWidgets.QMessageBox.Ok)
                self.clearStartStopNode()
        self.resz()
        self.selconChangedSignal.emit()

    """create a string with the uids of the stopnode from the uidlist"""
    def createStopnodeUidString(self):
        uidstr = ""
        for uid in self.stopnodeuids:
            if uidstr == "":
                uidstr = str(uid)
            else:
                uidstr = uidstr + ", " + str(uid)
        return uidstr

    """create a string with the names of the stopnode from the uidlist"""
    def createStopnodeString(self):
        stopnodetext = ""
        for uid in self.stopnodeuids:
            if stopnodetext == "":
                stopnodetext = self.treeManipulate.findNodeFromUid(uid).name()
            else:
                stopnodetext = stopnodetext + ", " + self.treeManipulate.findNodeFromUid(uid).name()
        return stopnodetext

    """update selection constraints when nodes are deleted in tree"""
    def updateSelConDelete(self):
        #getting the indices of the existing nodes
        indices = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())
        #getting the nodes of the tree
        nodes = []
        for ind in indices:
            nodes.append(self.treeManipulate.treeModel.getNode(ind[0]))
        #getting the selection constraints
        selConsList = self.outputSelConsList()
        #getting the uids of the existing nodes
        uids = []
        for node in nodes:
            uids.append(str(node.getUid()))
        #check if uids from sel cons are in uidlist of the tree
        notInList = []
        i = 0
        while i < len(selConsList):
            if selConsList[i][1] not in uids:
                notInList.append(i)
            i += 1
        j = 0
        while j < len(selConsList):
            stopuidsplit = selConsList[j][3].split(", ")
            for id in stopuidsplit:
                if id not in uids:
                    notInList.append(j)
            j += 1
        #build the union of i and j -> now it is solved different (see below)
        #union = set(i) | set(j)
        #build set to remove duplicates
        notInListSet = set(notInList)
        #build list again (without duplicates)
        notInList = list(notInListSet)
        #remove selection constraints containing removed nodes
        if notInList:
            notInList.sort(reverse=True)
            for rw in notInList:
                self.deleteSelCon(rw)
            QMessageBox.information(None, "Updated selection constraints", "The selection constraint list was updated. You deleted a node for which a selection constraint was defined.", QtWidgets.QMessageBox.Ok)

    """update selection constraints when the name of nodes is changed in the tree"""
    def updateSelConNameChanged(self):
        #getting the selection constraints
        selConsList = self.outputSelConsList()
        j = 0
        while j < len(selConsList):
            san = int(selConsList[j][1])
            sann = selConsList[j][0]
            nodefound = self.treeManipulate.findNodeFromUid(san)
            if sann != nodefound.name():
                index = self.selconsmodel.index(j, 0)
                self.changeNodenameSelCon(index, san, nodefound.name(), False)
            son = selConsList[j][3].split(", ")
            son  = [int(i) for i in son]
            sonn = selConsList[j][2].split(", ")
            i = 0
            while i < len(son) and i < len(sonn):
                nodefound = self.treeManipulate.findNodeFromUid(son[i])
                if sonn[i] != nodefound.name():
                    index = self.selconsmodel.index(j, 2)
                    self.changeNodenameSelCon(index, son[i], nodefound.name(), True)
                i += 1
            j += 1

    """change the nodename in a selection constraint with a given uid"""
    def changeNodenameSelCon(self, index, uid, newname, isSon):
        if not isSon:
            self.selconsmodel.setData(index, newname)
        else:
            indou = self.selconsmodel.item(index.row(), 3).data(QtCore.Qt.DisplayRole)
            indo = self.selconsmodel.item(index.row(), 2).data(QtCore.Qt.DisplayRole)
            indou = indou.split(", ")
            indo = indo.split(", ")
            indou = [int(i) for i in indou]
            uidpos = indou.index(uid)
            indo[uidpos] = newname
            stopnodetext = ""
            for ind in indo:
                if stopnodetext == "":
                    stopnodetext = ind
                else:
                    stopnodetext = stopnodetext + ", " + ind
            self.selconsmodel.setData(index, stopnodetext)

    """delete"""
    def deleteSelCon(self, rw=-1, selectall=False):
        if not selectall:
            selectedrows = self.selconsselectionmodel.selectedRows()
        else:
            selectedrows = []
            for row in range(self.selconsmodel.rowCount()):
                selectedrows.append(self.selconsmodel.index(row, 0))
            self.clearStartStopNode()

        if len(selectedrows) == 0 and rw == -1 and not selectall:
            QMessageBox.information(None, "Deleting not possible", "Please select at least one selection constraint to delete.", QtWidgets.QMessageBox.Ok)
        elif len(selectedrows) > 0:
            deleteListRows = []
            for rowind in selectedrows:
                deleteListRows.append(rowind.row())
            deleteListRows.sort(reverse=True)
            for row in deleteListRows:
                self.selconsmodel.removeRow(row, QtCore.QModelIndex())
        elif rw != -1:
            self.selconsmodel.removeRow(rw, QtCore.QModelIndex())
        self.resz()
        #setting the color of the nodes
        self.colorNodesInTreeModel()
        self.selconChangedSignal.emit()

    """setting the defined colors in the tree model"""
    def colorNodesInTreeModel(self):
        allInd = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())
        for ind in allInd:
            #set color black at first
            self.treeManipulate.treeModel.setData(ind[0], "#000000", QtCore.Qt.TextColorRole)
            #reset bold font at first
            self.treeManipulate.treeModel.setData(ind[0], False, QtCore.Qt.FontRole)
        for row in range(self.selconsmodel.rowCount()):
            #uids used -> but all nodes with the same name should be colored (not with the same uid, because nodes with the same name have different uids)
            """
            inda = self.selconsmodel.item(row, 1).data(QtCore.Qt.DisplayRole)
            indo = self.selconsmodel.item(row, 3).data(QtCore.Qt.DisplayRole)
            indc = self.selconsmodel.item(row, 4).data(QtCore.Qt.DisplayRole)
            inda = int(inda)
            indo = indo.split(",")
            indo = list(map(int, indo))
            for ind in allInd:
                nd = self.treeManipulate.treeModel.getNode(ind[0]).getUid()
                if nd == inda:
                    self.treeManipulate.treeModel.setData(ind[0], True, QtCore.Qt.FontRole)
                if nd == inda or nd in indo:
                    self.treeManipulate.treeModel.setData(ind[0], indc, QtCore.Qt.TextColorRole)
            """
            #instead names are used
            inda = self.selconsmodel.item(row, 0).data(QtCore.Qt.DisplayRole)
            indo = self.selconsmodel.item(row, 2).data(QtCore.Qt.DisplayRole)
            indc = self.selconsmodel.item(row, 4).data(QtCore.Qt.DisplayRole)
            indo = indo.split(", ")
            indo = [indoo.strip() for indoo in indo]
            for ind in allInd:
                nd = self.treeManipulate.treeModel.getNode(ind[0]).name()
                if nd == inda:
                    self.treeManipulate.treeModel.setData(ind[0], True, QtCore.Qt.FontRole)
                if nd == inda or nd in indo:
                    self.treeManipulate.treeModel.setData(ind[0], indc, QtCore.Qt.TextColorRole)

    """help"""
    def help(self):
        msgBox = QMessageBox(self.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("selection constraints: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()