# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *  #QItemSelectionModel

import ast
import re
import keyword

class SesVariables(QtCore.QObject):

    sesvarChangedSignal = pyqtSignal()

    def __init__(self, main, tabnumber):

        #since we inherited from QObject, we have to call the super class init
        super(SesVariables, self).__init__()

        self.main = main
        self.tabnumber = tabnumber
        self.tvsesvariableview = None
        self.lesesvariablename = None
        self.lesesvariablevalue = None
        self.bsesvariableinsert = None
        self.bsesvariabledelete = None
        self.bsesvariablehelp = None
        self.setUiInit()
        self.helptext = self.main.sesvarhelp
        #build empty model for data and the selection
        self.sesvarmodel = QStandardItemModel(self.tvsesvariableview)
        self.sesvarmodel.setHorizontalHeaderLabels(["Name", "Value", "Comment"])
        self.sesvarselectionmodel = QItemSelectionModel(self.sesvarmodel)
        #set model to tableview
        self.tvsesvariableview.setModel(self.sesvarmodel)
        self.tvsesvariableview.setSelectionModel(self.sesvarselectionmodel)
        #signals
        self.bsesvariableinsert.clicked.connect(self.addSesVariable)
        self.bsesvariabledelete.clicked.connect(self.deleteSesVariable)
        self.bsesvariablehelp.clicked.connect(self.help)
        self.sesvarmodel.itemChanged.connect(self.changeSesVariable)
        #resize
        self.resz()
        #variables
        self.changeOnce = True  #prevent the changeSesVariable() function from being executed twice (the second time by the model change)

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvsesvariableview = self.main.tvsesvariableviewt1
            self.lesesvariablename = self.main.lesesvariablenamet1
            self.lesesvariablevalue = self.main.lesesvariablevaluet1
            self.bsesvariableinsert = self.main.bsesvariableinsertt1
            self.bsesvariabledelete = self.main.bsesvariabledeletet1
            self.bsesvariablehelp = self.main.bsesvariablehelpt1
        elif self.tabnumber == 1:
            self.tvsesvariableview = self.main.tvsesvariableviewt2
            self.lesesvariablename = self.main.lesesvariablenamet2
            self.lesesvariablevalue = self.main.lesesvariablevaluet2
            self.bsesvariableinsert = self.main.bsesvariableinsertt2
            self.bsesvariabledelete = self.main.bsesvariabledeletet2
            self.bsesvariablehelp = self.main.bsesvariablehelpt2
        elif self.tabnumber == 2:
            self.tvsesvariableview = self.main.tvsesvariableviewt3
            self.lesesvariablename = self.main.lesesvariablenamet3
            self.lesesvariablevalue = self.main.lesesvariablevaluet3
            self.bsesvariableinsert = self.main.bsesvariableinsertt3
            self.bsesvariabledelete = self.main.bsesvariabledeletet3
            self.bsesvariablehelp = self.main.bsesvariablehelpt3
        elif self.tabnumber == 3:
            self.tvsesvariableview = self.main.tvsesvariableviewt4
            self.lesesvariablename = self.main.lesesvariablenamet4
            self.lesesvariablevalue = self.main.lesesvariablevaluet4
            self.bsesvariableinsert = self.main.bsesvariableinsertt4
            self.bsesvariabledelete = self.main.bsesvariabledeletet4
            self.bsesvariablehelp = self.main.bsesvariablehelpt4
        elif self.tabnumber == 4:
            self.tvsesvariableview = self.main.tvsesvariableviewt5
            self.lesesvariablename = self.main.lesesvariablenamet5
            self.lesesvariablevalue = self.main.lesesvariablevaluet5
            self.bsesvariableinsert = self.main.bsesvariableinsertt5
            self.bsesvariabledelete = self.main.bsesvariabledeletet5
            self.bsesvariablehelp = self.main.bsesvariablehelpt5
        elif self.tabnumber == 5:
            self.tvsesvariableview = self.main.tvsesvariableviewt6
            self.lesesvariablename = self.main.lesesvariablenamet6
            self.lesesvariablevalue = self.main.lesesvariablevaluet6
            self.bsesvariableinsert = self.main.bsesvariableinsertt6
            self.bsesvariabledelete = self.main.bsesvariabledeletet6
            self.bsesvariablehelp = self.main.bsesvariablehelpt6
        elif self.tabnumber == 6:
            self.tvsesvariableview = self.main.tvsesvariableviewt7
            self.lesesvariablename = self.main.lesesvariablenamet7
            self.lesesvariablevalue = self.main.lesesvariablevaluet7
            self.bsesvariableinsert = self.main.bsesvariableinsertt7
            self.bsesvariabledelete = self.main.bsesvariabledeletet7
            self.bsesvariablehelp = self.main.bsesvariablehelpt7
        elif self.tabnumber == 7:
            self.tvsesvariableview = self.main.tvsesvariableviewt8
            self.lesesvariablename = self.main.lesesvariablenamet8
            self.lesesvariablevalue = self.main.lesesvariablevaluet8
            self.bsesvariableinsert = self.main.bsesvariableinsertt8
            self.bsesvariabledelete = self.main.bsesvariabledeletet8
            self.bsesvariablehelp = self.main.bsesvariablehelpt8#
        elif self.tabnumber == 8:
            self.tvsesvariableview = self.main.tvsesvariableviewt9
            self.lesesvariablename = self.main.lesesvariablenamet9
            self.lesesvariablevalue = self.main.lesesvariablevaluet9
            self.bsesvariableinsert = self.main.bsesvariableinsertt9
            self.bsesvariabledelete = self.main.bsesvariabledeletet9
            self.bsesvariablehelp = self.main.bsesvariablehelpt9
        elif self.tabnumber == 9:
            self.tvsesvariableview = self.main.tvsesvariableviewt10
            self.lesesvariablename = self.main.lesesvariablenamet10
            self.lesesvariablevalue = self.main.lesesvariablevaluet10
            self.bsesvariableinsert = self.main.bsesvariableinsertt10
            self.bsesvariabledelete = self.main.bsesvariabledeletet10
            self.bsesvariablehelp = self.main.bsesvariablehelpt10

    """restore from save"""
    def fromSave(self, sv, subSES=False):
        if not subSES:
            for row in range(len(sv)):
                itemnme = QStandardItem(sv[row][0])
                itemval = QStandardItem(sv[row][1])
                itemcom = QStandardItem(sv[row][2])
                self.sesvarmodel.appendRow([itemnme, itemval, itemcom])
        else:
            varli = self.outputSesVarList()
            for row in range(len(sv)):
                if [sv[row][0], sv[row][1]] in varli:   #the same exists
                    pass
                else:
                    if varli:
                        varlinames = []
                        for v in varli:
                            varlinames.append(v[0])
                        if sv[row][0] in varlinames:
                            QMessageBox.information(None, "Can not insert an SES variable", "Can not insert the SES variable \""+ sv[row][0] +"\". It exists with a different value. Please check your semantic conditions and sub SES.", QtWidgets.QMessageBox.Ok)
                        else:
                            itemnme = QStandardItem(sv[row][0])
                            itemval = QStandardItem(sv[row][1])
                            itemcom = QStandardItem(sv[row][2])
                            self.sesvarmodel.appendRow([itemnme, itemval, itemcom])

                    else:
                        itemnme = QStandardItem(sv[row][0])
                        itemval = QStandardItem(sv[row][1])
                        itemcom = QStandardItem(sv[row][2])
                        self.sesvarmodel.appendRow([itemnme, itemval, itemcom])
        self.resz()

    """output"""
    def outputSesVarList(self):
        sesVarList = []
        for row in range(self.sesvarmodel.rowCount()):
            indnme = self.sesvarmodel.item(row, 0)
            indval = self.sesvarmodel.item(row, 1)
            indcom = self.sesvarmodel.item(row, 2)
            var = [indnme.data(QtCore.Qt.DisplayRole), indval.data(QtCore.Qt.DisplayRole), indcom.data(QtCore.Qt.DisplayRole)]
            sesVarList.append(var)
        return sesVarList

    """resize"""
    """
    def resz(self):
        self.tvsesvariableview.setColumnWidth(0, self.tvsesvariableview.width()*0.4)
        header = self.tvsesvariableview.horizontalHeader()
        header.setStretchLastSection(True)
    """
    def resz(self):
        i = 0
        while i < 2:
            self.tvsesvariableview.resizeColumnToContents(i)
            i += 1
        header = self.tvsesvariableview.horizontalHeader()
        header.setStretchLastSection(True)

    """add an SES variable to the model"""
    def addSesVariable(self):
        name = self.lesesvariablename.text()
        value = self.lesesvariablevalue.text()
        cname, cnameb, deleten = self.checkReturnName(name, False)
        cvalue, cvalueb, deletev = self.checkReturnValue(value, False)
        if cnameb and cvalueb:
            itemnm = QStandardItem(cname)
            itemval = QStandardItem(str(cvalue))
            itemcom = QStandardItem("") #empty comment
            self.sesvarmodel.appendRow([itemnm, itemval, itemcom])
            self.lesesvariablename.setText("")
            self.lesesvariablevalue.setText("")
        self.resz()
        self.sesvarChangedSignal.emit()

    """model changed via double click"""
    def changeSesVariable(self):
        if self.changeOnce:
            self.changeOnce = False
            index = self.tvsesvariableview.currentIndex()
            #column 0 -> name
            if index.column() == 0:
                namedic = self.sesvarmodel.itemData(index)
                name = namedic[0]
                cname, cnameb, deleten = self.checkReturnName(name, True)
                if cnameb:  #set data
                    dict = {0 : cname}
                    self.sesvarmodel.setItemData(index, dict)
                if deleten:   #remove row
                    self.deleteSesVariable(self.sesvarselectionmodel.currentIndex().row(), True)
                    # other possibility to delete the variable
                    # its = self.sesvarmodel.findItems(name)
                    # rw = self.sesvarmodel.indexFromItem(its[0]).row()
                    # self.deleteSesVariable(rw)
            #column 1 -> value
            elif index.column() == 1:
                valuedic = self.sesvarmodel.itemData(index)
                value = valuedic[0]
                cvalue, cvalueb, deletev = self.checkReturnValue(value, True)
                if cvalueb: #set data
                    dict = {0 : str(cvalue)}
                    self.sesvarmodel.setItemData(index, dict)
                if deletev: #remove row
                    self.deleteSesVariable(self.sesvarselectionmodel.currentIndex().row(), True)
                    # other possibility to delete the variable
                    # its = self.sesvarmodel.findItems(value)
                    # rw = self.sesvarmodel.indexFromItem(its[0]).row()
                    # self.deleteSesVariable(rw)
            self.resz()
            self.sesvarChangedSignal.emit()
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
            if not edited and len(self.sesvarmodel.findItems(name, Qt.MatchExactly)) != 0:
                QMessageBox.information(None, "Inserting not possible", "The variable name already exists. Please enter another variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and len(self.sesvarmodel.findItems(self.sesvarmodel.item(self.sesvarselectionmodel.currentIndex().row(), 0).data(QtCore.Qt.DisplayRole), Qt.MatchExactly)) > 1:
                QMessageBox.information(None, "Changing not possible", "The variable name already exists. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            # check that in the SES function the name is not already defined
            if not edited and len(self.main.modellist[self.main.activeTab][2].sesfunmodel.findItems(name)) != 0:
                QMessageBox.information(None, "Inserting not possible", "The variable name already exists as name in the SES functions. Please enter another variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and len(self.main.modellist[self.main.activeTab][2].sesfunmodel.findItems(self.sesvarmodel.item(self.sesvarselectionmodel.currentIndex().row(), 0).data(QtCore.Qt.DisplayRole))) != 0:
                QMessageBox.information(None, "Changing not possible", "The variable name already exists as name in the SES functions. The variable is deleted.", QtWidgets.QMessageBox.Ok)
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
            sesvarregex = re.compile('^([a-z]|[A-Z])(\w+)?$')
            sesvarregexcorrect = sesvarregex.match(name)
            if not edited and sesvarregexcorrect is None:
                QMessageBox.information(None, "Inserting not possible", "Please enter correct Python syntax for the variable name.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and sesvarregexcorrect is None:
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
            value = value.strip()    #remove whitespaces before and after
            isString = False
            if (ord(value[0]) == 39 and ord(value[-1]) == 39) or (ord(value[0]) == 34 and ord(value[-1]) == 34):    #check ascii code: ord() for getting the number and chr() for getting the character again, unichr() for getting the unicode character
                isString = True
            try:
                if not isString:  # a string shall stay a string, try to interprete if not entered as string
                    value = ast.literal_eval(value)
                return (value, True, False)
            except:
                QMessageBox.information(None, "Inserting not possible",
                                        "Please enter a variable using Python syntax. "
                                        "If edited the variable will be deleted.", QtWidgets.QMessageBox.Ok)
                if not edited:
                    return ("", False, False)
                else:
                    return ("", False, True)

        else:  # empty value
            if not edited:
                QMessageBox.information(None, "The variable value is empty", "The variable value is empty. The variable can not be inserted.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            else:
                QMessageBox.information(None, "The variable value is empty", "The variable value is empty. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)


    """check the value - old function which does only allow some constructs"""
    """
    def checkReturnValue(self, value, edited):

        if value != "":
            value = value.strip()    #remove whitespaces before and after

            noInsert = False

            #if value.isdigit():    #no floats are recognized
                #return (value, True, False)

            v = re.compile(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
            if v.match(value) != None:
                value = "".join(value.split())  #remove whitespaces
                return (value, True, False)

            elif value[0] == "[" and value[-1] == "]":
                try:
                    value = ast.literal_eval(value) #interprete string as python expression
                    if isinstance(value, list):
                        #if all values in value are strings
                        if all(isinstance(v, str) for v in value):
                            #if values in value are strings, strip them
                            v = 0
                            while v < len(value):
                                value[v] = value[v].strip()
                                v += 1
                            return (value, True, False)
                        else:
                            for v in value:
                                try:
                                    float(str(v))
                                except ValueError:
                                    noInsert = True
                            if not noInsert:
                                return (value, True, False)
                    else:
                        noInsert = True
                except:
                    noInsert = True

            elif value[0] == "{" and value[-1] == "}":
                try:
                    value = ast.literal_eval(value) #interprete string as python expression
                    if isinstance(value, dict):
                        return (value, True, False)
                    else:
                        noInsert = True
                except:
                    noInsert = True

            elif len(value) >= 2 and value[0] == "'" and value[-1] == "'":
                if value.count("'") == 2:
                    return (value, True, False)
                else:
                    noInsert = True

            else:
                noInsert = True

            if noInsert:
                QMessageBox.information(None, "Inserting not possible", "Please enter a string beginning and ending with ' and containing no more ' but only \", "
                                                                        "a number (decimal sign is point), a list or a dictionary "
                                                                        "in Python syntax. The list may contain strings ' or numbers. "
                                                                        "If edited the variable will be deleted.", QtWidgets.QMessageBox.Ok)
                if not edited:
                    return ("", False, False)
                else:
                    return ("", False, True)

        else:  # empty value
            if not edited:
                QMessageBox.information(None, "The variable value is empty", "The variable value is empty. The variable can not be inserted.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            else:
                QMessageBox.information(None, "The variable value is empty", "The variable value is empty. The variable is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)
    """

    """delete"""
    def deleteSesVariable(self, rw=-1, rowsdelete=False, selectall=False):
        if not selectall:
            selectedrows = self.sesvarselectionmodel.selectedRows()
        else:
            selectedrows = []
            for row in range(self.sesvarmodel.rowCount()):
                selectedrows.append(self.sesvarmodel.index(row, 0))
        if len(selectedrows) == 0 and rw == -1 and not selectall:
            QMessageBox.information(None, "Deleting not possible", "Please select at least one SES variable to delete.", QtWidgets.QMessageBox.Ok)
        elif len(selectedrows) > 0 and not rowsdelete:
            deleteListRows = []
            for rowind in selectedrows:
                deleteListRows.append(rowind.row())
            deleteListRows.sort(reverse=True)
            for row in deleteListRows:
                self.sesvarmodel.removeRow(row, QtCore.QModelIndex())
        elif rw != -1 and rowsdelete:
            self.sesvarmodel.removeRow(rw, QtCore.QModelIndex())
        self.resz()
        self.sesvarChangedSignal.emit()

    """help"""
    def help(self):
        msgBox = QMessageBox(self.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("SES variables: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()