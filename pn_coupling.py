# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QItemSelectionModel, Qt

import re
import ast

#redefine functions from QStandarditemmodel
class CouplingStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent):
        super(CouplingStandardItemModel, self).__init__(parent)

    #second, fifth and sixth row only changable (port names and commment)
    def flags(self, index):
        if index.column() == 2 or index.column() == 5 or index.column() == 6:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

class CouplingDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent):
        QtWidgets.QItemDelegate.__init__(self, parent)

    #createEditor method is called automatically, when the cell shall be edited
    def createEditor(self, parent, option, index):
        #the cell only gets a comboBox when it is edited
        #combo = QtWidgets.QComboBox(parent)
        #combo.addItems(["SignalPortReal", "SignalPortInt", "SignalPortBool", "PhysicalPort"])
        #return combo

        #the cell gets a widget of the class PortTypeWidget when it is edited
        tw = QtWidgets.QTableWidget(1, 1, parent)
        tw.horizontalHeader().hide()
        tw.verticalHeader().hide()
        tw.setCellWidget(0, 0, PortTypeWidget())
        return tw

    #setEditorData method is called automatically by the view, when an editor is initialized and when model data has been changed
    def setEditorData(self, editor, index):
        #editor.blockSignals(True)
        #editor.setCurrentIndex(int(index.model().data(index)))
        #editor.blockSignals(False)

        # get the widgets (which were created for the editor)
        ptw = editor.cellWidget(0, 0)
        hbox = ptw.layout()
        linee = hbox.itemAt(0).widget()  # the lineEdit with maybe chaged text
        combo = hbox.itemAt(1).widget()  # thecomboBox with maybe changed content
        # get the current data
        portandtype = index.data()
        # portandtype is None when the coupling port field has been left
        if portandtype:
            ptsplit = portandtype.split(" / ")
            try:
                #now set the content
                if len(ptsplit) == 2:
                    linee.setText(ptsplit[0])
                    #set the porttype to the right index
                    ptfound = False
                    porttypes = ["SPR", "SPI", "SPB", "PPEA", "PPMT"]
                    for n in range(len(porttypes)):
                        if porttypes[n] == ptsplit[1]:
                            combo.setCurrentIndex(n)
                            ptfound = True
                    if not ptfound:
                        combo.setCurrentIndex(0)
                else:   #maybe only a portname is given, but no porttype
                    linee.setText(ptsplit[0])
                    #set the porttype to the first in the list
                    combo.setCurrentIndex(0)
            except: #in case an error occurs -> set the porttype to the first in the list
                linee.setText(ptsplit[0])
                # set the porttype to the first in the list
                combo.setCurrentIndex(0)
        else:   #portandtype is None -> after leaving the coupling port field -> own function for that now (see next function)
            #portname = linee.text()
            #porttype = combo.currentIndex()
            #portnametype = portname + " / " + str(porttype)
            #currentRow = index.row()
            #currentColumn = index.column()
            pass

    #setModelData method is called automatically by the view, when the editor is left -> update the model after change
    def setModelData(self, editor, model, index):
        # model.setData(index, editor.itemText(editor.currentIndex()))

        # get the widgets (which were created for the editor)
        ptw = editor.cellWidget(0, 0)
        hbox = ptw.layout()
        linee = hbox.itemAt(0).widget()  # the lineEdit with maybe chaged text
        combo = hbox.itemAt(1).widget()  # thecomboBox with maybe changed content
        portname = linee.text()
        #porttypeComboNum = combo.currentIndex()    #number of the selected index in the comboBox
        porttype = combo.currentText()
        portnametype = portname + " / " + porttype
        model.setData(index, portnametype)

        #if the sourceporttype is changed, change the sinkporttype as well
        if index.column() == 2: #change in sourport -> column 2
            currentRow = index.row()
            newindex = model.index(currentRow, 5)   #the column for the sinkport is 5
            sinkportData = newindex.data()
            sinkportname = sinkportData.split(" / ")[0]
            newportnametype = sinkportname + " / " + porttype
            model.setData(newindex, newportnametype)

class PortTypeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PortTypeWidget, self).__init__(parent)
        #layout
        layout = QtWidgets.QHBoxLayout()
        #adjust spacings
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        #add elements
        linee = QtWidgets.QLineEdit()
        combo = QtWidgets.QComboBox()
        combo.addItems(["SPR", "SPI", "SPB", "PPEA", "PPMT"])
        layout.addWidget(linee)
        layout.addWidget(combo)
        #set the layout
        self.setLayout(layout)

class Coupling:
    def __init__(self, treeManipulate, tabnumber):
        self.treeManipulate = treeManipulate
        self.tabnumber = tabnumber
        self.tvcouplingview = None
        self.cbcouplingssoname = None
        self.cbcouplingssiname = None
        self.lelistcoupling = None
        self.bcouplingsinsert = None
        self.bcouplingsdelete = None
        self.bcouplingshelp = None
        self.cbcouplingfunselect = None
        self.lecouplingfunselect = None
        self.lecouplingfunselectres = None
        self.setUiInit()
        self.helptext = self.treeManipulate.main.couphelp
        #build empty model for data and the selection
        self.couplingmodel = CouplingStandardItemModel(self.tvcouplingview)
        self.couplingmodel.setHorizontalHeaderLabels(["source", "uid", "port name / type", "sink", "uid", "port name / type", "comment"])
        self.couplingselectionmodel = QItemSelectionModel(self.couplingmodel)
        #set model to tableview
        self.tvcouplingview.setModel(self.couplingmodel)
        self.tvcouplingview.setSelectionModel(self.couplingselectionmodel)
        self.tvcouplingview.setItemDelegateForColumn(2, CouplingDelegate(self.tvcouplingview))
        self.tvcouplingview.setItemDelegateForColumn(5, CouplingDelegate(self.tvcouplingview))
        #signals
        self.cbcouplingssoname.installEventFilter(self.treeManipulate.main)
        self.cbcouplingssiname.installEventFilter(self.treeManipulate.main)
        self.bcouplingsinsert.clicked.connect(self.addCoupling)
        self.bcouplingsdelete.clicked.connect(self.deleteCoupling)
        self.bcouplingsinsert.clicked.connect(self.actDeactFields)
        self.bcouplingsdelete.clicked.connect(self.actDeactFields)
        self.bcouplingshelp.clicked.connect(self.help)
        self.couplingmodel.itemChanged.connect(self.changeCoupling)
        self.cbcouplingfunselect.installEventFilter(self.treeManipulate.main)
        self.cbcouplingfunselect.currentIndexChanged.connect(self.setTextSelFun)
        self.lecouplingfunselect.textChanged.connect(self.setCheckValueFunctionChanged)
        self.lecouplingfunselect.textChanged.connect(self.actDeactFields)
        #self.treeManipulate.tbproperties.currentChanged.connect(self.getLastToolboxPage)
        self.treeManipulate.treeSelectionModel.currentChanged.connect(self.setCheckValueNodeChanged)  # the selection was changed so the selected node was changed
        self.treeManipulate.tbproperties.currentChanged.connect(self.setCheckValueNodeChanged)      # the toolbox is changed so the selected node was changed
        #self.treeManipulate.treeModel.nameChangedSignal.connect(self.updateCouplingsNameChanged)
        self.treeManipulate.treeModel.nameChangedSignal.connect(self.changeCouplingNodeName)
        #self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].sesfunChangedSignal.connect(self.fillSESFunSpinner)
        #resize
        self.resz()
        #variables
        #self.currentSelectedTbPage = -1
        #self.lastSelectedTbPage = -1

    def setUiInit(self):
        if self.tabnumber == 0:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst1[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst1[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst1[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst1[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst1[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst1[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst1[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst1[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst1[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst1[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst1[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst1[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst1[12]
        if self.tabnumber == 1:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst2[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst2[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst2[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst2[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst2[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst2[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst2[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst2[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst2[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst2[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst2[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst2[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst2[12]
        if self.tabnumber == 2:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst3[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst3[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst3[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst3[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst3[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst3[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst3[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst3[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst3[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst3[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst3[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst3[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst3[12]
        if self.tabnumber == 3:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst4[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst4[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst4[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst4[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst4[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst4[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst4[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst4[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst4[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst4[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst4[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst4[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst4[12]
        if self.tabnumber == 4:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst5[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst5[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst5[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst5[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst5[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst5[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst5[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst5[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst5[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst5[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst5[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst5[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst5[12]
        if self.tabnumber == 5:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst6[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst6[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst6[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst6[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst6[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst6[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst6[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst6[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst6[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst6[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst6[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst6[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst6[12]
        if self.tabnumber == 6:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst7[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst7[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst7[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst7[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst7[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst7[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst7[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst7[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst7[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst7[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst7[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst7[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst7[12]
        if self.tabnumber == 7:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst8[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst8[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst8[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst8[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst8[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst8[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst8[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst8[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst8[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst8[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst8[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst8[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst8[12]
        if self.tabnumber == 8:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst9[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst9[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst9[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst9[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst9[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst9[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst9[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst9[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst9[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst9[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst9[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst9[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst9[12]
        if self.tabnumber == 9:
            self.tvcouplingview = self.treeManipulate.main.couplingfieldst10[0]
            self.lcouplingssoname = self.treeManipulate.main.couplingfieldst10[1]
            self.lcouplingssiname = self.treeManipulate.main.couplingfieldst10[2]
            self.cbcouplingssoname = self.treeManipulate.main.couplingfieldst10[3]
            self.cbcouplingssiname = self.treeManipulate.main.couplingfieldst10[4]
            self.lelistcoupling = self.treeManipulate.main.couplingfieldst10[5]
            self.bcouplingsinsert = self.treeManipulate.main.couplingfieldst10[6]
            self.bcouplingsdelete = self.treeManipulate.main.couplingfieldst10[7]
            self.bcouplingshelp = self.treeManipulate.main.couplingfieldst10[8]
            self.lcbcouplingfunselect = self.treeManipulate.main.couplingfieldst10[9]
            self.cbcouplingfunselect = self.treeManipulate.main.couplingfieldst10[10]
            self.lecouplingfunselect = self.treeManipulate.main.couplingfieldst10[11]
            self.lecouplingfunselectres = self.treeManipulate.main.couplingfieldst10[12]

    def setSesVarsFunsInCoupling(self):
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
    def readCouplingList(self, lst):
        self.lecouplingfunselect.setText("")
        for row in range(len(lst)):
            #itemsonn = self.treeManipulate.findNodeFromUid(int(lst[row][1]))
            #if itemsonn != None:    # -> None, when tree is read because the model is read in -> maybe node does not exist yet -> take from lst
                #itemson = QStandardItem(itemsonn.name())
            #else:
                #itemson = QStandardItem(lst[row][0])
            itemson = QStandardItem(lst[row][0])
            itemsou = QStandardItem(lst[row][1])
            itemsop = QStandardItem(lst[row][2])
            #itemsinn = self.treeManipulate.findNodeFromUid(int(lst[row][4]))
            #if itemsinn != None:    # -> None, when tree is read because the model is read in -> maybe node does not exist yet -> take from lst
                #itemsin = QStandardItem(itemsinn.name())
            #else:
                #itemsin = QStandardItem(lst[row][3])
            itemsin = QStandardItem(lst[row][3])
            itemsiu = QStandardItem(lst[row][4])
            itemsip = QStandardItem(lst[row][5])
            itemfun = lst[row][6]
            itemcom = QStandardItem(lst[row][7])
            if lst[row][0] != "" and lst[row][1] != "" and lst[row][2] != "" and lst[row][3] != "" and lst[row][4] != "" and lst[row][5] != "" and lst[row][6] == "":
                self.couplingmodel.appendRow([itemson, itemsou, itemsop, itemsin, itemsiu, itemsip, itemcom])
            elif lst[row][0] == "" and lst[row][1] == "" and lst[row][2] == "" and lst[row][3] == "" and lst[row][4] == "" and lst[row][5] == "" and lst[row][6] != "":
                self.lecouplingfunselect.setText(itemfun)
        self.resz()
        self.validate()
        self.actDeactFields()

        #hide the uid columns
        #self.tvcouplingview.setColumnHidden(1, True)
        #self.tvcouplingview.setColumnHidden(4, True)

        #after a list is read in, make sure the comboboxes for selection of a node for the coupling are cleared
        self.cbcouplingssoname.clear()
        self.cbcouplingssiname.clear()

    """write -> the entries of the list in the current node or only output the list"""
    def writeCouplingList(self, onlyOutput=False, index=None):
        if not self.treeManipulate.isRestoringTree:  # only, if it is not called due to a selection change during reading the tree from save
            couplingList = []
            # get current selected node or the node from index depending whether an index is passed
            if index == None:
                index = self.treeManipulate.treeSelectionModel.currentIndex()   #no index to insert was passed, so set it
                nodeuid = self.treeManipulate.treeModel.getNode(index).getUid()
            else:   #an index to insert was passed
                nodeuid = self.treeManipulate.treeModel.getNode(index).getUid()
            for row in range(self.couplingmodel.rowCount()):
                #indson = self.couplingmodel.item(row, 0)
                indsou = self.couplingmodel.item(row, 1)
                indson = self.treeManipulate.findNodeFromUid(int(indsou.data(QtCore.Qt.DisplayRole))).name()
                indsop = self.couplingmodel.item(row, 2)
                #indsin = self.couplingmodel.item(row, 3)
                indsiu = self.couplingmodel.item(row, 4)
                indsin = self.treeManipulate.findNodeFromUid(int(indsiu.data(QtCore.Qt.DisplayRole))).name()
                indsip = self.couplingmodel.item(row, 5)
                indcom = self.couplingmodel.item(row, 6)
                var = [indson, indsou.data(QtCore.Qt.DisplayRole), indsop.data(QtCore.Qt.DisplayRole), indsin, indsiu.data(QtCore.Qt.DisplayRole), indsip.data(QtCore.Qt.DisplayRole), "", indcom.data(QtCore.Qt.DisplayRole)]
                couplingList.append(var)
            indfun = self.lecouplingfunselect.text()
            if indfun != "":
                var = ["", "", "", "", "", "", indfun, ""]
                couplingList.append(var)
            if not onlyOutput:
                self.treeManipulate.treeModel.insertNodeSpecProp(index, couplingList, "couplinglist", nodeuid)  # write into the node
            else:
                return couplingList

    """activate and deactivate the fields since either the coupling list can be filled or the coupling is defined by an SES function"""
    def actDeactFields(self):
        #activate / deactivate the function fields
        if self.couplingmodel.rowCount() == 0:
            self.lcbcouplingfunselect.setEnabled(True)
            self.cbcouplingfunselect.setEnabled(True)
            self.lecouplingfunselect.setEnabled(True)
            self.lecouplingfunselectres.setEnabled(True)
        else:
            self.lcbcouplingfunselect.setEnabled(False)
            self.cbcouplingfunselect.setEnabled(False)
            self.lecouplingfunselect.setEnabled(False)
            self.lecouplingfunselectres.setEnabled(False)
        #activate / deactivate the list fields
        funvalue = self.lecouplingfunselect.text()
        if funvalue == "":
            #activate the list
            self.tvcouplingview.setEnabled(True)
            self.lcouplingssoname.setEnabled(True)
            self.lcouplingssiname.setEnabled(True)
            self.cbcouplingssoname.setEnabled(True)
            self.cbcouplingssiname.setEnabled(True)
            self.lelistcoupling.setEnabled(True)
            self.bcouplingsinsert.setEnabled(True)
            self.bcouplingsdelete.setEnabled(True)
        else:
            #deactivate the list
            self.tvcouplingview.setEnabled(False)
            self.lcouplingssoname.setEnabled(False)
            self.lcouplingssiname.setEnabled(False)
            self.cbcouplingssoname.setEnabled(False)
            self.cbcouplingssiname.setEnabled(False)
            self.lelistcoupling.setEnabled(False)
            self.bcouplingsinsert.setEnabled(False)
            self.bcouplingsdelete.setEnabled(False)

    #-----functions for the iterator list-------------------------------------------------------------------------------

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
            self.tvcouplingview.resizeColumnToContents(i)
            i += 1
        header = self.tvcouplingview.horizontalHeader()
        header.setStretchLastSection(True)

    """select a sourcenode"""
    def fillSelectSourceNode(self):
        node = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
        parentindex = self.treeManipulate.treeModel.parent(self.treeManipulate.treeSelectionModel.currentIndex())
        parentnode = self.treeManipulate.treeModel.getNode(parentindex)
        childnodes = node.childrenlist()
        self.cbcouplingssoname.clear()
        self.cbcouplingssoname.addItem("Sourcenode")
        self.cbcouplingssoname.addItem(parentnode.name() + " - uid: " + str(parentnode.getUid()))
        for cn in childnodes:
            self.cbcouplingssoname.addItem(cn.name() + " - uid: " + str(cn.getUid()))

    """select a sinknode"""
    def fillSelectSinkNode(self):
        node = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
        parentindex = self.treeManipulate.treeModel.parent(self.treeManipulate.treeSelectionModel.currentIndex())
        parentnode = self.treeManipulate.treeModel.getNode(parentindex)
        childnodes = node.childrenlist()
        self.cbcouplingssiname.clear()
        self.cbcouplingssiname.addItem("Sinknode")
        self.cbcouplingssiname.addItem(parentnode.name() + " - uid: " + str(parentnode.getUid()))
        for cn in childnodes:
            self.cbcouplingssiname.addItem(cn.name() + " - uid: " + str(cn.getUid()))

    """add an attribute to the model"""
    def addCoupling(self):
        self.changeAppendValue(False)

    """model changed via double click"""
    def changeCoupling(self):
        self.changeAppendValue(True)

    """change the coupling when a node name was changed"""
    def changeCouplingNodeName(self):
        #get the name changed node
        index = self.treeManipulate.treeSelectionModel.currentIndex()
        node = self.treeManipulate.treeModel.getNode(index)
        #the name changed node could be the father or one son of a Aspect or Maspect with couplings which have to be changed
        cchildrenlist = node.childrenlist() #the name changed node as father -> it can have children which have the name changed node in their couplings
        cnodefather = node.parent()     #the name changed node as child -> the father can have the name changed node in its couplings
        for cchild in range(len(cchildrenlist)):
            if cchildrenlist[cchild].typeInfo() == "Aspect Node" or cchildrenlist[cchild].typeInfo() == "Maspect Node":
                self.writeCouplingList(False, self.treeManipulate.treeModel.index(index.row()+cchild, 0, index))    #build the index for writing the coupling list: current index.row() and where the next stand
        if cnodefather.typeInfo() == "Aspect Node" or cnodefather.typeInfo() == "Maspect Node":
            self.writeCouplingList(False, index.parent())

    """check the coupling"""
    def changeAppendValue(self, change):
        #new value
        if not change:
            coupling = self.lelistcoupling.text()
            cpl = re.findall('\[\s*?[\'\"]?[\w\s]+[\'\"]?\s*?,\s*?[\'\"]?[\w\s]+[\'\"]?\s*?\]', coupling)
            #get the possible selected nodes and uids
            parentindex = self.treeManipulate.treeModel.parent(self.treeManipulate.treeSelectionModel.currentIndex())
            parentnode = self.treeManipulate.treeModel.getNode(parentindex)
            node = self.treeManipulate.treeModel.getNode(self.treeManipulate.treeSelectionModel.currentIndex())
            children = node.childrenlist()
            possibleSelectedNodes = []
            possibleSelectedNodes.append([parentnode.name(), parentnode.getUid()])
            for n in children:
                possibleSelectedNodes.append([n.name(), n.getUid()])
            if cpl != []:
                insertable = True
                appendRows = []
                for cp in cpl:
                    #cp = ''.join(cp.split())
                    cp = cp.strip()
                    cp = cp[1:-1]
                    c = cp.split(",")
                    d = []  #this variable will hold the semantic condition [sourcenodename, sourcenodeuid, sourcenodeport, sinknodename, sinknodeuid, sinknodeport]
                    soCTname = self.cbcouplingssoname.currentText().split(" - uid: ")[0]
                    d.append(soCTname)  #add the sourcenodename in d
                    if self.cbcouplingssoname.currentText() == "Sourcenode":
                        pass
                    else:   #add the sourcenodeuid in d
                        for n in possibleSelectedNodes:
                            if n[0] == soCTname:
                                d.append(n[1])
                                break
                    d.append(c[0])  #add the sourcenodeport in d
                    siCTname = self.cbcouplingssiname.currentText().split(" - uid: ")[0]
                    d.append(siCTname)  #add the sinknodename in d
                    if self.cbcouplingssiname.currentText() == "Sinknode":
                        pass
                    else:   #add the sinknodeuid in d
                        for n in possibleSelectedNodes:
                            if n[0] == siCTname:
                                d.append(n[1])
                                break
                    d.append(c[1])  #add the sinknodeport in d
                    #strip the string elements in d
                    for i in range(len(d)):
                        if isinstance(d[i], str):
                            d[i] = d[i].strip()
                            if d[i] == "":
                                insertable = False
                    #create row, if okay
                    if len(d) == 6:
                        row = [d[0], d[1], d[2], d[3], d[4], d[5]]
                        appendRows.append(row)
                    if len(d) < 6 or (d[0] == d[3] and d[0]!=parentnode.name()) or self.cbcouplingssoname.currentText() == "Sourcenode" or self.cbcouplingssiname.currentText() == "Sinknode":
                        insertable = False
                if insertable:
                    for c in appendRows:
                        itemson = QStandardItem(str(c[0]))
                        itemsou = QStandardItem(str(c[1]))
                        itemsop = QStandardItem(str(c[2]) + " / SPR")   #the type is added
                        itemsin = QStandardItem(str(c[3]))
                        itemsiu = QStandardItem(str(c[4]))
                        itemsip = QStandardItem(str(c[5]) + " / SPR")   #the type is added
                        itemcom = QStandardItem("") #empty comment
                        self.couplingmodel.appendRow([itemson, itemsou, itemsop, itemsin, itemsiu, itemsip, itemcom])
                    self.lelistcoupling.setText("")
                else:
                    QMessageBox.information(None, "Can not insert", "A field is empty or the sourcenode is the same as the sinknode and not the fathernode.", QtWidgets.QMessageBox.Ok)
            else:
                QMessageBox.information(None, "Can not insert", "The syntax is not correct.", QtWidgets.QMessageBox.Ok)
        #value is changed
        else:
            index = self.tvcouplingview.currentIndex()
            #if index.column() == 0 or index.column() == 1 or index.column() == 2 or index.column() == 3:
            coupc = self.couplingmodel.itemData(index)
            if coupc != {}:
                coupling = str(coupc[0])
                if index.column() == 6: #the comment may contain any literal -> so in column 6 allow any literal
                    cpl = re.match('.', coupling)
                else:
                    #cpl = re.match('\s*?[\'\"]?[\w\s]+[\'\"]?\s*?', coupling)      #regex for port without porttype
                    cpl = re.match('\s*?[\'\"]?[\w\s]+[\'\"]?\s/\s\w+', coupling)   #regex for port with porttype
                if cpl is not None:
                    cpl = cpl.group()
                    if cpl == coupling and index.column() != 6: #further checks only if it is not the comment field
                        cpl = cpl.strip()
                        if cpl != "":
                            dict = {0: cpl}
                            self.couplingmodel.setItemData(index, dict)
                        else:
                            QMessageBox.information(None, "Changing not possible", "The changed field is empty. The coupling is deleted.", QtWidgets.QMessageBox.Ok)
                            self.deleteCoupling(self.couplingselectionmodel.currentIndex().row(), True)
                    elif index.column() == 6:
                        pass
                    else:
                        QMessageBox.information(None, "Changing not possible", "The syntax of the edited coupling field is not correct. The coupling is deleted.", QtWidgets.QMessageBox.Ok)
                        self.deleteCoupling(self.couplingselectionmodel.currentIndex().row(), True)
                else:
                    QMessageBox.information(None, "Changing not possible", "The syntax of the edited coupling field is not correct. The coupling is deleted.", QtWidgets.QMessageBox.Ok)
                    self.deleteCoupling(self.couplingselectionmodel.currentIndex().row(), True)
        self.writeCouplingList()
        self.resz()

    """update couplings when the name of nodes is changed in the tree"""
    """ -> now in the read and the write function - not needed anymore
    def updateCouplingsNameChanged(self):
        #getting the couplings
        couplingList = self.writeCouplingList(True)
        j = 0
        while j < len(couplingList):
            cplson = couplingList[j][0]
            cplsou = int(couplingList[j][1])
            cplsin = couplingList[j][3]
            cplsiu = int(couplingList[j][4])
            nodefoundso = self.treeManipulate.findNodeFromUid(cplsou)
            nodefoundsi = self.treeManipulate.findNodeFromUid(cplsiu)
            if nodefoundso is not None and cplson != nodefoundso.name():
                index = self.couplingmodel.index(j, 0)
                self.couplingmodel.setData(index, nodefoundso.name())
            if nodefoundsi is not None and cplsin != nodefoundsi.name():
                index = self.couplingmodel.index(j, 3)
                self.couplingmodel.setData(index, nodefoundsi.name())
            j += 1
    """

    """delete"""
    def deleteCoupling(self, rw=-1, rowsdelete=False):
        selectedrows = self.couplingselectionmodel.selectedRows()
        if len(selectedrows) == 0 and rw == -1:
            QMessageBox.information(None, "Deleting not possible", "Please select at least one coupling to delete.", QtWidgets.QMessageBox.Ok)
        elif len(selectedrows) > 0 and not rowsdelete:
            deleteListRows = []
            for rowind in selectedrows:
                deleteListRows.append(rowind.row())
            deleteListRows.sort(reverse=True)
            for row in deleteListRows:
                self.couplingmodel.removeRow(row, QtCore.QModelIndex())
        elif rw != -1 and rowsdelete:
            self.couplingmodel.removeRow(rw, QtCore.QModelIndex())
        self.writeCouplingList()
        self.resz()

    """empty the model"""
    def emptyCouplingModel(self):
        self.couplingmodel.clear()
        self.couplingmodel.setHorizontalHeaderLabels(["source", "uid", "port name / type", "sink", "uid", "port name / type", "comment"])

    """help"""
    def help(self):
        msgBox = QMessageBox(self.treeManipulate.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("couplings: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()

    """check the coupling -> old function ['sourcenodename', sourceport, 'sinknodename', sinkport][...] and all values were editable"""
    """
    def changeAppendValue(self, change):
        #new value
        if not change:
            coupling = self.lelistcoupling.text()
            cpl = re.findall('\[\s*?[\'\"]?[\w\s]+[\'\"]?\s*?,\s*?[\'\"]?[\w\s]+[\'\"]?\s*?,\s*?[\'\"]?[\w\s]+[\'\"]?\s*?,\s*?[\'\"]?[\w\s]+[\'\"]?\s*?\]', coupling)
            if cpl != []:
                insertable = True
                appendRows = []
                for cp in cpl:
                    #cp = ''.join(cp.split())
                    cp = cp.strip()
                    cp = cp[1:-1]
                    c = cp.split(",")
                    for i in range(len(c)):
                        c[i] = c[i].strip()
                        if c[i] == "":
                            insertable = False
                    row = [c[0], c[1], c[2], c[3]]
                    appendRows.append(row)
                if insertable:
                    for c in appendRows:
                        itemson = QStandardItem(str(c[0]))
                        itemsop = QStandardItem(str(c[1]))
                        itemsin = QStandardItem(str(c[2]))
                        itemsip = QStandardItem(str(c[3]))
                        self.couplingmodel.appendRow([itemson, itemsop, itemsin, itemsip])
                    self.lelistcoupling.setText("")
                else:
                    QMessageBox.information(None, "Can not insert", "A field is empty.", QtWidgets.QMessageBox.Ok)
            else:
                QMessageBox.information(None, "Can not insert", "The syntax is not correct.", QtWidgets.QMessageBox.Ok)
        #value is changed
        else:
            index = self.tvcouplingview.currentIndex()
            #if index.column() == 0 or index.column() == 1 or index.column() == 2 or index.column() == 3:
            coupc = self.couplingmodel.itemData(index)
            coupling = str(coupc[0])
            cpl = re.match('\s*?[\'\"]?[\w\s]+[\'\"]?\s*?', coupling)
            if cpl is not None:
                cpl = cpl.group()
                if cpl == coupling:
                    cpl = cpl.strip()
                    if cpl != "":
                        dict = {0: cpl}
                        self.couplingmodel.setItemData(index, dict)
                    else:
                        QMessageBox.information(None, "Changing not possible", "The changed field is empty. The coupling is deleted.", QtWidgets.QMessageBox.Ok)
                        self.deleteCoupling(self.couplingselectionmodel.currentIndex().row(), True)
                else:
                    QMessageBox.information(None, "Changing not possible", "The syntax of the edited coupling field is not correct. The coupling is deleted.", QtWidgets.QMessageBox.Ok)
                    self.deleteCoupling(self.couplingselectionmodel.currentIndex().row(), True)
            else:
                QMessageBox.information(None, "Changing not possible", "The syntax of the edited coupling field is not correct. The coupling is deleted.", QtWidgets.QMessageBox.Ok)
                self.deleteCoupling(self.couplingselectionmodel.currentIndex().row(), True)
        self.writeCouplingList()
        self.resz()
        """

    #-----functions for the coupling functions--------------------------------------------------------------------------

    """get the last selected page of the toolbox"""
    #def getLastToolboxPage(self):
        #self.lastSelectedTbPage = self.currentSelectedTbPage
        #self.currentSelectedTbPage = self.treeManipulate.tbproperties.currentIndex()

    """call check and set the value on toolbox change"""
    #def setCheckValueTbChanged(self):
        #self.setCheckValue("", True)

    """fill spinner with SES function names"""
    def fillSESFunSpinner(self):
        self.cbcouplingfunselect.clear()
        self.cbcouplingfunselect.addItem("SES function name")
        funlist = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()
        for f in funlist:
            self.cbcouplingfunselect.addItem(f[0])

    """put the selected function in the combobox as text in the line edit"""
    def setTextSelFun(self):
        if self.cbcouplingfunselect.currentText() == "SES function name":
            self.lecouplingfunselect.setText("")
        else:
            self.lecouplingfunselect.setText(self.cbcouplingfunselect.currentText() + "()")

    """call check and set the value on toolbox change"""
    def setCheckValueNodeChanged(self):
        self.setCheckValue("", True)

    """call check and set the value on text change in the function"""
    def setCheckValueFunctionChanged(self):
        self.setCheckValue("", False, True)

    """check and set the value"""
    def setCheckValue(self, abc, isNodeChange=False, isFunctionChange=False):

        value = self.lecouplingfunselect.text()
        value = value.strip()

        if not self.treeManipulate.isRestoringTree: #only if it is not called due to restoring the tree -> in couplings the children can be referred to as well, when restoring the tree, they do not exist yet
            nd = self.treeManipulate.treeModel.getNode(self.treeManipulate.currentSelectedIndex)
            if nd.typeInfo() == "Aspect Node" or nd.typeInfo() == "Maspect Node":
                if value == "": #needed for deleting a function, but hinder to delete a couplinglist
                    ndcpl = nd.coupling
                    if not isNodeChange and isFunctionChange and ndcpl and ndcpl[0][6] != "":
                        self.writeCouplingList()
                        self.validate()
                    return
                elif value != "":
                    if not isNodeChange:
                        # check if it can be the syntax of an SES variable or function
                        attribregex = re.compile('^([a-z]|[A-Z])(\w+)?(\(([\"\']?\w+[\"\']?)?(,\s*?[\"\']?\w+[\"\']?)*\))$')
                        attribregexcorrect = attribregex.match(value)
                        if attribregexcorrect is not None:
                            self.writeCouplingList()
                            self.validate()
                            return
                        else:
                            self.validate()
                    if isNodeChange:
                        ok = self.validate()
                        if not ok:
                            QMessageBox.information(None, "The coupling function is not correct",
                                                    "Please look at the result of your SES function. If you want to reference an SES variable or function, use the syntax\n"
                                                    "sesvarname or\nsesfunname(1[, 4.5]) or\nsesfunname(5[, sesvarname]).\n"
                                                    "The expression in square brackets is optional, do not type the square brackets. Use it if you want to pass parameters.\n"
                                                    "sesvarname and sesfunname must be alphanumeric not beginning with a number.\n"
                                                    "Furthermore, make sure, that the value evaluates to an expression like\n"
                                                    "[[\"sourcenodename\",\"sourcenodeport\",\"sinknodename\",\"sinknodeport\"]] or\n"
                                                    "[[\"sourcenodename\",\"sourcenodeport\",\"sinknodename\",\"sinknodeport\"],[\"sourcenodename\",\"sourcenodeport\",\"sinknodename\",\"sinknodeport\"]]\n"
                                                    "and make sure that the sourcenodename and the sinknodenames equal the parent's or one child's name.",
                                                    QtWidgets.QMessageBox.Ok)

    """color the fields depending on the content"""
    def validate(self, sesvarl="", sesfunl="", nd=None, paths=None):

        # sub function -> execute a function
        def execFunction(svicp, sesfunl, value, cplvalue, funFound):
            # check that the expression is an SES function
            if "(" in value and ")" in value:
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
                            ret = eval(v, globals(), svicp.__dict__)
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
                        sesfunvalue[1] = re.sub('def ' + re.escape(sesfunvalue[0]) + '\(.*\)',
                                                'def ' + re.escape(sesfunvalue[0]) + '(' + varstring + ')',
                                                sesfunvalue[1])

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
                                    cplvalue = self.ret
                                except:
                                    pass
                        except:
                            pass

            return cplvalue, funFound

        #sub function
        def validateCplgFun(nd, svicp, sesfunl):

            funFound = False
            funVarFound = True
            retval = []
            cplvalue = []

            if nd.coupling:     #if coupling is not empty
                value = nd.coupling[0][6]
                if value != "":
                    cplvalue, funFound = execFunction(svicp, sesfunl, value, cplvalue, funFound)

            #check that the type is correct: ["sourcenodename", "sourcenodeport", "sinknodename", "sinknodeport", "comment"] and the parent and childrennames are really parents and children
            typeOk = []
            parChilOk = []
            allOk = False
            try:
                #check the type, if it is okay, go on
                for cplv in range(len(cplvalue)):
                    # make to string
                    cplvaluestr = "[\"" + '\", \"'.join(str(e) for e in cplvalue[cplv]) + "\"]"
                    #match regular expression
                    #mat = re.match('\[\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,.*\]', cplvaluestr)  #regex without porttypes
                    mat = re.match('\[\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"][\w\s-]+\s/\s\w+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"][\w\s-]+\s/\s\w+[\'\"]\s*?,.*\]', cplvaluestr)   #regex with porttypes
                    if mat:
                        typeOk.append(True)

                        #check and add the uid information of the parent and child
                        #get the parent's name and uid
                        pname = {}
                        pname.update({nd.parent().name(): str(nd.parent().getUid())})
                        #get the children's names and uid
                        cnames = {}
                        for cl in nd.childrenlist():
                            # it has to be given out an uid (-> for the children created from the Maspect as well)
                            # if nd is no Maspect node: just add the children with their uids
                            # if nd is a Maspect node: children are created according to the number of replications during pruning and to the name _1, _2 etc. is added
                            #   couplings can refer to the different children created during pruning of the Maspect node, so the names of these children need to be created now (just the name of the child with an appended _1, _2 ...)
                            #   since a coupling function can refer to children of a Maspect node
                            if not nd.typeInfo() == "Maspect Node":
                                cnames.update({cl.name(): str(cl.getUid())})
                            else:       #create the children's names like during pruning and insert them in cnames
                                nr = nd.number_replication  # number_replication can be an SES variable or function itself -> it has to be interpreted as integer before
                                nrok = False
                                try:
                                    nr = int(nr)
                                    nrok = True
                                except ValueError:  # maybe it is an SES Variable -> get the value
                                    try:
                                        nr = eval(nr, globals(), svicp.__dict__)  # or using getattr(object, name[, default]) -> value
                                        nr = int(nr)  # if it is not an integer yet
                                        nrok = True
                                    except:
                                        # seems not be be interpretable as integer for now, but maybe it is a PATH function -> execute
                                        try:
                                            nr, ff = execFunction(svicp, sesfunl, nr, "", False)
                                            nr = int(nr)
                                            nrok = True
                                        except:
                                            # it definitely does not seem to be interpretable as integer
                                            pass

                                # for the current child create names as during pruning according to number of replications
                                if nrok:
                                    for number in range(1, nr + 1):
                                        # rename and append to childrenNames dictionary
                                        newname = cl.name() + "_" + str(number)
                                        cnames.update({newname: str(cl.getUid())})  # just take the old uid, it is updated when needed during pruning anyway, this is only to show and give back the right form

                        #now add the uid information
                        #for the source -> try to find it in the parent or the children
                        sourceuid = pname.get(cplvalue[cplv][0])
                        if not sourceuid:    #if the source name was found in the parent
                            sourceuid = cnames.get(cplvalue[cplv][0])
                        if sourceuid:   #if the source name was found in the parent or in the children
                            cplvalue[cplv].insert(1, str(sourceuid))
                        else:
                            cplvalue[cplv].insert(1, "source not found")
                            cplvalue[cplv][0] = "source not found"
                        #for the sink -> try to find in the parent or the children
                        sinkuid = pname.get(cplvalue[cplv][3])
                        if not sinkuid:     #if the sink name was found in the parent
                            sinkuid = cnames.get(cplvalue[cplv][3])
                        if sinkuid:     #if the sink name was found in the parent or in the children
                            cplvalue[cplv].insert(4, str(sinkuid))
                        else:
                            cplvalue[cplv].insert(4, "sink not found")
                            cplvalue[cplv][3] = "sink not found"

                        # make to string
                        cplvaluestr = "[\"" + '\", \"'.join(str(e) for e in cplvalue[cplv]) + "\"]"
                        # match regular expression now with the uid information
                        #mat = re.match('\[\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"]\d+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"]\d+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,.*\]', cplvaluestr)  #regex without porttypes
                        mat = re.match('\[\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"]\d+[\'\"]\s*?,\s*?[\'\"][\w\s-]+\s/\s\w+[\'\"]\s*?,\s*?[\'\"][\w\s-]+[\'\"]\s*?,\s*?[\'\"]\d+[\'\"]\s*?,\s*?[\'\"][\w\s-]+\s/\s\w+[\'\"]\s*?,.*\]', cplvaluestr)   #regex with porttypes
                        if mat:
                            parChilOk.append(True)
                        else:
                            parChilOk.append(False)
                        cplvalue[cplv].append("")   #now the field for the function is empty, since it has been interpreted
                        #append to retval -> place result in the field as if it was a coupling defined from the couplinglist
                        retval.append(cplvalue[cplv])
            except:
                pass

            #set allOk
            if typeOk:    #empty list: make sure, the list is not empty
                typeOk = all(typeOk)
            else:
                typeOk = False
            if parChilOk:
                parChilOk = all(parChilOk)
            else:
                parChilOk = False

            allOk = typeOk and parChilOk

            #if not retval:
                #retval.append(["","","","","","",""])


            return funFound, funVarFound, typeOk, parChilOk, allOk, retval

        # sub function -> add the special variables (node specific variables) to the sesvars class
        def addSpecialVars(sesvarsInRulesClass, sesfunl, currentNode=None, paths=None):
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

            #append PARENT
            if currentNode.parent():    #if the parent is not node -> is None, when first node at the beginning of the tree is the current node
                #setattr(svicp, "PARENT", [[currentNode.parent().getUid(), currentNode.parent().name()]])     #only set the parent's name as PARENT now
                setattr(svicp, "PARENT", currentNode.parent().name())

            #append CHILDREN
            childrenlist = currentNode.childrenlist()
            #childrenlistUidNames = []  #only pass names now (see below)
            childrenNames = []
            for child in childrenlist:
                # if currentNode is not a Maspect node: add the childrens' names
                # if currentNode is a Maspect node: children are created according to the number of replications during pruning and to the name _1, _2 etc. is added
                #   couplings can refer to the different children created during pruning of the Maspect node, so the names of these children need to be created now (just the name of the child with an appended _1, _2 ...)
                #   since a coupling function can refer to children of a Maspect node
                if not currentNode.typeInfo() == "Maspect Node":
                    #childrenlistUidNames.append([child.getUid(), child.name()])        #only pass the children's names as CHILDREN now
                    childrenNames.append(child.name())
                else:   #create the children's names like during pruning and insert them in childrenNames
                    nr = currentNode.number_replication  # number_replication can be an SES variable or function itself -> it has to be interpreted as integer before
                    nrok = False
                    try:
                        nr = int(nr)
                        nrok = True
                    except ValueError:  # maybe it is an SES Variable -> get the value
                        try:
                            nr = eval(nr, globals(), svicp.__dict__)  # or using getattr(object, name[, default]) -> value
                            nr = int(nr)  # if it is not an integer yet
                            nrok = True
                        except:
                            # seems not be be interpretable as integer for now, but maybe it is a PATH function -> execute
                            try:
                                nr, ff = execFunction(svicp, sesfunl, nr, "", False)
                                nr = int(nr)
                                nrok = True
                            except:
                                #it definitely does not seem to be interpretable as integer
                                pass

                    # for the current child create names as during pruning according to number of replications
                    if nrok:
                        for number in range(1, nr + 1):
                            # rename and append to childrenNames dictionary
                            newname = child.name() + "_" + str(number)
                            childrenNames.append(newname)
            #setattr(svicp, "CHILDREN", childrenlistUidNames)
            setattr(svicp, "CHILDREN", childrenNames)

            # append the NUMREP variable
            type = currentNode.typeInfo()
            if type == "Maspect Node":
                nr = currentNode.number_replication     #number_replication can be an SES variable or function itself -> it has to be interpreted as integer before
                try:
                    nr = int(nr)
                except ValueError:  #maybe it is an SES Variable -> get the value
                    try:
                        nr = eval(nr, globals(), svicp.__dict__)  # or using getattr(object, name[, default]) -> value
                        nr = int(nr)    #if it is not an integer yet
                    except:
                        pass    #seems not be be interpretable as integer
                setattr(svicp, "NUMREP", nr)
            else:
                setattr(svicp, "NUMREP", 1)   #aspect nodes -> number of replication is one

        #here the validate function begins

        # own class for SES variables
        class sesvarsincpl:
            pass

        # create an instance of the SES variables class
        svicp = sesvarsincpl

        if sesvarl == "" and sesfunl == "" and nd == None:  # the validate process was started from the editor for coloring the lines
            #fill the instance of the sesvar class
            for sesvarvalue in self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][1].outputSesVarList():
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(svicp, sesvarvalue[0], sesvarvalue[1])

            currentIndex = self.treeManipulate.treeSelectionModel.currentIndex()
            currentNode = self.treeManipulate.treeModel.getNode(currentIndex)

            #get the SES functions
            sesfunl = self.treeManipulate.main.modellist[self.treeManipulate.main.activeTab][2].outputSesFunList()

            # add special variables to the sesvar class
            addSpecialVars(svicp, sesfunl, currentNode)  #currentNode is passed here, since it is needed later anyway

            #the current node is already gotten, since needed to insert PARENT, CHILDREN, NUMREP and PATH

            #only continue if the current node has couplings
            if currentNode.typeInfo() == "Aspect Node" or currentNode.typeInfo() == "Maspect Node":
                funFound, funVarFound, typeOk, parChilOk, allOk, retval = validateCplgFun(currentNode, svicp, sesfunl)

                #update the line and set result field
                self.updateLine(funFound, funVarFound, allOk, currentNode, retval)

                #return
                return allOk
            return True

        else:   #the validate process was started for pruning
            #fill the instance of the sesvar class
            for sesvarvalue in sesvarl:
                try:
                    sesvarvalue[1] = ast.literal_eval(sesvarvalue[1])  # interprete the type of the value
                except:
                    pass  # do nothing, it stays a string
                setattr(svicp, sesvarvalue[0], sesvarvalue[1])

            # add special variables to the sesvar class
            addSpecialVars(svicp, sesfunl, nd, paths)

            #the SES functions are given in the pass list

            # only continue if the node has a coupling value
            if nd.typeInfo() == "Aspect Node" or nd.typeInfo() == "Maspect Node":
                funFound, funVarFound, typeOk, parChilOk, allOk, retval = validateCplgFun(nd, svicp, sesfunl)

                #return the evaluated result and whether the value is okay for pruning
                return retval, allOk

    def updateLine(self, funFound, funVarFound, allOk, nd, retval):
        if nd.coupling: #nd.coupling may not be empty
            if nd.coupling[0][6] == self.lecouplingfunselect.text() and nd.coupling[0][6] != "":
                if (not funFound) or (not funVarFound) or (not allOk):
                    self.lecouplingfunselect.setStyleSheet("QLineEdit { background: rgb(255, 195, 195); selection-background-color: rgb(0, 255, 255); }")
                elif funFound and funVarFound and allOk:
                    self.lecouplingfunselect.setStyleSheet("QLineEdit { background: rgb(195, 255, 195); selection-background-color: rgb(0, 255, 255); }")
                #make retval to string and set it in the resultfield
                for r in range(len(retval)):
                    del retval[r][6]
                    del retval[r][4]
                    del retval[r][1]
                #make to string and set resultline
                retval = "[\"" + '\", \"'.join(str(e) for e in retval) + "\"]"     # or: retval = "[\"" + '\", \"'.join(map(str, retval)) + "\"]"
                self.lecouplingfunselectres.setText(retval)
            else:
                self.lecouplingfunselect.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")  # if it is empty, simply set to white
                self.lecouplingfunselectres.setText("")
        else:
            self.lecouplingfunselect.setStyleSheet("QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(0, 255, 255); }")   #if it is empty, simply set to white
            self.lecouplingfunselectres.setText("")