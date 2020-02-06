import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
import datetime
import time
import re
from xml.etree import ElementTree
from xml.dom import minidom

#XML for the tree view program and interchange
def toXML(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist):
    root = Element('SESwithSettings', {'name': 'SES', 'xmlns:vc': 'http://www.w3.org/2007/XMLSchema-versioning', 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
    uidElementDict = {}  # a dictionary holding the node uid and the corresponding element

    #the global settings
    globalsgroup = SubElement(root, 'globals')
    SubElement(globalsgroup, 'sespes', {'value': sespes[0], 'comment': sespes[1]})
    sesvargroup = SubElement(globalsgroup, 'sesvars')
    for sesvar in sesvarlist:
        SubElement(sesvargroup, 'sesvar', {'name': sesvar[0], 'value': sesvar[1], 'comment': sesvar[2]})
    semcongroup = SubElement(globalsgroup, 'semcons')
    for semcon in semconlist:
        SubElement(semcongroup, 'semcon', {'value': semcon[0], 'result': semcon[1]})
    selcongroup = SubElement(globalsgroup, 'selcons')
    for selcon in selconlist:
        SubElement(selcongroup, 'selcon', {'startnode': selcon[0], 'stopnode': selcon[2], 'color': selcon[4], 'comment': selcon[5]})
    sesfcngroup = SubElement(globalsgroup, 'sesfcns')
    for sesfun in sesfunlist:
        SubElement(sesfcngroup, 'sesfcn', {'fcnname': sesfun[0],'fcn': sesfun[1],'language':'Python'})

    #the tree with nodes
    treegroup = SubElement(root, 'tree')
    uidElementDict.update({'0': treegroup})
    for node in nodelist:
        if node[1] == "Entity Node":
            parentElement = uidElementDict.get(node[3])
            childElement = SubElement(parentElement, 'node', {'name': node[2], 'type': 'entity', 'comment': ''})
            for attr in node[6]:
                SubElement(childElement, 'attr', {'name': attr[0], 'value': attr[1], 'varfun': attr[2], 'comment': attr[3]})
            uidElementDict.update({node[0]: childElement})
        elif node[1] == "Aspect Node" or node[1] == "Maspect Node":
            parentElement = uidElementDict.get(node[3])
            if node[1] == "Aspect Node":
                childElement = SubElement(parentElement, 'node', {'name': node[2], 'type': 'aspect', 'comment': ''})
            else:   #it must be a maspect
                childElement = SubElement(parentElement, 'node', {'name': node[2], 'type': 'multiaspect', 'comment': ''})
            for aspr in node[7]:
                SubElement(childElement, 'aspr', {'condition': aspr[2], 'result': aspr[3], 'comment': aspr[4]})
            SubElement(childElement, 'prio', {'value': node[11]})
            for cplg in node[8]:
                cplsplit = cplg[2].split(" / ")
                sop = cplsplit[0].strip()
                if len(cplsplit) > 1:
                    sot = cplsplit[1].strip()
                cplsplit = cplg[5].split(" / ")
                sip = cplsplit[0].strip()
                if len(cplsplit) > 1:
                    sit = cplsplit[1].strip()
                if sop != "" and sot != "" and sip != "" and sit != "":
                    SubElement(childElement, 'cplg', {'sourcenode': cplg[0], 'sourceport': sop, 'sourcetype': sot, 'sinknode': cplg[3], 'sinkport': sip, 'sinktype': sit, 'cplgfcn': cplg[6], 'comment': cplg[7]})
                else:
                    SubElement(childElement, 'cplg', {'sourcenode': cplg[0], 'sourceport': '', 'sourcetype': '', 'sinknode': cplg[3], 'sinkport': '', 'sinktype': '', 'cplgfcn': cplg[6], 'comment': cplg[7]})
            if node[1] == "Maspect Node":
                SubElement(childElement, 'numr', {'value': node[9]})
            uidElementDict.update({node[0]: childElement})
        elif node[1] == "Spec Node":
            parentElement = uidElementDict.get(node[3])
            childElement = SubElement(parentElement, 'node', {'name': node[2], 'type': 'specialization', 'comment': ''})
            for specr in node[10]:
                SubElement(childElement, 'specr', {'fornode': specr[0], 'condition': specr[2], 'result': specr[3], 'comment': specr[4]})
            uidElementDict.update({node[0]: childElement})
        elif node[1] == "Descriptive Node":
            parentElement = uidElementDict.get(node[3])
            childElement = SubElement(parentElement, 'node', {'name': node[2], 'type': 'descriptive'})
            uidElementDict.update({node[0]: childElement})
    rough_string = ElementTree.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="")

#read an XML file
def fromXML(xmlstr):

    def addEntity(nodelist, uid, depth, parentuid, name, childlayer):
        attriblist = []
        for ch in childlayer:  # on one layer deeper than the current node (the children of the current layer) are the node specific attributes (if the node has node specific attributes at all)
            if ch.tag == "attr":
                nm = ch.attrib['name']
                vl = ch.attrib['value']
                vf = ch.attrib['varfun']
                cm = ch.attrib['comment']
                attriblist.append([nm, vl, vf, cm])
        nodelist.append([str(uid), "Entity Node", name, str(parentuid), "#000000", 'False', attriblist, [], [], '1', [], '1', str(depth)])
        return nodelist

    def addAspect(nodelist, uid, depth, parentuid, name, childlayer):
        asprulelist = []
        priority = "1"
        couplinglist = []
        for ch in childlayer:  # on one layer deeper than the current node (the children of the current layer) are the node specific attributes (if the node has node specific attributes at all)
            if ch.tag == "aspr":
                cd = ch.attrib['condition']
                rs = ch.attrib['result']
                cm = ch.attrib['comment']
                asprulelist.append([name, uid, cd, rs, cm])
            if ch.tag == "prio":
                priority = ch.attrib['value']
            if ch.tag == "cplg":
                son = ch.attrib['sourcenode']
                sop = ch.attrib['sourceport']
                sot = ch.attrib['sourcetype']
                sin = ch.attrib['sinknode']
                sip = ch.attrib['sinkport']
                sit = ch.attrib['sinktype']
                fcn = ch.attrib['cplgfcn']
                com = ch.attrib['comment']
                if son != "" and sin != "":
                    couplinglist.append([son, "sourcenodeuid", sop + " / " + sot, sin, "sinknodeuid", sip + " / " + sit, "", com])
                else:
                    couplinglist.append(["", "", "", "", "", "", fcn, ""])
        nodelist.append([str(uid), "Aspect Node", name, str(parentuid), "#000000", 'False', [], asprulelist, couplinglist, '1', [], priority, str(depth)])
        return nodelist

    def addSpec(nodelist, uid, depth, parentuid, name, childlayer):
        specrulelist = []
        for ch in childlayer:  # on one layer deeper than the current node (the children of the current layer) are the node specific attributes (if the node has node specific attributes at all)
            if ch.tag == "specr":
                fn = ch.attrib['fornode']
                cd = ch.attrib['condition']
                rs = ch.attrib['result']
                cm = ch.attrib['comment']
                specrulelist.append([fn, "specrulenodeuid", cd, rs, cm])
        nodelist.append([str(uid), "Spec Node", name, str(parentuid), "#000000", 'False', [], [], [], '1', specrulelist, '1', str(depth)])
        return nodelist

    def addMaspect(nodelist, uid, depth, parentuid, name, childlayer):
        asprulelist = []
        priority = "1"
        numrep = "1"
        couplinglist = []
        for ch in childlayer:  # on one layer deeper than the current node (the children of the current layer) are the node specific attributes (if the node has node specific attributes at all)
            if ch.tag == "aspr":
                cd = ch.attrib['condition']
                rs = ch.attrib['result']
                cm = ch.attrib['comment']
                asprulelist.append([name, uid, cd, rs, cm])
            if ch.tag == "prio":
                priority = ch.attrib['value']
            if ch.tag == "numr":
                numrep = ch.attrib['value']
            if ch.tag == "cplg":
                son = ch.attrib['sourcenode']
                sop = ch.attrib['sourceport']
                sot = ch.attrib['sourcetype']
                sin = ch.attrib['sinknode']
                sip = ch.attrib['sinkport']
                sit = ch.attrib['sinktype']
                fcn = ch.attrib['cplgfcn']
                com = ch.attrib['comment']
                if son != "" and sin != "":
                    couplinglist.append([son, "sourcenodeuid", sop + " / " + sot, sin, "sinknodeuid", sip + " / " + sit, "", com])
                else:
                    couplinglist.append(["", "", "", "", "", "", fcn, ""])
        nodelist.append([str(uid), "Maspect Node", name, str(parentuid), "#000000", 'False', [], asprulelist, couplinglist, numrep, [], priority, str(depth)])
        return nodelist

    def addDescriptive(nodelist, uid, depth, parentuid, name):
        nodelist.append([str(uid), "Descriptive Node", name, str(parentuid), "#000000", 'False', [], [], [], '1', [], '1', str(depth)])
        return nodelist

    #beginning of the function
    sespeslist = []
    sesvarlist = []
    semconlist = []
    selconlist = []
    sesfunlist = []
    nodelist=[]
    uid = 1
    depth = 0
    #get the tree
    root = ET.fromstring(xmlstr)
    parentChildIndexDict = {c: p for p in root.iter() for c in p}     #parentindex-childindex dictionary of the tree -> for every index the parent can be found
    indexUidDict = {}  #a dictionary where to every index of the ElementTree the uid is placed -> index: uid
    uidIndexDict = {}   #a dictionary where to every uid the index of the ElementTree is placed -> uid: index
    parentChildrenUidsDict = {}     #for every parentuid the children's uids can be found -> {parentuid: [[childuid, childname], [childuid, childname], ...} -> specrules and couplings
    childParentUidsDict = {}        #for every childuid the parent's uid can be found -> childuid: [parentuid, parentname] -> couplings

    #get the children of root
    for chi in root:    #a child of root can also be accessed by root[0], root[1] etc.

        if chi.tag == "globals":
            for ch in chi:

                if ch.tag == "sespes":
                    vl = ch.attrib['value']
                    cm = ch.attrib['comment']
                    sespeslist.append([vl, cm])
                if ch.tag == "sesvars":
                    for chil in ch:
                        if chil.tag == "sesvar":
                            nm = chil.attrib['name']
                            vl = chil.attrib['value']
                            cm = chil.attrib['comment']
                            sesvarlist.append([nm, vl, cm])
                if ch.tag == "semcons":
                    for chil in ch:
                        if chil.tag == "semcon":
                            vl = chil.attrib['value']
                            rs = chil.attrib['result']
                            semconlist.append([vl, rs])
                if ch.tag == "selcons":
                    for chil in ch:
                        if chil.tag == "selcon":
                            san = chil.attrib['startnode']
                            son = chil.attrib['stopnode']
                            col = chil.attrib['color']
                            com = chil.attrib['comment']
                            selconlist.append([san, "startnodeuid", son, "stopnodeuid", col, com])
                if ch.tag == "sesfcns":
                    try:
                        chil = ch[0]    #no need to go through all tags sesfcn with a for loop -> all functions are found with the regex in re.findall(...)
                        if chil.tag == "sesfcn":
                            #fn = chil.attrib['fcnname']
                            #fc = chil.attrib['fcn']
                            #sesfunlist.append([fn, fc])

                            # since cr lf is not recognized -> regular expression
                            ffun = re.findall('<sesfcn fcn=\".*\" fcnname=\".*\" language="Python"/>', xmlstr, re.DOTALL)
                            if len(ffun) > 0:
                                f = ffun[0].split("<sesfcn fcn=")
                                del f[0]
                                for fx in f:
                                    fp = fx.split('language="Python"')
                                    del fp[1]
                                    ffn = fp[0].split('fcnname=')
                                    for x in range(len(ffn)):
                                        ffn[x] = ffn[x].strip()
                                        ffn[x] = ffn[x][1:-1]
                                    #extract the name and the function itself
                                    nm = ffn[1]
                                    fu = ffn[0]
                                    # replace the special characters
                                    fu = fu.replace("&quot;", '"')
                                    fu = fu.replace("&apos;", "'")
                                    fu = fu.replace("&lt;", "<")
                                    fu = fu.replace("&gt;", ">")
                                    fu = fu.replace("&amp;", "&")
                                    sesfunlist.append([nm, fu])
                    except:
                        pass

        if chi.tag == "tree":

            treeLayer = chi

            #pre-order traversal
            nodeStack = []
            #l = len(treeLayer)
            nodeStack.append([treeLayer[0], depth])  #append root
            #a = treeLayer[0].attrib['name']
            #t = treeLayer[0].tag

            while len(nodeStack) > 0:

                curEl = nodeStack.pop()
                ch = curEl[0]
                depth = curEl[1]
                """
                try:
                    a = ch.attrib['name']
                except:
                    t = ch.tag
                """

                if ch.tag == "node" and ch.attrib['type'] == "entity":
                    name = ch.attrib['name']
                    if not nodelist:    #the root node of the tree
                        parentUid = 0   #for the first node in the tree the parentuid is 0
                    else:
                        parentUid = indexUidDict.get(parentChildIndexDict.get(ch))  #get the parentUid of the ch
                    nodelist = addEntity(nodelist, uid, depth, parentUid, name, ch)    #add entry
                    # update the index - uid dictionaries
                    indexUidDict.update({ch: uid})  # place the ch index with the given uid in the dictionary
                    uidIndexDict.update({uid: ch})  # place the uid with the ch index in the dictionary
                    # update the parent - children dictionary (one parent can have several children)
                    puid = parentChildrenUidsDict.get(str(parentUid))
                    if not puid:
                        parentChildrenUidsDict.update({str(parentUid): [[str(uid), name]]})
                    else:
                        puid.append([str(uid), name])
                        parentChildrenUidsDict.update({str(parentUid): puid})
                    # update the child - parent dictionary (one child can only have one parent)
                    if parentUid == 0:
                        childParentUidsDict.update({str(uid): [str(parentUid), None]})
                    else:
                        childParentUidsDict.update({str(uid): [str(parentUid), uidIndexDict.get(parentUid).attrib['name']]})
                    uid += 1

                if ch.tag == "node" and ch.attrib['type'] == "aspect":
                    name = ch.attrib['name']
                    parentUid = indexUidDict.get(parentChildIndexDict.get(ch))     #get the parentUid of the ch
                    nodelist = addAspect(nodelist, uid, depth, parentUid, name, ch)     #add entry
                    # update the index - uid dictionaries
                    indexUidDict.update({ch: uid})  # place the ch index with the given uid in the dictionary
                    uidIndexDict.update({uid: ch})  # place the uid with the ch index in the dictionary
                    # update the parent - children dictionary (one parent can have several children)
                    puid = parentChildrenUidsDict.get(str(parentUid))
                    if not puid:
                        parentChildrenUidsDict.update({str(parentUid): [[str(uid), name]]})
                    else:
                        puid.append([str(uid), name])
                        parentChildrenUidsDict.update({str(parentUid): puid})
                    # update the child - parent dictionary (one child can only have one parent)
                    childParentUidsDict.update({str(uid): [str(parentUid), uidIndexDict.get(parentUid).attrib['name']]})
                    uid += 1

                if ch.tag == "node" and ch.attrib['type'] == "specialization":
                    name = ch.attrib['name']
                    parentUid = indexUidDict.get(parentChildIndexDict.get(ch))     #get the parentUid of the ch
                    nodelist = addSpec(nodelist, uid, depth, parentUid, name, ch)       #add entry
                    # update the index - uid dictionaries
                    indexUidDict.update({ch: uid})  # place the ch index with the given uid in the dictionary
                    uidIndexDict.update({uid: ch})  # place the uid with the ch index in the dictionary
                    # update the parent - children dictionary (one parent can have several children)
                    puid = parentChildrenUidsDict.get(str(parentUid))
                    if not puid:
                        parentChildrenUidsDict.update({str(parentUid): [[str(uid), name]]})
                    else:
                        puid.append([str(uid), name])
                        parentChildrenUidsDict.update({str(parentUid): puid})
                    # update the child - parent dictionary (one child can only have one parent)
                    childParentUidsDict.update({str(uid): [str(parentUid), uidIndexDict.get(parentUid).attrib['name']]})
                    uid += 1

                if ch.tag == "node" and ch.attrib['type'] == "multiaspect":
                    name = ch.attrib['name']
                    parentUid = indexUidDict.get(parentChildIndexDict.get(ch))     #get the parentUid of the ch
                    nodelist = addMaspect(nodelist, uid, depth, parentUid, name, ch)    #add entry
                    # update the index - uid dictionaries
                    indexUidDict.update({ch: uid})  # place the ch index with the given uid in the dictionary
                    uidIndexDict.update({uid: ch})  # place the uid with the ch index in the dictionary
                    # update the parent - children dictionary (one parent can have several children)
                    puid = parentChildrenUidsDict.get(str(parentUid))
                    if not puid:
                        parentChildrenUidsDict.update({str(parentUid): [[str(uid), name]]})
                    else:
                        puid.append([str(uid), name])
                        parentChildrenUidsDict.update({str(parentUid): puid})
                    # update the child - parent dictionary (one child can only have one parent)
                    childParentUidsDict.update({str(uid): [str(parentUid), uidIndexDict.get(parentUid).attrib['name']]})
                    uid += 1

                if ch.tag == "node" and ch.attrib['type'] == "descriptive":
                    name = ch.attrib['name']
                    parentUid = indexUidDict.get(parentChildIndexDict.get(ch))     #get the parentUid of the ch
                    nodelist = addDescriptive(nodelist, uid, depth, parentUid, name)    #add entry
                    # update the index - uid dictionaries
                    indexUidDict.update({ch: uid})  # place the ch index with the given uid in the dictionary
                    uidIndexDict.update({uid: ch})  # place the uid with the ch index in the dictionary
                    # update the parent - children dictionary (one parent can have several children)
                    puid = parentChildrenUidsDict.get(str(parentUid))
                    if not puid:
                        parentChildrenUidsDict.update({str(parentUid): [[str(uid), name]]})
                    else:
                        puid.append([str(uid), name])
                        parentChildrenUidsDict.update({str(parentUid): puid})
                    # update the child - parent dictionary (one child can only have one parent)
                    childParentUidsDict.update({str(uid): [str(parentUid), uidIndexDict.get(parentUid).attrib['name']]})
                    uid += 1

                depth += 1
                numSub = len(ch) - 1
                while numSub >= 0:
                    nodeStack.append([ch[numSub], depth])
                    numSub -= 1

    #set necessary uids in selection constraints -> in selection constraints
    #set the color and bold properties according to the selection constraints -> in nodelist
    #set necessary uids in specrules -> in nodelist
    #set necessary uids in couplings -> in nodelist
    for nd in range(len(nodelist)):

        for slc in selconlist:
            #startnode
            if nodelist[nd][2] == slc[0]:   #if the name fits
                #set the uid in the selection constraint
                slc[1] = nodelist[nd][0]
                #set the color and bold property in the node
                nodelist[nd][4] = slc[4]
                nodelist[nd][5] = "True"
            #stopnode(s)
            sns = slc[2].split(", ")
            if nodelist[nd][2] in sns:  #if the name fits
                #set the uid in the selection constraint
                uids = slc[3].split(", ")
                if uids[0] == "stopnodeuid":  # remove existing entry "stopnodeuid"
                    del uids[0]
                uids.append(nodelist[nd][0])
                uids = ', '.join(uids)
                slc[3] = uids
                #set the color in the node
                nodelist[nd][4] = slc[4]

        if nodelist[nd][1] == "Spec Node":
            children = parentChildrenUidsDict.get(nodelist[nd][0])
            for sr in nodelist[nd][10]:
                for ch in children:
                    if sr[0] == ch[1]: #the name fits
                        sr[1] = ch[0]

        if nodelist[nd][1] in ["Aspect Node", "Maspect Node"]:
            children = parentChildrenUidsDict.get(nodelist[nd][0])
            parent = childParentUidsDict.get(nodelist[nd][0])
            for cp in nodelist[nd][8]:
                #check if one coupling refers to a child
                for ch in children:
                    if cp[0] == ch[1]: #the name fits
                        cp[1] = ch[0]
                    if cp[3] == ch[1]: #the name fits
                        cp[4] = ch[0]
                #now check if one coupling refers to the parent
                if cp[0] == parent[1]: #the name fits
                    cp[1] = parent[0]
                if cp[3] == parent[1]: #the name fits
                    cp[4] = parent[0]

    return (True, nodelist, sespeslist, sesvarlist, semconlist, selconlist, sesfunlist)



#defined for interchange with SES editor developed at Deutsches Zentrum fuer Luft- und Raumfahrt
# -> currently not used
#An upper limit and a lower limit for the value can be specified in the commentfield of an attribute. This can be done for example
# by setting upper=<value> and lower=<value> in the text. Please be aware, that this is only for information in this
# editor, because limits are usually set by defining selection constraints for an SES variable. However, when
# exporting the SES as XML, these values are set to the attribute.
#Examples for the comment:
# This is a comment. The limits vor this variable are upper=55.0 and lower=25.0.
# This is another comment specifying the limits upper=55 and lower=25.
def toXML_DLR(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist):
    def addAttributes(parent, node):
        for attr in node[6]:
            try:
                lower = ''.join(re.findall(r'(lower\s*?=\s*?)([+-]?\d+)(\.\d+)?', attr[3])[0])
                lower=lower.split("=")[1].strip()
            except:
                lower = ""
            try:
                upper = ''.join(re.findall(r'(upper\s*?=\s*?)([+-]?\d+)(\.\d+)?', attr[3])[0])
                upper = upper.split("=")[1].strip()
            except:
                upper = ""
            SubElement(parent, 'var', {'name': attr[0], 'default': attr[1], 'lower': lower, 'upper': upper})

    #beginning of the function
    uidElementDict = {}   #a dictionary holding the uid and the corresponding element
    root = None
    for node in nodelist:
        if node[12] == "0": #beginning
            root = Element('entity', {'name': node[2], 'xmlns:vc': 'http://www.w3.org/2007/XMLSchema-versioning', 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:noNamespaceSchemaLocation': 'ses.xsd'})
            addAttributes(root, node)
            uidElementDict.update({node[0]: root})
        else:   #further
            if node[1] == "Entity Node":
                parentElement = uidElementDict.get(node[3])
                childElement = SubElement(parentElement, 'entity', {'name': node[2]})
                addAttributes(childElement, node)
                uidElementDict.update({node[0]: childElement})
            elif node[1] == "Aspect Node":
                parentElement = uidElementDict.get(node[3])
                # add Dec to the node's name if it is not there
                nodename = node[2]
                nodenamelow = nodename.lower()
                if nodenamelow[-3:] == "dec":
                    nodename = nodename[:-3]
                nodename = nodename + "Dec"
                # add the node
                childElement = SubElement(parentElement, 'aspect', {'name': nodename})
                uidElementDict.update({node[0]: childElement})
            elif node[1] == "Spec Node":
                parentElement = uidElementDict.get(node[3])
                # add Spec to the node's name if it is not there
                nodename = node[2]
                nodenamelow = nodename.lower()
                if nodenamelow[-4:] == "spec":
                    nodename = nodename[:-4]
                nodename = nodename + "Spec"
                # add the node
                childElement = SubElement(parentElement, 'specialization', {'name': nodename})
                uidElementDict.update({node[0]: childElement})
            elif node[1] == "Maspect Node":
                parentElement = uidElementDict.get(node[3])
                # add MAsp to the node's name if it is not there
                nodename = node[2]
                nodenamelow = nodename.lower()
                if nodenamelow[-4:] == "masp":
                    nodename = nodename[:-4]
                nodename = nodename + "MAsp"
                # add the node
                childElement = SubElement(parentElement, 'multiAspect', {'name': nodename})
                uidElementDict.update({node[0]: childElement})
    #bytesString = ElementTree.tostring(root, 'utf-8')
    #treeString = bytesString.decode()
    #return treeString
    rough_string = ElementTree.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="")

#defined for interchange with SES editor developed at Deutsches Zentrum fuer Luft- und Raumfahrt
# -> currently not used
# upper limits and lower limits specified in the XML are set in the commentfield (see function toXML_DLR)
def fromXML_DLR(xmlstr):
    def addEntity(nodelist, uidNodelistindexDict, uid, depth, parentuid, name, layer):
        attriblist = []
        for ch in layer:  # one layer deeper than the current node (the children of the current layer) are attributes (if the node has attributes at all)
            if ch.tag == "var":
                nm = ch.attrib['name']
                vl = ch.attrib['default']
                lw = ch.attrib['lower']
                up = ch.attrib['upper']
                attriblist.append([nm, vl, "", "lower=" + lw + ", upper=" + up])
        if parentuid == 0:          #the root: insert at the beginning
            nodelistIndex = 0
        else:
            nodelistIndex = uidNodelistindexDict.get(parentuid)+1  # insert after the parent as the nodelistIndex item
            while nodelistIndex < len(nodelist) and int(nodelist[nodelistIndex][12]) == depth:  #but insert at the end of the siblings with the same depth
                nodelistIndex += 1
        nodelist.insert(nodelistIndex, [str(uid), "Entity Node", name, str(parentuid), "#000000", 'False', attriblist, [], [], '1', [], '1', str(depth)])
        uidNodelistindexDict.update({uid: nodelistIndex}) #insert the uid with the index where it is placed in the nodelist
        return (nodelist, uidNodelistindexDict)

    def addAspect(nodelist, uidNodelistindexDict, uid, depth, parentuid, name):
        nodelistIndex = uidNodelistindexDict.get(parentuid)+1  # insert after the parent as the nodelistIndex item
        while nodelistIndex < len(nodelist) and int(nodelist[nodelistIndex][12]) == depth:  # but insert at the end of the siblings with the same depth
            nodelistIndex += 1
        nodelist.insert(nodelistIndex, [str(uid), "Aspect Node", name, str(parentuid), "#000000", 'False', [], [], [], '1', [], '1', str(depth)])
        uidNodelistindexDict.update({uid: nodelistIndex})  #insert the uid with the index where it is placed in the nodelist
        return (nodelist, uidNodelistindexDict)

    def addSpec(nodelist, uidNodelistindexDict, uid, depth, parentuid, name):
        nodelistIndex = uidNodelistindexDict.get(parentuid)+1  # insert after the parent as the nodelistIndex item
        while nodelistIndex < len(nodelist) and int(nodelist[nodelistIndex][12]) == depth:  # but insert at the end of the siblings with the same depth
            nodelistIndex += 1
        nodelist.insert(nodelistIndex, [str(uid), "Spec Node", name, str(parentuid), "#000000", 'False', [], [], [], '1', [], '1', str(depth)])
        uidNodelistindexDict.update({uid: nodelistIndex})  #insert the uid with the index where it is placed in the nodelist
        return (nodelist, uidNodelistindexDict)

    def addMaspect(nodelist, uidNodelistindexDict, uid, depth, parentuid, name):
        nodelistIndex = uidNodelistindexDict.get(parentuid)+1  # insert after the parent as the nodelistIndex item
        while nodelistIndex < len(nodelist) and int(nodelist[nodelistIndex][12]) == depth:  # but insert at the end of the siblings with the same depth
            nodelistIndex += 1
        nodelist.insert(nodelistIndex, [str(uid), "Maspect Node", name, str(parentuid), "#000000", 'False', [], [], [], '1', [], '1', str(depth)])
        uidNodelistindexDict.update({uid: nodelistIndex})  #insert the uid with the index where it is placed in the nodelist
        return (nodelist, uidNodelistindexDict)

    #beginning of the function
    nodelist=[]
    uid = 1
    depth = 0
    #get the tree
    root = ET.fromstring(xmlstr)
    parentChildIndexDict = {c: p for p in root.iter() for c in p}     #parentindex-childindex dictionary of the tree -> for every index the parent can be found
    indexUidDict = {}  #a dictionary where to every index of the ElementTree the uid is placed
    uidNodelistindexDict = {}   #a dictionary where to every uid the nodelist-index of the node is placed

    #append root
    name = root.attrib['name']
    parentuid = 0   #for the first element the parentuid is 0
    nodelist, uidNodelistindexDict = addEntity(nodelist, uidNodelistindexDict, uid, depth, parentuid, name, root)
    indexUidDict.update({root: uid})    #add to indexUidDict    #or: indexUidDict[root] = uid
    uid += 1
    depth += 1

    currentLayer = root

    while currentLayer:     #as long as it is not None -> get the children of the current layer
        for chi in currentLayer:    #a child of the currentLayer can also be accessed by currentLayer[0], currentLayer[1] etc.

            if chi.tag == "entity":
                name = chi.attrib['name']
                parentUid = indexUidDict.get(parentChildIndexDict.get(chi))         #get the parentUid of the chi
                nodelist, uidNodelistindexDict = addEntity(nodelist, uidNodelistindexDict, uid, depth, parentUid, name, chi)    #add entry
                indexUidDict.update({chi: uid}) #place the chi index with the given uid in the dictionary
                uid += 1

            if chi.tag == "aspect":
                name = chi.attrib['name']
                parentUid = indexUidDict.get(parentChildIndexDict.get(chi))     #get the parentUid of the chi
                nodelist, uidNodelistindexDict = addAspect(nodelist, uidNodelistindexDict, uid, depth, parentUid, name)     #add entry
                indexUidDict.update({chi: uid}) #place the chi index with the given uid in the dictionary
                uid += 1

            if chi.tag == "specialization":
                name = chi.attrib['name']
                parentUid = indexUidDict.get(parentChildIndexDict.get(chi))     #get the parentUid of the chi
                nodelist, uidNodelistindexDict = addSpec(nodelist, uidNodelistindexDict, uid, depth, parentUid, name)       #add entry
                indexUidDict.update({chi: uid}) #place the chi index with the given uid in the dictionary
                uid += 1

            if chi.tag == "multiAspect":
                name = chi.attrib['name']
                parentUid = indexUidDict.get(parentChildIndexDict.get(chi))     #get the parentUid of the chi
                nodelist, uidNodelistindexDict = addMaspect(nodelist, uidNodelistindexDict, uid, depth, parentUid, name)    #add entry
                indexUidDict.update({chi: uid}) #place the chi index with the given uid in the dictionary
                uid += 1

        try:
            currentLayer = currentLayer[0]
            depth += 1
        except:
            currentLayer = None

    return (True, nodelist, [['ses', '']], [], [], [], [])


"""
old functions saving all elements in this editor as xml -> now a json format is used for this
"""
"""
def toXML(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist):

    # Configure one attribute with set()
    root = Element('ses')
    root.set('version', '1.0')

    root.append(Comment('Generated by SESToPy (University of Applied Sciences Wismar, Research Group Computational Engineering and Automation); Contact: Prof. Dr.-Ing. Thorsten Pawletta, thorsten.pawletta@hs-wismar.de; developed by Hendrik Martin Folkerts originally using Python 3.4.1 and PyQt 5.5'))

    head = SubElement(root, 'head')
    title = SubElement(head, 'title')
    title.text = 'System Entity Structure tree with settings generated by SESToPy (University of Applied Sciences Wismar, Research Group Computational Engineering and Automation)'
    dc = SubElement(head, 'dateCreated')
    dc.text = str(datetime.datetime.now())
    #dm = SubElement(head, 'sse')
    #dm.text = str(time.time())

    body = SubElement(root, 'body')

    treenodegroup = SubElement(body, 'treenodes', {'text':'treenodes'})
    for node in nodelist:
        nodegroup = SubElement(treenodegroup, 'treenode', {'uid':node[0], 'type':node[1], 'name':node[2], 'parentuid':node[3], 'textColor':node[4], 'bold':node[5], 'depth':node[12],})
        if node[1] == "Entity Node":
            for attr in node[6]:
                SubElement(nodegroup, 'attribute', {'name':attr[0], 'value':attr[1], 'varfun':attr[2], 'comment':attr[3]})
        if node[1] == "Aspect Node":
            for asp in node[7]:
                SubElement(nodegroup, 'aspectrule', {'node': asp[0], 'uid': asp[1], 'condition': asp[2], 'result': asp[3], 'comment': asp[4],})
            for cpl in node[8]:
                SubElement(nodegroup, 'coupling', {'sourcename': cpl[0], 'sourceuid': cpl[1], 'sourceport': cpl[2], 'sinkname': cpl[3], 'sinkuid': cpl[4], 'sinkport': cpl[5],'cplfun': cpl[6],})
            SubElement(nodegroup, 'priority', {'value': node[11],})
        if node[1] == "Maspect Node":
            for asp in node[7]:
                SubElement(nodegroup, 'aspectrule', {'node': asp[0], 'uid': asp[1], 'condition': asp[2], 'result': asp[3], 'comment': asp[4],})
            for cpl in node[8]:
                SubElement(nodegroup, 'coupling', {'sourcename': cpl[0], 'sourceuid': cpl[1], 'sourceport': cpl[2], 'sinkname': cpl[3], 'sinkuid': cpl[4], 'sinkport': cpl[5], 'cplfun': cpl[6],})
            SubElement(nodegroup, 'num_rep', {'value': node[9],})
            SubElement(nodegroup, 'priority', {'value': node[11],})
        if node[1] == "Spec Node":
            for spe in node[10]:
                SubElement(nodegroup, 'specrule', {'node': spe[0], 'uid': spe[1], 'condition': spe[2], 'result': spe[3], 'comment': spe[4],})

    sespesgroup = SubElement(body, 'sespess', {'text': 'sespes'})
    SubElement(sespesgroup, 'sespes', {'value': sespes[0], 'comment': sespes[1],})

    sesvargroup = SubElement(body, 'sesvars', {'text': 'sesvars'})
    for sesvar in sesvarlist:
        SubElement(sesvargroup, 'sesvar', {'name':sesvar[0], 'value':sesvar[1],})

    semcongroup = SubElement(body, 'semcons', {'text':'semcons'})
    for semcon in semconlist:
        SubElement(semcongroup, 'semcon', {'value':semcon[0], 'result':semcon[1],})

    selcongroup = SubElement(body, 'selcons', {'text':'selcons'})
    for selcon in selconlist:
        SubElement(selcongroup, 'selcon', {'startnode':selcon[0], 'startnodeuid':selcon[1], 'stopnode':selcon[2], 'stopnodeuid':selcon[3],'color':selcon[4],})

    sesfungroup = SubElement(body, 'sesfuns', {'text':'sesfuns'})
    for sesfun in sesfunlist:
        SubElement(sesfungroup, 'sesfun', {'funname':sesfun[0],'fun':sesfun[1],})

    #pretty-printed XML string for the Element
    rough_string = ElementTree.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def fromXML(xmlstr):
    root = ET.fromstring(xmlstr)
    versionok = False
    headok = False
    istOkay = False
    nodelist = []
    spes = []
    sesvarlist = []
    semconlist = []
    selconlist = []
    sesfunlist = []
    xmltype = root.tag
    if root.attrib['version'] == '1.0': #check version information
        versionok = True
    for child in root:
        if child.tag == 'head':
            for chil in child:
                if chil.tag == 'title': #check title information
                    if xmltype == 'ses' and chil.text == 'System Entity Structure tree with settings generated by SESToPy (University of Applied Sciences Wismar, Research Group Computational Engineering and Automation)':
                        headok = True
                #if chil.tag == 'sse':   #check time information
                    #t = float(chil.text)
                    #now = float(time.time())
                    #if now > t:
                        #timeOkay = True
        if versionok and headok:
            istOkay = True
        if istOkay and child.tag == 'body':
            for chil in child:
                if chil.tag == 'treenodes':
                    for chi in chil.iter('treenode'):
                        uid = chi.attrib['uid']
                        ty = chi.attrib['type']
                        nm = chi.attrib['name']
                        pa = chi.attrib['parentuid']
                        tc = chi.attrib['textColor']
                        bd = chi.attrib['bold']
                        dp = chi.attrib['depth']
                        attributelist = []
                        aspectlist = []
                        couplinglist = []
                        nrep = '1'
                        specrulelist = []
                        prio = '1'
                        for ch in chi.iter('attribute'):
                            atnm = ch.attrib['name']
                            atvl = ch.attrib['value']
                            atvarfun = ch.attrib['varfun']
                            atcomment = ch.attrib['comment']
                            attributelist.append([atnm, atvl, atvarfun, atcomment])
                        for ch in chi.iter('aspectrule'):
                            asnm = ch.attrib['node']
                            asui = ch.attrib['uid']
                            asco = ch.attrib['condition']
                            asre = ch.attrib['result']
                            asct = ch.attrib['comment']
                            aspectlist.append([asnm, asui, asco, asre, asct])
                        for ch in chi.iter('coupling'):
                            clson = ch.attrib['sourcename']
                            clsou = ch.attrib['sourceuid']
                            clsop = ch.attrib['sourceport']
                            clsin = ch.attrib['sinkname']
                            clsiu = ch.attrib['sinkuid']
                            clsip = ch.attrib['sinkport']
                            clfun = ch.attrib['cplfun']
                            couplinglist.append([clson, clsou, clsop, clsin, clsiu, clsip, clfun])
                        for ch in chi.iter('num_rep'):
                            nrep = ch.attrib['value']
                        for ch in chi.iter('specrule'):
                            spnm = ch.attrib['node']
                            spui = ch.attrib['uid']
                            spco = ch.attrib['condition']
                            spre = ch.attrib['result']
                            spct = ch.attrib['comment']
                            specrulelist.append([spnm, spui, spco, spre, spct])
                        for ch in chi.iter('priority'):
                            prio = ch.attrib['value']
                        nodelist.append([uid, ty, nm, pa, tc, bd, attributelist, aspectlist, couplinglist, nrep, specrulelist, prio, dp])
                if chil.tag == 'sespess':
                    for chi in chil.iter('sespes'):
                        vl = chi.attrib['value']
                        cm = chi.attrib['comment']
                        spes.append([vl, cm])
                if chil.tag == 'sesvars':
                    for chi in chil.iter('sesvar'):
                        nm = chi.attrib['name']
                        vl = chi.attrib['value']
                        sesvarlist.append([nm, vl])
                if chil.tag == 'semcons':
                    for chi in chil.iter('semcon'):
                        vl = chi.attrib['value']
                        rs = chi.attrib['result']
                        semconlist.append([vl, rs])
                if chil.tag == 'selcons':
                    for chi in chil.iter('selcon'):
                        san = chi.attrib['startnode']
                        sanu = chi.attrib['startnodeuid']
                        son = chi.attrib['stopnode']
                        sonu = chi.attrib['stopnodeuid']
                        col = chi.attrib['color']
                        selconlist.append([san, sanu, son, sonu, col])
                if chil.tag == 'sesfuns':
                    #for chi in chil.iter('sesfun'):
                        #nm = chi.attrib['funname']
                        #fu = chi.attrib['fun']
                        #sesfunlist.append([nm, fu])
                    #since cr lf is not recognized -> regular expression
                    ffun = re.findall('<sesfun fun=\".*\" funname=\".*\"/>', xmlstr, re.DOTALL)
                    if len(ffun) > 0:
                        f = ffun[0].split("<sesfun fun=")
                        del f[0]
                        for fx in f:
                            f1 = fx.split("funname=")
                            nm = f1[1]
                            nm = nm.strip()
                            nm = nm[1:-3]
                            fu = f1[0]
                            fu = fu.strip()
                            #replace the special characters
                            fu = fu.replace("&quot;", '"')
                            fu = fu.replace("&apos;", "'")
                            fu = fu.replace("&lt;", "<")
                            fu = fu.replace("&gt;", ">")
                            fu = fu.replace("&amp;", "&")
                            #go on
                            fu = re.findall('\".*\"', fu, re.DOTALL)
                            fu = fu[0][1:-1]
                            sesfunlist.append([nm, fu])

    return (istOkay, nodelist, spes, sesvarlist, semconlist, selconlist, sesfunlist)
"""