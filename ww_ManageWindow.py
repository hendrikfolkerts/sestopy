# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

class ManageWindow:
    def __init__(self, propertiesToolBox, treeModel, treeSelectionModel, hMTV):
        self.propertiesToolBox = propertiesToolBox
        self.tmo = treeModel
        self.tsm = treeSelectionModel
        self.hmtv = hMTV

        self.propertiesToolBox.setItemEnabled(0, False)
        self.propertiesToolBox.setItemEnabled(1, False)
        self.propertiesToolBox.setItemEnabled(2, False)
        self.propertiesToolBox.setItemEnabled(3, False)
        self.propertiesToolBox.setItemEnabled(4, False)
        self.propertiesToolBox.setItemEnabled(5, False)
        self.propertiesToolBox.setCurrentIndex(0)

        #Signale
        self.tsm.currentChanged.connect(self.setDisplayNodeType)


    def setDisplayNodeType(self):
        actualNodeType = self.tmo.getNode(self.hmtv.currentIndex()).typeInfo()

        if actualNodeType == "Entity Node":
            self.propertiesToolBox.setItemEnabled(0, False)
            self.propertiesToolBox.setItemEnabled(1, True)
            self.propertiesToolBox.setItemEnabled(2, False)
            self.propertiesToolBox.setItemEnabled(3, False)
            self.propertiesToolBox.setItemEnabled(4, False)
            self.propertiesToolBox.setItemEnabled(5, False)
            self.propertiesToolBox.setCurrentIndex(1)
        elif actualNodeType == "Descriptive Node":
            self.propertiesToolBox.setItemEnabled(0, False)
            self.propertiesToolBox.setItemEnabled(1, False)
            self.propertiesToolBox.setItemEnabled(2, False)
            self.propertiesToolBox.setItemEnabled(3, False)
            self.propertiesToolBox.setItemEnabled(4, False)
            self.propertiesToolBox.setItemEnabled(5, False)
            self.propertiesToolBox.setCurrentIndex(0)
        elif actualNodeType == "Aspect Node":
            self.propertiesToolBox.setItemEnabled(0, False)
            self.propertiesToolBox.setItemEnabled(1, False)
            self.propertiesToolBox.setItemEnabled(2, True)
            self.propertiesToolBox.setItemEnabled(3, False)
            self.propertiesToolBox.setItemEnabled(4, True)
            self.propertiesToolBox.setItemEnabled(5, False)
            self.propertiesToolBox.setCurrentIndex(2)
        elif actualNodeType == "Maspect Node":
            self.propertiesToolBox.setItemEnabled(0, False)
            self.propertiesToolBox.setItemEnabled(1, False)
            self.propertiesToolBox.setItemEnabled(2, True)
            self.propertiesToolBox.setItemEnabled(3, True)
            self.propertiesToolBox.setItemEnabled(4, True)
            self.propertiesToolBox.setItemEnabled(5, False)
            self.propertiesToolBox.setCurrentIndex(2)
        elif actualNodeType == "Spec Node":
            self.propertiesToolBox.setItemEnabled(0, False)
            self.propertiesToolBox.setItemEnabled(1, False)
            self.propertiesToolBox.setItemEnabled(2, False)
            self.propertiesToolBox.setItemEnabled(3, False)
            self.propertiesToolBox.setItemEnabled(4, False)
            self.propertiesToolBox.setItemEnabled(5, True)
            self.propertiesToolBox.setCurrentIndex(5)
        else:           #NodeType is "Node"
            self.propertiesToolBox.setItemEnabled(0, False)
            self.propertiesToolBox.setItemEnabled(1, False)
            self.propertiesToolBox.setItemEnabled(2, False)
            self.propertiesToolBox.setItemEnabled(3, False)
            self.propertiesToolBox.setItemEnabled(4, False)
            self.propertiesToolBox.setItemEnabled(5, False)
            self.propertiesToolBox.setCurrentIndex(0)