#! /usr/bin/env python

import os, sys, re, json

from env import WORKENV
from hosts import TARGETHOSTS
from var.app.installedPackageForLinux import InstalledPackageForLinux
from var.app.installedSoftwareForWindow import InstalledSoftwareForWindow

#from var.common.mergeremoterunresult import MERGE_REMOTE_RUN_RESULT
#from var.common.mergelocalrunresult import MERGE_LOCAL_RUN_RESULT
from var.common.common import Common
from var.common.commonutils import Commonutils

from multiprocessing import Process
import paramiko

class Main:
    
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.installedPackageForLinux = InstalledPackageForLinux()
        self.installedSoftwareForWindow = InstalledSoftwareForWindow()

    def mergeJsonOut(self, runmethod):
        if runmethod == 2:
           c = Commonutils()
           c.mergeJsonOut(TARGETHOSTS, WORKENV)

    def convertOriginJson(self, runmethod):
        if runmethod == 2:
           c = Commonutils()
           c.convertOriginJson(WORKENV)

    def runRemoteRun(self, runmethod):
        if runmethod == 1:
           pList = []
           for targethost in TARGETHOSTS:
               if re.match(targethost['ostype'], "linux"):
                  p = Process(target=self.installedPackageForLinux.installedPackageForLinux, args=(targethost, WORKENV,))
               elif re.match(targethost['ostype'], "window"):
                  p = Process(target=self.installedSoftwareForWindow.installedSoftwareForWindow, args=(targethost, WORKENV,))
               else:
                  continue
               p.start()
               pList.append(p)
           for p in pList:
               p.join()
        else:
           print "this option does not work"
           sys.exit()
    

    def runInstance(self, inputArgvList, runmethod):
        if runmethod == 1:
           argcountnumber = len(inputArgvList)
           if argcountnumber > 2:
              print "use Option help"
              sys.exit()
           else:
              if argcountnumber == 2:
                 optionstring = inputArgvList[1]
                 optinlist = dir(self)
                 newoptlist = []
                 for optn in optinlist:
                     if not re.compile("_").search(optn):
                        newoptlist.append(optn)
                 if optionstring not in newoptlist:
                    print newoptlist
                    print "select one of items for options"
                    sys.exit()
                 else:
                    getattr(self, optionstring)(2)
              else: 
                 self.runRemoteRun(1)



if __name__ == "__main__":
    # Input Parameter
    inputArgvList = sys.argv
    # Run
    m = Main()
    m.runInstance(inputArgvList, 1)

