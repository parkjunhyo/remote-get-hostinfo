#! /usr/bin/env python

import os, sys, re, json

class MERGE_REMOTE_RUN_RESULT:
    
    def __init__(self):
        pass
    
    def runCmd(self, TARGETHOSTS, WORKENV):
        # search used os type
        alllistostype = []
        for itemname in TARGETHOSTS:
           if itemname["ostype"] not in alllistostype:
             alllistostype.append(itemname["ostype"])
        # search output directory
        alllistdir = os.listdir(WORKENV["RESULTPATH"])
        matchedlist = []
        for dirname in alllistdir:
           for prefixstring in alllistostype:
              if re.compile("^"+prefixstring+"-").search(dirname):
                 if dirname not in matchedlist:
                    matchedlist.append(dirname)
        # find file and read
        returnalllist = []
        for dirname in matchedlist:
           OUTPUTFILEFULLPATH = WORKENV["RESULTPATH"]+"/"+dirname+"/output.json"
           if os.path.isfile(OUTPUTFILEFULLPATH):
              f = open(OUTPUTFILEFULLPATH, 'r')
              rmsg = f.read()
              f.close()
              changed_json = json.loads(rmsg)
              for tempitem in changed_json:
                 returnalllist.append(tempitem)
        # create single file
        OUTPUTJSON = WORKENV["RESULTPATH"]+"/remote-get-hostinfo-output.json"
        f = open(OUTPUTJSON, 'w')
        f.write(json.dumps(returnalllist))
        f.close()