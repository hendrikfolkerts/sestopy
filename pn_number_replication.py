# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QItemSelectionModel, Qt

import re
import ast

class NumberReplication:
    def __init__(self, treeManipulate, tabnumber):
        self.treeManipulate = treeManipulate
        self.tabnumber = tabnumber
        self.levaluenumberofreplication = None
        self.levaluenumberofreplicationres = None
        self.bnumberofreplicationhelp = None
        self.setUiInit()
        self.helptext = self.treeManipulate.main.nrephelp
        #signals
        self.bnumberofreplicationhelp.clicked.connect(self.help)
        self.levaluenumberofreplication.textChanged.connect(self.setCheckValue)
        #self.treeManipulate.tbproperties.currentChanged.connect(self.getLastToolboxPage)
        self.treeManipulate.treeSelectionModel.currentChanged.connect(self.setCheckValueNodeChanged)  # the selection was changed so the selected node was changed
        self.treeManipulate.tbproperties.currentChanged.connect(self.setCheckValueNodeChanged)    #the toolbox is changed so the selected node was changed
        #variables
        #self.currentSelectedTbPage = -1
        #self.lastSelectedTbPage = -1

    def setUiInit(self):
        if self.tabnumber == 0:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst1[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst1[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst1[2]
        if self.tabnumber == 1:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst2[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst2[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst2[2]
        if self.tabnumber == 2:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst3[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst3[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst3[2]
        if self.tabnumber == 3:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst4[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst4[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst4[2]
        if self.tabnumber == 4:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst5[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst5[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst5[2]
        if self.tabnumber == 5:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst6[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst6[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst6[2]
        if self.tabnumber == 6:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst7[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst7[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst7[2]
        if self.tabnumber == 7:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst8[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst8[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst8[2]
        if self.tabnumber == 8:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst9[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst9[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst9[2]
        if self.tabnumber == 9:
            self.levaluenumberofreplication = self.treeManipulate.main.numberofreplicationfieldst10[0]
            self.levaluenumberofreplicationres = self.treeManipulate.main.numberofreplicationfieldst10[1]
            self.bnumberofreplicationhelp = self.treeManipulate.main.numberofreplicationfieldst10[2]

    def setSesVarsFunsInNrep(self):
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
    def readNumRep(self, value):
        self.levaluenumberofreplication.setText(value)
        self.validate()

    """write -> the entries in the current node"""
    def writeNumRep(self):
        if not self.treeManipulate.isRestoringTree:  # only, if it is not called due to a selection change during reading the tree from save
            node = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
            formernode = self.treeManipulate.treeModel.getNode(self.treeManipulate.lastSelectedIndex)
            if node.typeInfo() == "Maspect Node":
                self.treeManipulate.treeModel.insertNodeSpecProp(self.treeManipulate.treeSelectionModel.currentIndex(), self.levaluenumberofreplication.text(), "numrep", node.getUid())  # write into the node
            elif formernode.typeInfo() == "Maspect Node":
                self.treeManipulate.treeModel.insertNodeSpecProp(self.treeManipulate.lastSelectedIndex, self.levaluenumberofreplication.text(), "numrep", formernode.getUid())  # write into the node

    """get the last selected page of the toolbox"""
    #def getLastToolboxPage(self):
        #self.lastSelectedTbPage = self.currentSelectedTbPage
        #self.currentSelectedTbPage = self.treeManipulate.tbproperties.currentIndex()

    """call check and set the value on toolbox change"""
    def setCheckValueNodeChanged(self):
        self.setCheckValue("", True)

    """check and set the value"""
    def setCheckValue(self, abc, isNodeChange=False):

        value = self.levaluenumberofreplication.text()
        value = value.strip()

        if value != "":
            if not isNodeChange:
                try:
                    value = ast.literal_eval(value)
                    if isinstance(value, int):
                        if value > 0:
                            self.writeNumRep()
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
                        self.writeNumRep()
                        self.validate()
                        return
                    else:
                        pass
            if isNodeChange:# and self.lastSelectedTbPage == 3:
                ok = self.validate("", "", None, True)
                if not ok:
                    QMessageBox.information(None, "The number of replication value cannot be evaluated",
                                            "Please enter an integer >0 or if you want to reference an SES variable or function, use the syntax\n"
                                            "sesvarname or\nsesfunname(1[, 4.5]) or\nsesfunname(5[, sesvarname]).\n"
                                            "The expression in square brackets is optional, do not type the square brackets. Use it if you want to pass parameters.\n"
                                            "sesvarname and sesfunname must be alphanumeric not beginning with a number.", QtWidgets.QMessageBox.Ok)
        else:
            self.validate()

    """color the value field if an SES variable or SES function can be interpreted"""
    def validate(self, sesvarl="", sesfunl="", nd=None, needAllOkReturn=False, paths=None):

        #sub function
        def validateNumRep(nd, svipr, sesfunl):

            value = nd.number_replication

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

                    #evaluate the SES variable
                    try:
                        ret = eval(value, globals(), svinr.__dict__)
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
                                    ret = eval(v, globals(), svinr.__dict__)
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
        class sesvarsinnrep:
            pass

        #create an instance of the SES variables class and fill it
        svinr = sesvarsinnrep

        #was the process started for coloring the lines or for pruning
        if sesvarl == "" and sesfunl == "" and nd == None:     #the validate process was started from the editor for coloring the lines
            #fill the instance of the sesvar class
            for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  #interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(svinr, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svinr)

            #get the SES functions
            sesfunl = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()

            #get the current node
            currentIndex = self.treeManipulate.treeSelectionModel.currentIndex()
            currentNode = self.treeManipulate.treeModel.getNode(currentIndex)

            #only continue if the node has a num rep value
            if currentNode.typeInfo() == "Maspect Node":

                isInteger, varFound, funFound, funVarFound, varOk, funOk, allOk, retval = validateNumRep(currentNode, svinr, sesfunl)

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
                setattr(svinr, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svinr, nd, paths)

            #the SES functions are given in the pass list

            #only continue if the node has a numRep value
            if nd.typeInfo() == "Maspect Node":

                isInteger, varFound, funFound, funVarFound, varOk, funOk, allOk, retval = validateNumRep(nd, svinr, sesfunl)

                #return the evaluated result and whether the value is okay for pruning
                return retval, allOk


    def updateLine(self, isInteger, varFound, funFound, funVarFound, varOk, funOk, nd, retval):
        if self.levaluenumberofreplication.text() == "":
            #color red if no value is inserted
            self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
            self.levaluenumberofreplicationres.setText("")

        if nd.number_replication == self.levaluenumberofreplication.text():
            # color the rows according to the found result
            self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")
            if isInteger:  #color white
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")

            elif not isInteger and varFound and not varOk:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
            elif not isInteger and varFound and varOk:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(195, 255, 195); selection-background-color: rgb(0, 255, 255); }")

            elif not isInteger and funFound and not funOk:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
            elif not isInteger and funFound and funVarFound and funOk:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(195, 255, 195); selection-background-color: rgb(0, 255, 255); }")

            else:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")

            #set the return value field (retval should be a string (already given back as string from the validateNumRep function))
            self.levaluenumberofreplicationres.setText(retval)

            return True


    """help"""
    def help(self):
        msgBox = QMessageBox(self.treeManipulate.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("number of replication: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()


    #---------------old functions with var() and fun()------------------------------------------------------------------
    """check and set the value"""
    """
    def setCheckValue(self, abc, isToolboxChange=False):

        def checkQuotes(val):   #it must be an even number of quotes and one type of quotes may only be twice in the string since it defines the string
            quote = val.count("'")
            doublequote = val.count('"')
            if quote % 2 == 1 or doublequote % 2 == 1:  #if one number of quotetype is odd -> return False
                return False
            elif quote == 2 or doublequote == 2:        #one number of quotetype must be 2
                return True
            else:
                return False

        value = self.levaluenumberofreplication.text()
        value = value.strip()

        if value != "":
            sesvarregex = re.compile('^[\"\']var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)[\"\']$')  # regular expression: var("abc") or var('abc'), not found: var("abc def") since SES variable names may not contain whitespaces
            sesfunregex = re.compile('^[\"\']fun\([\"\']([a-z]|[A-Z])(\w+)?[\"\'](,\s?((\d+(\.\d+)?)|([\"\']var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)[\"\'])))*\)[\"\']$')  # regular expression: fun("abc"[...]) or fun('abc'[...]) with [...] optional containing: , 4 or , "var("a")" with whitespace optional between , and text
            sesvarkeyfound = sesvarregex.match(value)
            sesfunkeyfound = sesfunregex.match(value)

            if value.isdigit():
                valint = int(value)
                strvalint = str(valint)
                if valint > 0 and strvalint == value:   #strvalint == value: check if it is an integer
                    self.writeNumRep()
            elif (sesvarkeyfound is not None or sesfunkeyfound is not None) and checkQuotes(value):
                self.writeNumRep()
            elif isToolboxChange and self.lastSelectedTbPage == 3:    #toolbox is changed but the value can not be inserted -> error
                QMessageBox.information(None, "Changing not possible",
                                        "Please enter an integer or if you want to reference an SES variable or function, use the syntax\n"
                                        "\"var('sesvarname')\" or\n\"fun('sesfunname'[, 4.5])\" or\n\"fun('sesfunname'[, 'var('sesvarname')'])\" .\n"
                                        "The expression in square brackets is optional, do not type the square brackets. Use it if you want to pass parameters.\n"
                                        "sesvarname and sesfunname must be alphanumeric not beginning with a number. The \" and \' can be commuted.\n"
                                        "The value is not changed.", QtWidgets.QMessageBox.Ok)
        self.validate()
    """

    """color the value field if a var() or fun() can be interpreted"""
    """
    def validate(self):
        value = self.levaluenumberofreplication.text()
        #find all occurences of var
        matches = re.findall('[\"\']var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)[\"\']', value)
        sesvarfound = []
        for ma in matches:
            # connect the tuple of each resulting group
            m = ma[0] + ma[1]
            # check if SES variable with this found name exists
            nameexists = False
            for sesvarvalue in self.sesVariables.outputSesVarList():
                if m == sesvarvalue[0]:
                    nameexists = True
                    break
            sesvarfound.append(nameexists)
        #find all occurrences of fun
        matches = re.findall('[\"\']fun\([\"\']([a-z]|[A-Z])(\w+)?[\"\'](,\s?((\d+(\.\d+)?)|([\"\']var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)[\"\'])))*\)[\"\']', value)
        sesfunfound = []
        for ma in matches:
            # connect the tuple of each resulting group
            m = ma[0] + ma[1]
            # check if SES variable with this found name exists
            nameexists = False
            for sesfunvalue in self.sesFunctions.outputSesFunList():
                if m == sesfunvalue[0]:
                    nameexists = True
                    break
            sesfunfound.append(nameexists)

        # color the rows according to the found result
        self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")
        if not (not sesvarfound and not sesfunfound):  # if both lists are empty -> line does not contain fun(...) or var(...) -> do not color
            sesvarallfound = all(sesvarfound)
            sesfunallfound = all(sesfunfound)
            if sesvarallfound and sesfunallfound:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(195, 255, 195); selection-background-color: rgb(0, 255, 255); }")
            else:
                self.levaluenumberofreplication.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
    """