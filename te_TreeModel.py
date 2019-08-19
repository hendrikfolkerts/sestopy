# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from te_TreeNode import *

"""Tree Model for View"""
class TreeModel(QAbstractItemModel):

    nameChangedSignal = pyqtSignal()
    attributeInsertedSignal = pyqtSignal()
    aspectruleInsertedSignal = pyqtSignal()
    priorityInsertedSignal = pyqtSignal()
    numrepInsertedSignal = pyqtSignal()
    couplingInsertedSignal = pyqtSignal()
    specruleInsertedSignal = pyqtSignal()
    treeChangedSignal = pyqtSignal()

    """INPUTS: Node, QObject"""
    def __init__(self, root, treeview, parent=None):
        super(TreeModel, self).__init__(parent)
        self._rootNode = root
        self.treeview = treeview

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()
    
    """number of columns in TreeView Window"""
    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 8
    
    """display something on view"""
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()  #get our node to display

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole: #role == QtCore.Qt.EditRole assures, that the name does not disappear when starting to edit (double click on node name) 
            if index.column() == 0:     #0 is the first column
                return node.name()
            if index.column() == 1:     #1 is the second column
                if node.typeInfo() != "Node":
                    return node.typeInfo()[:-5]
                else:
                    return node.typeInfo()
            if index.column() == 2:     #2 is the third column -> show if there is an attribute mb
                if node.typeInfo() == "Entity Node":
                    for attrib in node.attributes:
                        if attrib[0] == "MB" or attrib[0] == "mb":
                            return attrib[1]
            if index.column() == 3:
                if node.typeInfo() == "Entity Node":
                    if len(node.attributes) > 0:
                        return "x"
                #rb = QRadioButton(self.treeview)
                #rb.setChecked(False)
                #rb.show()
                #if node.typeInfo() == "Entity Node":
                    #if len(node.attributes) > 0:
                        #rb.setChecked(True)
            if index.column() == 4:
                if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
                    #if len(node.aspectrule) > 0:
                        #return "x"
                    #now every node has one single aspectrule, so look if the condition field contains an entry
                    if node.aspectrule and node.aspectrule[0][2] != "":
                        return "x"
            if index.column() == 5:
                if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
                    if len(node.coupling) > 0:
                        return "x"
            if index.column() == 6:
                if node.typeInfo() == "Spec Node":
                    for i in range(len(node.specrule)):
                        if node.specrule[i][2] != "":
                            return "x"

                #which properties are set for the node -> replaced by x (see above)
                """
                nodeproperties = ""
                if node.typeInfo() == "Entity Node":
                    if node.attributes:
                        nodeproperties = "Attributes"
                if node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node":
                    if node.aspectrule:
                        nodeproperties = "Aspectrules"
                    if node.coupling and nodeproperties == "":
                        nodeproperties = "Couplings"
                    if node.coupling and nodeproperties == "":
                        nodeproperties = nodeproperties + ", Couplings"
                if node.typeInfo() == "Spec Node":
                    if node.specrule:
                        nodeproperties = "Specrules"
                return nodeproperties
                """
            if index.column() == 7:
                return node.getUid()

        #icons
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:   #in first column (column0)
                typeInfo = node.typeInfo()
                if typeInfo == "Entity Node":
                    return QtGui.QIcon(QtGui.QPixmap("ienode.png"))    #icon from icons_rc.py
                elif typeInfo == "Descriptive Node":
                    return QtGui.QIcon(QtGui.QPixmap("idnode.png"))    #icon from icons_rc.py
                elif typeInfo == "Aspect Node":
                    return QtGui.QIcon(QtGui.QPixmap("ianode.png"))    #icon from icons_rc.py
                elif typeInfo == "Maspect Node":
                    return QtGui.QIcon(QtGui.QPixmap("imanode.png"))    #icon from icons_rc.py
                elif typeInfo == "Spec Node":
                    return QtGui.QIcon(QtGui.QPixmap("isnode.png"))    #icon from icons_rc.py
                else:   #typeInfo() is "node"
                    return QtGui.QIcon(QtGui.QPixmap("inode.png"))    #icon from icons_rc.py

        #background color
        #if role == QtCore.Qt.BackgroundRole:
            #redBackground = QBrush(Qt.red)
            #return redBackground

        #text color
        if role == QtCore.Qt.ForegroundRole:
            color = QColor()
            color.setNamedColor(node.color())
            return color

        #bold text
        if role == QtCore.Qt.FontRole:
            if node.bold() == True:
                bold = QFont()
                bold.setBold(True)
                return bold


    """to make data editable (is for example called double clicking and editing a node name)"""
    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole, bold=False):

        if index.isValid():
            
            if role == QtCore.Qt.EditRole:
                
                node = index.internalPointer()
                node.setName(value)

                self.nameChangedSignal.emit()
                self.treeChangedSignal.emit()
                
                return True

            if role == QtCore.Qt.ForegroundRole:

                node = index.internalPointer()
                node.setColor(value)
                self.treeChangedSignal.emit()

                return True

            if role == QtCore.Qt.FontRole:

                node = index.internalPointer()
                node.setBold(value)
                self.treeChangedSignal.emit()

        return False

    """insert the node specific properties into the corresponding lists of the nodes"""
    def insertNodeSpecProp(self, index, value, listtype, uid, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                if node.getUid() == uid:
                    if listtype == "attriblist" and node.typeInfo() == "Entity Node":
                        node.setAttributes(value)
                        self.attributeInsertedSignal.emit()
                    elif listtype == "asprulelist" and (node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node"):
                        node.setAspectrules(value)
                        self.aspectruleInsertedSignal.emit()
                    elif listtype == "prio" and (node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node"):
                        node.setPriority(value)
                        self.priorityInsertedSignal.emit()
                    elif listtype == "numrep" and node.typeInfo() == "Maspect Node":
                        node.setNumberReplication(value)
                        self.numrepInsertedSignal.emit()
                    elif listtype == "couplinglist" and (node.typeInfo() == "Aspect Node" or node.typeInfo() == "Maspect Node"):
                        node.setCoupling(value)
                        self.couplingInsertedSignal.emit()
                    elif listtype == "specrulelist" and node.typeInfo() == "Spec Node":
                        node.setSpecrules(value)
                        self.specruleInsertedSignal.emit()
        self.treeChangedSignal.emit()

    """display something on view header"""
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:        #in first column of the header display "Tree"
                return "Tree"
            elif section == 1:                   #in the other column of the header display "TypeInfo"
                return "Type"
            elif section == 2:
                return "MB"
            elif section == 3:
                return "atr"
            elif section == 4:
                return "ars"
            elif section == 5:
                return "cpl"
            elif section == 6:
                return "srs"
            else:
                return "uid"

        
    """for selecting items or enable items"""
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        editflags = 0
        if index.column() == 0:
            editflags = QtCore.Qt.ItemIsEditable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | editflags  #flags to set what we can do with the graph

    
    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex (row and column -> know where item is)"""
    def parent(self, index):
        """
        node = self.internalPointer()   #returns node of the moment
        """
        #replace the commented code above with the following line
        node = self.getNode(index)      #returns node of the moment 
        
        parentNode = node.parent()      #returns parent of node of the moment
        
        #check, if parentNode is parent of the tree model (is true at first call of this method by the treeView)
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        #necessary, when empty current model was selected
        if parentNode.row() == None:
            return QtCore.QModelIndex()

        #it is not the root, so return the index of the parent -> createIndex from QAbstractItemModel
        return self.createIndex(parentNode.row(), 0, parentNode)    #0 in second argument says that the second column of the tree view is not shown hierarchical -> only build hierarchical structure on first column (column0)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):
        if self.hasIndex(row, column, parent):  #if this line is missing, removing the last child will crash the program
            parentNode = self.getNode(parent)
            #get the child
            childItem = parentNode.child(row)

            if childItem:   #if child exists
                return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex() #return empty QModelIndex

    """fetch the node at the QModelIndex"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    """insert existing node into parent"""
    """QModelIndex, node"""
    def insertExistingNode(self, parent, childNode):
        #where to insert
        parentNode = self.getNode(parent)
        position = parentNode.childCount()  #always insert at end because the tree was flattened that way
        rows = 1    #one row to insert
        #insert
        self.beginInsertRows(parent, position, position + rows - 1)
        parentNode.addChild(childNode)
        success = parentNode.insertChild(position, childNode, childNode.childrenlist())
        self.endInsertRows()
        return success

    """INPUTS: int, int, QModelIndex, int, str, str, list, ..."""
    """insert children into the parent"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), uid=-1, type="Node", name="", childrlist=None, textColor = "#000000", bold=False, attributes="", aspectrules="", couplings="", numrep="1", specrules="", priority="1"):  #default empty QModelIndex() as parent -> insert in root

        parentNode = self.getNode(parent)

        #if position is -1, add at end
        if position == -1:
            position = parentNode.childCount()

        if not uid or uid == -1:
            #get next uid
            uid = self.getNextUID()

        self.beginInsertRows(parent, position, position + rows - 1)

        success = False
        for row in range(rows):

            if type == "Entity Node":
                if name == "":
                    childNode = EntityNode(uid, "ENuid" + str(uid), parentNode, textColor, bold, [])
                else:
                    childNode = EntityNode(uid, name, parentNode, textColor, bold, attributes)
            elif type == "Descriptive Node":
                if name == "":
                    childNode = DescriptiveNode(uid, "DNuid" + str(uid), parentNode, textColor, bold)
                else:
                    childNode = DescriptiveNode(uid, name, parentNode, textColor, bold)
            elif type == "Aspect Node":
                if name == "":
                    childNode = AspectNode(uid, "ANuid" + str(uid), parentNode, textColor, bold, [], [], "1")
                else:
                    childNode = AspectNode(uid, name, parentNode, textColor, bold, aspectrules, couplings, priority)
            elif type == "Maspect Node":
                if name == "":
                    childNode = MaspectNode(uid, "MNuid" + str(uid), parentNode, textColor, bold, [], [], "1", "1")
                else:
                    childNode = MaspectNode(uid, name, parentNode, textColor, bold, aspectrules, couplings, numrep, priority)
            elif type == "Spec Node":
                if name == "":
                    childNode = SpecNode(uid, "SNuid" + str(uid), parentNode, textColor, bold, [])
                else:
                    childNode = SpecNode(uid, name, parentNode, textColor, bold, specrules)
            else:
                if name == "":
                    childNode = Node(uid, "Nuid" + str(uid), parentNode, textColor, bold)
                else:
                    childNode = Node(uid, name, parentNode, textColor, bold)

            success = parentNode.insertChild(position, childNode, childrlist)   #insert at the same position, because the other children are pushed down

        self.endInsertRows()

        return success

    """find the uid for inserting the nodes"""
    def getNextUID(self):
        return (self._rootNode.findHighestUid() + 1)

    """INPUTS: int, int, QModelIndex"""
    """remove children"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):  #default empty QModelIndex() as parent -> remove in root

        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        success = False

        for row in range(rows):
            success = parentNode.removeChild(position)  #remove at the same position, because the other children are pulled up
            
        self.endRemoveRows()
        
        return success

