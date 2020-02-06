# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import re
import inspect
import ast

#redefine functions from QStandarditemmodel
class SemConStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super(SemConStandardItemModel, self).__init__(parent)

    def flags(self, index):
        editflags = 0
        if index.column() == 0:
            editflags = QtCore.Qt.ItemIsEditable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | editflags

        #return super(StandardItemModel, self).data(index, role)

class SemanticConditions(QtCore.QObject):

    semconChangedSignal = pyqtSignal()

    def __init__(self, main, tabnumber):

        # since we inherited from QObject, we have to call the super class init
        super(SemanticConditions, self).__init__()

        self.main = main
        self.tabnumber = tabnumber
        self.tbgeneralsettings = None
        self.tvsemanticconditionview = None
        self.lesemanticcondition = None
        self.bsemanticconditioninsert = None
        self.bsemanticconditiondelete = None
        self.bsemanticconditionhelp = None
        self.setUiInit()
        self.helptext = self.main.semconhelp
        #build empty model for data and the selection
        self.semcondmodel = SemConStandardItemModel(self.tvsemanticconditionview)
        self.semcondmodel.setHorizontalHeaderLabels(["Semantic Condition", "result"])
        self.semcondselectionmodel = QItemSelectionModel(self.semcondmodel)
        #set model to tableview
        self.tvsemanticconditionview.setModel(self.semcondmodel)
        self.tvsemanticconditionview.setSelectionModel(self.semcondselectionmodel)
        #signals
        self.bsemanticconditioninsert.clicked.connect(self.addSemCond)
        self.bsemanticconditiondelete.clicked.connect(self.deleteSemCond)
        self.bsemanticconditionhelp.clicked.connect(self.help)
        self.semcondmodel.itemChanged.connect(self.changeSemCond)
        #resize
        self.resz()
        #variables
        self.changeOnce = True

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tbgeneralsettings = self.main.tbgeneralsettingst1
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt1
            self.lesemanticcondition = self.main.lesemanticconditiont1
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt1
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet1
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt1
        if self.tabnumber == 1:
            self.tbgeneralsettings = self.main.tbgeneralsettingst2
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt2
            self.lesemanticcondition = self.main.lesemanticconditiont2
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt2
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet2
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt2
        if self.tabnumber == 2:
            self.tbgeneralsettings = self.main.tbgeneralsettingst3
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt3
            self.lesemanticcondition = self.main.lesemanticconditiont3
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt3
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet3
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt3
        if self.tabnumber == 3:
            self.tbgeneralsettings = self.main.tbgeneralsettingst4
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt4
            self.lesemanticcondition = self.main.lesemanticconditiont4
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt4
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet4
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt4
        if self.tabnumber == 4:
            self.tbgeneralsettings = self.main.tbgeneralsettingst5
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt5
            self.lesemanticcondition = self.main.lesemanticconditiont5
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt5
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet5
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt5
        if self.tabnumber == 5:
            self.tbgeneralsettings = self.main.tbgeneralsettingst6
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt6
            self.lesemanticcondition = self.main.lesemanticconditiont6
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt6
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet6
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt6
        if self.tabnumber == 6:
            self.tbgeneralsettings = self.main.tbgeneralsettingst7
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt7
            self.lesemanticcondition = self.main.lesemanticconditiont7
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt7
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet7
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt7
        if self.tabnumber == 7:
            self.tbgeneralsettings = self.main.tbgeneralsettingst8
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt8
            self.lesemanticcondition = self.main.lesemanticconditiont8
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt8
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet8
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt8
        if self.tabnumber == 8:
            self.tbgeneralsettings = self.main.tbgeneralsettingst9
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt9
            self.lesemanticcondition = self.main.lesemanticconditiont9
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt9
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet9
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt9
        if self.tabnumber == 9:
            self.tbgeneralsettings = self.main.tbgeneralsettingst10
            self.tvsemanticconditionview = self.main.tvsemanticconditionviewt10
            self.lesemanticcondition = self.main.lesemanticconditiont10
            self.bsemanticconditioninsert = self.main.bsemanticconditioninsertt10
            self.bsemanticconditiondelete = self.main.bsemanticconditiondeletet10
            self.bsemanticconditionhelp = self.main.bsemanticconditionhelpt10

    def setSesVarsInSemCond(self):
        if self.tabnumber == 0:
            self.sesVariablest1 = self.main.modellist[0][1]
            self.sesVariablest1.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest1.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 1:
            self.sesVariablest2 = self.main.modellist[1][1]
            self.sesVariablest2.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest2.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 2:
            self.sesVariablest3 = self.main.modellist[2][1]
            self.sesVariablest3.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest3.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 3:
            self.sesVariablest4 = self.main.modellist[3][1]
            self.sesVariablest4.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest4.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 4:
            self.sesVariablest5 = self.main.modellist[4][1]
            self.sesVariablest5.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest5.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 5:
            self.sesVariablest6 = self.main.modellist[5][1]
            self.sesVariablest6.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest6.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 6:
            self.sesVariablest7 = self.main.modellist[6][1]
            self.sesVariablest7.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest7.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 7:
            self.sesVariablest8 = self.main.modellist[7][1]
            self.sesVariablest8.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest8.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 8:
            self.sesVariablest9 = self.main.modellist[8][1]
            self.sesVariablest9.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest9.sesvarChangedSignal.connect(self.viewHint)
        if self.tabnumber == 9:
            self.sesVariablest10 = self.main.modellist[9][1]
            self.sesVariablest10.sesvarChangedSignal.connect(self.validate)
            self.sesVariablest10.sesvarChangedSignal.connect(self.viewHint)

    """restore from save"""
    def fromSave(self, sc, subSES=False):
        if not subSES:
            for row in range(len(sc)):
                itemsc = QStandardItem(sc[row][0])
                itemres = QStandardItem(sc[row][1])
                self.semcondmodel.appendRow([itemsc, itemres])
        else:
            secoli = self.outputSemCondList()
            for row in range(len(sc)):
                if [sc[row][0]] in secoli:  #the same exists
                    pass
                else:
                    itemsc = QStandardItem(sc[row][0])
                    itemres = QStandardItem(sc[row][1])
                    self.semcondmodel.appendRow([itemsc, itemres])
        self.resz()
        self.validate()

    """output"""
    def outputSemCondList(self):
        semCondList = []
        for row in range(self.semcondmodel.rowCount()):
            indsc = self.semcondmodel.item(row, 0)
            indres = self.semcondmodel.item(row, 1)
            var = [indsc.data(QtCore.Qt.DisplayRole), indres.data(QtCore.Qt.DisplayRole)]
            semCondList.append(var)
        return semCondList

    """resize"""
    """
    def resz(self):
        self.tvsemanticconditionview.setColumnWidth(0, self.tvsemanticconditionview.width() * 0.7)
        self.tvsemanticconditionview.setColumnWidth(1, self.tvsemanticconditionview.width() * 0.15)
        self.tvsemanticconditionview.setColumnWidth(2, self.tvsemanticconditionview.width() * 0.15)
        header = self.tvsemanticconditionview.horizontalHeader()
        header.setStretchLastSection(True)
    """
    def resz(self):
        i = 0
        while i < 3:
            self.tvsemanticconditionview.resizeColumnToContents(i)
            i += 1
        header = self.tvsemanticconditionview.horizontalHeader()
        header.setStretchLastSection(True)

    """add a semantic condition to the model"""
    def addSemCond(self):
        value = self.lesemanticcondition.text()
        cvalue, cvalueb, deletev = self.checkReturnValue(value, False)
        if cvalueb:
            itemsc = QStandardItem(cvalue)
            self.semcondmodel.appendRow([itemsc])
            self.lesemanticcondition.setText("")
        self.resz()
        self.validate()
        self.semconChangedSignal.emit()

    """model changed via double click"""
    def changeSemCond(self):
        if self.changeOnce:
            self.changeOnce = False
            index = self.tvsemanticconditionview.currentIndex()
            if index.isValid():
                valuedic = self.semcondmodel.itemData(index)
                value = valuedic[0]
                cvalue, cvalueb, deletev = self.checkReturnValue(value, True)
                if cvalueb: #set data
                    dict = {0 : cvalue}
                    self.semcondmodel.setItemData(index, dict)
                if deletev: #remove row
                    self.deleteSemCond(self.semcondselectionmodel.currentIndex().row(), True)
            self.resz()
            self.validate()
            self.semconChangedSignal.emit()
            self.changeOnce = True

    """check the value of a semantic condition -> can it be evaluated? Return it afterwards"""
    def checkReturnValue(self, value, edited):

        if value != "" and not value == "''" and not value == '""' and not value == '\n':
            value = value.strip()   #remove whitespaces before and after
            value = re.sub('\s+', ' ', value).strip()  # or: ' '.join(mystring.split())     #replace several whitespaces with one whitespace
            value = value.replace(' ==', '==')
            value = value.replace('== ', '==')
            value = value.replace(' !=', '!=')
            value = value.replace('!= ', '!=')

            # check for doing shit -> not needed an more since we use ast.literal_eval(...)
            """
            if not edited and ("os.system" in value or "__import__('os').system" in value or '__import__("os").system' in value):
                QMessageBox.information(None, "What did you try?", "Are you insane? Simply forget whatever you tried. Please enter an expression in Python syntax without importing the Python module os.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and ("os.system" in value or "__import__('os').system" in value or '__import__("os").system' in value):
                QMessageBox.information(None, "What did you try?", "Are you insane? Simply forget whatever you tried. The expression is deleted. Please enter an expression in Python syntax without importing the Python module os.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)
            """

            # check for duplicates of variable name
            sclst = self.outputSemCondList()
            valueForCheck = value.replace(' ', '')  #for checking replace all whitespaces from the value to insert
            for i in range(len(sclst)):
                sclst[i][0] = sclst[i][0].replace(' ', '')
            timesFound = 0
            for i in range(len(sclst)):
                if sclst[i][0] == valueForCheck:
                    timesFound += 1
            if not edited and timesFound != 0:
                QMessageBox.information(None, "Inserting not possible", "The semantic condition already exists.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            elif edited and timesFound > 1:
                QMessageBox.information(None, "Changing not possible", "The semantic condition already exists. It is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

            # if the variable is no duplicate the variable has to be checked
            ev = -1
            ok = True
            try:
                #ev = eval(value)       #unsafe
                ev = ast.literal_eval(value)
            except:
                if ev == -1:
                    lv = sys.exc_info()
                    # if hasattr(lv[1], 'msg') and lv[1].msg == 'invalid syntax':   #does not function -> not every syntax error has the attribute msg
                    if type(lv[1]) is SyntaxError:
                        ok = False
            if not edited:
                if not ok:
                    QMessageBox.information(None, "Inserting not possible", "Please enter a logical expression using Python syntax.", QtWidgets.QMessageBox.Ok)
                return (value, ok, False)
            if edited:
                if not ok:
                    QMessageBox.information(None, "Changing not possible", "Please enter a logical expression using Python syntax. The expression is deleted.", QtWidgets.QMessageBox.Ok)
                    return (value, ok, True)
                else:
                    return (value, ok, False)

        else:  # empty value
            if not edited:
                QMessageBox.information(None, "The variable value is empty", "The value is empty. The value can not be inserted.", QtWidgets.QMessageBox.Ok)
                return ("", False, False)
            else:
                QMessageBox.information(None, "The variable value is empty", "The value is empty. The value is deleted.", QtWidgets.QMessageBox.Ok)
                return ("", False, True)

    """delete a semantic condition"""
    def deleteSemCond(self, rw=-1, rowsdelete=False, selectall=False):
        if not selectall:
            selectedrows = self.semcondselectionmodel.selectedRows()
        else:
            selectedrows = []
            for row in range(self.semcondmodel.rowCount()):
                selectedrows.append(self.semcondmodel.index(row, 0))
        if len(selectedrows) == 0 and rw == -1 and not selectall:
            QMessageBox.information(None, "Deleting not possible", "Please select at least one semantic condition to delete.", QtWidgets.QMessageBox.Ok)
        elif len(selectedrows) > 0 and not rowsdelete:
            deleteListRows = []
            for rowind in selectedrows:
                deleteListRows.append(rowind.row())
            deleteListRows.sort(reverse=True)
            for row in deleteListRows:
                self.semcondmodel.removeRow(row, QtCore.QModelIndex())
        elif rw != -1 and rowsdelete:
            self.semcondmodel.removeRow(rw, QtCore.QModelIndex())
        self.resz()
        self.semconChangedSignal.emit()
        self.viewHint()

    """check the content and evaluate the result, sesvarl is "" and semconl is "" if the validate process was started from the editor"""
    def validate(self, sesvarl="", semconl=""):

        def execAsFun(data, svisc, ret, calculable):
            # maybe it can be interpreted as code -> replace all variables with their values
            # go through the svisc class variables
            datarep = data
            for var in svisc.__dict__:
                # var     #is the variable
                # svisc.__dict__[var]     #is the value of var
                if var[0] != "_":  # only if the var does not begin with underscore -> SES variables may not have a name beginning with underscore
                    datarep = re.sub('\\b' + re.escape(var) + '\\b', str(svisc.__dict__[var]), datarep)  # word boundary in Python regex -> \\b -> escape the \ with another \
            # all existing variables are replaced with the values now -> execute
            execute = "self.funretdata = " + datarep
            try:
                exec(execute)
                ret = self.funretdata
            except:
                calculable = False
            return ret, calculable

        # own class for SES variables
        class sesvarsinsemcons:
            pass

        # create an instance of the SES variables class
        svisc = sesvarsinsemcons

        #was the process started for coloring the lines or for pruning?
        if sesvarl == "" and semconl == "":   #the validate process was started from the editor for coloring the lines
            #fill the instance of the sesvar class
            for sesvarvalue in self.main.modellist[self.main.activeTab][1].outputSesVarList():
                # either
                #exec("%s = %s" % (sesvarvalue[0], sesvarvalue[1]))
                # better and much safer -> if you want to set the variables of an object
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])   #interprete the type of the value
                except:
                    pass    #do nothing, it stays a string
                setattr(svisc, sesvarvalue[0], sesvarvalue[1])  # if you want to add the variables to this class object: setattr(self, sesvarvalue[0], sesvarvalue[1]

            #get attributes of svisc -> not needed any more
            #attributes = [attr for attr in dir(svisc) if not callable(attr) and not attr.startswith("__")]
            #get attributes with values from svisc -> not needed any more
            #attributes = inspect.getmembers(svisc, lambda a: not (inspect.isroutine(a)))
            #attributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]

            #now try to interprete the semantic conditions
            for row in range(self.semcondmodel.rowCount()):

                data = self.semcondmodel.item(row, 0).data(QtCore.Qt.DisplayRole)

                #numbers to string -> not needed any more
                #number = re.search(r'\b\d+\b', data).group()
                #index = data.find(number)
                #data = data[:index]+'"'+data[index:(index+len(number))]+'"'+data[(index+len(number)):]

                #check
                calculable = True
                ret = None
                try:
                    #try to interprete it as expression
                    ret = eval(data, globals(), svisc.__dict__)
                except:
                    ret, calculable = execAsFun(data, svisc, ret, calculable)

                self.updateModel(data, ret, calculable)
                self.viewHint()

        else:   #the validate process was started for pruning
            # fill the instance of the sesvar class
            for sesvarvalue in sesvarl:
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])   #interprete the type of the value
                except:
                    pass    #do nothing, it stays a string
                setattr(svisc, sesvarvalue[0], sesvarvalue[1])  # if you want to add the variables to this class object: setattr(self, sesvarvalue[0], sesvarvalue[1]

            #now try to interprete the semantic conditions
            retvalues = []
            for semconvalue in semconl:

                data = semconvalue[0]

                #check
                calculable = True
                ret = None
                try:
                    ret = eval(data, globals(), svisc.__dict__)
                except:
                    ret, calculable = execAsFun(data, svisc, ret, calculable)

                if calculable and ret:
                    retvalues.append("T")
                else:
                    retvalues.append("F")

            return retvalues


    def updateModel(self, data, ret, calculable):
        for row in range(self.semcondmodel.rowCount()):
            #if it is the condition data and ret were evaluated for
            if data == self.semcondmodel.item(row, 0).data(QtCore.Qt.DisplayRole):
                #set the valid flag and the result flag
                index0 = self.semcondmodel.index(row, 0)
                index1 = self.semcondmodel.index(row, 1)
                if calculable:
                    color0 = QtGui.QColor(195, 255, 195, 255)
                    if ret == True:
                        dict = {0: "T"}
                        color1 = QtGui.QColor(195, 255, 195, 255)
                    else:
                        dict = {0: "F"}
                        color1 = QtGui.QColor(255, 195, 195, 255)
                else:
                    dict = {0: ""}
                    color0 = QtGui.QColor(255, 195, 195, 255)
                    color1 = QtGui.QColor(255, 195, 195, 255)
                self.semcondmodel.setItemData(index1, dict)
                self.semcondmodel.setData(index0, color0, QtCore.Qt.BackgroundColorRole)
                self.semcondmodel.setData(index1, color1, QtCore.Qt.BackgroundColorRole)

    def viewHint(self):
        sesvars =  self.main.modellist[self.main.activeTab][1].outputSesVarList()
        isOkay = True
        if len(sesvars) > 0:
            i = 0
            while isOkay and i < self.semcondmodel.rowCount():
                ite = self.semcondmodel.item(i, 1)
                if ite is not None and ite.data(QtCore.Qt.DisplayRole) == "F":
                    isOkay = False
                i += 1
        if isOkay:
            self.tbgeneralsettings.setItemIcon(2, self.main.okayIcon)
        else:
            self.tbgeneralsettings.setItemIcon(2, self.main.notOkayIcon)

    """help"""
    def help(self):
        msgBox = QMessageBox(self.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("semantic conditions: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()