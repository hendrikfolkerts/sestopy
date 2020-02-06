# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QItemSelectionModel, Qt

import ast
import re
import keyword

#redefine functions from QStandarditemmodel
class AttribStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super(AttribStandardItemModel, self).__init__(parent)

    #the second column is not editable, underscore attributes are not editable at all
    def flags(self, index):
        #get the name (column 0)
        it = self.item(index.row(), 0)
        itname = it.data(QtCore.Qt.DisplayRole)
        #now set the flags
        editflags = 0
        if not itname.startswith('_') and (index.column() == 0 or index.column() == 1 or index.column() == 3):
            editflags = QtCore.Qt.ItemIsEditable
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | editflags
        else:
            return QtCore.Qt.NoItemFlags

class Attributes():
    def __init__(self, treeManipulate, tabnumber):
        self.treeManipulate = treeManipulate
        self.tabnumber = tabnumber
        self.tvattributesview = None
        self.lenameattributes = None
        self.levalueattributes = None
        self.battributesinsert = None
        self.battributesdelete = None
        self.battributeshelp = None
        self.setUiInit()
        self.helptext = self.treeManipulate.main.attribhelp
        #build empty model for data and the selection
        self.attribmodel = AttribStandardItemModel(self.tvattributesview)
        self.attribmodel.setHorizontalHeaderLabels(["Name", "Value", "var/fun", "comment"])
        self.attribselectionmodel = QItemSelectionModel(self.attribmodel)
        #set model to tableview
        self.tvattributesview.setModel(self.attribmodel)
        self.tvattributesview.setSelectionModel(self.attribselectionmodel)
        #signals
        self.battributesinsert.clicked.connect(self.addAttrib)
        self.battributesdelete.clicked.connect(self.deleteAttrib)
        self.battributeshelp.clicked.connect(self.help)
        self.attribmodel.itemChanged.connect(self.changeAttrib)
        #resize
        self.resz()
        #variables
        self.changeOnce = True  #prevent the changeAttrib() function from being executed twice (the second time by the model change)
        self.validateOnce = True

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvattributesview = self.treeManipulate.main.attributefieldst1[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst1[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst1[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst1[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst1[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst1[5]
        if self.tabnumber == 1:
            self.tvattributesview = self.treeManipulate.main.attributefieldst2[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst2[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst2[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst2[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst2[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst2[5]
        if self.tabnumber == 2:
            self.tvattributesview = self.treeManipulate.main.attributefieldst3[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst3[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst3[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst3[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst3[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst3[5]
        if self.tabnumber == 3:
            self.tvattributesview = self.treeManipulate.main.attributefieldst4[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst4[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst4[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst4[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst4[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst4[5]
        if self.tabnumber == 4:
            self.tvattributesview = self.treeManipulate.main.attributefieldst5[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst5[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst5[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst5[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst5[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst5[5]
        if self.tabnumber == 5:
            self.tvattributesview = self.treeManipulate.main.attributefieldst6[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst6[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst6[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst6[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst6[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst6[5]
        if self.tabnumber == 6:
            self.tvattributesview = self.treeManipulate.main.attributefieldst7[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst7[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst7[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst7[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst7[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst7[5]
        if self.tabnumber == 7:
            self.tvattributesview = self.treeManipulate.main.attributefieldst8[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst8[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst8[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst8[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst8[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst8[5]
        if self.tabnumber == 8:
            self.tvattributesview = self.treeManipulate.main.attributefieldst9[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst9[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst9[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst9[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst9[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst9[5]
        if self.tabnumber == 9:
            self.tvattributesview = self.treeManipulate.main.attributefieldst10[0]
            self.lenameattributes = self.treeManipulate.main.attributefieldst10[1]
            self.levalueattributes = self.treeManipulate.main.attributefieldst10[2]
            self.battributesinsert = self.treeManipulate.main.attributefieldst10[3]
            self.battributesdelete = self.treeManipulate.main.attributefieldst10[4]
            self.battributeshelp = self.treeManipulate.main.attributefieldst10[5]

    def setSesVarsFunsInAttributes(self):
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
    def readAttribList(self, lst):
        for row in range(len(lst)):
            itemnme = QStandardItem(lst[row][0])
            itemval = QStandardItem(lst[row][1])
            itemvarfun = QStandardItem(lst[row][2])
            itemcomment = QStandardItem(lst[row][3])
            self.attribmodel.appendRow([itemnme, itemval, itemvarfun, itemcomment])
        self.resz()
        if (self.validateOnce):
            self.validateOnce = False
            self.validate()
            self.validateOnce = True

    """write -> the entries of the list in the current node"""
    def writeAttribList(self):
        if not self.treeManipulate.isRestoringTree:  # only, if it is not called due to a selection change during reading the tree from save
            attribList = []
            # get current selected node
            nodeuid = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex()).getUid()
            for row in range(self.attribmodel.rowCount()):
                indnme = self.attribmodel.item(row, 0)
                indval = self.attribmodel.item(row, 1)
                indvarfun = self.attribmodel.item(row, 2)
                indcomment = self.attribmodel.item(row, 3)
                var = [indnme.data(QtCore.Qt.DisplayRole), indval.data(QtCore.Qt.DisplayRole), indvarfun.data(QtCore.Qt.DisplayRole), indcomment.data(QtCore.Qt.DisplayRole)]
                attribList.append(var)
            self.treeManipulate.treeModel.insertNodeSpecProp(self.treeManipulate.treeSelectionModel.currentIndex(), attribList, "attriblist", nodeuid)  # write into the node

    """resize"""
    """
    def resz(self):
        self.tvattributesview.setColumnWidth(0, self.tvattributesview.width()*0.4)
        header = self.tvattributesview.horizontalHeader()
        header.setStretchLastSection(True)
    """
    def resz(self):
        i = 0
        while i < 2:
            self.tvattributesview.resizeColumnToContents(i)
            i += 1
        header = self.tvattributesview.horizontalHeader()
        header.setStretchLastSection(True)

    """add an attribute to the model"""
    def addAttrib(self):
        name = self.lenameattributes.text()
        value = self.levalueattributes.text()
        cname, cnameb, deleten = self.checkReturnName(name, False)
        cvalue, cvalueb, deletev, varfun = self.checkReturnValue(value, False)
        if cnameb and cvalueb:
            itemnm = QStandardItem(cname)
            itemval = QStandardItem(str(cvalue))
            itemvarfun = QStandardItem(varfun)
            itemcomment = QStandardItem("")
            self.attribmodel.appendRow([itemnm, itemval, itemvarfun, itemcomment])
            self.lenameattributes.setText("")
            self.levalueattributes.setText("")
        self.writeAttribList()
        self.resz()
        self.validate()

    """model changed via double click"""
    def changeAttrib(self):
        if self.changeOnce:
            self.changeOnce = False
            index = self.tvattributesview.currentIndex()
            #cloumn 0 -> name
            if index.column() == 0:
                namedic = self.attribmodel.itemData(index)
                name = namedic[0]
                cname, cnameb, deleten = self.checkReturnName(name, True)
                if cnameb:  # set data
                    dict = {0: cname}
                    self.attribmodel.setItemData(index, dict)
                if deleten:  # remove row
                    self.deleteAttrib(self.attribselectionmodel.currentIndex().row(), True)
            #column 1 -> value
            elif index.column() == 1:
                valuedic = self.attribmodel.itemData(index)
                value = valuedic[0]
                cvalue, cvalueb, deletev, varfun = self.checkReturnValue(value, True)
                if cvalueb:  # set data
                    dict = {0: str(cvalue)}
                    self.attribmodel.setItemData(index, dict)
                    #set the value for the varfun column
                    index2 = self.attribmodel.index(index.row(), 2)
                    dict2 = {0: varfun}
                    self.attribmodel.setItemData(index2, dict2)
                if deletev:  # remove row
                    self.deleteAttrib(self.attribselectionmodel.currentIndex().row(), True)
            self.writeAttribList()
            self.resz()
            if self.validateOnce:
                self.validate()
            self.changeOnce = True

    """check the name"""
    def checkReturnName(self, name, edited):
        if name != "" and not name == "''" and not name == '""' and not name == '\n':
            name = name.strip() #remove whitespaces before and after

            # check for two words as name
            namesplit = name.split(" ")
            if not edited and len(namesplit) > 1:
                QMessageBox.information(None, "Inserting not possible", "The variable name contains spaces. Please remove them.", QtWidgets.QMessageBox.Ok)
                return("", False, False)
            elif edited and len(namesplit) > 1:
                QMessageBox.information(None, "Changing not possible", "The variable name contains spaces. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return("", False, True)

            # check for duplicates of variable name
            if not edited and len(self.attribmodel.findItems(name)) != 0:
                QMessageBox.information(None, "Inserting not possible", "The variable name already exists. Please enter another variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and len(self.attribmodel.findItems(self.attribmodel.item(self.attribselectionmodel.currentIndex().row(), 0).data(QtCore.Qt.DisplayRole))) > 1:
                QMessageBox.information(None, "Changing not possible", "The variable name already exists. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            # check that the variable name is no Python keyword
            if not edited and keyword.iskeyword(name):
                QMessageBox.information(None, "Inserting not possible", "The variable name denotes a Python keyword. Please enter another variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and keyword.iskeyword(name):
                QMessageBox.information(None, "Changing not possible", "The variable name denotes a Python keyword. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            # check that the variable name is not 'PARENT', 'CHILDREN' or 'NUMREP'
            if not edited and (name == 'PARENT' or name == 'CHILDREN' or name == 'NUMREP' or name == 'PATH'):
                QMessageBox.information(None, "Inserting not possible", "The variable name is 'PARENT', 'CHILDREN', 'NUMREP' or 'PATH'. Please enter another variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and (name == 'PARENT' or name == 'CHILDREN' or name == 'NUMREP' or name == 'PATH'):
                QMessageBox.information(None, "Changing not possible", "The variable name is 'PARENT', 'CHILDREN', 'NUMREP' or 'PATH'. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            #check if the variable name is in Python syntax
            attribregex = re.compile('^([a-z]|[A-Z])(\w+)?$')
            attribregexcorrect = attribregex.match(name)
            if not edited and attribregexcorrect is None:
                QMessageBox.information(None, "Inserting not possible", "Please enter correct Python syntax for the variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and attribregexcorrect is None:
                QMessageBox.information(None, "Changing not possible", "Please enter correct Python syntax for the variable name. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            return (name, True, False)

        else:   #empty name
            if not edited:
                QMessageBox.information(None, "The variable name is empty", "The variable name is empty. The variable can not be inserted.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            else:
                QMessageBox.information(None, "The variable name is empty", "The variable name is empty. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

    """check the value"""
    def checkReturnValue(self, value, edited):
        if value != "" and not value == "''" and not value == '""' and not value == '\n':
            value = value.strip()  # remove whitespaces before and after
            isString = False
            if (ord(value[0]) == 39 and ord(value[-1]) == 39) or (ord(value[0]) == 34 and ord(value[-1]) == 34):    #check ascii code: ord() for getting the number and chr() for getting the character again, unichr() for getting the unicode character
                isString = True
            try:
                if not isString:    #a string shall stay a string, try to interprete if not entered as string
                    value = ast.literal_eval(value)
                return (value, True, False, "")
            except:
                #the value is no Python value so it could be the name of an SES variable or function
                #check if it can be the syntax of an SES variable or function
                attribregex = re.compile('^([a-z]|[A-Z])(\w+)?(\(([\"\']?\w+[\"\']?)?(,\s*?[\"\']?\w+[\"\']?)*\))?$')
                attribregexcorrect = attribregex.match(value)
                if attribregexcorrect is not None and not isString:
                    return (value, True, False, "x")
                QMessageBox.information(None, "Inserting not possible",
                                        "Please enter a variable using Python syntax or the possible name of an SES variable or function. SES variables and functions may not be part of a list or other Python datatype.\n"
                                        "If edited the variable will be deleted.", QtWidgets.QMessageBox.Ok)
                if not edited:
                    return ("", False, False, "")
                else:
                    return ("", False, True, "")

        else:  # empty value
            if not edited:
                QMessageBox.information(None, "The variable value is empty",
                                        "The variable value is empty. The variable can not be inserted.",
                                        QtWidgets.QMessageBox.Ok)
                return ("", False, False, "")
            else:
                QMessageBox.information(None, "The variable value is empty",
                                        "The variable value is empty. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True, "")

    """delete"""
    def deleteAttrib(self, rw=-1, rowsdelete=False):
        selectedrows = self.attribselectionmodel.selectedRows()
        if len(selectedrows) == 0 and rw == -1:
            QMessageBox.information(None, "Deleting not possible", "Please select at least one attribute to delete.", QtWidgets.QMessageBox.Ok)
        elif len(selectedrows) > 0 and not rowsdelete:
            deleteListRows = []
            for rowind in selectedrows:
                deleteListRows.append(rowind.row())
            deleteListRows.sort(reverse=True)
            for row in deleteListRows:
                self.attribmodel.removeRow(row, QtCore.QModelIndex())
        elif rw != -1 and rowsdelete:
            self.attribmodel.removeRow(rw, QtCore.QModelIndex())
        self.writeAttribList()
        self.resz()

    """color the value field if an SES variable or SES function can be interpreted"""
    def validate(self, sesvarl="", sesfunl="", nd=None, paths=None):

        #sub function
        def validateAttr(nd, sviat, sesfunl):

            attrlist = nd.attributes

            #there can be several attributes, so we have to put the results of this sub function into lists
            attrlinel = []
            isVarFunl = []
            varFoundl = []
            funFoundl = []
            funVarFoundl = []
            resl = []
            for row in attrlist:
                data = row[1]
                datavarfun = row[2]

                attrline = row
                isVarFun = False
                varFound = False
                funFound = False
                funVarFound = True
                res = ""
                #check if it is an SES variable or function
                if datavarfun == "":
                    #if type(data) is str:  #it can only be a string
                    res = data
                elif datavarfun == "x":
                    isVarFun = True

                    # evaluate the SES variable
                    try:
                        res = eval(data, globals(), sviat.__dict__)
                        varFound = True
                    except:
                        pass

                    # check if the expression is an SES function
                    if isinstance(data, str) and "(" in data and ")" in data:
                        funname = data.split("(")
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
                                    ret = eval(v, globals(), sviat.__dict__)
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
                                            res = self.ret
                                        except:
                                            pass
                                except:
                                    pass

                #always return a string
                res = str(res)

                attrlinel.append(attrline)
                isVarFunl.append(isVarFun)
                varFoundl.append(varFound)
                funFoundl.append(funFound)
                funVarFoundl.append(funVarFound)
                resl.append(res)

            return attrlinel, isVarFunl, varFoundl, funFoundl, funVarFoundl, resl

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
        class sesvarsinattr:
            pass

        # create an instance of the SES variables class
        sviat = sesvarsinattr

        #was the process started for coloring the lines or for pruning?
        if sesvarl == "" and sesfunl == "" and nd == None:  # the validate process was started from the editor for coloring the lines
            # fill the instance of the sesvar class
            for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(sviat, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(sviat)

            #get the SES functions
            sesfunl = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()

            #go through all nodes
            indices = self.treeManipulate.listAllIndices(self.treeManipulate.treeSelectionModel.currentIndex())
            for ind in indices:
                #get the node
                nd = self.treeManipulate.treeModel.getNode(ind[0])
                #only continue if the node has attributes
                if nd.typeInfo() == "Entity Node":

                    attrlinel, isVarFunl, varFoundl, funFoundl, funVarFoundl, resl = validateAttr(nd, sviat, sesfunl)

                    #update the model
                    self.updateModel(attrlinel, isVarFunl, varFoundl, funFoundl, funVarFoundl)

        else:   # the validate process was started for pruning
            # fill the instance of the sesvar class
            for sesvarvalue in sesvarl:
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(sviat, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(sviat, nd, paths)

            #the SES functions are given in the pass list

            #only continue if the node has attributes
            if nd.typeInfo() == "Entity Node":

                attrlinel, isVarFunl, varFoundl, funFoundl, funVarFoundl, resl = validateAttr(nd, sviat, sesfunl)

                #return the evaluated results
                return resl



    def updateModel(self, attrlinel, isVarFunl, varFoundl, funFoundl, funVarFoundl):    #the information how to color the rows is not in the node (no True/False), so we have to pass the lists

        for row in range(self.attribmodel.rowCount()):
            index0 = self.attribmodel.index(row, 0)
            index1 = self.attribmodel.index(row, 1)
            index2 = self.attribmodel.index(row, 2)
            index3 = self.attribmodel.index(row, 3)

            #if the attribute the parameters were calculated for fits the attribute of the line
            attrname = index0.data(QtCore.Qt.DisplayRole)
            attrvalue = index1.data(QtCore.Qt.DisplayRole)
            attrvarfun = index2.data(QtCore.Qt.DisplayRole)
            attrcomment = index3.data(QtCore.Qt.DisplayRole)
            for i in range(len(attrlinel)):
                if attrlinel[i][0] == attrname and attrlinel[i][1] == attrvalue and attrlinel[i][2] == attrvarfun and attrlinel[i][3] == attrcomment:
                    if isVarFunl[i]:
                        #color the rows according to the found result
                        if varFoundl[i] or (funFoundl[i] and funVarFoundl[i]):
                            color1 = QtGui.QColor(195, 255, 195, 255)
                        else:
                            color1 = QtGui.QColor(255, 195, 195, 255)
                    else:
                        #get the alternating colors
                        if row % 2 == 0:
                            color1 = QtGui.QColor(QtCore.Qt.white)
                        else:
                            color1 = QtGui.QColor(239, 240, 241, 255)
                    self.attribmodel.setData(index1, color1, QtCore.Qt.BackgroundColorRole)
                    self.attribmodel.setData(index2, color1, QtCore.Qt.BackgroundColorRole)

    """empty the model"""
    def emptyAttribModel(self):
        self.attribmodel.clear()
        self.attribmodel.setHorizontalHeaderLabels(["Name", "Value", "var/fun", "comment"])

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

    #validate function where only the existence of the SES function and parameters is checked but not if it is interpretable
    """
    def validate(self):
        self.changeOnce = False
        for row in range(self.attribmodel.rowCount()):
            data = self.attribmodel.item(row, 1).data(QtCore.Qt.DisplayRole)
            datavarfun = self.attribmodel.item(row, 2).data(QtCore.Qt.DisplayRole)
            index1 = self.attribmodel.index(row, 1)
            index2 = self.attribmodel.index(row, 2)
            #if it is an SES variable or function
            if datavarfun == "x":
                varFound = False
                funFound = False
                parameterFound = []

                for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                    if data == sesvarvalue[0]:
                        varFound = True

                attribregex = re.compile('^([a-z]|[A-Z])(\w+)?(\(([\"\']?\w+[\"\']?)?(,\s*?[\"\']?\w+[\"\']?)*\))$')
                attribregexfun = attribregex.match(data)
                if attribregexfun is not None:
                    funsplit = data.split("(")
                    funsplit[1] = funsplit[1][0:len(funsplit[1])-1]
                    for sesfunvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList():
                        if funsplit[0] == sesfunvalue[0]:
                            funFound = True
                            #now interprete the parameters
                            parameters = funsplit[1].split(",")
                            for p in range(len(parameters)):
                                parameters[p] = parameters[p].strip()
                                if not parameters[p] == "":
                                    try:
                                        ast.literal_eval(parameters[p])
                                    except: #the parameter is maybe an SES variable
                                        found = False
                                        for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                                            if parameters[p] == sesvarvalue[0]:
                                                found = True
                                        if found:
                                            parameterFound.append(True)
                                        else:
                                            parameterFound.append(False)

                #color the rows according to the found result
                parameterFoundRes = all(parameterFound)

                if varFound or (funFound and parameterFoundRes):
                    color1 = QtGui.QColor(195, 255, 195, 255)
                else:
                    color1 = QtGui.QColor(255, 195, 195, 255)
            else:
                #get the alternating colors
                if row % 2 == 0:
                    color1 = QtGui.QColor(QtCore.Qt.white)
                else:
                    color1 = QtGui.QColor(239, 240, 241, 255)
            self.attribmodel.setData(index1, color1, QtCore.Qt.BackgroundColorRole)
            self.attribmodel.setData(index2, color1, QtCore.Qt.BackgroundColorRole)
        self.changeOnce = True
    """

    #functions when the syntax var() and fun() is used------------------------------------------------------------------

    """check the value -> old function: with var as keyword for SES Variable and fun as keyword for SES function"""
    """
    def checkReturnValue(self, value, edited):
        def checkQuotes(val):  # it must be an even number of quotes and one type of quotes may only be twice in the string since it defines the string
            quote = val.count("'")
            doublequote = val.count('"')
            if quote % 2 == 1 or doublequote % 2 == 1:  # if one number of quotetype is odd -> return False
                return False
            elif quote == 0 or doublequote == 0:  # one number of quotetype must be 0 (since the string delimiters are not counted)
                return True
            else:
                return False

        if value != "":
            value = value.strip()  # remove whitespaces before and after
            try:
                value = ast.literal_eval(value)

                sesvarfunkeyexists = False
                sesvarkeyfound = None
                sesfunkeyfound = None
                sesvarregex = re.compile('^var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)$')  # regular expression: var("abc") or var('abc'), not found: var("abc def") since SES variable names may not contain whitespaces
                sesfunregex = re.compile('^fun\([\"\']([a-z]|[A-Z])(\w+)?[\"\'](,\s?((\d+(\.\d+)?)|([\"\']var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)[\"\'])))*\)$')  # regular expression: fun("abc"[...]) or fun('abc'[...]) with [...] optional containing: , 4 or , "var("a")" with whitespace optional between , and text
                checkquotes = False

                if isinstance(value, str) and ("var(" in value or "fun(" in value):
                    sesvarfunkeyexists = True
                    sesvarkeyfound = sesvarregex.match(value)
                    sesfunkeyfound = sesfunregex.match(value)
                    checkquotes = checkQuotes(value)
                # if isinstance(value, list) and (("var(" in v for v in value) or ("fun(" in v for v in value)):   #does not perfectly function
                if isinstance(value, list):
                    for v in value:
                        if isinstance(v, str) and ("var(" in v or "fun(" in v):
                            sesvarfunkeyexists = True
                            sesvarkeyfound = sesvarregex.match(v)
                            sesfunkeyfound = sesfunregex.match(v)
                            checkquotes = checkQuotes(v)
                # if isinstance(value, tuple) and (("var(" in v for v in value) or ("fun(" in v for v in value)):  #does not perfectly function
                if isinstance(value, tuple):
                    for v in value:
                        if isinstance(v, str) and ("var(" in v or "fun(" in v):
                            sesvarfunkeyexists = True
                            sesvarkeyfound = sesvarregex.match(v)
                            sesfunkeyfound = sesfunregex.match(v)
                            checkquotes = checkQuotes(v)
                # if isinstance(value, dict) and (("var(" in v for v in list(value.values())) or ("fun(" in v for v in list(value.values()))): #does not perfectly function
                if isinstance(value, dict):
                    for v in list(value.values()):
                        if isinstance(v, str) and ("var(" in v or "fun(" in v):
                            sesvarfunkeyexists = True
                            sesvarkeyfound = sesvarregex.match(v)
                            sesfunkeyfound = sesfunregex.match(v)
                            checkquotes = checkQuotes(v)

                if not sesvarfunkeyexists:  # all correct Python values which do not contain the keywords fun( or var(
                    return (value, True, False)
                elif sesvarfunkeyexists and sesvarkeyfound is not None and checkquotes:  # value contains var( keyword in correct syntax
                    return (value, True, False)
                elif sesvarfunkeyexists and sesfunkeyfound is not None and checkquotes:  # value contains fun( keyword in correct syntax
                    return (value, True, False)
                elif sesvarfunkeyexists and (sesvarkeyfound is not None or sesfunkeyfound is not None) and not checkquotes:
                    QMessageBox.information(None, "Inserting not possible",
                                            "It seems you want to reference an SES variable or function. Please watch your quotes. "
                                            "If edited the variable will be deleted.", QtWidgets.QMessageBox.Ok)
                    if not edited:
                        return (value, False, False)
                    else:
                        return (value, False, True)
                elif sesvarfunkeyexists and sesvarkeyfound is None and sesfunkeyfound is None:  # value contains var( or fun( keywords not in correct syntax
                    QMessageBox.information(None, "Inserting not possible",
                                            "It seems you want to reference an SES variable or function.\n"
                                            "Please use the syntax\n\"var('sesvarname')\" or\n\"fun('sesfunname'[, 4.5])\" or\n\"fun('sesfunname'[, 'var('sesvarname')'])\" .\n"
                                            "The expression in square brackets is optional, do not type the square brackets. Use it if you want to pass parameters.\n"
                                            "sesvarname and sesfunname must be alphanumeric not beginning with a number.\n"
                                            "If edited the variable will be deleted.", QtWidgets.QMessageBox.Ok)
                    if not edited:
                        return (value, False, False)
                    else:
                        return (value, False, True)
                else:
                    return (value, False, False)  # if it is none of the above cases -> do nothing
            except:
                QMessageBox.information(None, "Inserting not possible",
                                        "Please enter a variable using Python syntax.\n"
                                        "If edited the variable will be deleted.", QtWidgets.QMessageBox.Ok)
                if not edited:
                    return ("", False, False)
                else:
                    return ("", False, True)

        else:  # empty value
            if not edited:
                QMessageBox.information(None, "The variable value is empty",
                                        "The variable value is empty. The variable can not be inserted.",
                                        QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            else:
                QMessageBox.information(None, "The variable value is empty",
                                        "The variable value is empty. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)
    """

    """color the value field if a var() or fun() can be interpreted -> old function: with var as keyword for SES Variable and fun as keyword for SES function"""
    """
    def validate(self):
        self.changeOnce = False
        for row in range(self.attribmodel.rowCount()):
            data = self.attribmodel.item(row, 1).data(QtCore.Qt.DisplayRole)
            #find all occurences of var
            matches = re.findall('var\([\"\']([a-z]|[A-Z])(\w+)?[\"\']\)', data)
            sesvarfound = []
            for ma in matches:
                #connect the tuple of each resulting group
                m = ma[0] + ma[1]
                #check if SES variable with this found name exists
                nameexists = False
                for sesvarvalue in self.sesVariables.outputSesVarList():
                    if m == sesvarvalue[0]:
                        nameexists = True
                        break
                sesvarfound.append(nameexists)
            #find all occurrences of fun
            matches = re.findall('fun\([\"\']([a-z]|[A-Z])(\w+)?[\"\'].*\)', data)
            sesfunfound = []
            for ma in matches:
                #connect the tuple of each resulting group
                m = ma[0] + ma[1]
                #check if SES function with this found name exists
                nameexists = False
                for sesfunvalue in self.sesFunctions.outputSesFunList():
                    if m == sesfunvalue[0]:
                        nameexists = True
                        break
                sesfunfound.append(nameexists)

            #color the rows according to the found result
            if not (not sesvarfound and not sesfunfound):   #if both lists are empty -> line does not contain fun(...) or var(...) -> do not color
                sesvarallfound = all(sesvarfound)
                sesfunallfound = all(sesfunfound)
                index1 = self.attribmodel.index(row, 1)
                if sesvarallfound and sesfunallfound:
                    color1 = QtGui.QColor(195, 255, 195, 255)
                else:
                    color1 = QtGui.QColor(255, 195, 195, 255)
                self.attribmodel.setData(index1, color1, QtCore.Qt.BackgroundColorRole)
        self.changeOnce = True
    """

    """new function: validate (commented function above)"""
    """
    def colorValueField(self):
        self.changeOnce = False
        for row in range(self.attribmodel.rowCount()):
            data = self.attribmodel.item(row, 1).data(QtCore.Qt.DisplayRole)
            index1 = self.attribmodel.index(row, 1)
            #color1 = QtGui.QColor(QtCore.Qt.white)
            if "var(" in data or "fun(" in data:
                color1 = QtGui.QColor(255, 255, 195, 255)
            else:
                #get the alternating colors
                if row % 2 == 0:
                    color1 = QtGui.QColor(QtCore.Qt.white)
                else:
                    color1 = QtGui.QColor(239, 240, 241, 255)
            self.attribmodel.setData(index1, color1, QtCore.Qt.BackgroundColorRole)
        self.changeOnce = True
    """