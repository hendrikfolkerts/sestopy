import json
import datetime

def toJSON(nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist):
    info = "SES JSON Version 1 - DO NOT EDIT THIS FILE MANUALLY!"
    comment1 = "Generated by SESToPy (University of Applied Sciences Wismar, Research Group Computational Engineering and Automation); Contact: Prof. Dr.-Ing. Thorsten Pawletta, thorsten.pawletta@hs-wismar.de; developed by Hendrik Martin Folkerts originally using Python 3.4.1 and PyQt 5.5"
    comment2 = "System Entity Structure tree with settings generated by SESToPy (University of Applied Sciences Wismar, Research Group Computational Engineering and Automation)"
    date = "Created: " + datetime.datetime.now().strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H:%M:%S")
    nl = json.dumps(nodelist)
    sp = json.dumps([sespes])
    sv = json.dumps(sesvarlist)
    smc = json.dumps(semconlist)
    slc = json.dumps(selconlist)
    sf = json.dumps(sesfunlist)
    jsonstr = info+"\n"+comment1+"\n"+comment2+"\n"+date+"\n"+nl+"\n"+sp+"\n"+sv+"\n"+smc+"\n"+slc+"\n"+sf
    return jsonstr

def fromJSON(jsonstr):
    try:
        jsonstrsplit = jsonstr.split("\n")
        if jsonstrsplit[0] == "SES JSON Version 1 - DO NOT EDIT THIS FILE MANUALLY!":
            loadtime = jsonstrsplit[3]
            nodelist = json.loads(jsonstrsplit[4])
            sespes = json.loads(jsonstrsplit[5])
            sesvarlist = json.loads(jsonstrsplit[6])
            semconlist = json.loads(jsonstrsplit[7])
            selconlist = json.loads(jsonstrsplit[8])
            sesfunlist = json.loads(jsonstrsplit[9])
            return (True, nodelist, sespes, sesvarlist, semconlist, selconlist, sesfunlist, loadtime)
        else:
            return (False, [], [], [], [], [], [])
    except:
        return (False, [], [], [], [], [], [])
