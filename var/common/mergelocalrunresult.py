#! /usr/bin/env python

import os, sys, re, json
from multiprocessing import Process

class MERGE_LOCAL_RUN_RESULT:
    
    def __init__(self):
        self.stringstartercomp = re.compile(": result from script :")
    
    def conditionmatchfilelist(self, filenameslist, comppattern, targetdirname):
        matchedlist = []
        for fname in filenameslist:
            if comppattern.search(fname):
               fpath = targetdirname+"/"+fname
               f = open(fpath, 'r')
               msglist = f.readlines()
               f.close()
               if self.stringstartercomp.search(msglist[0]):
                  matchedlist.append(fname)
        return matchedlist

    def parseLinuxOrigin(self, WORKENV):
        print "run"

    def runCmd(self, WORKENV):
        filenameslist = os.listdir(WORKENV['LOCALRUNUTILSRCPATH'])
        matchedlinuxlist = self.conditionmatchfilelist(filenameslist, re.compile("linux-", re.I), WORKENV['LOCALRUNUTILSRCPATH'])
        matchedwindowlist = self.conditionmatchfilelist(filenameslist, re.compile("window-", re.I), WORKENV['LOCALRUNUTILSRCPATH'])
        pList = []
        for targets in matchedlinuxlist:
            pass
        for targets in matchedwindowlist:
            p = Process(target=self.parseLinuxOrigin, args=(WORKENV,))
            p.start()
            pList.append(p)
        for p in pList:
            p.join()

        #wincomp = re.compile("window-", re.I)
        #print "hohoho"
