#! /usr/bin/env python

import os, sys, re, json

from env import WORKENV
from hosts import TARGETHOSTS
from var.app.installedPackageForLinux import InstalledPackageForLinux
from var.app.installedSoftwareForWindow import InstalledSoftwareForWindow

from var.common.mergeremoterunresult import MERGE_REMOTE_RUN_RESULT

from multiprocessing import Process
import paramiko

class Main:
    
    def __init__(self):
        self.installedPackageForLinux = InstalledPackageForLinux()
        self.installedSoftwareForWindow = InstalledSoftwareForWindow()

    def mergeremoterunresult(self, runmethod):
        if runmethod == 2:
           c = MERGE_REMOTE_RUN_RESULT()
           c.runCmd(TARGETHOSTS, WORKENV)

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
               pList.append(p)
               p.start()
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
                 if optionstring not in optinlist:
                    print optinlist
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

