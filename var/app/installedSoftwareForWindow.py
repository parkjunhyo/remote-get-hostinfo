#! /usr/bin/env python

import os, shutil, re
import wmi_client_wrapper as wmi

class InstalledSoftwareForWindow:
    def __init__(self):
        self.supportedcmd = {
                "rpm -qa --last\n" : [
                    "centos",
                    "rhel",
                    "fedora",
                    "suse"
                ],
                "dpkg -l | awk \'{print $2\"!!!!!\"$3}\'\n" : [
                    "debian"
                ]
        }

    def installedSoftwareForWindow(self, targethost, WORKENV):
        # clean and make directory for result
        ipstring = str(''.join(targethost['host'].strip().split('.')))
        RESULTFULLPATH = WORKENV['RESULTPATH']+"/"+ipstring+str(targethost['port'])
        if os.path.isdir(RESULTFULLPATH):
          shutil.rmtree(RESULTFULLPATH)
        os.mkdir(RESULTFULLPATH)
        # 
        wmic = wmi.WmiClientWrapper(
            username=targethost['username'],
            password=targethost['option']['password'],
            host=targethost['host'],
        )
        # write file for Win32_OperatingSystem
        rdict = wmic.query("SELECT * FROM Win32_OperatingSystem")
        fname = RESULTFULLPATH+"/Win32_OperatingSystem"
        f = open(fname, 'w')
        f.write(str(rdict))
        f.close()
        # wirte file for Win32_Product
        rdict = wmic.query("SELECT * FROM Win32_Product")
        fname = RESULTFULLPATH+"/Win32_Product"
        f = open(fname, 'w')
        f.write(str(rdict))
        f.close()
