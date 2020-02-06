# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

import sys
import types
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QItemSelectionModel, Qt

import ast
import re
import keyword

#redefine functions from QStandarditemmodel
class AspRuleStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent, aspectrule):
        super(AspRuleStandardItemModel, self).__init__(parent)
        self.aspectrule = aspectrule

    #third column is only changable if in the first column the currently selected node is shown
    def flags(self, index):
        #get the uid in the selected line (aspectrule)
        it = self.item(index.row(), 1)
        uidasprule = int(it.data(QtCore.Qt.DisplayRole))
        #get the uid of the selected node in the tree model
        uidtm = self.aspectrule.treeManipulate.treeModel.getNode(self.aspectrule.treeManipulate.currentSelectedIndex).getUid()
        #number of entrys (-> number of aspectnodes in this layer)
        rc = self.rowCount()

        #only set the edit flags if the selected node in the tree equals the node for which the aspectrule exists and only allow to change the condition column
        #and there is more than 1 entry (node)
        if uidasprule == uidtm and (index.column() == 2 or index.column() == 4) and rc > 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        elif uidasprule == uidtm and rc == 1:
            return QtCore.Qt.NoItemFlags
        elif uidasprule == uidtm:
            return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsSelectable
        if uidasprule != uidtm:
            return QtCore.Qt.NoItemFlags

class Aspectrule:
    def __init__(self, treeManipulate, tabnumber):
        self.treeManipulate = treeManipulate
        self.tabnumber = tabnumber
        self.tvaspectruleview = None
        self.baspectrulehelp = None
        self.setUiInit()
        self.helptext = self.treeManipulate.main.asprulehelp
        #build empty model for data and the selection
        self.asprulemodel = AspRuleStandardItemModel(self.tvaspectruleview, self)
        self.asprulemodel.setHorizontalHeaderLabels(["Node", "uid", "Condition", "result", "comment"])
        self.aspruleselectionmodel = QItemSelectionModel(self.asprulemodel)
        #set model to tableview
        self.tvaspectruleview.setModel(self.asprulemodel)
        self.tvaspectruleview.setSelectionModel(self.aspruleselectionmodel)
        #signals
        self.baspectrulehelp.clicked.connect(self.help)
        self.asprulemodel.itemChanged.connect(self.changeAspRule)
        self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateAspRuleNameChanged)
        self.treeManipulate.nodeDeletedSignal.connect(self.nodeDeletedCheckDeleteAspRule)
        #resize
        self.resz()
        #variables
        self.changeOnce = True
        self.validateOnce = True

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst1[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst1[3]
        if self.tabnumber == 1:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst2[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst2[3]
        if self.tabnumber == 2:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst3[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst3[3]
        if self.tabnumber == 3:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst4[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst4[3]
        if self.tabnumber == 4:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst5[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst5[3]
        if self.tabnumber == 5:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst6[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst6[3]
        if self.tabnumber == 6:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst7[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst7[3]
        if self.tabnumber == 7:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst8[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst8[3]
        if self.tabnumber == 8:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst9[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst9[3]
        if self.tabnumber == 9:
            self.tvaspectruleview = self.treeManipulate.main.aspectrulefieldst10[0]
            self.baspectrulehelp = self.treeManipulate.main.aspectrulefieldst10[3]

    def setSesVarsFunsInAspectrules(self):
        if self.tabnumber == 0:
            self.sesVariablest1 = self.treeManipulate.main.modellist[0][1]
            self.sesFunctionst1 = self.treeManipulate.main.modellist[0][2]
            self.sesVariablest1.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst1.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 1:
            self.sesVariablest2 = self.treeManipulate.main.modellist[1][1]
            self.sesFunctionst2 = self.treeManipulate.main.modellist[1][2]
            self.sesVariablest2.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst2.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 2:
            self.sesVariablest3 = self.treeManipulate.main.modellist[2][1]
            self.sesFunctionst3 = self.treeManipulate.main.modellist[2][2]
            self.sesVariablest3.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst3.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 3:
            self.sesVariablest4 = self.treeManipulate.main.modellist[3][1]
            self.sesFunctionst4 = self.treeManipulate.main.modellist[3][2]
            self.sesVariablest4.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst4.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 4:
            self.sesVariablest5 = self.treeManipulate.main.modellist[4][1]
            self.sesFunctionst5 = self.treeManipulate.main.modellist[4][2]
            self.sesVariablest5.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst5.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 5:
            self.sesVariablest6 = self.treeManipulate.main.modellist[5][1]
            self.sesFunctionst6 = self.treeManipulate.main.modellist[5][2]
            self.sesVariablest6.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst6.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 6:
            self.sesVariablest7 = self.treeManipulate.main.modellist[6][1]
            self.sesFunctionst7 = self.treeManipulate.main.modellist[6][2]
            self.sesVariablest7.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst7.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 7:
            self.sesVariablest8 = self.treeManipulate.main.modellist[7][1]
            self.sesFunctionst8 = self.treeManipulate.main.modellist[7][2]
            self.sesVariablest8.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst8.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 8:
            self.sesVariablest9 = self.treeManipulate.main.modellist[8][1]
            self.sesFunctionst9 = self.treeManipulate.main.modellist[8][2]
            self.sesVariablest9.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst9.sesfunChangedSignal.connect(self.validateSESvarfunChanged)
        if self.tabnumber == 9:
            self.sesVariablest10 = self.treeManipulate.main.modellist[9][1]
            self.sesFunctionst10 = self.treeManipulate.main.modellist[9][2]
            self.sesVariablest10.sesvarChangedSignal.connect(self.validateSESvarfunChanged)
            self.sesFunctionst10.sesfunChangedSignal.connect(self.validateSESvarfunChanged)

    """read"""
    def readAspRuleList(self, lst):
        #get current node
        currentnode = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
        itemnme = QStandardItem(currentnode.name())
        itemuid = QStandardItem(str(currentnode.getUid()))
        itemcon = QStandardItem("")
        itemres = QStandardItem("")
        itemcom = QStandardItem("")
        if len(lst) == 0:
            self.asprulemodel.appendRow([itemnme, itemuid, itemcon, itemres, itemcom])
        else:
            itemcon = QStandardItem(lst[0][2])
            itemres = QStandardItem(lst[0][3])
            itemcom = QStandardItem(lst[0][4])
            self.asprulemodel.appendRow([itemnme, itemuid, itemcon, itemres, itemcom])

        #seek aspectrules from brothers of the same nodetype and add them
        #getting the indices of the existing nodes
        indices = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())
        #getting the nodes of the tree
        nodes = []
        for ind in indices:
            nodes.append(self.treeManipulate.treeModel.getNode(ind[0]))
        #find uid of current node
        currentnodeuid = currentnode.getUid()
        #get the brothers of the same nodetype
        brothernodes = []
        for node in nodes:
            if node.getUid() != currentnodeuid and self.treeManipulate.areBrothers(node.getUid(), currentnodeuid) and (node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node"):
                brothernodes.append(node)
        #add the aspectrules of the brothers of the same nodetype
        for bro in brothernodes:
            if len(bro.aspectrule) > 0: #the node already has a aspectrule defined
                itemnme = QStandardItem(bro.aspectrule[0][0])
                itemuid = QStandardItem(bro.aspectrule[0][1])
                itemcon = QStandardItem(bro.aspectrule[0][2])
                itemres = QStandardItem(bro.aspectrule[0][3])
                itemcom = QStandardItem(bro.aspectrule[0][4])
            else:   #we have to define an aspectrule
                itemnme = QStandardItem(bro.name())
                itemuid = QStandardItem(str(bro.getUid()))
                itemcon = QStandardItem("")
                itemres = QStandardItem("")
                itemcom = QStandardItem("")
            self.asprulemodel.appendRow([itemnme, itemuid, itemcon, itemres, itemcom])

        #resize and validate
        self.resz()
        if (self.validateOnce):
            self.validateOnce = False
            self.validate()
            self.validateOnce = True

        #trigger a click on the couplings-toolbox-page
        if self.treeManipulate.main.activeTab == 0:
            self.treeManipulate.main.tbpropertiest1.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 1:
            self.treeManipulate.main.tbpropertiest2.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 2:
            self.treeManipulate.main.tbpropertiest3.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 3:
            self.treeManipulate.main.tbpropertiest4.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 4:
            self.treeManipulate.main.tbpropertiest5.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 5:
            self.treeManipulate.main.tbpropertiest6.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 6:
            self.treeManipulate.main.tbpropertiest7.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 7:
            self.treeManipulate.main.tbpropertiest8.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 8:
            self.treeManipulate.main.tbpropertiest9.setCurrentIndex(4)
        elif self.treeManipulate.main.activeTab == 9:
            self.treeManipulate.main.tbpropertiest10.setCurrentIndex(4)

        #hide the uid column
        #self.tvaspectruleview.setColumnHidden(1, True)

    """write -> the entries of the list in the changed node or only output the list of the node"""
    def writeAspRuleList(self, index=None, isCurrentChanged=False, res=""):
        if not self.treeManipulate.isRestoringTree:  # only, if it is not called due to a selection change during reading the tree from save
            aspRuleListForWrite = []
            aspRuleListAll = []
            #shall the list for a special index be written or should the content of the model for the current node be given back
            if index == None:
                #the asprulelist in the current model is returned
                for row in range(self.asprulemodel.rowCount()):
                    indnme = self.asprulemodel.item(row, 0)
                    induid = self.asprulemodel.item(row, 1)
                    indcon = self.asprulemodel.item(row, 2)
                    indres = self.asprulemodel.item(row, 3)
                    indcom = self.asprulemodel.item(row, 4)
                    var = [indnme.data(QtCore.Qt.DisplayRole), induid.data(QtCore.Qt.DisplayRole), indcon.data(QtCore.Qt.DisplayRole), indres.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                    #all aspectrules in the model
                    aspRuleListAll.append(var)
                return aspRuleListAll
            else:
                #the aspectrule for index shall be written
                node = self.treeManipulate.treeModel.getNode(index)
                nodeuid = node.getUid()
                #if the node that is changed is the current node, take the information from the current asprulemodel and write it in the node
                if isCurrentChanged:
                    for row in range(self.asprulemodel.rowCount()):
                        #only if the aspectrule belongs to the current node
                        if int(self.asprulemodel.item(row, 1).data(QtCore.Qt.DisplayRole)) == nodeuid:
                            indnme = self.asprulemodel.item(row, 0)
                            induid = self.asprulemodel.item(row, 1)
                            indcon = self.asprulemodel.item(row, 2)
                            indres = self.asprulemodel.item(row, 3)
                            indcom = self.asprulemodel.item(row, 4)
                            var = [indnme.data(QtCore.Qt.DisplayRole), induid.data(QtCore.Qt.DisplayRole), indcon.data(QtCore.Qt.DisplayRole), indres.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                            aspRuleListForWrite.append(var)
                    self.treeManipulate.treeModel.insertNodeSpecProp(index, aspRuleListForWrite, "asprulelist", nodeuid)  # write into the node
                #another node than the current node shall be changed
                else:
                    #at the moment there is only one line of aspectrules for each node
                    for ar in node.aspectrule:
                        var =  [ar[0], ar[1], ar[2], res, ar[4]]
                        aspRuleListForWrite.append(var)
                    self.treeManipulate.treeModel.insertNodeSpecProp(index, aspRuleListForWrite, "asprulelist", nodeuid)  # write into the node


    """resize"""
    """
    def resz(self):
        self.tvaspectruleview.setColumnWidth(0, self.tvaspectruleview.width() * 0.4)
        header = self.tvaspectruleview.horizontalHeader()
        header.setStretchLastSection(True)
    """
    def resz(self):
        i = 0
        while i < 3:
            self.tvaspectruleview.resizeColumnToContents(i)
            i += 1
        header = self.tvaspectruleview.horizontalHeader()
        header.setStretchLastSection(True)

    """model changed via double click"""
    def changeAspRule(self):
        if self.changeOnce:
            self.changeOnce = False
            index = self.tvaspectruleview.currentIndex()
            if index.isValid():
                condic = self.asprulemodel.itemData(index)
                condition = condic[0]
                ccondition, cconditionb, resetc = self.checkReturnCondition(condition)
                if cconditionb: #set data
                    dict = {0 : ccondition}
                    self.asprulemodel.setItemData(index, dict)
                if resetc:
                    dict = {0 : ""}
                    self.asprulemodel.setItemData(index, dict)
            self.writeAspRuleList(self.treeManipulate.treeSelectionModel.currentIndex(), True)
            self.resz()
            if self.validateOnce:
                self.validate()
            self.changeOnce = True

    """a node is deleted, the view has to be updated and checked if only one brother exists -> then the aspectrule for the only child has to be removed"""
    def nodeDeletedCheckDeleteAspRule(self):
        ind = self.treeManipulate.treeSelectionModel.currentIndex()
        nd = self.treeManipulate.treeModel.getNode(ind)
        if nd.typeInfo() == "Aspect Node" or nd.typeInfo() == "Maspect Node":
            rc = self.asprulemodel.rowCount()
            if rc == 2:
                #delete the aspectrule
                j = 2
                while j < 5:
                    index = self.asprulemodel.index(0, j)
                    self.asprulemodel.setData(index, "")
                    j += 1
            self.writeAspRuleList()
            self.treeManipulate.readPropertiesNode()

    """check the value"""
    def checkReturnCondition(self, value):

        if value != "" and not value == "''" and not value == '""' and not value == '\n':
            value = value.strip()   #remove whitespaces before and after
            value = re.sub('\s+', ' ', value).strip()  # or: ' '.join(mystring.split())     #replace several whitespaces with one whitespace

            # check for duplicates of condition
            arlst = self.writeAspRuleList()
            valueForCheck = value.replace(' ', '')  #for checking replace all whitespaces from the value to insert
            for i in range(len(arlst)):
                arlst[i][0] = arlst[i][0].replace(' ', '')
            timesFound = 0
            for i in range(len(arlst)):
                if arlst[i][2] == valueForCheck:
                    timesFound += 1
            if timesFound > 1:
                QMessageBox.information(None, "Changing not possible", "The aspectrule already exists. The condition field is emptied.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            # if the variable is no duplicate the variable has to be checked
            ev = -1
            ok = True
            try:
                ev = ast.literal_eval(value)
            except:
                if ev == -1:
                    lv = sys.exc_info()
                    if type(lv[1]) is SyntaxError:
                        ok = False
            if not ok:
                QMessageBox.information(None, "Changing not possible", "Please enter a logical expression using Python syntax. The expression is deleted.", QtWidgets.QMessageBox.Ok)
                return (value, ok, True)
            else:
                return (value, ok, False)
        else:  # empty value
            QMessageBox.information(None, "The variable condition is empty", "The variable condition is empty.", QtWidgets.QMessageBox.Ok)
            return ("", False, True)

    """update aspectrule when the name of nodes is changed in the tree"""
    def updateAspRuleNameChanged(self):
        #getting the aspectrules
        arlst = self.writeAspRuleList()
        j = 0
        while j < len(arlst):
            aru = int(arlst[j][1])
            arn = arlst[j][1]
            nodefound = self.treeManipulate.findNodeFromUid(aru)
            if nodefound is not None and arn != nodefound.name():
                index = self.asprulemodel.index(j, 0)
                self.asprulemodel.setData(index, nodefound.name())
            j += 1

    """call validate if an SESvar or SESfun changed -> normally not all nodes are validated -> to make program faster"""
    def validateSESvarfunChanged(self):
        self.validate("", "", None, True)

    """check the content and evaluate the result"""
    def validate(self, sesvarl="", sesfunl="", nd=None, validateAllNodes=False, paths=None):

        #sub function
        def validateAspRule(nd, sviar, sesfunl):

            asprulelist = nd.aspectrule

            empty = True
            calculable = False
            funVarFound = False
            ret = ""
            if asprulelist: #if there is an aspectrule:
                dataline = nd.aspectrule[0][2]

                # now try to interprete the aspectrule

                """
                exp = []
    
                #first try
                #separate at whitespaces
                spacesplit = dataline.split(" ")
    
                #separate at keywords
                keysplit = []
                for s in spacesplit:
                    if not keyword.iskeyword(s):
                        keysplit.append(s)
                """

                """
                #next try
                #separate at keywords
                keysplit = re.split("re.escape(keyword.kwlist)\s*", dataline)
    
                for k in keysplit:
                    gleichsplit = k.split("==")
                    for g in gleichsplit:
                        ungleichsplit = g.split("!=")
                        for ug in ungleichsplit:
                            ggsplit = ug.split(">=")
                            for gg in ggsplit:
                                kgsplit = gg.split("<=")
                                for kg in kgsplit:
                                    gasplit = kg.split(">")
                                    for ga in gasplit:
                                        kasplit = ga.split("<")
                                        exp.append(kasplit)
    
                expressions = []
                for e in exp:
                    if e[0] != "":
                        e[0] = e[0].strip()
                        expressions.append(e[0])
                """

                funVarFound = True

                #replace True and False by an expression -> it should be two connected expressions
                dataline = dataline.replace('False', '0==1')
                dataline = dataline.replace('True', '1==1')
                #now find the Python commands and split the string
                keywordlistforre = ' |'.join(keyword.kwlist) + " |==|!=|<=|>=|<|>"
                #separators = re.findall(keywordlistforre, dataline)
                expressions = re.split(keywordlistforre, dataline)

                #strip every item and remove if empty
                #s = len(separators)-1
                #while s >= 0:
                    #separators[s] = separators[s].strip()
                    #remove if empty
                    #if separators[s] == "":
                        #del separators[s]
                    #s -= 1
                e = len(expressions)-1
                while e >= 0:
                    expressions[e] = expressions[e].strip()
                    #remove if empty
                    if expressions[e] == "":
                        del expressions[e]
                    e -= 1

                expressionvarfunval = []
                for k in range(len(expressions)):

                    # check if the expression is an SES variable or function
                    try:
                        ast.literal_eval(expressions[k])
                    except:
                        # the value is no Python value so it could be the name of an SES variable or function
                        # check if the expression is an SES variable
                        try:
                            ret = eval(expressions[k], globals(), sviar.__dict__)
                            # replace the name with the value
                            if isinstance(ret, str):
                                ret = '"' + ret + '"'
                            #expressions[k] = ret
                            expressionvarfunval.append([expressions[k], ret])
                        except:
                            pass

                        # check if the expression is an SES function
                        if isinstance(expressions[k], str) and "(" in expressions[k] and ")" in expressions[k]:
                            funname = expressions[k].split("(")
                            funname[1] = funname[1][0:-1]
                            vars = funname[1].split(",")
                            if vars[0] == '':
                                del vars[0]
                            for v in range(len(vars)):
                                vars[v] = vars[v].strip()
                            # check if the parameters are SES variables and get the values
                            varvalues = []
                            for v in vars:
                                try:
                                    vv = ast.literal_eval(v)
                                    varvalues.append(vv)
                                except:
                                    # the value is no Python value so it could be the name of an SES variable or function
                                    # check if the expression is an SES variable
                                    try:
                                        ret = eval(v, globals(), sviar.__dict__)
                                        # replace the name with the value
                                        varvalues.append(ret)
                                    except:
                                        varvalues.append("")

                            # now get the function from the sesFunctions and try to find a match with the entry
                            sesfunlcopy = [d[:] for d in sesfunl]  # make a copy of the list and the list elements
                            for sesfunvalue in sesfunlcopy:
                                if sesfunvalue[0] == funname[0]:
                                    # get the vars of the found function match since the parameters in the function definition do not have to match the SES variable names
                                    funvarsfound = re.findall('def\s+' + re.escape(funname[0]) + '\(.*\)', sesfunvalue[1])
                                    funvarsfound[0] = funvarsfound[0].replace("def", "")
                                    funvarsfound[0] = funvarsfound[0].replace(funname[0] + "(", "")
                                    funvarsfound[0] = funvarsfound[0].replace(")", "")
                                    funvarsfound[0] = funvarsfound[0].strip()
                                    vars2 = funvarsfound[0].split(",")
                                    if vars2[0] == '':
                                        del vars2[0]
                                    # remove existing default values
                                    for i in range(len(vars2)):
                                        if i < len(vars):
                                            vars2[i] = vars2[i].split("=")[0]
                                    # make variables to default variables by position
                                    for i in range(len(vars2)):
                                        if i < len(vars):
                                            if varvalues[i] != "":
                                                if isinstance(varvalues[i], str):
                                                    vars2[i] = vars2[i] + " = '" + varvalues[i] + "'"
                                                else:
                                                    vars2[i] = vars2[i] + " = " + str(varvalues[i])
                                            else:
                                                funVarFound = False

                                    # build a string from the variables to pass
                                    for i in range(len(vars2)):
                                        vars2[i] = str(vars2[i])
                                    varstring = ', '.join(vars2)

                                    # replace parameters in the function with the varstring
                                    sesfunvalue[1] = re.sub('def ' + re.escape(sesfunvalue[0]) + '\(.*\)', 'def ' + re.escape(sesfunvalue[0]) + '(' + varstring + ')', sesfunvalue[1])

                                    # try to execute the function
                                    try:
                                        exec(sesfunvalue[1])
                                        self.ret = None
                                        execute = "self.ret = " + sesfunvalue[0] + "()"
                                        if sesfunvalue[0] in locals():
                                            try:
                                                exec(execute)
                                                # replace the entry with the result
                                                #expressions[k] = self.ret
                                                expressionvarfunval.append([expressions[k], self.ret])
                                            except:
                                                pass
                                    except:
                                        pass
                """
                # place ' again for strings -> now this is replaced by the next blocks
                for i in range(len(expressions)):
                    try:
                        expressions[i] = ast.literal_eval(expressions[i])
                        expressions[i] = str(expressions[i])
                    except:
                        pass
                        #expressions[i] = "'" + expressions[i] + "'"
                        #expressions[i] = expressions[i][1:-1]
                """

                #delete empty fields in the expressions
                #lenex = list(range(0,len(expressions)))    #not needed to create list
                for s in range(len(expressions)):
                    if expressions[s] == "":
                        del expressions[s]
                """
                #place ' again for strings
                lenex = range(len(expressions))
                toExamine = lenex[::2]      #take every second element
                for s in toExamine:
                    if type(expressions[s]) is str:
                        expressions[s] = expressions[s+1][0] + expressions[s] + expressions[s+1][0]
                """

                # rebuild the complete expression now with the inserted data (expression and separator in turn) -> not needed anymore, now only the expressions are replaced (see below)
                #n = 0
                #completeline = []
                #while n < len(expressions):
                    #completeline.append(str(expressions[n]))
                    #if n < len(separators):
                        #completeline.append(separators[n])
                    #n += 1
                #dataline = ' '.join(completeline)

                #replace the evaluated SESvar / SESfuns expressions
                dataline1 = ""
                dataline2 = ""
                for evfv in expressionvarfunval:
                    dataline1 = re.sub(r"\b"+re.escape(evfv[0])+r"\b", str(evfv[1]), dataline)
                    dataline2 = re.sub(re.escape(evfv[0]), repr(evfv[1]), dataline)

                # check if the whole expression can be interpreted now containing no more SES variables and functions
                empty = False
                ret = False
                calculable = True
                if dataline == "":
                    empty = True
                try:
                    ret = eval(dataline1)
                except:
                    try:
                        ret = eval(dataline2)
                    except:
                        calculable = False

            return empty, calculable, funVarFound, ret

        #sub function
        def findBrothernodes(currentnode):
            # getting the indices of the existing nodes
            indices = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())
            # getting the nodes of the tree
            nodes = []
            for ind in indices:
                nodes.append(self.treeManipulate.treeModel.getNode(ind[0]))
            # find uid of current node
            currentnodeuid = currentnode.getUid()
            # get the brothers of the same nodetype
            brothernodes = []
            brotherindices = []
            for i in range(len(nodes)):
                if self.treeManipulate.areBrothers(nodes[i].getUid(), currentnodeuid) and nodes[i].typeInfo() == currentnode.typeInfo():
                    brothernodes.append(nodes[i])
                    brotherindices.append(indices[i])
            return brothernodes, brotherindices

        #sub function
        def checkXor(brothernodes, currentnode, ret):
            failxor = False
            numTrue = 0
            for ndbro in brothernodes:
                if ndbro.getUid() != currentnode.getUid() and ndbro.aspectrule != [] and (ndbro.aspectrule[0][3] == "T" or ndbro.aspectrule[0][3] == "T -> F"):
                    numTrue += 1
            # check what is the return value of the aspectrule of the current node and add it if true
            if ret == True:
                numTrue += 1
            # now decide if the xor is failed
            if numTrue > 1:
                failxor = True
            return failxor

        #sub function
        def addSpecialVars(sesvarsInRulesClass, currentNode=None, paths=None):
            #add the special variables (node specific variables)
            if currentNode == None:
                currentIndex = self.treeManipulate.treeSelectionModel.currentIndex()
                currentNode = self.treeManipulate.treeModel.getNode(currentIndex)
            #append path underscore variables
            #if this function is started for pruning, paths is passed
            if not paths:
                paths = self.treeManipulate.findPaths()  # get the paths of the tree
            #get the path with this node
            path = []
            i, j, nf = 0, 0, False
            while i < len(paths) and not nf:
                j = 0
                while j < len(paths[i]) and not nf:
                    if paths[i][j][0].getUid() == currentNode.getUid():
                        nf = True
                    j += 1
                i += 1
            i -= 1
            j -= 1
            k = 0
            while k <= j:
                path.append(paths[i][k])
                k += 1
            #the variable "path" now holds all nodes from the current node to the root
            pathUnderscoreVar = {}
            for pa in path:
                if pa[0].typeInfo() == "Entity Node":
                    for at in pa[0].attributes:
                        if at[0].startswith("_"):
                            pathUnderscoreVar.update({at[0]: at[1]})
            #append all _ variables in the path of the current node
            setattr(sesvarsInRulesClass, "PATH", pathUnderscoreVar)

        #here the validate function begins

        # own class for SES variables
        class sesvarsinasprules:
            pass

        #create an instance of the SES variables class
        sviar = sesvarsinasprules

        #was the process started for coloring the lines or for pruning?
        if sesvarl == "" and sesfunl == "" and nd == None:  # the validate process was started from the editor for coloring the lines
            # fill the instance of the sesvar class
            for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])   #interprete the type of the value
                except:
                    pass    #do nothing, it stays a string
                setattr(sviar, sesvarvalue[0], sesvarvalue[1])  # if you want to add the variables to this class object: setattr(self, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(sviar)

            #get the SES functions
            sesfunl = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()

            #go through all nodes
            indices = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())

            for ind in indices:
                #get the node
                nd = self.treeManipulate.treeModel.getNode(ind[0])

                ########################################################################################################
                ###The following lines only exist for aspectrules -> to exclude checks and to make the program faster###
                #only continue:
                # a) if a SESvar or a SESfun is changed, all nodes need to be recalculated -> validateAllNodes is true
                # b) if the node behind ind[0] is a brother of the current selected node -> then the aspecrule needs to be revalidated for ind
                validateNode = False
                if not validateAllNodes:    #this only needs to be checked if not all nodes need to be validated anyway
                    nds = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
                    chl = nds.parent().childrenlist()   #childrenlist of the parent of the current selected node -> only if nd is in chl, check it (either it is the node itself or it is a brother)
                    for chil in chl:
                        if chil.getUid() == nd.getUid():
                            validateNode = True
                ########################################################################################################

                #only continue if the node has aspectrules (and validateAllNodes or validateNode is true -> to make the program faster)
                if (nd.typeInfo() == "Aspect Node" or nd.typeInfo() == "Maspect Node") and (validateAllNodes or validateNode):

                    empty, calculable, funVarFound, ret = validateAspRule(nd, sviar, sesfunl)

                    #if there are aspect siblings only one aspect may evaluate to true -> check if there are brothers
                    brothernodes, brotherindices = findBrothernodes(nd)

                    #if there are brothers, only one aspectrule condition may evaluate to true
                    failXor = checkXor(brothernodes, nd, ret)

                    #write evaluated result into the node
                    r = ""
                    if calculable and funVarFound:
                        if ret == True and not failXor:
                            r = "T"
                        elif ret == True and failXor:
                            r = "T -> F"
                        else:
                            r = "F"
                    self.writeAspRuleList(ind[0], False, r)

                    #update the model if the validate process comes from the editor
                    self.updateModel(ind[0])

                    #remove just updated node from the brothers
                    brothernodes.remove(nd)
                    brotherindices.remove(ind)

                    #if failxor or not we have to update the other nodes and update the model
                    for i in range(len(brothernodes)):
                        if failXor:
                            if brothernodes[i].aspectrule != [] and brothernodes[i].aspectrule[0][3] == "T":
                                self.writeAspRuleList(brotherindices[i][0], False, "T -> F")
                                self.updateModel(brotherindices[i][0])
                        else:
                            if brothernodes[i].aspectrule != [] and brothernodes[i].aspectrule[0][3] == "T -> F":
                                self.writeAspRuleList(brotherindices[i][0], False, "T")
                                self.updateModel(brotherindices[i][0])

        else:  #the validate process was started for pruning
            # fill the instance of the sesvar class
            for sesvarvalue in sesvarl:
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])   #interprete the type of the value
                except:
                    pass    #do nothing, it stays a string
                setattr(sviar, sesvarvalue[0], sesvarvalue[1])  # if you want to add the variables to this class object: setattr(self, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(sviar, nd, paths)

            #the SES functions are given in the pass list

            #only continue if the node has aspectrules (only for safety, this part of the function is called from the pruning function only for Aspect or Maspect nodes)
            if nd.typeInfo() == "Aspect Node" or nd.typeInfo() == "Maspect Node":

                empty, calculable, funVarFound, ret = validateAspRule(nd, sviar, sesfunl)

                #return the evaluated result
                if not empty:
                    if calculable and funVarFound and ret:
                        return "T"
                    else:
                        return "F"
                else:
                    return ""


    def updateModel(self, ind):
        #get the current aspectrules for the node
        asp = self.treeManipulate.treeModel.getNode(ind).aspectrule

        for row in range(self.asprulemodel.rowCount()):
            index0 = self.asprulemodel.index(row, 0)
            index1 = self.asprulemodel.index(row, 1)
            index2 = self.asprulemodel.index(row, 2)
            index3 = self.asprulemodel.index(row, 3)
            dict = {0: ""}

            # if the nodeuid for which the specrule is fits the nodeuid of the line
            modellineuid = int(index1.data(QtCore.Qt.DisplayRole))
            for ar in asp:
                if int(ar[1]) == modellineuid:
                    if ar[2] == "":
                        #no aspectrule specified -> get the alternating colors
                        if row % 2 == 0:
                            color0 = QtGui.QColor(QtCore.Qt.white)
                            color2 = color0
                        else:
                            color0 = QtGui.QColor(239, 240, 241, 255)
                            color2 = color0
                    elif ar[2] != "" and ar[3] == "":
                        #the specified aspectrule can not be evaluated (e.g. it contains a SES variable which is not defined)
                        dict = {0: ""}
                        color2 = QtGui.QColor(255, 195, 195, 255)
                        color0 = QtGui.QColor(255, 195, 195, 255)
                    else:
                        #there is a result -> get the result and color the row
                        color2 = QtGui.QColor(195, 255, 195, 255)
                        if ar[3] == "T":
                            dict = {0: "T"}
                            color0 = QtGui.QColor(195, 255, 195, 255)
                        elif ar[3] == "F":
                            dict = {0: "F"}
                            color0 = QtGui.QColor(255, 195, 195, 255)
                        elif ar[3] == "T -> F":
                            dict = {0: "T -> F"}
                            color0 = QtGui.QColor(255, 195, 195, 255)

                    self.asprulemodel.setItemData(index3, dict)
                    self.asprulemodel.setData(index0, color0, QtCore.Qt.BackgroundColorRole)
                    self.asprulemodel.setData(index1, color0, QtCore.Qt.BackgroundColorRole)
                    self.asprulemodel.setData(index2, color2, QtCore.Qt.BackgroundColorRole)
                    self.asprulemodel.setData(index3, color0, QtCore.Qt.BackgroundColorRole)

    """empty the model"""
    def emptyAspruleModel(self):
        self.asprulemodel.clear()
        self.asprulemodel.setHorizontalHeaderLabels(["Node", "uid", "Condition", "result", "comment"])

    """help"""
    def help(self):
        msgBox = QMessageBox(self.treeManipulate.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("attributes: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()

    #old functions where the keywords var and fun were used-------------------------------------------------------------


    """color the fields depending on the content"""
    """
    def validate(self):
        # own class for SES variables
        class sesvarsinasprules:
            pass

        # create an instance of the SES variables class and fill it
        sviar = sesvarsinasprules
        for sesvarvalue in self.sesVariables.outputSesVarList():
            try:
                sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
            except:
                pass  # do nothing, it stays a string
            setattr(sviar, sesvarvalue[0], sesvarvalue[1])

        # now try to interprete the aspectrule
        for row in range(self.asprulemodel.rowCount()):
            dataline = self.asprulemodel.item(row, 2).data(QtCore.Qt.DisplayRole)

            # separate at ==
            datasplit = dataline.split("==")

            # look if the part (seperated by ==) is interpretable
            partinterpretable = []

            for k in range(len(datasplit)):
                data = datasplit[k].strip()

                # find all occurrences of var between the == and replace it with the value
                matchessv = re.
                ('var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)', data)
                foundsv = []
                for ma in matchessv:
                    # connect the tuple of each resulting group
                    varname = ma[0] + ma[1]
                    try:
                        ret = eval(varname, globals(), sviar.__dict__)
                        # replace the name with the value in data
                        data = re.sub('var\([\"\']' + re.escape(varname) + '[\"\']\)', '' + re.escape(str(ret)), data)
                        foundsv.append(True)
                    except:
                        foundsv.append(False)

                # look if all SES variables could be interpreted
                foundsvall = all(foundsv)

                # find all occurrences of fun between the == and replace it with the result
                foundsf = []
                # only go on if all SES variables could be interpreted
                if foundsvall:
                    # find all fun() in the entry
                    matchessf = re.findall('fun\([\"\']([a-z]|[A-Z])(\w+)?[\"\'](.*)\)', data)
                    for ma in matchessf:
                        # connect the tuple of each resulting group
                        funname = ma[0] + ma[1]
                        # find parameters for the function and replace them with the value
                        if ma[2] == "":
                            vars = []
                        else:
                            vars = ma[2].split(",")
                            del vars[0]
                            for i in range(len(vars)):
                                value = vars[i].strip()
                                value = value.replace("'", "")
                                value = value.replace('"', "")
                                # vars with correct type
                                try:
                                    vars[i] = ast.literal_eval(value)
                                except:
                                    vars[i] = value

                        # now get the function from the sesFunctions and try to find a match with the entry
                        functionfound = False
                        sesfunvalue = []
                        for sesfunvalue in self.sesFunctions.outputSesFunList():
                            if sesfunvalue[0] == funname:
                                functionfound = True
                                # get the vars of the found function match
                                funvarsfound = re.findall('def\s+' + re.escape(funname) + '\(.*\)', sesfunvalue[1])
                                funvarsfound[0] = funvarsfound[0].replace("def", "")
                                funvarsfound[0] = funvarsfound[0].replace(funname + "(", "")
                                funvarsfound[0] = funvarsfound[0].replace(")", "")
                                funvarsfound[0] = funvarsfound[0].strip()
                                vars2 = funvarsfound[0].split(",")
                                # make variables to default variables by position
                                for i in range(len(vars2)):
                                    if i < len(vars):
                                        if isinstance(vars[i], str):
                                            vars2[i] = vars2[i] + " = '" + vars[i] + "'"
                                        else:
                                            vars2[i] = vars2[i] + " = " + str(vars[i])
                                # build a string from the variables to pass
                                varstring = ""
                                for var in vars2:
                                    if varstring == "":
                                        varstring = var
                                    else:
                                        varstring = varstring + ", " + var

                                # replace parameters in the function with the varstring
                                sesfunvalue[1] = re.sub('def ' + re.escape(sesfunvalue[0]) + '\(.*\)',
                                                        'def ' + re.escape(sesfunvalue[0]) + '(' + varstring + ')',
                                                        sesfunvalue[1])
                                break

                        # if the function was found
                        if functionfound:
                            foundsf.append(True)
                        else:
                            foundsf.append(False)

                        # try to execute the function
                        exec(sesfunvalue[1])
                        ret = None
                        execute = "ret = " + sesfunvalue[0] + "()"
                        a = locals()
                        exec(execute, locals())
                        a = 0

                        # replace the fun(...) in the entry with the result
                        # data =

                # set the datasplit to the changed data
                datasplit[k] = data

                # look if all SES variables could be interpreted
                # foundsfall = all(foundsf)

                if foundsvall:  # and foundsfall:
                    partinterpretable.append(True)
                else:
                    partinterpretable.append(False)

            # check if the whole expression can be interpreted now containing no more fun() and var()
            ret = False
            calculable = True
            if all(partinterpretable):
                # place ' again for strings
                for i in range(len(datasplit)):
                    try:
                        datasplit[i] = ast.literal_eval(datasplit[i])
                        datasplit[i] = str(datasplit[i])
                    except:
                        datasplit[i] = "'" + datasplit[i] + "'"
                # connect datasplit again
                data = '=='.join(datasplit)
                try:
                    ret = eval(data)
                except:
                    pass
            else:
                calculable = False

            # set the colors
            index0 = self.asprulemodel.index(row, 0)
            index1 = self.asprulemodel.index(row, 1)
            index2 = self.asprulemodel.index(row, 2)
            if calculable:
                color2 = QtGui.QColor(195, 255, 195, 255)
                if ret == True:
                    color0 = QtGui.QColor(195, 255, 195, 255)
                else:
                    color0 = QtGui.QColor(255, 195, 195, 255)
            else:
                color2 = QtGui.QColor(255, 195, 195, 255)
                color0 = QtGui.QColor(255, 195, 195, 255)
            self.asprulemodel.setData(index0, color0, QtCore.Qt.BackgroundColorRole)
            self.asprulemodel.setData(index1, color0, QtCore.Qt.BackgroundColorRole)
            self.asprulemodel.setData(index2, color2, QtCore.Qt.BackgroundColorRole)
    """

class Priority:
    def __init__(self, treeManipulate, tabnumber):
        self.treeManipulate = treeManipulate
        self.tabnumber = tabnumber
        self.lepriority = None
        self.lepriorityres = None
        self.setUiInit()
        #signals
        self.lepriority.textChanged.connect(self.setCheckValue)
        #self.treeManipulate.tbproperties.currentChanged.connect(self.getLastToolboxPage)
        self.treeManipulate.treeSelectionModel.currentChanged.connect(self.setCheckValueNodeChanged)  #the selection was changed so the selected node was changed
        self.treeManipulate.tbproperties.currentChanged.connect(self.setCheckValueNodeChanged)    #the toolbox is changed so the selected node was changed
        #variables
        self.currentSelectedTbPage = -1
        self.lastSelectedTbPage = -1

    def setUiInit(self):
        if self.tabnumber == 0:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst1[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst1[2]
        if self.tabnumber == 1:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst2[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst2[2]
        if self.tabnumber == 2:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst3[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst3[2]
        if self.tabnumber == 3:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst4[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst4[2]
        if self.tabnumber == 4:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst5[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst5[2]
        if self.tabnumber == 5:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst6[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst6[2]
        if self.tabnumber == 6:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst7[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst7[2]
        if self.tabnumber == 7:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst8[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst8[2]
        if self.tabnumber == 8:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst9[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst9[2]
        if self.tabnumber == 9:
            self.lepriority = self.treeManipulate.main.aspectrulefieldst10[1]
            self.lepriorityres = self.treeManipulate.main.aspectrulefieldst10[2]

    def setSesVarsFunsInPrio(self):
        if self.tabnumber == 0:
            self.sesVariablest1 = self.treeManipulate.main.modellist[0][1]
            self.sesFunctionst1 = self.treeManipulate.main.modellist[0][2]
            self.sesVariablest1.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst1.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 1:
            self.sesVariablest2 = self.treeManipulate.main.modellist[1][1]
            self.sesFunctionst2 = self.treeManipulate.main.modellist[1][2]
            self.sesVariablest2.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst2.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 2:
            self.sesVariablest3 = self.treeManipulate.main.modellist[2][1]
            self.sesFunctionst3 = self.treeManipulate.main.modellist[2][2]
            self.sesVariablest3.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst3.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 3:
            self.sesVariablest4 = self.treeManipulate.main.modellist[3][1]
            self.sesFunctionst4 = self.treeManipulate.main.modellist[3][2]
            self.sesVariablest4.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst4.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 4:
            self.sesVariablest5 = self.treeManipulate.main.modellist[4][1]
            self.sesFunctionst5 = self.treeManipulate.main.modellist[4][2]
            self.sesVariablest5.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst5.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 5:
            self.sesVariablest6 = self.treeManipulate.main.modellist[5][1]
            self.sesFunctionst6 = self.treeManipulate.main.modellist[5][2]
            self.sesVariablest6.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst6.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 6:
            self.sesVariablest7 = self.treeManipulate.main.modellist[6][1]
            self.sesFunctionst7 = self.treeManipulate.main.modellist[6][2]
            self.sesVariablest7.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst7.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 7:
            self.sesVariablest8 = self.treeManipulate.main.modellist[7][1]
            self.sesFunctionst8 = self.treeManipulate.main.modellist[7][2]
            self.sesVariablest8.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst8.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 8:
            self.sesVariablest9 = self.treeManipulate.main.modellist[8][1]
            self.sesFunctionst9 = self.treeManipulate.main.modellist[8][2]
            self.sesVariablest9.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst9.sesfunChangedSignal.connect(self.validate)
        if self.tabnumber == 9:
            self.sesVariablest10 = self.treeManipulate.main.modellist[9][1]
            self.sesFunctionst10 = self.treeManipulate.main.modellist[9][2]
            self.sesVariablest10.sesvarChangedSignal.connect(self.validate)
            self.sesFunctionst10.sesfunChangedSignal.connect(self.validate)

    """read -> called from tree manipulate"""
    def readPrio(self, value):
        self.lepriority.setText(value)
        self.validate()

    """write -> the entries in the current node"""
    def writePrio(self):

        node = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
        formernode = self.treeManipulate.treeModel.getNode(self.treeManipulate.lastSelectedIndex)
        if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
            self.treeManipulate.treeModel.insertNodeSpecProp(self.treeManipulate.treeSelectionModel.currentIndex(), self.lepriority.text(), "prio", node.getUid())  # write into the node
        elif formernode.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
            self.treeManipulate.treeModel.insertNodeSpecProp(self.treeManipulate.lastSelectedIndex, self.lepriority.text(), "prio", formernode.getUid())  # write into the node

    """get the last selected page of the toolbox"""
    #def getLastToolboxPage(self):
        #self.lastSelectedTbPage = self.currentSelectedTbPage
        #self.currentSelectedTbPage = self.treeManipulate.tbproperties.currentIndex()

    """call check and set the value on toolbox change -> not needed any more"""
    def setCheckValueNodeChanged(self):
        self.setCheckValue("", True)

    """check and set the value"""
    def setCheckValue(self, abc, isNodeChange=False):

        value = self.lepriority.text()
        value = value.strip()

        if value != "":
            if not isNodeChange:
                try:
                    value = ast.literal_eval(value)
                    if isinstance(value, int):
                        if value > 0:
                            self.writePrio()
                            self.validate()
                            return
                        else:
                            self.validate()
                            QMessageBox.information(None, "Changing not possible","Please enter a value >0.", QtWidgets.QMessageBox.Ok)
                    else:
                        self.validate()
                        QMessageBox.information(None, "Changing not possible", "Please enter an integer value >0, the name of an SES variable or function.", QtWidgets.QMessageBox.Ok)
                except:
                    # the value is no Python value so it could be the name of an SES variable or function
                    # check if it can be the syntax of an SES variable or function
                    attribregex = re.compile('^([a-z]|[A-Z])(\w+)?(\(([\"\']?\w+[\"\']?)?(,\s*?[\"\']?\w+[\"\']?)*\))?$')
                    attribregexcorrect = attribregex.match(value)
                    if attribregexcorrect is not None:
                        self.writePrio()
                        self.validate()
                        return
                    else:
                        pass
            if isNodeChange:# and self.lastSelectedTbPage == 2:
                ok = self.validate("", "", None, True)
                if not ok:
                    QMessageBox.information(None, "The priority value cannot be evaluated",
                                            "Please enter an integer >0 or if you want to reference an SES variable or function, use the syntax\n"
                                            "sesvarname or\nsesfunname(1[, 4.5]) or\nsesfunname(5[, sesvarname]).\n"
                                            "The expression in square brackets is optional, do not type the square brackets. Use it if you want to pass parameters.\n"
                                            "sesvarname and sesfunname must be alphanumeric not beginning with a number.", QtWidgets.QMessageBox.Ok)

    """color the value field if an SES variable or SES function can be interpreted"""
    def validate(self, sesvarl="", sesfunl="", nd=None, needAllOkReturn=False, paths=None):

        #sub function
        def validatePrio(nd, svipr, sesfunl):

            value = nd.priority

            isInteger = False
            varFound = False
            funFound = False
            funVarFound = True
            varOk = False
            funOk = False
            allOk = False
            retval = 1

            if value != "":
                try:
                    value = ast.literal_eval(value)
                    if isinstance(value, int):
                        retval = value
                        isInteger = True
                except:
                    # the value is no Python value so it could be the name of an SES variable or function
                    # check if the expression is an SES variable

                    # evaluate the SES variable
                    try:
                        ret = eval(value, globals(), svipr.__dict__)
                        varFound = True
                        if isinstance(ret, int):
                            retval = ret
                            varOk = True
                    except:
                        pass

                    # check if the expression is an SES function
                    if isinstance(value, str) and "(" in value and ")" in value:
                        funname = value.split("(")
                        funname[1] = funname[1][0:-1]
                        vars = funname[1].split(",")
                        if vars[0] == '':
                            del vars[0]
                        for v in range(len(vars)):
                            vars[v] = vars[v].strip()
                        # check if the parameters are SES variables and get the values
                        varvalues = []
                        for v in vars:
                            try:
                                vv = ast.literal_eval(v)
                                varvalues.append(vv)
                            except:
                                # the value is no Python value so it could be the name of an SES variable or function
                                # check if the expression is an SES variable
                                try:
                                    ret = eval(v, globals(), svipr.__dict__)
                                    # replace the name with the value
                                    varvalues.append(ret)
                                except:
                                    varvalues.append("")

                        # now get the function from the sesFunctions and try to find a match with the entry
                        for sesfunvalue in sesfunl:
                            if sesfunvalue[0] == funname[0]:
                                # get the vars of the found function match since the parameters in the function definition do not have to match the SES variable names
                                funvarsfound = re.findall('def\s+' + re.escape(funname[0]) + '\(.*\)', sesfunvalue[1])
                                funvarsfound[0] = funvarsfound[0].replace("def", "")
                                funvarsfound[0] = funvarsfound[0].replace(funname[0] + "(", "")
                                funvarsfound[0] = funvarsfound[0].replace(")", "")
                                funvarsfound[0] = funvarsfound[0].strip()
                                vars2 = funvarsfound[0].split(",")
                                if vars2[0] == '':
                                    del vars2[0]
                                # remove existing default values
                                for i in range(len(vars2)):
                                    if i < len(vars):
                                        vars2[i] = vars2[i].split("=")[0]
                                # make variables to default variables by position
                                for i in range(len(vars2)):
                                    if i < len(vars):
                                        if varvalues[i] != "":
                                            if isinstance(varvalues[i], str):
                                                vars2[i] = vars2[i] + " = '" + varvalues[i] + "'"
                                            else:
                                                vars2[i] = vars2[i] + " = " + str(varvalues[i])
                                        else:
                                            funVarFound = False

                                # build a string from the variables to pass
                                for i in range(len(vars2)):
                                    vars2[i] = str(vars2[i])
                                varstring = ', '.join(vars2)

                                # replace parameters in the function with the varstring
                                sesfunvalue[1] = re.sub('def ' + re.escape(sesfunvalue[0]) + '\(.*\)', 'def ' + re.escape(sesfunvalue[0]) + '(' + varstring + ')', sesfunvalue[1])

                                # try to execute the function
                                try:
                                    exec(sesfunvalue[1])
                                    self.ret = None
                                    execute = "self.ret = " + sesfunvalue[0] + "()"
                                    if sesfunvalue[0] in locals():
                                        try:
                                            exec(execute)
                                            funFound = True
                                            # replace the entry with the result
                                            value = self.ret
                                            if isinstance(value, int):
                                                if value > 0:
                                                    retval = self.ret
                                                    funOk = True
                                        except:
                                            pass
                                except:
                                    pass

            if isInteger or (not isInteger and varFound and varOk) or (not isInteger and funFound and funVarFound and funOk):
                allOk = True

            #always return a string
            retval = str(retval)

            return isInteger, varFound, funFound, funVarFound, varOk, funOk, allOk, retval

        # sub function -> add the special variables (node specific variables) to the sesvars class
        def addSpecialVars(sesvarsInRulesClass, currentNode=None, paths=None):
            # find the current node, if it is not passed
            if currentNode == None:
                currentIndex = self.treeManipulate.treeSelectionModel.currentIndex()
                currentNode = self.treeManipulate.treeModel.getNode(currentIndex)

            # append PATH underscore variables
            #if this function is started for pruning, paths is passed
            if not paths:
                paths = self.treeManipulate.findPaths()  # get the paths of the tree
            # get the path with this node
            path = []
            i, j, nf = 0, 0, False
            while i < len(paths) and not nf:
                j = 0
                while j < len(paths[i]) and not nf:
                    if paths[i][j][0].getUid() == currentNode.getUid():
                        nf = True
                    j += 1
                i += 1
            i -= 1
            j -= 1
            k = 0
            while k <= j:
                path.append(paths[i][k])
                k += 1
            # the variable "path" now holds all nodes from the current node to the root
            pathUnderscoreVar = {}
            for pa in path:
                if pa[0].typeInfo() == "Entity Node":
                    for at in pa[0].attributes:
                        if at[0].startswith("_"):
                            pathUnderscoreVar.update({at[0]: at[1]})
            # append all _ variables in the path of the current node
            setattr(sesvarsInRulesClass, "PATH", pathUnderscoreVar)

        #here the validate function begins

        #own class for SES variables
        class sesvarsinprio:
            pass

        #create an instance of the SES variables class and fill it
        svipr = sesvarsinprio

        #was the process started for coloring the lines or for pruning
        if sesvarl == "" and sesfunl == "" and nd == None:     # the validate process was started from the editor for coloring the lines
            # fill the instance of the sesvar class
            for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(svipr, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svipr)

            # get the SES functions
            sesfunl = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()

            #get the current node
            currentIndex = self.treeManipulate.treeSelectionModel.currentIndex()
            currentNode = self.treeManipulate.treeModel.getNode(currentIndex)

            #only continue if the node has a priority value
            if currentNode.typeInfo() == "Aspect Node" or currentNode.typeInfo() == "Maspect Node":

                isInteger, varFound, funFound, funVarFound, varOk, funOk, allOk, retval = validatePrio(currentNode, svipr, sesfunl)

                #update the line and set result field
                correctLineUpdated = self.updateLine(isInteger, varFound, funFound, funVarFound, varOk, funOk, currentNode, retval)
                if needAllOkReturn and correctLineUpdated:
                    return allOk
            return True

        else:  # the validate process was started for pruning
            #fill the instance of the sesvar class
            for sesvarvalue in sesvarl:
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(svipr, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svipr, nd, paths)

            #the SES functions are given in the pass list

            #only continue if the node has a priority value
            if nd.typeInfo() == "Aspect Node" or nd.typeInfo() == "Maspect Node":

                isInteger, varFound, funFound, funVarFound, varOk, funOk, allOk, retval = validatePrio(nd, svipr, sesfunl)

                #return the evaluated result and whether the value is okay for pruning
                return retval, allOk


    def updateLine(self, isInteger, varFound, funFound, funVarFound, varOk, funOk, nd, retval):
        if nd.priority == self.lepriority.text():
            # color the rows according to the found result
            self.lepriority.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")
            if isInteger:  #color white
                self.lepriority.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")

            elif not isInteger and varFound and not varOk:
                self.lepriority.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
            elif not isInteger and varFound and varOk:
                self.lepriority.setStyleSheet("QLineEdit { background: rgb(195, 255, 195); selection-background-color: rgb(0, 255, 255); }")

            elif not isInteger and funFound and not funOk:
                self.lepriority.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
            elif not isInteger and funFound and funVarFound and funOk:
                self.lepriority.setStyleSheet("QLineEdit { background: rgb(195, 255, 195); selection-background-color: rgb(0, 255, 255); }")

            else:
                self.lepriority.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")

            #set the return value field (retval should be a string (already given back as string from the validateNumRep function))
            self.lepriorityres.setText(retval)

            return True