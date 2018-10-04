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

    def mergeremoterunresult(self):
        c = MERGE_REMOTE_RUN_RESULT()
        c.runCmd(TARGETHOSTS, WORKENV)

    def runRemoteRun(self):
        # run remote access and run command
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


    def runInstance(self, inputArgvList):
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
                 getattr(self, optionstring)()
           else: 
              # run remote access and run command
              self.runRemoteRun()



if __name__ == "__main__":
    # Input Parameter
    inputArgvList = sys.argv
    # Run
    m = Main()
    m.runInstance(inputArgvList)

