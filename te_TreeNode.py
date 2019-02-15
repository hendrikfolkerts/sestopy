# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

"""Node for the Tree"""
class Node(object):

    def __init__(self, uid, name, parent=None, tc="#000000", bd=False):  #if Node is not called with a parent argument, set parent to None

        self._uid = uid
        self._name = name
        self._children = []
        self._parent = parent
        self._textColor = tc
        self._bold = bd
        
        if parent is not None:
            parent.addChild(self)

    def getUid(self):
        return self._uid

    def setUid(self, uid):
        self._uid = uid

    def typeInfo(self):
        return "Node"

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child, childrlist):
        
        if position < 0 or position > len(self._children):
            return False
        
        #the child which has a parent is already added by the addChild() method called in __init__ -> remove it
        if child._parent is not None:
            self._children.pop()

        #insert childrenlist if not None
        if childrlist is not None:
            child.setChildrenlist(childrlist)
            for c in childrlist:
                c._parent = child

        #insert the new child
        self._children.insert(position, child)
        child._parent = self

        return True

    def removeChild(self, position):
        
        if position < 0 or position > len(self._children):
            return False
        
        child = self._children.pop(position)
        child._parent = None

        return True

    def name(self):
        return self._name

    def childrenlist(self):
        return self._children

    def setName(self, name):
        self._name = name

    def setChildrenlist(self, cl):
        self._children = cl

    def child(self, row):
        return self._children[row]
    
    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def setParent(self, p):
        self._parent = p

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def setColor(self, sc):
        self._textColor = sc

    def color(self):
        return self._textColor

    def setBold(self, bd):
        self._bold = bd

    def bold(self):
        return self._bold

    def findHighestUid(self):
        id = self.logUid()
        uidstr = id.split("-")
        uidstr.pop()    #remove last empty field
        uidint = []
        for id in uidstr:
            uidint.append(int(id))
        maxnum = -1
        for id in uidint:
            if id > maxnum:
                maxnum = id
        return maxnum

    #log functions------------------------------------------------------------------------------------------------------

    def log(self, tabLevel=-1):

        output = ""
        tabLevel += 1
        
        for i in range(tabLevel):
            output += "\t"
        
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"
        
        return output

    def logUid(self, tabLevel = -1):

        output = ""
        tabLevel += 1

        output += str(self.getUid())+"-"

        for child in self._children:
            output += child.logUid(tabLevel)

        tabLevel -= 1

        return output

    """
    def logType(self, tabLevel = -1):

        output = ""
        tabLevel += 1

        output += self.typeInfo()+"-"

        for child in self._children:
            output += child.logType(tabLevel)

        tabLevel -= 1

        return output
    """


    #end log functions--------------------------------------------------------------------------------------------------

    """in case a print() is needed (during development)"""
    def __repr__(self):
        return self.log()

    
"""Subclasses of Node Class -> using super class constructor"""
class EntityNode(Node):

    def __init__(self, uid, name, parent, textcolor, bold, attributes):   #this class must have a parent and be called with it (can not be root)
        super(EntityNode, self).__init__(uid, name, parent, textcolor, bold)   #super class constructor
        self.attributes = attributes

    def typeInfo(self):
        return "Entity Node"

    def setAttributes(self, aslist):
        self.attributes = aslist

class DescriptiveNode(Node):

    def __init__(self, uid, name, parent, textcolor, bold):   #this class must have a parent and be called with it (can not be root)
        super(DescriptiveNode, self).__init__(uid, name, parent, textcolor, bold)   #super class constructor

    def typeInfo(self):
        return "Descriptive Node"

class AspectNode(Node):
    
    def __init__(self, uid, name, parent, textcolor, bold, aspectrules, couplings, priority):   #this class must have a parent and be called with it (can not be root)
        super(AspectNode, self).__init__(uid, name, parent, textcolor, bold)   #super class constructor
        self.aspectrule = aspectrules
        self.coupling = couplings
        self.priority = priority

    def typeInfo(self):
        return "Aspect Node"

    def setAspectrules(self, arlist):
        self.aspectrule = arlist

    def setCoupling(self, cglist):
        self.coupling = cglist

    def setPriority(self, prio):
        self.priority = prio

class MaspectNode(Node):
    
    def __init__(self, uid, name, parent, textcolor, bold, aspectrules, couplings, numrep, priority):   #this class must have a parent and be called with it (can not be root)
        super(MaspectNode, self).__init__(uid, name, parent, textcolor, bold)   #super class constructor
        self.aspectrule = aspectrules
        self.coupling = couplings
        self.number_replication = numrep
        self.priority = priority

    def typeInfo(self):
        return "Maspect Node"

    def setAspectrules(self, arlist):
        self.aspectrule = arlist

    def setCoupling(self, cglist):
        self.coupling = cglist

    def setNumberReplication(self, nrlist):
        self.number_replication = nrlist

    def setPriority(self, prio):
        self.priority = prio

class SpecNode(Node):
    
    def __init__(self, uid, name, parent, textcolor, bold, specrules):   #this class must have a parent and be called with it (can not be root)
        super(SpecNode, self).__init__(uid, name, parent, textcolor, bold)   #super class constructor
        self.specrule = specrules

    def typeInfo(self):
        return "Spec Node"

    def setSpecrules(self, srlist):
        self.specrule = srlist