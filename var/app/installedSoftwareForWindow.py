#! /usr/bin/env python

import os, shutil, re, sys, json
import wmi_client_wrapper as wmi

class InstalledSoftwareForWindow:
    def __init__(self):
        self.outputformat = {
            "hostname":"",
            "ipaddress":"",
            "osname":"",
            "osdomain":"",
            "osworkgroup":"",
            "osversion":"",
            "osid":"",
            "osidlike":"",
            "osarchitecture":"",
            "installedapp":[]
        }

    def obtainWin32Computersystem(self, rdict):
        fixed_rdict = rdict[0]
        fixed_rdictkey = fixed_rdict.keys()
        for kname in fixed_rdictkey:
            if re.compile("^name",re.I).search(kname) and len(kname) == 4:
               self.outputformat["hostname"] = fixed_rdict[kname].strip()
               continue
            elif re.compile("^workgroup",re.I).search(kname) and len(kname) == 9:
               self.outputformat["osworkgroup"] = fixed_rdict[kname].strip()
               continue
            elif re.compile("^domain",re.I).search(kname) and len(kname) == 6:
               self.outputformat["osdomain"] = fixed_rdict[kname].strip()
               continue

    def obtainWin32Operatingsystem(self, rdict):
        fixed_rdict = rdict[0]
        fixed_rdictkey = fixed_rdict.keys()
        for kname in fixed_rdictkey:
            if re.compile("^caption",re.I).search(kname) and len(kname) == 7:
               self.outputformat["osname"] = fixed_rdict[kname].strip()
               continue
            elif re.compile("^osarchitecture",re.I).search(kname) and len(kname) == 14:
               self.outputformat["osarchitecture"] = fixed_rdict[kname].strip()
               continue
            elif re.compile("^version",re.I).search(kname) and len(kname) == 7:
               self.outputformat["osversion"] = fixed_rdict[kname].strip()
               continue

    def obtainWin32Product(self, rdict):
        applist = []
        for fixed_rdict in rdict:
           tmpdict = {}
           fixed_rdictkey = fixed_rdict.keys()
           for kname in fixed_rdictkey:
               if re.compile("^caption",re.I).search(kname) and len(kname) == 7:
                  tmpdict["softwarename"] = fixed_rdict[kname].strip()
                  #tmpdict["caption"] = fixed_rdict[kname].strip()
                  continue
               elif re.compile("^version",re.I).search(kname) and len(kname) == 7:
                  tmpdict["version"] = fixed_rdict[kname].strip()
                  continue
           applist.append(tmpdict)
        self.outputformat["installedapp"] = applist

    def installedSoftwareForWindow(self, targethost, WORKENV):
        #  
        wmic = wmi.WmiClientWrapper(
            username=targethost['username'],
            password=targethost['option']['password'],
            host=targethost['host'],
        )
        #
        self.outputformat["ipaddress"] = targethost['host'] 
        #
        rdict = wmic.query("SELECT * FROM Win32_ComputerSystem")
        self.obtainWin32Computersystem(rdict)
        # clean and make directory for result
        ipstring = str(''.join(targethost['host'].strip().split('.')))
        RESULTFULLPATH = WORKENV['RESULTPATH']+"/"+targethost["ostype"]+"-"+self.outputformat["hostname"]+"-"+ipstring
        if os.path.isdir(RESULTFULLPATH):
          shutil.rmtree(RESULTFULLPATH)
        os.makedirs(RESULTFULLPATH)
        # write file for Win32_OperatingSystem
        rdict = wmic.query("SELECT * FROM Win32_OperatingSystem")
        self.obtainWin32Operatingsystem(rdict)
        # wirte file for Win32_Product
        rdict = wmic.query("SELECT * FROM Win32_Product")
        self.obtainWin32Product(rdict)
        # write all files
        changelistformat = [self.outputformat]
        fname = RESULTFULLPATH+"/output.json"
        f = open(fname, 'w')
        f.write(json.dumps(changelistformat))
        f.close()

