#! /usr/bin/env python

import os, sys

# {'WORKPATH': '/root/sample.code'}
# [{'host': '54.180.9.144', 'method': 'key', 'option': {'keyname': 'aws-seoul-junhyo2.park-kp1.pem'}}]
from env import WORKENV
from hosts import TARGETHOSTS
#from var.common.common import Common
from var.app.installedPackageForLinux import InstalledPackageForLinux

from multiprocessing import Process
import paramiko

class Main:
    
    def __init__(self):
        #self.common = Common()
        self.installedPackageForLinux = InstalledPackageForLinux()

    def runInstance(self, inputArgvList):
        pList = []
        for targethost in TARGETHOSTS:
            p = Process(target=self.installedPackageForLinux.installedPackageForLinux, args=(targethost, WORKENV,))
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

