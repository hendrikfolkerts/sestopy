# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QItemSelectionModel, Qt

import ast
import re
import keyword

#redefine functions from QStandarditemmodel
class SpecRuleStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent, specrule):
        super(SpecRuleStandardItemModel, self).__init__(parent)
        self.specrule = specrule

    #second row only changable
    def flags(self, index):
        #only set the edit flags if the selected node in the tree equals the node for which the specrule exists and only allow to change the condition column
        if index.column() == 2 or index.column() == 4:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsSelectable

class Specrule:
    def __init__(self, treeManipulate, tabnumber):
        self.treeManipulate = treeManipulate
        self.tabnumber = tabnumber
        self.tvspecruleview = None
        self.bspecrulehelp = None
        self.setUiInit()
        self.helptext = self.treeManipulate.main.specrulehelp
        #build empty model for data and the selection
        self.specrulemodel = SpecRuleStandardItemModel(self.tvspecruleview, self)
        self.specrulemodel.setHorizontalHeaderLabels(["Node", "uid", "Condition", "result", "comment"])
        self.specruleselectionmodel = QItemSelectionModel(self.specrulemodel)
        #set model to tableview
        self.tvspecruleview.setModel(self.specrulemodel)
        self.tvspecruleview.setSelectionModel(self.specruleselectionmodel)
        #signals
        self.bspecrulehelp.clicked.connect(self.help)
        self.specrulemodel.itemChanged.connect(self.changeSpecRule)
        self.treeManipulate.treeModel.nameChangedSignal.connect(self.changeSpecRuleNodeName)
        #resize
        self.resz()
        #variables
        self.changeOnce = True
        self.validateOnce = True

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst1[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst1[1]
        if self.tabnumber == 1:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst2[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst2[1]
        if self.tabnumber == 2:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst3[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst3[1]
        if self.tabnumber == 3:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst4[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst4[1]
        if self.tabnumber == 4:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst5[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst5[1]
        if self.tabnumber == 5:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst6[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst6[1]
        if self.tabnumber == 6:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst7[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst7[1]
        if self.tabnumber == 7:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst8[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst8[1]
        if self.tabnumber == 8:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst9[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst9[1]
        if self.tabnumber == 9:
            self.tvspecruleview = self.treeManipulate.main.specrulefieldst10[0]
            self.bspecrulehelp = self.treeManipulate.main.specrulefieldst10[1]

    def setSesVarsFunsInSpecrules(self):
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

    """read"""
    def readSpecRuleList(self, lst):
        #get the children
        currentnodechildren = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex()).childrenlist()
        #if child is already in lst
        for child in currentnodechildren:
            inList = False
            for l in lst:
                if child.getUid() == int(l[1]):
                    inList = True
                    itemnme = QStandardItem(child.name())
                    itemuid = QStandardItem(str(child.getUid()))
                    itemcon = QStandardItem(l[2])
                    itemres = QStandardItem(l[3])
                    itemcom = QStandardItem(l[4])
                    self.specrulemodel.appendRow([itemnme, itemuid, itemcon, itemres, itemcom])
                    break
            #if the node is not in the list, add it to the list
            if not inList:
                itemnme = QStandardItem(child.name())
                itemuid = QStandardItem(str(child.getUid()))
                itemcon = QStandardItem("")
                itemres = QStandardItem("")
                itemcom = QStandardItem("")
                self.specrulemodel.appendRow([itemnme, itemuid, itemcon, itemres, itemcom])
        #creating the tree from save -> there are no children at the time of inserting the specnode
        if currentnodechildren == []:
            for l in lst:
                itemnme = QStandardItem(l[0])
                itemuid = QStandardItem(l[1])
                itemcon = QStandardItem(l[2])
                itemres = QStandardItem(l[3])
                itemcom = QStandardItem(l[4])
                self.specrulemodel.appendRow([itemnme, itemuid, itemcon, itemres, itemcom])

        #resize and validate
        self.resz()
        if (self.validateOnce):
            self.validateOnce = False
            self.validate()
            self.validateOnce = True

        #hide the uid column
        #self.tvspecruleview.setColumnHidden(1, True)

    """write -> the entries of the list in the changed node or only output the list of the node"""
    def writeSpecRuleList(self, index=None, isCurrentChanged=False, res="", forNodeUid=-1):
        if not self.treeManipulate.isRestoringTree:  # only, if it is not called due to a selection change during reading the tree from save
            specRuleList = []
            #shall the list for a special index be written or should the content of the model for the current node be given back
            if index == None:
                #the specrulelist in the current model is returned
                for row in range(self.specrulemodel.rowCount()):
                    indnme = self.specrulemodel.item(row, 0)
                    induid = self.specrulemodel.item(row, 1)
                    indcon = self.specrulemodel.item(row, 2)
                    indres = self.specrulemodel.item(row, 3)
                    indcom = self.specrulemodel.item(row, 4)
                    var = [indnme.data(QtCore.Qt.DisplayRole), induid.data(QtCore.Qt.DisplayRole), indcon.data(QtCore.Qt.DisplayRole), indres.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                    #specrules in the model
                    specRuleList.append(var)
                return specRuleList
            else:
                #the specrule for index shall be written
                node = self.treeManipulate.treeModel.getNode(index)
                nodeuid = node.getUid()
                #only continue if it is a specialization node
                if node.typeInfo() == "Spec Node":
                    #if the node that is changed is the current node, take the information from the current specrulemodel and write it in the node
                    if isCurrentChanged:
                        for row in range(self.specrulemodel.rowCount()):
                            indnme = self.specrulemodel.item(row, 0)
                            induid = self.specrulemodel.item(row, 1)
                            indcon = self.specrulemodel.item(row, 2)
                            indres = self.specrulemodel.item(row, 3)
                            indcom = self.specrulemodel.item(row, 4)
                            var = [indnme.data(QtCore.Qt.DisplayRole), induid.data(QtCore.Qt.DisplayRole), indcon.data(QtCore.Qt.DisplayRole), indres.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
                            specRuleList.append(var)
                        self.treeManipulate.treeModel.insertNodeSpecProp(index, specRuleList, "specrulelist", nodeuid)  # write into the node
                    #another node than the current node shall be changed
                    else:
                        #there are specrules for each child of the specnode so it is important which specrule for which child shall be written
                        for sp in node.specrule:
                            if forNodeUid != -1 and forNodeUid == int(sp[1]):   #if it is the specrule for which res was calculated
                                var = [sp[0], sp[1], sp[2], res, sp[4]]
                            else:
                                # for other specrules simply take what is currently in the specrule (just get the current name if possible)
                                specrulenode = self.treeManipulate.findNodeFromUid(int(sp[1]))
                                if specrulenode != None:
                                    var = [specrulenode.name(), sp[1], sp[2], sp[3], sp[4]]
                                else:
                                    var = [sp[0], sp[1], sp[2], sp[3], sp[4]]
                            specRuleList.append(var)
                        self.treeManipulate.treeModel.insertNodeSpecProp(index, specRuleList, "specrulelist", nodeuid)  # write into the node

    """resize"""
    """
    def resz(self):
        self.tvspecruleview.setColumnWidth(0, self.tvspecruleview.width() * 0.4)
        header = self.tvspecruleview.horizontalHeader()
        header.setStretchLastSection(True)
    """
    def resz(self):
        i = 0
        while i < 3:
            self.tvspecruleview.resizeColumnToContents(i)
            i += 1
        header = self.tvspecruleview.horizontalHeader()
        header.setStretchLastSection(True)

    """model changed via double click"""
    def changeSpecRule(self):
        if self.changeOnce:
            self.changeOnce = False
            index = self.tvspecruleview.currentIndex()
            if index.isValid():
                condic = self.specrulemodel.itemData(index)
                condition = condic[0]
                ccondition, cconditionb, resetc = self.checkReturnCondition(condition)
                if cconditionb: #set data
                    dict = {0 : ccondition}
                    self.specrulemodel.setItemData(index, dict)
                if resetc:
                    dict = {0 : ""}
                    self.specrulemodel.setItemData(index, dict)
            self.writeSpecRuleList(self.treeManipulate.treeSelectionModel.currentIndex(), True)
            self.resz()
            if self.validateOnce:
                self.validate()
            self.changeOnce = True

    """change the specrule when a node name was changed"""
    def changeSpecRuleNodeName(self):
        self.writeSpecRuleList(self.treeManipulate.treeSelectionModel.currentIndex().parent(), False)

    """check the value"""
    def checkReturnCondition(self, value):

        if value != "" and not value == "''" and not value == '""' and not value == '\n':
            value = value.strip()   #remove whitespaces before and after
            value = re.sub('\s+', ' ', value).strip()  # or: ' '.join(mystring.split())     #replace several whitespaces with one whitespace

            # check for duplicates of condition
            srlst = self.writeSpecRuleList()
            valueForCheck = value.replace(' ', '')  #for checking replace all whitespaces from the value to insert
            for i in range(len(srlst)):
                srlst[i][0] = srlst[i][0].replace(' ', '')
            timesFound = 0
            for i in range(len(srlst)):
                if srlst[i][2] == valueForCheck:
                    timesFound += 1
            if timesFound > 1:
                QMessageBox.information(None, "Changing not possible", "The specrule already exists. The condition field is emptied.", QtWidgets.QMessageBox.Ok)
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

    """check the content and evaluate the result"""
    def validate(self, sesvarl="", sesfunl="", nd=None, paths=None):

        # sub function
        def validateSpecRule(nd, svisr, sesfunl):

            specrulelist = nd.specrule

            #there can be several specrules (one for each child), so we have to put the results of this sub function into lists
            emptyl = []
            calculablel = []
            funVarFoundl = []
            retl = []
            rulel = []
            for rule in specrulelist:
                dataline = rule[2]

                # now try to interprete the specrule

                funVarFound = True

                #replace True and False by an expression -> it should be two connected expressions
                dataline = dataline.replace('False', '0==1')
                dataline = dataline.replace('True', '1==1')
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
                            ret = eval(expressions[k], globals(), svisr.__dict__)
                            # replace the name with the value
                            if isinstance(ret, str):
                                ret = '"' + ret + '"'
                            #expressions[k] = ret
                            expressionvarfunval.append([expressions[k], ret])
                        except:
                            pass

                        # check if the expression is an SES function
                        if isinstance(expressions[k], str) and "(" in expressions[k] and ")" in expressions[
                            k]:
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
                                        ret = eval(v, globals(), svisr.__dict__)
                                        # replace the name with the value
                                        varvalues.append(ret)
                                    except:
                                        varvalues.append("")

                            # now get the function from the sesFunctions and try to find a match with the entry
                            sesfunlcopy = [d[:] for d in sesfunl]  # make a copy of the list and the list elements
                            for sesfunvalue in sesfunlcopy:
                                if sesfunvalue[0] == funname[0]:
                                    # get the vars of the found function match since the parameters in the function definition do not have to match the SES variable names
                                    funvarsfound = re.findall('def\s+' + re.escape(funname[0]) + '\(.*\)',
                                                              sesfunvalue[1])
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

                # delete empty fields in the expressions
                # lenex = list(range(0,len(expressions)))    #not needed to create list
                for s in range(len(expressions)):
                    if expressions[s] == "":
                        del expressions[s]
                """
                # place ' again for strings
                lenex = range(len(expressions))
                toExamine = lenex[::2]
                for s in toExamine:
                    if type(expressions[s]) is str:
                        expressions[s] = expressions[s + 1][0] + expressions[s] + expressions[s + 1][0]
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

                emptyl.append(empty)
                calculablel.append(calculable)
                funVarFoundl.append(funVarFound)
                retl.append(ret)
                rulel.append(rule)

            return emptyl, calculablel, funVarFoundl, retl, rulel

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

        # own class for SES variables
        class sesvarsinspecrules:
            pass

        # create an instance of the SES variables class
        svisr = sesvarsinspecrules

        #was the process started for coloring the lines or for pruning?
        if sesvarl == "" and sesfunl == "" and nd == None:  # the validate process was started from the editor for coloring the lines
            # fill the instance of the sesvar class
            for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])   #interprete the type of the value
                except:
                    pass    #do nothing, it stays a string
                setattr(svisr, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svisr)

            #get the SES functions
            sesfunl = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()

            #go through all nodes
            indices = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())
            for ind in indices:
                #get the node
                nd = self.treeManipulate.treeModel.getNode(ind[0])
                #only continue if the node has specrules
                if nd.typeInfo() == "Spec Node":

                    emptyl, calculablel, funVarFoundl, retl, rulel = validateSpecRule(nd, svisr, sesfunl)

                    #check that only one specrule condition evaluates to true (xor) -> if not set all to false
                    failxor = False
                    numTrue = retl.count(True)  #for how many children the specrule is evaluated to True
                    if numTrue > 1:
                        failxor = True

                    #write evaluated result into the node
                    for i in range(len(emptyl)):
                        r = ""
                        if calculablel[i] and funVarFoundl[i]:
                            if retl[i] and not failxor:
                                r = "T"
                            elif retl[i] and failxor:
                                r = "T -> F"
                            else:
                                r = "F"

                        self.writeSpecRuleList(ind[0], False, r, int(rulel[i][1]))

                    #update the model
                    self.updateModel(ind[0])

        else:  # the validate process was started for pruning
            # fill the instance of the sesvar class
            for sesvarvalue in sesvarl:
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])   #interprete the type of the value
                except:
                    pass    #do nothing, it stays a string
                setattr(svisr, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svisr, nd, paths)

            #the SES functions are given in the pass list

            #only continue if the node has specrules (only for safety, this part of the function is called from the pruning function only for Spec nodes)
            if nd.typeInfo() == "Spec Node":

                emptyl, calculablel, funVarFoundl, retl, rulel = validateSpecRule(nd, svisr, sesfunl)

                #check that only one specrule condition evaluates to true (xor) -> if not set all to false
                failxor = False
                numTrue = retl.count(True)  #for how many children the specrule is evaluated to True
                if numTrue > 1:
                    failxor = True

                #return the evaluated results
                retvalues = []
                for i in range(len(emptyl)):
                    if calculablel[i] and funVarFoundl[i] and not failxor:
                        if retl[i] and not failxor:
                            retvalues.append("T")
                        elif retl[i] and failxor:
                            retvalues.append("T -> F")
                        else:
                            retvalues.append("F")
                    else:
                        retvalues.append("")

                return retvalues



    def updateModel(self, ind):
        #get the current specrules for the node
        spe = self.treeManipulate.treeModel.getNode(ind).specrule

        for row in range(self.specrulemodel.rowCount()):
            index0 = self.specrulemodel.index(row, 0)
            index1 = self.specrulemodel.index(row, 1)
            index2 = self.specrulemodel.index(row, 2)
            index3 = self.specrulemodel.index(row, 3)
            dict = {0: ""}

            #if the nodeuid for which the specrule is fits the nodeuid of the line
            modellineuid = int(index1.data(QtCore.Qt.DisplayRole))
            for sp in spe:
                if int(sp[1]) == modellineuid:
                    #there are specrules for each child of the specnode
                    if sp[2] == "":
                        #no specrule specified -> get the alternating colors
                        if row % 2 == 0:
                            color0 = QtGui.QColor(QtCore.Qt.white)
                            color2 = color0
                        else:
                            color0 = QtGui.QColor(239, 240, 241, 255)
                            color2 = color0
                    elif sp[2] != "" and sp[3] == "":
                        #the specified specrule can not be evaluated (e.g. it contains a SES variable which is not defined)
                        dict = {0: ""}
                        color2 = QtGui.QColor(255, 195, 195, 255)
                        color0 = QtGui.QColor(255, 195, 195, 255)
                    else:
                        #there is a result -> get the result and color the row
                        color2 = QtGui.QColor(195, 255, 195, 255)
                        if sp[3] == "T":
                            dict = {0: "T"}
                            color0 = QtGui.QColor(195, 255, 195, 255)
                        elif sp[3] == "F":
                            dict = {0: "F"}
                            color0 = QtGui.QColor(255, 195, 195, 255)
                        elif sp[3] == "T -> F":
                            dict = {0: "T -> F"}
                            color0 = QtGui.QColor(255, 195, 195, 255)

                    self.specrulemodel.setItemData(index3, dict)
                    self.specrulemodel.setData(index0, color0, QtCore.Qt.BackgroundColorRole)
                    self.specrulemodel.setData(index1, color0, QtCore.Qt.BackgroundColorRole)
                    self.specrulemodel.setData(index2, color2, QtCore.Qt.BackgroundColorRole)
                    self.specrulemodel.setData(index3, color0, QtCore.Qt.BackgroundColorRole)

    """empty the model"""
    def emptySpecruleModel(self):
        self.specrulemodel.clear()
        self.specrulemodel.setHorizontalHeaderLabels(["Node", "uid", "Condition", "result", "comment"])

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