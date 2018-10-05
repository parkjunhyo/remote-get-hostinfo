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

    def parseWindowOrigin(self, targethost, WORKENV):
        fpath = WORKENV['LOCALRUNUTILSRCPATH']+"/"+targethost
        # read files
        f = open(fpath, 'r')
        msglist = f.readlines()
        f.close()
        # computersystem search
        indexcount = 0
        beginindex = 0
        endindex = len(msglist)
        for rline in msglist:
            if re.compile(": begin computersystem :",re.I).search(rline):
               beginindex = indexcount
               continue
            if re.compile(": end computersystem :",re.I).search(rline):
               endindex = indexcount
               continue
            indexcount = indexcount + 1
        print len(msglist[beginindex+1:endindex])
        print len(msglist[beginindex+1].split())
        print msglist[endindex-1]
        print len(msglist[endindex-1].split())
        sys.exit()
        

    def runCmd(self, WORKENV):
        filenameslist = os.listdir(WORKENV['LOCALRUNUTILSRCPATH'])
        matchedlinuxlist = self.conditionmatchfilelist(filenameslist, re.compile("linux-", re.I), WORKENV['LOCALRUNUTILSRCPATH'])
        matchedwindowlist = self.conditionmatchfilelist(filenameslist, re.compile("window-", re.I), WORKENV['LOCALRUNUTILSRCPATH'])
        pList = []
        for targethost in matchedlinuxlist:
            pass
        for targethost in matchedwindowlist:
            p = Process(target=self.parseWindowOrigin, args=(targethost, WORKENV,))
            p.start()
            pList.append(p)
        for p in pList:
            p.join()

        #wincomp = re.compile("window-", re.I)
        #print "hohoho"
