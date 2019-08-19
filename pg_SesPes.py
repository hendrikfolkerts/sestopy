# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SesPes(QtCore.QObject):

    sespesChangedSignal = pyqtSignal()

    def __init__(self, main, tabnumber):

        # since we inherited from QObject, we have to call the super class init
        super(SesPes, self).__init__()

        self.main = main
        self.tabnumber = tabnumber
        self.rbses = None
        self.rbipes = None
        self.rbpes = None
        self.rbfpes = None
        self.tesescomment = None
        self.bsespeshelp = None
        self.setUiInit()
        self.helptext = self.main.sespeshelp
        self.rbses.setChecked(True)
        self.rbipes.setChecked(False)
        self.rbpes.setChecked(False)
        self.rbfpes.setChecked(False)
        self.rbses.toggled.connect(self.change)
        self.rbipes.toggled.connect(self.change)
        self.rbpes.toggled.connect(self.change)
        self.rbfpes.toggled.connect(self.change)
        self.tesescomment.textChanged.connect(self.change)
        self.bsespeshelp.clicked.connect(self.help)

    def setUiInit(self):
        if self.tabnumber == 0:
            self.rbses = self.main.rbsest1
            self.rbipes = self.main.rbipest1
            self.rbpes = self.main.rbpest1
            self.rbfpes = self.main.rbfpest1
            self.tesescomment = self.main.tesescommentt1
            self.bsespeshelp = self.main.bsespeshelpt1
        if self.tabnumber == 1:
            self.rbses = self.main.rbsest2
            self.rbipes = self.main.rbipest2
            self.rbpes = self.main.rbpest2
            self.rbfpes = self.main.rbfpest2
            self.tesescomment = self.main.tesescommentt2
            self.bsespeshelp = self.main.bsespeshelpt2
        if self.tabnumber == 2:
            self.rbses = self.main.rbsest3
            self.rbipes = self.main.rbipest3
            self.rbpes = self.main.rbpest3
            self.rbfpes = self.main.rbfpest3
            self.tesescomment = self.main.tesescommentt3
            self.bsespeshelp = self.main.bsespeshelpt3
        if self.tabnumber == 3:
            self.rbses = self.main.rbsest4
            self.rbipes = self.main.rbipest4
            self.rbpes = self.main.rbpest4
            self.rbfpes = self.main.rbfpest4
            self.tesescomment = self.main.tesescommentt4
            self.bsespeshelp = self.main.bsespeshelpt4
        if self.tabnumber == 4:
            self.rbses = self.main.rbsest5
            self.rbipes = self.main.rbipest5
            self.rbpes = self.main.rbpest5
            self.rbfpes = self.main.rbfpest5
            self.tesescomment = self.main.tesescommentt5
            self.bsespeshelp = self.main.bsespeshelpt5
        if self.tabnumber == 5:
            self.rbses = self.main.rbsest6
            self.rbipes = self.main.rbipest6
            self.rbpes = self.main.rbpest6
            self.rbfpes = self.main.rbfpest6
            self.tesescomment = self.main.tesescommentt6
            self.bsespeshelp = self.main.bsespeshelpt6
        if self.tabnumber == 6:
            self.rbses = self.main.rbsest7
            self.rbipes = self.main.rbipest7
            self.rbpes = self.main.rbpest7
            self.rbfpes = self.main.rbfpest7
            self.tesescomment = self.main.tesescommentt7
            self.bsespeshelp = self.main.bsespeshelpt7
        if self.tabnumber == 7:
            self.rbses = self.main.rbsest8
            self.rbipes = self.main.rbipest8
            self.rbpes = self.main.rbpest8
            self.rbfpes = self.main.rbfpest8
            self.tesescomment = self.main.tesescommentt8
            self.bsespeshelp = self.main.bsespeshelpt8
        if self.tabnumber == 8:
            self.rbses = self.main.rbsest9
            self.rbipes = self.main.rbipest9
            self.rbpes = self.main.rbpest9
            self.rbfpes = self.main.rbfpest9
            self.tesescomment = self.main.tesescommentt9
            self.bsespeshelp = self.main.bsespeshelpt9
        if self.tabnumber == 9:
            self.rbses = self.main.rbsest10
            self.rbipes = self.main.rbipest10
            self.rbpes = self.main.rbpest10
            self.rbfpes = self.main.rbfpest10
            self.tesescomment = self.main.tesescommentt10
            self.bsespeshelp = self.main.bsespeshelpt10

    """restore from save"""
    def fromSave(self, sv):
        if sv[0][0] == 'ses':
            self.rbses.setChecked(True)
            self.rbipes.setChecked(False)
            self.rbpes.setChecked(False)
            self.rbfpes.setChecked(False)
        if sv[0][0] == 'ipes':
            self.rbses.setChecked(False)
            self.rbipes.setChecked(True)
            self.rbpes.setChecked(False)
            self.rbfpes.setChecked(False)
        if sv[0][0] == 'pes':
            self.rbses.setChecked(False)
            self.rbipes.setChecked(False)
            self.rbpes.setChecked(True)
            self.rbfpes.setChecked(False)
        if sv[0][0] == 'fpes':
            self.rbses.setChecked(False)
            self.rbipes.setChecked(False)
            self.rbpes.setChecked(False)
            self.rbfpes.setChecked(True)
        self.tesescomment.setText(sv[0][1])

    """output"""
    def outputSesPes(self):
        if self.rbses.isChecked():
            return ['ses', self.tesescomment.toPlainText()]
        if self.rbipes.isChecked():
            return ['ipes', self.tesescomment.toPlainText()]
        if self.rbpes.isChecked():
            return ['pes', self.tesescomment.toPlainText()]
        if self.rbfpes.isChecked():
            return ['fpes', self.tesescomment.toPlainText()]

    #send the treeChanged signal when there occurs a change
    def change(self):
        self.sespesChangedSignal.emit()

    """delete -> reset"""
    def deleteSesPes(self):
        self.rbses.setChecked(True)
        self.rbipes.setChecked(False)
        self.rbpes.setChecked(False)
        self.rbfpes.setChecked(False)
        self.tesescomment.clear()


    """help"""
    def help(self):
        msgBox = QMessageBox(self.main)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("SES/PES selection: Help")
        msgBox.setText(self.helptext[0])
        msgBox.setDetailedText(self.helptext[1])
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Ok)
        msgBox.show()