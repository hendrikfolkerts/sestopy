# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import keyword

class SesFunctions(QtCore.QObject):

    sesfunChangedSignal = pyqtSignal()

    def __init__(self, main, tabnumber):

        #since we inherited from QObject, we have to call the super class init
        super(SesFunctions, self).__init__()

        self.main = main
        self.tabnumber = tabnumber
        self.tvsesfunctionsview = None
        self.bsesfunctioninsert = None
        self.bsesfunctiondelete = None
        self.bsesfunctionhelp = None
        self.setUiInit()
        self.helptext = self.main.sesfunhelp
        #build empty model for data and the selection
        self.sesfunmodel = QStandardItemModel(self.tvsesfunctionsview)
        self.sesfunmodel.setHorizontalHeaderLabels(["name", "SES function"])
        self.sesfunselectionmodel = QItemSelectionModel(self.sesfunmodel)
        #set model to tableview
        self.tvsesfunctionsview.setModel(self.sesfunmodel)
        self.tvsesfunctionsview.setSelectionModel(self.sesfunselectionmodel)
        #signals
        self.bsesfunctioninsert.clicked.connect(self.insertSesFun)
        self.bsesfunctiondelete.clicked.connect(self.deleteSesFun)
        self.bsesfunctionhelp.clicked.connect(self.help)
        #resize
        self.resz()

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt1
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt1
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet1
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt1
        if self.tabnumber == 1:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt2
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt2
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet2
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt2
        if self.tabnumber == 2:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt3
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt3
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet3
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt3
        if self.tabnumber == 3:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt4
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt4
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet4
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt4
        if self.tabnumber == 4:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt5
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt5
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet5
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt5
        if self.tabnumber == 5:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt6
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt6
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet6
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt6
        if self.tabnumber == 6:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt7
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt7
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet7
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt7
        if self.tabnumber == 7:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt8
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt8
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet8
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt8
        if self.tabnumber == 8:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt9
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt9
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet9
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt9
        if self.tabnumber == 9:
            self.tvsesfunctionsview = self.main.tvsesfunctionsviewt10
            self.bsesfunctioninsert = self.main.bsesfunctioninsertt10
            self.bsesfunctiondelete = self.main.bsesfunctiondeletet10
            self.bsesfunctionhelp = self.main.bsesfunctionhelpt10

    """restore from save"""
    def fromSave(self, sf, subSES=False):
        if not subSES:
            for row in range(len(sf)):
                itemnme = QStandardItem(sf[row][0])
                itemval = QStandardItem(sf[row][1])
                self.sesfunmodel.appendRow([itemnme, itemval])
        else:
            funli = self.outputSesFunList()
            for row in range(len(sf)):
                if [sf[row][0], sf[row][1]] in funli:  # the same exists
                    pass
                else:
                    if funli:
                        funlinames = []
                        for f in funli:
                            funlinames.append(f[0])
                        if sf[row][0] in funlinames:
                            QMessageBox.information(None, "Can not insert an SES function", "Can not insert the SES function \"" + sf[row][0] + "\". It exists with a different function. Please check your sub SES.", QtWidgets.QMessageBox.Ok)
                        else:
                            itemnme = QStandardItem(sf[row][0])
                            itemval = QStandardItem(sf[row][1])
                            self.sesfunmodel.appendRow([itemnme, itemval])
                    else:
                        itemnme = QStandardItem(sf[row][0])
                        itemval = QStandardItem(sf[row][1])
                        self.sesfunmodel.appendRow([itemnme, itemval])
        self.resz()

    """output"""
    def outputSesFunList(self):
        sesFunList = []
        for row in range(self.sesfunmodel.rowCount()):
            indnme = self.sesfunmodel.item(row, 0)
            indval = self.sesfunmodel.item(row, 1)
            var = [indnme.data(QtCore.Qt.DisplayRole), indval.data(QtCore.Qt.DisplayRole)]
            sesFunList.append(var)
        return sesFunList

    """resize"""
    def resz(self):
        i = 0
        while i < 2:
            self.tvsesfunctionsview.resizeColumnToContents(i)
            i += 1

    """insert py file"""
    def insertSesFun(self):
        dateiname = QFileDialog.getOpenFileName(None, "Open SES function (Python py-file)", '', "Python py-file (*.py);;Alle files (*)")
        if not dateiname:
            return
        try:
            convok, fconv = self.check(str(dateiname[0]))   #if everything is okay return array with filename and data
            if convok:
                self.addSesFun(fconv)
            elif not convok and fconv == 3:
                QMessageBox.warning(None, "Error importing SES function", "The function contains os.system. Please remove it.", QtWidgets.QMessageBox.Ok)
            elif not convok and fconv == 0:
                QMessageBox.warning(None, "Error importing SES function", "The name could not be found or the name is 'PARENT', 'CHILDREN', 'NUMREP' or 'PATH'.", QtWidgets.QMessageBox.Ok)
            elif not convok and fconv == 1:
                QMessageBox.warning(None, "Error importing SES function", "The function is not executable. Please check the syntax.", QtWidgets.QMessageBox.Ok)
            elif not convok and fconv == 2:
                QMessageBox.warning(None, "Error importing SES function", "Neither the name was found nor is the function executable or the name is 'PARENT', 'CHILDREN', 'NUMREP' or 'PATH'. Please check the syntax.", QtWidgets.QMessageBox.Ok)
        except:
            QMessageBox.warning(None, "Can not read file", "Error reading \"%s\". Are you sure this is a Python py-file containing an SES function?" % str(dateiname[0]), QtWidgets.QMessageBox.Ok)
            return

    """add a ses function"""
    def addSesFun(self, fconv):
        # check for duplicates of function name, the function name may not be in the SES variables and the function name may not be a Python keyword
        if len(self.sesfunmodel.findItems(fconv[0], Qt.MatchExactly)) == 0 and len(self.main.modellist[self.main.activeTab][1].sesvarmodel.findItems(fconv[0])) == 0 and not keyword.iskeyword(fconv[0]):
            itemnm = QStandardItem(fconv[0])
            itemval = QStandardItem(fconv[1])
            self.sesfunmodel.appendRow([itemnm, itemval])
        else:
            QMessageBox.information(None, "Inserting not possible", "The function name exists already, is a name of an SES variable or denotes a Python keyword.", QtWidgets.QMessageBox.Ok)
        self.resz()
        self.sesfunChangedSignal.emit()

    """checks if ses function has correct syntax"""
    def check(self, fname):
        with open(fname, 'r') as f:
            fundata = f.read()
        lines = fundata.split("\n")
        i = 0
        for l in lines:
            lines[i] = l.strip()
            i += 1
        #all lines are stripped now
        namefound = False
        funname = ""
        funexecutable = True
        funallowed = True

        for l in lines:
            if l == "": #ignore empty lines
                pass
            elif l[0] == "#":   #ignore commented lines
                pass
            elif "def " in l and "(" in l and ")" in l:
                wordlist = l.split("(")
                wordlist = wordlist[0].split()
                funname = wordlist[1]
                if funname != "" and funname != 'PARENT' and funname != 'CHILDREN' and funname != 'NUMREP' and funname != 'PATH':
                    namefound = True
        if not ("os.system" in fundata or "__import__('os').system" in fundata or '__import__("os").system' in fundata):
            try:
                exec(fundata)
            except:
                funexecutable = False
        else:
            funallowed = False

        #return value
        if namefound and funexecutable and funallowed:
            return (True, [funname, fundata])
        elif not funallowed:
            return (False, 3)
        elif not namefound and funexecutable:
            return (False, 0)
        elif namefound and not funexecutable:
            return (False, 1)
        elif not namefound and not funexecutable:
            return (False, 2)

    """delete"""
    def deleteSesFun(self, selectall = False):
        if not selectall:
            selectedrows = self.sesfunselectionmodel.selectedRows()
        else:
            selectedrows = []
            for row in range(self.sesfunmodel.rowCount()):
                selectedrows.append(self.sesfunmodel.index(row, 0))
        if len(selectedrows) == 0 and not selectall:
            QMessageBox.information(None, "Deleting not possible", "Please select at least one SES function to delete.", QtWidgets.QMessageBox.Ok)
        else:
            deleteListRows = []
            for rowind in selectedrows:
                deleteListRows.append(rowind.row())
            deleteListRows.sort(reverse=True)
            for row in deleteListRows:
                self.sesfunmodel.removeRow(row, QtCore.QModelIndex())
        self.resz()
        self.sesfunChangedSignal.emit()

    """help"""
    def help(self):
        msgBox = QMessageBox(self.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("SES functions: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()
