#! /usr/bin/env python

import os, sys, re

# {'WORKPATH': '/root/sample.code'}
# [{'host': '54.180.9.144', 'method': 'key', 'option': {'keyname': 'aws-seoul-junhyo2.park-kp1.pem'}}]
from env import WORKENV
from hosts import TARGETHOSTS
#from var.common.common import Common
from var.app.installedPackageForLinux import InstalledPackageForLinux
from var.app.installedSoftwareForWindow import InstalledSoftwareForWindow

from multiprocessing import Process
import paramiko

class Main:
    
    def __init__(self):
        self.installedPackageForLinux = InstalledPackageForLinux()
        self.installedSoftwareForWindow = InstalledSoftwareForWindow()

    def runInstance(self, inputArgvList):
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



if __name__ == "__main__":
    # Input Parameter
    inputArgvList = sys.argv
    # Run
    m = Main()
    m.runInstance(inputArgvList)

