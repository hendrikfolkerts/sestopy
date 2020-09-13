# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts, University of Applied Sciences Wismar, RG CEA'

#system imports
import sys
import os
from pathlib import Path
from os.path import splitext
from time import strftime
import platform
from PyQt5.Qt import PYQT_VERSION_STR

__version__ = strftime("%Y"+"."+"%m"+"."+"%d") #for development
#__version__ = str(1.0)

"""
This program is written in Python3 with the Qt5 bindings PyQt5
The project has been started using Python3.4.1 and PyQt5.5 and is running with current versions of Python3 and PyQt5.

Call this program with:
python3 main.py

Start pruning without using the graphical editor with the SES variables a=1, b=2 and c=3:
python3 main.py -p ~/HDD/Promotion/SES_Tests/PruneTest.jsonsestree [a=1,b=2,c=3]
Start flattening without using the graphical editor:
python3 main.py -f ~/HDD/Promotion/SES_Tests/FlattenTest.jsonsestree
For more options please call:
python main.py -h
"""

#import ui class
from main_ui import Ui_MainWindow

#tree
from te_TreeManipulate import *
from pg_SesPes import *
from pg_SesVariables import *
from pg_SemanticConditions import *
from pg_SelectionConstraints import *
from pg_SesFunctions import *
from xml_xml import *
from json_json import *

from main_ui_tabfields import *

from pu_prune import *
from fn_flatten import *

from client import *

class Main(QtWidgets.QMainWindow):

    """initialize"""
    def __init__(self, parent=None):
        super(Main, self).__init__()

        #connection to a program taking the tree as xml, e.g. a program for the tree view (which serves as server)
        #execute the client functions in an own thread (needs to be done before the setupUi is called)
        #create thread object
        self.clientThread = QThread()
        self.clientObj = socketClient()
        #move client object to thread
        self.clientObj.moveToThread(self.clientThread)
        #connect client signals to slots in this class
        self.clientObj.clientConnectionSignal.connect(self.onConnectPressed)    #bind clientConnectionSignal from the clientObj to a slot in this class
        self.clientObj.clientNoSendSignal.connect(self.onConnectionLost)        #bind clientNoSendSignal from the clientObj to a slot in this class
        #self.clientObj.clientreturndataSignal.connect(a function = slot in this class)   #data are not shown anywhere yet
        #connect thread started signal to a slot -> execute when the thread is started
        self.clientThread.started.connect(self.clientObj.clientSend)   #start the clientSend function in the clientObj -> it will wait until it gets data
        #start the thread
        self.clientThread.start()

        #initialize window
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #change in directory of main
        mainfilePath = os.path.dirname(os.path.realpath(__file__))
        os.chdir(mainfilePath)

        #model name
        self.modelname = self.ui.modelname
        #connection elements in the ui
        self.bserverConnect = self.ui.bserverconnect        #button: connect client in this program to a server
        self.bserverDisconnect = self.ui.bserverdisconnect    #button: disconnect client in this program from a server
        self.serverIP = self.ui.leserverip
        self.serverPort = self.ui.leserverport
        #tab
        self.tabs = self.ui.tabs
        #menu with the name File
        self.menuFile = self.ui.menuFile

        #ui elements middle
        self.hierarchymodeltreeviewt1 = None
        self.cbnodetypet1 = None
        self.buttonst1 = []
        self.tbpropertiest1 = None
        self.attributefieldst1 = []
        self.aspectrulefieldst1 = []
        self.numberofreplicationfieldst1 = []
        self.couplingfieldst1 = []
        self.specrulefieldst1 = []

        self.hierarchymodeltreeviewt2 = None
        self.cbnodetypet2 = None
        self.buttonst2 = []
        self.tbpropertiest2 = None
        self.attributefieldst2 = []
        self.aspectrulefieldst2 = []
        self.numberofreplicationfieldst2 = []
        self.couplingfieldst2 = []
        self.specrulefieldst2 = []

        self.hierarchymodeltreeviewt3 = None
        self.cbnodetypet3 = None
        self.buttonst3 = []
        self.tbpropertiest3 = None
        self.attributefieldst3 = []
        self.aspectrulefieldst3 = []
        self.numberofreplicationfieldst3 = []
        self.couplingfieldst3 = []
        self.specrulefieldst3 = []

        self.hierarchymodeltreeviewt4 = None
        self.cbnodetypet4 = None
        self.buttonst4 = []
        self.tbpropertiest4 = None
        self.attributefieldst4 = []
        self.aspectrulefieldst4 = []
        self.numberofreplicationfieldst4 = []
        self.couplingfieldst4 = []
        self.specrulefieldst4 = []

        self.hierarchymodeltreeviewt5 = None
        self.cbnodetypet5 = None
        self.buttonst5 = []
        self.tbpropertiest5 = None
        self.attributefieldst5 = []
        self.aspectrulefieldst5 = []
        self.numberofreplicationfieldst5 = []
        self.couplingfieldst5 = []
        self.specrulefieldst5 = []

        self.hierarchymodeltreeviewt6 = None
        self.cbnodetypet6 = None
        self.buttonst6 = []
        self.tbpropertiest6 = None
        self.attributefieldst6 = []
        self.aspectrulefieldst6 = []
        self.numberofreplicationfieldst6 = []
        self.couplingfieldst6 = []
        self.specrulefieldst6 = []

        self.hierarchymodeltreeviewt7 = None
        self.cbnodetypet7 = None
        self.buttonst7 = []
        self.tbpropertiest7 = None
        self.attributefieldst7 = []
        self.aspectrulefieldst7 = []
        self.numberofreplicationfieldst7 = []
        self.couplingfieldst7 = []
        self.specrulefieldst7 = []

        self.hierarchymodeltreeviewt8 = None
        self.cbnodetypet8 = None
        self.buttonst8 = []
        self.tbpropertiest8 = None
        self.attributefieldst8 = []
        self.aspectrulefieldst8 = []
        self.numberofreplicationfieldst8 = []
        self.couplingfieldst8 = []
        self.specrulefieldst8 = []

        self.hierarchymodeltreeviewt9 = None
        self.cbnodetypet9 = None
        self.buttonst9 = []
        self.tbpropertiest9 = None
        self.attributefieldst9 = []
        self.aspectrulefieldst9 = []
        self.numberofreplicationfieldst9 = []
        self.couplingfieldst9 = []
        self.specrulefieldst9 = []

        self.hierarchymodeltreeviewt10 = None
        self.cbnodetypet10 = None
        self.buttonst10 = []
        self.tbpropertiest10 = None
        self.attributefieldst10 = []
        self.aspectrulefieldst10 = []
        self.numberofreplicationfieldst10 = []
        self.couplingfieldst10 = []
        self.specrulefieldst10 = []

        #ui variables left side
        self.tbgeneralsettingst1 = None
        self.tbgeneralsettingst2 = None
        self.tbgeneralsettingst3 = None
        self.tbgeneralsettingst4 = None
        self.tbgeneralsettingst5 = None
        self.tbgeneralsettingst6 = None
        self.tbgeneralsettingst7 = None
        self.tbgeneralsettingst8 = None
        self.tbgeneralsettingst9 = None
        self.tbgeneralsettingst10 = None

        #ui variables ses pes
        self.rbsest1 = None
        self.rbipest1 = None
        self.rbpest1 = None
        self.rbfpest1 = None
        self.tesescommentt1 = None
        self.bsespeshelpt1 = None

        self.rbsest2 = None
        self.rbipest2 = None
        self.rbpest2 = None
        self.rbfpest2 = None
        self.tesescommentt2 = None
        self.bsespeshelpt2 = None

        self.rbsest3 = None
        self.rbipest3 = None
        self.rbpest3 = None
        self.rbfpest3 = None
        self.tesescommentt3 = None
        self.bsespeshelpt3 = None

        self.rbsest4 = None
        self.rbipest4 = None
        self.rbpest4 = None
        self.rbfpest4 = None
        self.tesescommentt4 = None
        self.bsespeshelpt4 = None

        self.rbsest5 = None
        self.rbipest5 = None
        self.rbpest5 = None
        self.rbfpest5 = None
        self.tesescommentt5 = None
        self.bsespeshelpt5 = None

        self.rbsest6 = None
        self.rbipest6 = None
        self.rbpest6 = None
        self.rbfpest6 = None
        self.tesescommentt6 = None
        self.bsespeshelpt6 = None

        self.rbsest7 = None
        self.rbipest7 = None
        self.rbpest7 = None
        self.rbfpest7 = None
        self.tesescommentt7 = None
        self.bsespeshelpt7 = None

        self.rbsest8 = None
        self.rbipest8 = None
        self.rbpest8 = None
        self.rbfpest8 = None
        self.tesescommentt8 = None
        self.bsespeshelpt8 = None

        self.rbsest9 = None
        self.rbipest9 = None
        self.rbpest9 = None
        self.rbfpest9 = None
        self.tesescommentt9 = None
        self.bsespeshelpt9 = None

        self.rbsest10 = None
        self.rbipest10 = None
        self.rbpest10 = None
        self.rbfpest10 = None
        self.tesescommentt10 = None
        self.bsespeshelpt10 = None

        #ui variables ses variables
        self.tvsesvariableviewt1 = None
        self.lesesvariablenamet1 = None
        self.lesesvariablevaluet1 = None
        self.bsesvariableinsertt1 = None
        self.bsesvariabledeletet1 = None
        self.bsesvariablehelpt1 = None

        self.tvsesvariableviewt2 = None
        self.lesesvariablenamet2 = None
        self.lesesvariablevaluet2 = None
        self.bsesvariableinsertt2 = None
        self.bsesvariabledeletet2 = None
        self.bsesvariablehelpt2 = None

        self.tvsesvariableviewt3 = None
        self.lesesvariablenamet3 = None
        self.lesesvariablevaluet3 = None
        self.bsesvariableinsertt3 = None
        self.bsesvariabledeletet3 = None
        self.bsesvariablehelpt3 = None

        self.tvsesvariableviewt4 = None
        self.lesesvariablenamet4 = None
        self.lesesvariablevaluet4 = None
        self.bsesvariableinsertt4 = None
        self.bsesvariabledeletet4 = None
        self.bsesvariablehelpt4 = None

        self.tvsesvariableviewt5 = None
        self.lesesvariablenamet5 = None
        self.lesesvariablevaluet5 = None
        self.bsesvariableinsertt5 = None
        self.bsesvariabledeletet5 = None
        self.bsesvariablehelpt5 = None

        self.tvsesvariableviewt6 = None
        self.lesesvariablenamet6 = None
        self.lesesvariablevaluet6 = None
        self.bsesvariableinsertt6 = None
        self.bsesvariabledeletet6 = None
        self.bsesvariablehelpt6 = None

        self.tvsesvariableviewt7 = None
        self.lesesvariablenamet7 = None
        self.lesesvariablevaluet7 = None
        self.bsesvariableinsertt7 = None
        self.bsesvariabledeletet7 = None
        self.bsesvariablehelpt7 = None

        self.tvsesvariableviewt8 = None
        self.lesesvariablenamet8 = None
        self.lesesvariablevaluet8 = None
        self.bsesvariableinsertt8 = None
        self.bsesvariabledeletet8 = None
        self.bsesvariablehelpt8 = None

        self.tvsesvariableviewt9 = None
        self.lesesvariablenamet9 = None
        self.lesesvariablevaluet9 = None
        self.bsesvariableinsertt9 = None
        self.bsesvariabledeletet9 = None
        self.bsesvariablehelpt9 = None

        self.tvsesvariableviewt10 = None
        self.lesesvariablenamet10 = None
        self.lesesvariablevaluet10 = None
        self.bsesvariableinsertt10 = None
        self.bsesvariabledeletet10 = None
        self.bsesvariablehelpt10 = None

        #ui variables ses functions
        self.tvsesfunctionsviewt1 = None
        self.bsesfunctioninsertt1 = None
        self.bsesfunctiondeletet1 = None
        self.bsesfunctionhelpt1 = None

        self.tvsesfunctionsviewt2 = None
        self.bsesfunctioninsertt2 = None
        self.bsesfunctiondeletet2 = None
        self.bsesfunctionhelpt2 = None

        self.tvsesfunctionsviewt3 = None
        self.bsesfunctioninsertt3 = None
        self.bsesfunctiondeletet3 = None
        self.bsesfunctionhelpt3 = None

        self.tvsesfunctionsviewt4 = None
        self.bsesfunctioninsertt4 = None
        self.bsesfunctiondeletet4 = None
        self.bsesfunctionhelpt4 = None

        self.tvsesfunctionsviewt5 = None
        self.bsesfunctioninsertt5 = None
        self.bsesfunctiondeletet5 = None
        self.bsesfunctionhelpt5 = None

        self.tvsesfunctionsviewt6 = None
        self.bsesfunctioninsertt6 = None
        self.bsesfunctiondeletet6 = None
        self.bsesfunctionhelpt6 = None

        self.tvsesfunctionsviewt7 = None
        self.bsesfunctioninsertt7 = None
        self.bsesfunctiondeletet7 = None
        self.bsesfunctionhelpt7 = None

        self.tvsesfunctionsviewt8 = None
        self.bsesfunctioninsertt8 = None
        self.bsesfunctiondeletet8 = None
        self.bsesfunctionhelpt8 = None

        self.tvsesfunctionsviewt9 = None
        self.bsesfunctioninsertt9 = None
        self.bsesfunctiondeletet9 = None
        self.bsesfunctionhelpt9 = None

        self.tvsesfunctionsviewt10 = None
        self.bsesfunctioninsertt10 = None
        self.bsesfunctiondeletet10 = None
        self.bsesfunctionhelpt10 = None

        #ui variables semantic conditions
        self.tvsemanticconditionviewt1 = None
        self.lesemanticconditiont1 = None
        self.bsemanticconditioninsertt1 = None
        self.bsemanticconditiondeletet1 = None
        self.bsemanticconditionhelpt1 = None

        self.tvsemanticconditionviewt2 = None
        self.lesemanticconditiont2 = None
        self.bsemanticconditioninsertt2 = None
        self.bsemanticconditiondeletet2 = None
        self.bsemanticconditionhelpt2 = None

        self.tvsemanticconditionviewt3 = None
        self.lesemanticconditiont3 = None
        self.bsemanticconditioninsertt3 = None
        self.bsemanticconditiondeletet3 = None
        self.bsemanticconditionhelpt3 = None

        self.tvsemanticconditionviewt4 = None
        self.lesemanticconditiont4 = None
        self.bsemanticconditioninsertt4 = None
        self.bsemanticconditiondeletet4 = None
        self.bsemanticconditionhelpt4 = None

        self.tvsemanticconditionviewt5 = None
        self.lesemanticconditiont5 = None
        self.bsemanticconditioninsertt5 = None
        self.bsemanticconditiondeletet5 = None
        self.bsemanticconditionhelpt5 = None

        self.tvsemanticconditionviewt6 = None
        self.lesemanticconditiont6 = None
        self.bsemanticconditioninsertt6 = None
        self.bsemanticconditiondeletet6 = None
        self.bsemanticconditionhelpt6 = None

        self.tvsemanticconditionviewt7 = None
        self.lesemanticconditiont7 = None
        self.bsemanticconditioninsertt7 = None
        self.bsemanticconditiondeletet7 = None
        self.bsemanticconditionhelpt7 = None

        self.tvsemanticconditionviewt8 = None
        self.lesemanticconditiont8 = None
        self.bsemanticconditioninsertt8 = None
        self.bsemanticconditiondeletet8 = None
        self.bsemanticconditionhelpt8 = None

        self.tvsemanticconditionviewt9 = None
        self.lesemanticconditiont9 = None
        self.bsemanticconditioninsertt9 = None
        self.bsemanticconditiondeletet9 = None
        self.bsemanticconditionhelpt9 = None

        self.tvsemanticconditionviewt10 = None
        self.lesemanticconditiont10 = None
        self.bsemanticconditioninsertt10 = None
        self.bsemanticconditiondeletet10 = None
        self.bsemanticconditionhelpt10 = None

        # ui variables selection constraints
        self.tvselectionconstraintsviewt1 = None
        self.bselectionconstraintsstartt1 = None
        self.bselectionconstraintsstopt1 = None
        self.bselectionconstraintscleart1 = None
        self.lstartnodenamet1 = None
        self.lstopnodenamet1 = None
        self.bselectionconstraintsinsertt1 = None
        self.bselectionconstraintsdeletet1 = None
        self.bselectionconstraintshelpt1 = None

        self.tvselectionconstraintsviewt2 = None
        self.bselectionconstraintsstartt2 = None
        self.bselectionconstraintsstopt2 = None
        self.bselectionconstraintscleart2 = None
        self.lstartnodenamet2 = None
        self.lstopnodenamet2 = None
        self.bselectionconstraintsinsertt2 = None
        self.bselectionconstraintsdeletet2 = None
        self.bselectionconstraintshelpt2 = None

        self.tvselectionconstraintsviewt3 = None
        self.bselectionconstraintsstartt3 = None
        self.bselectionconstraintsstopt3 = None
        self.bselectionconstraintscleart3 = None
        self.lstartnodenamet3 = None
        self.lstopnodenamet3 = None
        self.bselectionconstraintsinsertt3 = None
        self.bselectionconstraintsdeletet3 = None
        self.bselectionconstraintshelpt3 = None

        self.tvselectionconstraintsviewt4 = None
        self.bselectionconstraintsstartt4 = None
        self.bselectionconstraintsstopt4 = None
        self.bselectionconstraintscleart4 = None
        self.lstartnodenamet4 = None
        self.lstopnodenamet4 = None
        self.bselectionconstraintsinsertt4 = None
        self.bselectionconstraintsdeletet4 = None
        self.bselectionconstraintshelpt4 = None

        self.tvselectionconstraintsviewt5 = None
        self.bselectionconstraintsstartt5 = None
        self.bselectionconstraintsstopt5 = None
        self.bselectionconstraintscleart5 = None
        self.lstartnodenamet5 = None
        self.lstopnodenamet5 = None
        self.bselectionconstraintsinsertt5 = None
        self.bselectionconstraintsdeletet5 = None
        self.bselectionconstraintshelpt5 = None

        self.tvselectionconstraintsviewt6 = None
        self.bselectionconstraintsstartt6 = None
        self.bselectionconstraintsstopt6 = None
        self.bselectionconstraintscleart6 = None
        self.lstartnodenamet6 = None
        self.lstopnodenamet6 = None
        self.bselectionconstraintsinsertt6 = None
        self.bselectionconstraintsdeletet6 = None
        self.bselectionconstraintshelpt6 = None

        self.tvselectionconstraintsviewt7 = None
        self.bselectionconstraintsstartt7 = None
        self.bselectionconstraintsstopt7 = None
        self.bselectionconstraintscleart7 = None
        self.lstartnodenamet7 = None
        self.lstopnodenamet7 = None
        self.bselectionconstraintsinsertt7 = None
        self.bselectionconstraintsdeletet7 = None
        self.bselectionconstraintshelpt7 = None

        self.tvselectionconstraintsviewt8 = None
        self.bselectionconstraintsstartt8 = None
        self.bselectionconstraintsstopt8 = None
        self.bselectionconstraintscleart8 = None
        self.lstartnodenamet8 = None
        self.lstopnodenamet8 = None
        self.bselectionconstraintsinsertt8 = None
        self.bselectionconstraintsdeletet8 = None
        self.bselectionconstraintshelpt8 = None

        self.tvselectionconstraintsviewt9 = None
        self.bselectionconstraintsstartt9 = None
        self.bselectionconstraintsstopt9 = None
        self.bselectionconstraintscleart9 = None
        self.lstartnodenamet9 = None
        self.lstopnodenamet9 = None
        self.bselectionconstraintsinsertt9 = None
        self.bselectionconstraintsdeletet9 = None
        self.bselectionconstraintshelpt9 = None

        self.tvselectionconstraintsviewt10 = None
        self.bselectionconstraintsstartt10 = None
        self.bselectionconstraintsstopt10 = None
        self.bselectionconstraintscleart10 = None
        self.lstartnodenamet10 = None
        self.lstopnodenamet10 = None
        self.bselectionconstraintsinsertt10 = None
        self.bselectionconstraintsdeletet10 = None
        self.bselectionconstraintshelpt10 = None

        #set all fields
        self.settabfields = SetTabFields(self)
        self.settabfields.setTabFields()

        #variables
        #self.programPath = self.getProgramPath()    #not needed at the moment -> needed in function documentation() but the corresponding line is commented out
        # active tab and former active tab
        self.activeTab = self.tabs.currentIndex()
        self.formerActiveTab = -1

        #read config, create config variables and do necessary steps
        self.lastOpenedFiles = []
        self.lastOpenedFilesMenuEntrys = []
        self.readConfig()
        self.connectLastOpenedFilesMenuEntry()

        #set the file name and the last saved variables for every model
        self.filePathName = []
        self.lastsaved = []
        for x in range(0, 10):
            self.filePathName.append("")
            self.lastsaved.append("")

        #set possible nodetypes
        self.nodeTypes = ["Node", "Entity Node", "Descriptive Node", "Aspect Node", "Maspect Node", "Spec Node"]

        #set icons for nodes
        self.nodeIcon = QtGui.QIcon(QtGui.QPixmap("inode.png"))
        self.eNodeIcon = QtGui.QIcon(QtGui.QPixmap("ienode.png"))
        self.dNodeIcon = QtGui.QIcon(QtGui.QPixmap("idnode.png"))
        self.aNodeIcon = QtGui.QIcon(QtGui.QPixmap("ianode.png"))
        self.mAspectNodeIcon = QtGui.QIcon(QtGui.QPixmap("imanode.png"))
        self.specNodeIcon = QtGui.QIcon(QtGui.QPixmap("isnode.png"))
        self.nodeTypeIcons = [self.nodeIcon, self.eNodeIcon, self.dNodeIcon, self.aNodeIcon, self.mAspectNodeIcon, self.specNodeIcon]
        #set other icons
        self.mainIcon = QtGui.QIcon(QtGui.QPixmap("i2rightarrow.png"))
        self.helpIcon = QtGui.QIcon(QtGui.QPixmap("ihelp.png"))
        self.okayIcon = QtGui.QIcon(QtGui.QPixmap("iok.png"))
        self.notOkayIcon = QtGui.QIcon(QtGui.QPixmap("inok.png"))

        # read help and create help variables
        hfname = "./helptext.txt"
        self.attribhelp = []
        self.asprulehelp = []
        self.nrephelp = []
        self.couphelp = []
        self.specrulehelp = []
        self.sespeshelp = []
        self.sesvarhelp = []
        self.semconhelp = []
        self.selconhelp = []
        self.sesfunhelp = []
        try:
            helpfile = open(hfname)
            helptext = helpfile.read()
            self.attribhelp, self.asprulehelp, self.nrephelp, self.couphelp, self.specrulehelp, self.sespeshelp, self.sesvarhelp, self.semconhelp, self.selconhelp, self.sesfunhelp = self.readHelp(helptext)
        except:
            QMessageBox.information(self, "Help", "The help could not be loaded.", QtWidgets.QMessageBox.Ok)

        #build models and set sesVars, sesFuns and treeManipulate where necessary
        self.modellist = []
        for x in range(0, 10):
            self.modellist.append(self.createModel(x))
            self.modellist[x][3].setSesVarsFunsInTm()
            self.modellist[x][4].setSesVarsInSemCond()
            self.modellist[x][5].setTreeManipulateInSelCon()

        #main ui signals
        self.tabs.currentChanged.connect(self.tabWasChanged)

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.saveAction)
        self.ui.actionSaveAs.triggered.connect(self.saveAsAction)
        self.ui.actionEmpty_Current_Model.triggered.connect(self.emptyCurrentModel)
        self.ui.actionImport_XML.triggered.connect(self.importXMLAction)
        self.ui.actionExport_XML.triggered.connect(self.exportXMLAction)
        self.ui.actionAdd_SubSES.triggered.connect(self.addSubSES)
        self.ui.actionSave_SubSES.triggered.connect(self.saveSubSESAction)
        self.ui.actionImport_SubSES_XML.triggered.connect(self.importSubSESXMLAction)
        self.ui.actionExport_SubSES_XML.triggered.connect(self.exportSubSESXMLAction)
        self.ui.actionPrune.triggered.connect(self.prune)
        self.ui.actionFlatten.triggered.connect(self.flatten)
        self.ui.actionDocumentation.triggered.connect(self.documentation)
        self.ui.actionInfo.triggered.connect(self.info)
        self.ui.actionAbout.triggered.connect(self.about)

        #main ui signals - connection
        self.bserverConnect.clicked.connect(self.connectButtonPressed)
        self.bserverDisconnect.clicked.connect(self.disconnectButtonPressed)

        #connection: further signals -> detect changes in the editor -> clientSend
        #when a tab is changed, these signals need to be reconnected -> see function tabWasChanged
        self.modellist[self.activeTab][0].sespesChangedSignal.connect(self.clientSend)          #changes in the sespes
        self.modellist[self.activeTab][1].sesvarChangedSignal.connect(self.clientSend)          #changes in the sesvars
        self.modellist[self.activeTab][2].sesfunChangedSignal.connect(self.clientSend)          #changes in the sesfuns
        self.modellist[self.activeTab][3].treeChangedSignal.connect(self.clientSend)            #changes in the tree: add sub/sibling node, delete node, change type, add subtree
        self.modellist[self.activeTab][3].treeModel.treeChangedSignal.connect(self.clientSend)  #changes in ui (e.g. rename node in ui), paste changes in node specific properties
        self.modellist[self.activeTab][4].semconChangedSignal.connect(self.clientSend)          #changes in the semcons
        self.modellist[self.activeTab][5].selconChangedSignal.connect(self.clientSend)          #changes in the selcons

        #set modelname
        self.setModelname()

        #set connection variable and buttons
        self.connectionEstablished = False
        self.sendInProgress = False
        self.setConnectionButtons()

        #set variables and start the clock in the statusbar
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.getTimestring)   #connect to the function with the name getTimestring (the slot)
        self.timer.start(1000)

        #show Version in statusbar
        self.versionmessage = "Version " + __version__
        self.setFooter()

        #resize
        #self.resz()

        #show window maximized
        self.showMaximized()

        #number of mouseclicks
        self.mouseclicks = 0

        #setup keyboard shortcuts
        #openShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_O), self)
        self.openshortcut = QShortcut(QKeySequence("Shift+O"), self)
        self.openshortcut.activated.connect(self.open)
        self.saveshortcut = QShortcut(QKeySequence("Shift+S"), self)
        self.saveshortcut.activated.connect(self.saveAction)
        self.saveasshortcut = QShortcut(QKeySequence("Shift+D"), self)
        self.saveasshortcut.activated.connect(self.saveAsAction)
        self.emptyshortcut = QShortcut(QKeySequence("Shift+E"), self)
        self.emptyshortcut.activated.connect(self.emptyCurrentModelAction)

        #global dictionary to keep track of uids and nodenames
        self.uidNodenameDict = {}

        #warning, if Python / PyQt5 version is not development version
        #pythonversion = sys.version.split()[0]
        pythonversion = platform.python_version()
        pyqtversion = PYQT_VERSION_STR
        if pythonversion != "3.4.1" or pyqtversion != "5.5":
            QMessageBox.information(self, "Python / PyQt version", "SESToPy was developed using Python 3.4.1 with PyQt 5.5 for the user interface. In case you face problems, they could be due to incompatibilities to the versions you are using. You are using Python %s and PyQt %s ." % (pythonversion, pyqtversion), QtWidgets.QMessageBox.Ok)

    #-----preparation functions-----------------------------------------------------------------------------------------

    """preparation functions"""
    def createModel(self, tabnumber):
        #prepare ses/pes selection
        sesPes = SesPes(self, tabnumber)

        #prepare the ses variables
        sesVar = SesVariables(self, tabnumber)

        #prepare the ses functions
        sesFun = SesFunctions(self, tabnumber)

        #prepare the tree
        tm = TreeManipulate(self, tabnumber)

        #prepare the semantic conditions
        semCon = SemanticConditions(self, tabnumber)

        #prepare the selection constraints
        selCon = SelectionConstraints(self, tabnumber)

        return [sesPes, sesVar, sesFun, tm, semCon, selCon]

    #-----tab changed---------------------------------------------------------------------------------------------------

    def tabWasChanged(self):
        self.formerActiveTab = self.activeTab
        self.activeTab = self.tabs.currentIndex()
        self.setModelname()
        self.setFooter()

        #connection: further signals -> detect changes in the editor -> clientSend
        #when a tab is changed, these signals need to be reconnected
        self.modellist[self.activeTab][0].sespesChangedSignal.connect(self.clientSend)          #changes in the sespes
        self.modellist[self.activeTab][1].sesvarChangedSignal.connect(self.clientSend)          #changes in the sesvars
        self.modellist[self.activeTab][2].sesfunChangedSignal.connect(self.clientSend)          #changes in the sesfuns
        self.modellist[self.activeTab][3].treeChangedSignal.connect(self.clientSend)            #changes in the tree: add sub/sibling node, delete node, change type, add subtree
        self.modellist[self.activeTab][3].treeModel.treeChangedSignal.connect(self.clientSend)  #changes in ui (e.g. rename node in ui), paste changes in node specific properties
        self.modellist[self.activeTab][4].semconChangedSignal.connect(self.clientSend)          #changes in the semcons
        self.modellist[self.activeTab][5].selconChangedSignal.connect(self.clientSend)          #changes in the selcons

        #the content of the current tab shall be sent
        self.modellist[self.activeTab][3].treeChangedSignal.emit()

    #-----events--------------------------------------------------------------------------------------------------------

    """event filter"""
    def eventFilter(self, obj, event):
        if obj == self.couplingfieldst1[3] or obj == self.couplingfieldst2[3] or obj == self.couplingfieldst3[3] or obj == self.couplingfieldst4[3] or obj == self.couplingfieldst5[3] \
                or obj == self.couplingfieldst6[3] or obj == self.couplingfieldst7[3] or obj == self.couplingfieldst8[3] or obj == self.couplingfieldst9[3] or obj == self.couplingfieldst10[3]:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.modellist[self.activeTab][3].cp.fillSelectSourceNode()
        if obj == self.couplingfieldst1[4] or obj == self.couplingfieldst2[4] or obj == self.couplingfieldst3[4] or obj == self.couplingfieldst4[4] or obj == self.couplingfieldst5[4] \
                or obj == self.couplingfieldst6[4] or obj == self.couplingfieldst7[4] or obj == self.couplingfieldst8[4] or obj == self.couplingfieldst9[4] or obj == self.couplingfieldst10[4]:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.modellist[self.activeTab][3].cp.fillSelectSinkNode()
        if obj == self.couplingfieldst1[10] or obj == self.couplingfieldst2[10] or obj == self.couplingfieldst3[10] or obj == self.couplingfieldst4[10] or obj == self.couplingfieldst5[10] \
                or obj == self.couplingfieldst6[10] or obj == self.couplingfieldst7[10] or obj == self.couplingfieldst8[10] or obj == self.couplingfieldst9[10] or obj == self.couplingfieldst10[10]:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.modellist[self.activeTab][3].cp.fillSESFunSpinner()
        return False

    """resize Event"""
    def resizeEvent(self, QResizeEvent):
        self.resz()

    """exit event"""
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Close', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            #close the connection -> the client thread as well
            self.clientThread.quit()
        else:
            event.ignore()

    """right click event"""
    def contextMenuEvent(self, event):
        self.menu = QMenu(self)

        addSubNodeAction = QAction('Add SubNode', self)
        addSubNodeAction.setIcon(QIcon('iaddsubnode.png'))
        addSubNodeAction.triggered.connect(self.modellist[self.activeTab][3].addSubNode)
        self.menu.addAction(addSubNodeAction)

        addSiblingNodeAction = QAction('Add SiblingNode', self)
        addSiblingNodeAction.setIcon(QIcon('iaddsiblingnode.png'))
        addSiblingNodeAction.triggered.connect(self.modellist[self.activeTab][3].addSiblingNode)
        self.menu.addAction(addSiblingNodeAction)

        deleteNodeAction = QAction('Delete Node', self)
        deleteNodeAction.setIcon(QIcon('ideletenode.png'))
        deleteNodeAction.triggered.connect(self.modellist[self.activeTab][3].deleteNode)
        self.menu.addAction(deleteNodeAction)

        self.menu.addSeparator()

        setAspectTypeAction = QAction('Set to Aspect', self)
        setAspectTypeAction.setIcon(QIcon("ianode.png"))
        setAspectTypeAction.triggered.connect(self.modellist[self.activeTab][3].typeChangeAspect)
        self.menu.addAction(setAspectTypeAction)

        setMaspectTypeAction = QAction('Set to Maspect', self)
        setMaspectTypeAction.setIcon(QIcon("imanode.png"))
        setMaspectTypeAction.triggered.connect(self.modellist[self.activeTab][3].typeChangeMaspect)
        self.menu.addAction(setMaspectTypeAction)

        setSpecTypeAction = QAction('Set to Spec', self)
        setSpecTypeAction.setIcon(QIcon("isnode.png"))
        setSpecTypeAction.triggered.connect(self.modellist[self.activeTab][3].typeChangeSpec)
        self.menu.addAction(setSpecTypeAction)

        self.menu.popup(QtGui.QCursor.pos())

    """easter egg click event"""
    def mousePressEvent(self, QMouseEvent):
        self.mouseclicks += 1
        if self.mouseclicks == 5:
            QMessageBox.information(self, "You seem to have fun...", "Please give me some money :-) .\n\nCredits:\nResearch Group Computational Engineering and Automation at the University of Applied Sciences Wismar, Germany.", QtWidgets.QMessageBox.Ok)
        if self.mouseclicks == 10:
            QMessageBox.information(self, "You really must have fun...", "Now it is definitely time to give me a lot of money. I also take gold or platinum.", QtWidgets.QMessageBox.Ok)
        if self.mouseclicks == 15:
            QMessageBox.information(self, "You are crazy...", "...and are very brave still using this piece of buggy software.\n\nBy the way - did I get money from you?", QtWidgets.QMessageBox.Ok)
            self.mouseclicks = 0

    #-----set the modelname field and the connection buttons, clientSend function---------------------------------------

    """set the modelname field according to the selected model"""
    def setModelname(self):
        if self.filePathName[self.activeTab] == "":
            self.modelname.setText("<html><b>Model " + str(self.activeTab+1) + ": not saved</b></html>")
        else:
            fname = self.filePathName[self.activeTab].split("/")[-1].split(".")[0]
            self.modelname.setText("<html><b>Model " + str(self.activeTab+1) + ": " + fname + "</b></html>")

    """set the connection buttons"""
    def setConnectionButtons(self):
        if not self.connectionEstablished:
            self.bserverConnect.setDisabled(False)
            self.bserverDisconnect.setDisabled(True)
        else:
            self.bserverConnect.setDisabled(True)
            self.bserverDisconnect.setDisabled(False)

    """connection slots"""
    def connectButtonPressed(self):
        def checkIp(ip):
            ipOK = True
            ips = ip.split(".", 4)
            if len(ips) == 4:
                for l in ips:
                    if l.isdigit():
                        if int(l) < 256:
                            pass
                        else:
                            ipOK = False
                    else:
                        ipOK = False
            else:
                ipOK = False
            return ipOK
        def checkPort(port):
            portOK = True
            try:
                intport = int(port)
                if intport > 65535:
                    portOK = False
            except:
                portOK = False
            return portOK

        #here the function begins

        serverIP = self.serverIP.text()
        serverPort = self.serverPort.text()
        #check that these are okay
        ipok = checkIp(serverIP)
        portok = checkPort(serverPort)
        if ipok and portok:
            #set the variables in the client object
            self.clientObj.serverIP = serverIP
            self.clientObj.serverPort = int(serverPort)
            #now that the values are set, the client is connected in the thread
        else:
            QMessageBox.critical(self, "IP or Port not allowed", "The IP or the port you entered are not allowed.", QtWidgets.QMessageBox.Ok)

    #slot connected with clientConnectionSignal from client class -> set the buttons according to the success of the connection
    def onConnectPressed(self, connectionSuccessful):
        self.connectionEstablished = connectionSuccessful
        self.setConnectionButtons()
        if not connectionSuccessful:
            QMessageBox.critical(self, "No connection", "The connection could not be established. Is there a server under this IP/Port combination? If there is, please restart the server and this program.", QtWidgets.QMessageBox.Ok)
        else:
            self.clientSend()

    #slot connected with clientNoSendSignal from client class -> set the buttons when the connection is lost
    def onConnectionLost(self):
        #disconnect, when the connection is lost
        self.connectionEstablished = False
        self.setConnectionButtons()
        QMessageBox.critical(self, "Connection lost", "The connection to the server was lost and therefore the connection is resetted.", QtWidgets.QMessageBox.Ok)

    def disconnectButtonPressed(self):
        self.clientObj.serverIP = ""
        self.clientObj.serverPort = 0
        #now that the values are nulled, the client is disconnected in the thread
        self.connectionEstablished = False
        self.setConnectionButtons()

    def clientSend(self):
        if self.connectionEstablished and not self.sendInProgress and not self.modellist[self.activeTab][3].isRestoringTree:
            self.sendInProgress = True
            # tree
            nodelist = self.modellist[self.activeTab][3].treeToList(False)
            # ses/pes
            sespes = self.modellist[self.activeTab][0].outputSesPes()
            # ses variables
            sesvarlist = self.modellist[self.activeTab][1].outputSesVarList()
            # semantic conditions
            semconlist = self.modellist[self.activeTab][4].outputSemCondList()
            # selection constraints
            selconlist = self.modellist[self.activeTab][5].outputSelConsList(False, nodelist)
            selconsok = True
            if selconlist == [["", "", "", "", ""]]:
                selconlist = []
                selconsok = False
            # ses functions
            sesfunlist = self.modellist[self.activeTab][2].outputSesFunList()
            if selconsok:
                xmlstr = toXML(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist)
                self.clientObj.sendstring = xmlstr
                #the data is set so that clientObj.clientSend() can work
            self.sendInProgress = False

    #-----set the footer------------------------------------------------------------------------------------------------

    """get the timestring for the footer"""
    def getTimestring(self):     #slot for the clock in the statusbar
        timestring = strftime("%Y"+"-"+"%m"+"-"+"%d"+" / "+"%H"+":"+"%M"+":"+"%S")
        self.setFooter(timestring)

    """set the footer"""
    def setFooter(self, timestring="0000-00-00 / 00:00:00"):
        if self.filePathName[self.activeTab] == "":
            self.statusBar().showMessage(timestring + " / " + self.versionmessage)
        elif self.filePathName[self.activeTab] != "" and self.lastsaved[self.activeTab] == "":
            self.statusBar().showMessage(timestring + " / " + self.versionmessage + " / File: " + self.filePathName[self.activeTab])
        elif self.filePathName[self.activeTab] != "" and self.lastsaved[self.activeTab] != "":
            self.statusBar().showMessage(timestring + " / " + self.versionmessage + " / File: " + self.filePathName[self.activeTab] + " / Last saved: " + self.lastsaved[self.activeTab])

    #--------get program path-------------------------------------------------------------------------------------------

    """get the path of the program (this file)"""
    def getProgramPath(self):
        #self.programPath = os.path.dirname(os.path.realpath(__file__)) #problem when built as executable -> workaround: see lines below
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        #self.programPath = os.path.dirname(os.path.abspath(filename))  #difficulties in handling Windows / Linux -> therefore the next lines are used
        filenamelist = filename.split("/")
        del filenamelist[-1]
        programPath = '/'.join(filenamelist)
        programPath = programPath + "/"
        return programPath

    #--------resize-----------------------------------------------------------------------------------------------------

    """resize"""
    def resz(self):
        #resize the main splitter
        self.ui.mainsplitterm1.setSizes([100, 1, 100])
        self.ui.mainsplitterm2.setSizes([100, 1, 100])
        self.ui.mainsplitterm3.setSizes([100, 1, 100])
        self.ui.mainsplitterm3.setSizes([100, 1, 100])
        self.ui.mainsplitterm4.setSizes([100, 1, 100])
        self.ui.mainsplitterm5.setSizes([100, 1, 100])
        self.ui.mainsplitterm6.setSizes([100, 1, 100])
        self.ui.mainsplitterm7.setSizes([100, 1, 100])
        self.ui.mainsplitterm8.setSizes([100, 1, 100])
        self.ui.mainsplitterm9.setSizes([100, 1, 100])
        self.ui.mainsplitterm10.setSizes([100, 1, 100])
        #resize the general settings
        for x in range(0, 10):
            self.modellist[x][1].resz()
            self.modellist[x][2].resz()
            self.modellist[x][3].resz()
            self.modellist[x][4].resz()
            self.modellist[x][5].resz()

    #--------read config------------------------------------------------------------------------------------------------

    """read config file"""
    def readConfig(self):
        try:
            self.lastOpenedFiles = []
            self.lastOpenedFilesMenuEntrys = []
            conftext = open('./config.txt').read()
            conf = conftext.split("#")
            conf = conf[1:]
            for line in range(len(conf)):
                if conf[line] == "!LastOpenedFiles!":
                    if (line+1) <= len(conf):
                        lof = conf[line+1].split("\n")
                        self.lastOpenedFiles = [x for x in lof if x != '']   #remove '' from list
            for item in self.lastOpenedFiles:
                ac = QAction(item, self.menuFile)
                self.menuFile.addAction(ac)
                self.lastOpenedFilesMenuEntrys.append(ac)
        except:
            QMessageBox.information(self, "Configuration", "The configuration could not be loaded.", QtWidgets.QMessageBox.Ok)

    """write config file"""
    def writeConfig(self, lastOpenedFile=""):
        lastOpenedFiles = self.lastOpenedFiles
        #if lastOpenedFile is the new content
        if lastOpenedFile != "":
            #remove the old menu entries
            for item in self.lastOpenedFilesMenuEntrys:
                self.menuFile.removeAction(item)
            #now build new
            lastOpenedFiles.insert(0, lastOpenedFile)
            lastOpenedFiles = lastOpenedFiles[0:9]  #limit on 10 entries
            #remove duplicates but preserve the order
            seen = set()
            seen_add = seen.add
            lastOpenedFiles = [x for x in lastOpenedFiles if not (x in seen or seen_add(x))]
        #write the new contents
        conffile = open('./config.txt', 'w')
        conffile.write('#!LastOpenedFiles!#\n')
        for item in lastOpenedFiles:
            conffile.write("%s\n" % item)
        conffile.close()
        #now read the new config
        self.readConfig()

    """connect the signals in lastOpenedFilesMenuEntry"""
    def connectLastOpenedFilesMenuEntry(self):
        self.mapper = QtCore.QSignalMapper(self)
        for i in range(len(self.lastOpenedFilesMenuEntrys)):
            menutext = self.lastOpenedFiles[i]
            action = self.lastOpenedFilesMenuEntrys[i]
            self.mapper.setMapping(action, menutext)
            action.triggered.connect(self.mapper.map)
        self.mapper.mapped['QString'].connect(self.open)

    #--------read help--------------------------------------------------------------------------------------------------

    """read help file"""
    def readHelp(self, helptext):
        attribhelp = []
        asprulehelp = []
        nrephelp = []
        couphelp = []
        specrulehelp = []
        sespeshelp = []
        sesvarhelp = []
        semconhelp = []
        selconhelp = []
        sesfunhelp = []
        helptext = helptext.replace(";\n", ";")
        helptext = helptext.replace("\\n", "\n")
        helptext = helptext.replace('\\"', '\"')
        help = helptext.split(";")
        for i in range(len(help)):
            if help[i] == "attribhelp":
                attribhelp.append(help[i + 1])
                attribhelp.append(help[i + 2])
            if help[i] == "asprulehelp":
                asprulehelp.append(help[i + 1])
                asprulehelp.append(help[i + 2])
            if help[i] == "nrephelp":
                nrephelp.append(help[i + 1])
                nrephelp.append(help[i + 2])
            if help[i] == "couphelp":
                couphelp.append(help[i + 1])
                couphelp.append(help[i + 2])
            if help[i] == "specrulehelp":
                specrulehelp.append(help[i + 1])
                specrulehelp.append(help[i + 2])
            if help[i] == "sespeshelp":
                sespeshelp.append(help[i + 1])
                sespeshelp.append(help[i + 2])
            if help[i] == "sesvarhelp":
                sesvarhelp.append(help[i + 1])
                sesvarhelp.append(help[i + 2])
            if help[i] == "semconhelp":
                semconhelp.append(help[i + 1])
                semconhelp.append(help[i + 2])
            if help[i] == "selconhelp":
                selconhelp.append(help[i + 1])
                selconhelp.append(help[i + 2])
            if help[i] == "sesfunhelp":
                sesfunhelp.append(help[i + 1])
                sesfunhelp.append(help[i + 2])
        return (attribhelp, asprulehelp, nrephelp, couphelp, specrulehelp, sespeshelp, sesvarhelp, semconhelp, selconhelp, sesfunhelp)

    #--------Open / Save------------------------------------------------------------------------------------------------

    """Open"""
    def importXMLAction(self):
        self.open("", True)

    def open(self, filenameToOpen="", exXML=False):
        if filenameToOpen == '' or not filenameToOpen:  #sometimes the check for empty string functions, sometimes the bool check
            if not exXML:
                fname = QFileDialog.getOpenFileName(self, "Open an SES from JSON", '', "JSON SES Tree (*.jsonsestree);;All files (*)")
            else:
                fname = QFileDialog.getOpenFileName(self, "Import an SES from XML", '', "XML SES Tree (*.xml);;All files (*)")
        else:
            fname = (filenameToOpen, 'SES Tree (*.jsonsestree)')
        if not fname:
            self.setModelname()
            self.setFooter()
            return
        loadDialog = QDialog()
        #l = QLabel(loadDialog)
        #l.setText("Loading. Please Wait.")
        loadDialog.setWindowIcon(self.mainIcon)
        loadDialog.setWindowTitle("Loading. Please wait.")
        loadDialog.setModal(True)
        #loadDialog.setWindowModality(Qt.NonModal)
        try:
            if not (fname[0] == "" and fname[1] == ""):     #only if a new file is selected
                loadDialog.show()
                if not exXML:
                    self.filePathName[self.activeTab] = str(fname[0])
                    success = self.restore()
                    if success:
                        self.filePathName[self.activeTab] = str(fname[0])   #if the model was emptied, the filePathName was reset -> set it again anyway
                        self.setModelname()
                        self.setFooter()
                        self.writeConfig(str(fname[0])) #write the last opened files in the config
                        self.connectLastOpenedFilesMenuEntry()  #reconnect the entries
                else:
                    success = self.restore(exXML, str(fname[0]))
                loadDialog.close()
        except:
            loadDialog.close()
            QMessageBox.critical(self, "Can not open file", "Error opening \"%s\"." % str(fname[0]), QtWidgets.QMessageBox.Ok)
            self.filePathName[self.activeTab] = ""
            self.setModelname()
            self.setFooter()
            return

    """open the saved file"""
    def restore(self, exXML=False, filePathName=""):
        if not exXML:
            f = open(self.filePathName[self.activeTab], "r")
        else:
            f = open(filePathName, "r")
        filestr = f.read()
        f.close()
        isemptymodel = False
        nodelist = self.modellist[self.activeTab][3].treeToList()
        sesvarlist = self.modellist[self.activeTab][1].outputSesVarList()
        semconlist = self.modellist[self.activeTab][4].outputSemCondList()
        selconlist = self.modellist[self.activeTab][5].outputSelConsList()
        sesfunlist = self.modellist[self.activeTab][2].outputSesFunList()
        if len(nodelist) == 1 and nodelist[0][1] == 'Node' and nodelist[0][2] == 'SES' and nodelist[0][3] == 'None' and len(sesvarlist) == 0 and len(semconlist) == 0 and len(selconlist) == 0 and len(sesfunlist) == 0:
            isemptymodel = True
        if not isemptymodel:
            reply = QMessageBox.question(self, "Model not empty", "The model is not empty. Shall I empty it? Unsaved changes will be lost.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.emptyCurrentModel(True)
                isemptymodel = True
            else:
                pass

        if isemptymodel:
            loadtime = ""
            if not exXML:
                okay, nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist, loadtime = fromJSON(filestr)
            else:
                okay, nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist = fromXML(filestr)
            #it may be no subtree -> check depth
            if nodelist[0][12] == '0':
                if okay:
                    #ses pes
                    self.modellist[self.activeTab][0].fromSave(sespes)
                    #ses variables
                    if sesvarlist:
                        self.modellist[self.activeTab][1].fromSave(sesvarlist)
                    #ses functions
                    if sesfunlist:
                        self.modellist[self.activeTab][2].fromSave(sesfunlist)
                    #nodelist
                    if nodelist:
                        self.modellist[self.activeTab][3].fromSave(nodelist)
                    #semantic conditions
                    if semconlist:
                        self.modellist[self.activeTab][4].fromSave(semconlist)
                    #selection constraints
                    if selconlist:
                        self.modellist[self.activeTab][5].fromSave(selconlist)
                    #time
                    if loadtime != "":
                        self.lastsaved[self.activeTab] = loadtime[9:].replace(" ", " - ")
                    # recalculate all decision nodes if imported
                    if exXML:
                        self.modellist[self.activeTab][1].sesvarChangedSignal.emit()
                        self.modellist[self.activeTab][2].sesfunChangedSignal.emit()
                    #return
                    return True
                else:
                    QMessageBox.critical(self, "Can not insert", "Can not insert. The file is created by a new SES-Editor version, is corrupt, manipulated or constructed with another program.", QtWidgets.QMessageBox.Ok)
                    return False
            else:
                QMessageBox.critical(self, "Can not insert", "Can not insert. The depth of the first node is not zero.", QtWidgets.QMessageBox.Ok)
                return False
        else:
            QMessageBox.critical(self, "Can not insert", "Can not insert. The model is not empty.", QtWidgets.QMessageBox.Ok)
            return False

    """Save"""
    def saveAction(self):
        self.save()

    def saveAsAction(self):
        self.save(True, False)

    def exportXMLAction(self):
        self.save(True, False, True)

    def saveSubSESAction(self):
        self.save(False, True)

    def exportSubSESXMLAction(self):
        self.save(True, True, True)

    def save(self, saveAs=False, subSES=False, asXML=False):
        def error():
            QMessageBox.critical(self, "File not saved", "Error saving \"%s\"" % str(fname[0]), QtWidgets.QMessageBox.Ok)
            self.filePathName[self.activeTab] = ""
            self.lastsaved[self.activeTab] = ""

        if not subSES:
            if self.filePathName[self.activeTab] == "" or saveAs:   #file is not saved yet or saveAs is selected
                if not asXML:
                    fname = QFileDialog.getSaveFileName(self, "Save an SES as JSON", '', "JSON SES Tree (*.jsonsestree);;All files (*)")
                else:
                    fname = QFileDialog.getSaveFileName(self, "Export an SES to XML", '', "XML SES Tree (*.xml);;All files (*)")
                if not fname:
                    self.setModelname()
                    self.setFooter()
                    return
                try:
                    if not (fname[0] == "" and fname[1] == ""):     #only if a new file is selected
                        filepathname = str(fname[0])   #in KDE the fileending is added automatically, in other Linux based environments it is not -> deal with it
                        if not asXML:
                            if "jsonsestree" not in filepathname[-11:]:
                                filepathname = filepathname + ".jsonsestree"
                            self.filePathName[self.activeTab] = filepathname
                            self.lastsaved[self.activeTab] = strftime("%Y"+"-"+"%m"+"-"+"%d"+" - "+"%H"+":"+"%M"+":"+"%S")
                            self.buildsave(False, "", asXML)
                            self.setModelname()
                            self.setFooter()
                            self.writeConfig(filepathname) #write file in last selected files
                        if asXML:
                            if "xml" not in filepathname[-3:]:
                                filepathname = filepathname + ".xml"
                            self.buildsave(False, filepathname, asXML)
                        self.connectLastOpenedFilesMenuEntry()  # reconnect the entries
                except IOError:
                    error()
                    self.setModelname()
                    self.setFooter()
                    return
            else:   #file is saved already -> filePathName not ""
                try:
                    self.lastsaved[self.activeTab] = strftime("%Y" + "-" + "%m" + "-" + "%d" + " - " + "%H" + ":" + "%M" + ":" + "%S")
                    self.buildsave(False, "", asXML)
                    self.setModelname()
                    self.setFooter()
                except IOError:
                    error()
                    self.lastsaved[self.activeTab] = ""
                    self.setModelname()
                    self.setFooter()
                    return
        else:
            try:
                nodelist = self.modellist[self.activeTab][3].treeToList(True)
                if not asXML:
                    fname = QFileDialog.getSaveFileName(self, "Save a Sub SES as JSON", nodelist[0][2]+"_subSES", "JSON SES Tree (*.jsonsestree);;All files (*)")
                else:
                    fname = QFileDialog.getSaveFileName(self, "Export a Sub SES to XML", nodelist[0][2]+"_subSES", "XML SES Tree (*.xml);;All files (*)")
                if not fname:
                    return
                try:
                    filepathname = str(fname[0])  # in KDE the fileending is added automatically, in other Linux based environments it is not -> deal with it
                    if not asXML:
                        if "jsonsestree" not in filepathname[-11:]:
                            filepathname = filepathname + ".jsonsestree"
                    if asXML:
                        if "xml" not in filepathname[-3:]:
                            filepathname = filepathname + ".xml"
                    self.buildsave(subSES, filepathname, asXML)
                except IOError:
                    error()
                    return
            except:
                #there is no entry, it cannot be done anything
                QMessageBox.critical(self, "Can not save", "Can not save subtree. Please select an entity node.", QtWidgets.QMessageBox.Ok)

    """building the file for saving"""
    def buildsave(self, subSES=False, fPN="", asXML=False):
        # tree
        nodelist = self.modellist[self.activeTab][3].treeToList(subSES)
        # ses/pes
        sespes = self.modellist[self.activeTab][0].outputSesPes()
        # ses variables
        sesvarlist = self.modellist[self.activeTab][1].outputSesVarList()
        # semantic conditions
        semconlist = self.modellist[self.activeTab][4].outputSemCondList()
        # selection constraints
        selconlist = self.modellist[self.activeTab][5].outputSelConsList(subSES, nodelist)
        selconsok = True
        if selconlist == [["", "", "", "", ""]]:
            selconlist = []
            selconsok = False
        # ses functions
        sesfunlist = self.modellist[self.activeTab][2].outputSesFunList()
        # in JSON oder XML
        if selconsok:
            if not asXML:
                filestr = toJSON(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist)
            else:
                filestr = toXML(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist)
            # write
            if not nodelist and subSES:
                QMessageBox.information(None, "Nothing exported", "Maybe you did not select an entity node.", QtWidgets.QMessageBox.Ok)
            else:
                if not subSES and fPN == "":
                    f = open(self.filePathName[self.activeTab], "w")
                elif not subSES and fPN != "":  #just to make clear, could also be in else-branch
                    f = open(fPN, "w")
                else:
                    f = open(fPN, "w")
                f.write(filestr)
                # close
                f.close()

    #--------empty current model----------------------------------------------------------------------------------------
    def emptyCurrentModelAction(self):
        self.emptyCurrentModel(False)

    def emptyCurrentModel(self, noquestion, modelnrtoempty=-1):
        if modelnrtoempty == -1:
            modeltoempty = self.activeTab
        else:
            modeltoempty = modelnrtoempty
        answer = 0
        msgBox = QMessageBox()
        if not noquestion:
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowIcon(self.mainIcon)
            msgBox.setWindowTitle("Empty model")
            msgBox.setTextFormat(Qt.RichText)
            msgBox.setText("Do you really want to empty the model?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            answer = msgBox.exec()
        if noquestion or answer == msgBox.Yes:
            self.filePathName[modeltoempty] = ""
            self.lastsaved[modeltoempty] = ""
            self.setModelname()
            self.setFooter()
            self.modellist[modeltoempty][3].deleteNode(True)
            self.modellist[modeltoempty][0].deleteSesPes()
            self.modellist[modeltoempty][1].deleteSesVariable(-1, False, True)
            self.modellist[modeltoempty][2].deleteSesFun(True)
            self.modellist[modeltoempty][4].deleteSemCond(-1, False, True)
            self.modellist[modeltoempty][5].deleteSelCon(-1, True)
            return True
        return False

    #--------SubSES-----------------------------------------------------------------------------------------------------

    """open a subSES"""
    def importSubSESXMLAction(self):
        self.addSubSES(True)

    def addSubSES(self, exXML=False):
        if not exXML:
            fname = QFileDialog.getOpenFileName(self, "Add a Sub SES to an SES (from JSON)", '', "JSON SES Tree (*.jsonsestree);;All files (*)")
        else:
            fname = QFileDialog.getOpenFileName(self, "Add a Sub SES to an SES (import from XML)", '', "XML SES Tree (*.xml);;All files (*)")
        if not fname:
            return
        try:
            self.restoreSubSES(str(fname[0]), exXML)
        except:
            if not (fname[0] == "" and fname[1] == ""):
                QMessageBox.critical(self, "Can not open file for subtree", "Error opening \"%s\"." % str(fname[0]), QtWidgets.QMessageBox.Ok)
            return

    """open the saved subSES"""
    def restoreSubSES(self, filename, exXML):
        f = open(filename, "r")
        filestr = f.read()
        isemptymodel = True
        nodelist = self.modellist[self.activeTab][3].treeToList()
        if (len(nodelist) > 1) or (len(nodelist) == 1 and nodelist[0][1] != 'Node' and nodelist[0][2] != 'SES' and nodelist[0][3] != 'None'):
            isemptymodel = False
        if not isemptymodel:
            if not exXML:
                okay, nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist, loadtime = fromJSON(filestr)
            else:
                okay, nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist = fromXML(filestr)
            if okay:
                if nodelist:
                    #nodelist
                    amok = self.modellist[self.activeTab][3].fromSave(nodelist, True, selconlist)
                    if amok:
                        #ses variables
                        if sesvarlist:
                            self.modellist[self.activeTab][1].fromSave(sesvarlist, True)
                        #ses functions
                        if sesfunlist:
                            self.modellist[self.activeTab][2].fromSave(sesfunlist, True)
                        #semantic conditions
                        if semconlist:
                            self.modellist[self.activeTab][4].fromSave(semconlist, True)
                        #selection constraints -> now in the restoring of the nodelist since uids have to be updated
                        #if selconlist:
                            #self.modellist[self.activeTab][5].fromSave(selconlist, True)
                        # recalculate all decision nodes if imported
                        if exXML:
                            self.modellist[self.activeTab][1].sesvarChangedSignal.emit()
                            self.modellist[self.activeTab][2].sesfunChangedSignal.emit()
                        QMessageBox.information(self, "Please check", "You inserted a SubSES. Please check the general settings and the SubSES.", QtWidgets.QMessageBox.Ok)
                    if not amok:
                        QMessageBox.critical(self, "Can not insert", "Can not insert. The node in which the SubSES shall be inserted does not have the same name as the first node of the subtree, at least one of the nodenames already exists or the alternating mode would not be satisfied.", QtWidgets.QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Can not insert", "Can not insert. The file is created by a new SES-Editor version, is corrupt, manipulated or constructed with another program.", QtWidgets.QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Can not insert", "Can not insert subtree. The model is empty.", QtWidgets.QMessageBox.Ok)
        f.close()

    #--------prune------------------------------------------------------------------------------------------------------

    def prune(self):
        self.prune = Prune
        self.prune.pruneMain(Prune, "", "", "", True, self)

    #--------flatten----------------------------------------------------------------------------------------------------

    def flatten(self):
        self.flatten = Flatten
        self.flatten.flattenMain(Flatten, "", "", True, self)

    #--------documentation----------------------------------------------------------------------------------------------

    """documentation"""
    def documentation(self):
        #QDesktopServices.openUrl(QUrl(self.programPath + "Documentation/Doc_LaTeX/doc.pdf"))
        if not QDesktopServices.openUrl(QUrl("file:Documentation/Doc_LaTeX/doc.pdf")):
            QDesktopServices.openUrl(QUrl("file:doc.pdf"))  #if the doc.pdf is in the main folder (e.g. after building executable)


    #--------info-------------------------------------------------------------------------------------------------------

    """info"""
    def info(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("SESToPy: Info")
        msgBox.setWindowIcon(self.helpIcon)
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setText("If you use this program, please help with the publication by referencing it in your papers.")
        msgBox.setInformativeText("Further information is available in the documentation and on this website: "
									"<a href='https://www.cea-wismar.de'>Research Group Computational Engineering and Automation, "
									"University of Applied Sciences Wismar, Germany</a>")
        #msgBox.setDetailedText("The details are as follows:")
        #msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()

    #--------about------------------------------------------------------------------------------------------------------

    """about"""
    def about(self):
        QMessageBox.information(self, "SESToPy: About", "Credits:\n\nResearch Group Computational Engineering and Automation (CEA) "
                                                    "at the University of Applied Sciences Wismar, Germany.\n\nThe program was "
                                                    "created by Hendrik Martin Folkerts with support from Thorsten Pawletta, "
                                                    "Sven Pawletta, and the Research Group CEA.", QtWidgets.QMessageBox.Ok)

#-----execute program---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #check if the application is called for pruning or flattening -> no graphical interface shall be started -> sys.argv contains two elements
    if len(sys.argv) == 1:
        window = Main(None)
        window.show()
        sys.exit(app.exec_())
    if len(sys.argv) > 1:
        printHowToCall = False

        if sys.argv[1] == "-h" or sys.argv[1] == "--help":         #help called
            printHowToCall = True

        elif sys.argv[1] != "-p" and sys.argv[1] != "-f":         #no switch to prune or to flatten
            printHowToCall = True

        elif sys.argv[1] == "-p" and len(sys.argv) != 4 and len(sys.argv) != 6:   #length of arguments does not fit at all for pruning
            printHowToCall = True
        elif sys.argv[1] == "-f" and len(sys.argv) != 3 and len(sys.argv) != 5:   #length of arguments does not fit at all for flattening
            printHowToCall = True

        elif sys.argv[1] == "-p" and len(sys.argv) == 6 and sys.argv[4] != "-o":  #pruning: an output tree shall be defined, but the switch to define the pestree is not given
            printHowToCall = True
        elif sys.argv[1] == "-f" and len(sys.argv) == 5 and sys.argv[3] != "-o":  #flattening: an output tree shall be defined, but the switch to define the fpestree is not given
            printHowToCall = True

        elif sys.argv[1] == "-p" and len(sys.argv) == 6 and sys.argv[4] == "-o" and sys.argv[2] == sys.argv[5]:   #pruning: same name of input file and output file
            printHowToCall = True
            print("\nThe SES and the PES have the same name.")
        elif sys.argv[1] == "-f" and len(sys.argv) == 5 and sys.argv[3] == "-o" and sys.argv[2] == sys.argv[4]:   #flattening: same name of input file and output file
            printHowToCall = True
            print("\nThe PES and the FPES have the same name.")

        elif sys.argv[1] == "-p" and len(sys.argv) == 6 and sys.argv[4] == "-o" and sys.argv[5][-12:] != ".jsonsestree":   #wrong ending of the PES filename
            printHowToCall = True
            print("\nThe PES file name does not have the ending \".jsonsestree\".")
        elif sys.argv[1] == "-f" and len(sys.argv) == 5 and sys.argv[3] == "-o" and sys.argv[4][-12:] != ".jsonsestree":   #wrong ending of the FPES filename
            printHowToCall = True
            print("\nThe FPES file name does not have the ending \".jsonsestree\".")

        if printHowToCall:
            print("\n")
            print("For pruning please call \"python3 main.py -p /path/to/sesfilename.jsonsestree [list of SES variables]\" e.g. \"python3 main.py -p /home/linux/ses.jsonsestree [A=1,B=2,C=3]\".")
            print("If you also want to specify an output file please call \"python3 main.py -p /path/to/sesfilename.jsonsestree [list of SES variables] -o /path/to/pesfilename.jsonsestree\" e.g. \"python3 main.py -p /home/linux/ses.jsonsestree [A=1,B=2,C=3] -o /home/linux/pes.jsonsestree\".")
            print("\n")
            print("For flattening please call \"python3 main.py -f /path/to/pesfilename.jsonsestree\" e.g. \"python3 main.py -f /home/linux/pes.jsonsestree\".")
            print("If you also want to specify an output file please call \"python3 main.py -f /path/to/pesfilename.jsonsestree -o /path/to/fpesfilename.jsonsestree\" e.g. \"python3 main.py -f /home/linux/pes.jsonsestree -o /home/linux/fpes.jsonsestree\".")
            print("\n")
            print("Remember to take the operating system's specific folder separator (/ or \) and the command \"python3\" may just be called \"python\" in Windows.")
            print("Exiting the program.")
            print("\n")
        else:
            #pruning or flattening
            if sys.argv[1] == "-p":     #pruning
                sesfile = sys.argv[2]
                sesvars = sys.argv[3]
                pesfile = ""
                if len(sys.argv) == 6 and sys.argv[4] == "-o":
                    pesfile = sys.argv[5]
                #check if the path is okay and it could be an SES JSON file
                if not Path(sesfile).is_file() or splitext(sesfile)[1] != ".jsonsestree":
                    #the file does not exist
                    print("The file containing the SES as JSON you stated does not exist or is no file with the ending \"jsonsestree\". Exiting the program.")
                else:
                    #now check the SES variables
                    if not (sesvars[0] == "[" and sesvars[-1] == "]"):
                        print("Please give a list of SES variables in the form [a=1,b=2,c=3]. Exiting the program.")
                    else:
                        sesvars = sesvars[1:-1]
                        sesvarlist = sesvars.split(",")
                        sesvarlist = [x.strip(' ') for x in sesvarlist]

                        if pesfile == "":   #only create the filename if it is not given
                            #pesfile = splitext(sesfile)[0]+"_pruned_"+"_".join(sesvarlist)+".jsonsestree"  #sesvars in filename of pes
                            #pesfile = pesfile.replace("=", "e").replace("'","").replace('"', '')
                            pesfile = splitext(sesfile)[0] + "_pruned.jsonsestree"

                        print("\nPruning using the SES file: "+sesfile)
                        print("Using the SES variables: "+sesvars)
                        print("The PES file will be saved as: "+pesfile+"\n")

                        #now prune
                        Prune.pruneMain(Prune, sesfile, sesvarlist, pesfile)

            elif sys.argv[1] == "-f":   #flattening
                pesfile = sys.argv[2]
                fpesfile = ""
                if len(sys.argv) == 5 and sys.argv[3] == "-o":
                    fpesfile = sys.argv[4]
                #check if the path is okay and it could be a PES JSON file
                if not Path(pesfile).is_file() or splitext(pesfile)[1] != ".jsonsestree":
                    #the file does not exist
                    print("The file containing the PES as JSON you stated does not exist or is no file with the ending \"jsonsestree\". Exiting the program.")
                else:
                    if fpesfile == "":  # only create the filename if it is not given
                        fpesfile = splitext(pesfile)[0] + "_flattened" + ".jsonsestree"

                    print("\nFlattening using the PES file: " + pesfile)
                    print("The FPES file will be saved as: " + fpesfile + "\n")

                    #now flatten
                    Flatten.flattenMain(Flatten, pesfile, fpesfile)