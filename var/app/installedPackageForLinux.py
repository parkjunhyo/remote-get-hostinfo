#! /usr/bin/env python

from var.common.common import Common
from var.common.bash_command import CMD_GET_OS_RELEASE
from var.common.bash_command import CMD_GET_INSTALLED_PACKAGES
from var.common.bash_command import CMD_GET_HOSTNAME
from var.common.bash_command import CMD_GET_KERNAL_VER
import os, shutil, re, sys, json

class InstalledPackageForLinux:
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
            "oskernal":"",
            "installedapp":[]
        }
        self.supportedcmd = {
                "rpm -qa\n" : [
                    "centos",
                    "rhel",
                    "redhat",
                    "fedora",
                    "suse",
                    "sles",
                ],
                "dpkg -l | awk \'{print $2\"!!!!!\"$3}\'\n" : [
                    "debian",
                    "ubuntu",
                ]
        }

    def findCmd(self, rdict):
        commandlist = self.supportedcmd.keys()
        returnmsg = "exit\n"
        for tempcmd in commandlist:
            for osname in self.supportedcmd[tempcmd]:
                recomp = re.compile(osname, re.I)
                #
                if 'ID_LIKE' in rdict.keys():
                   targetIDname = 'ID_LIKE'
                else:
                   targetIDname = 'ID'
                # 
                if recomp.search(rdict[targetIDname]):
                    return tempcmd
        return returnmsg

    def removeMark(self, string_value, mark):
        compilepattern = re.compile(mark, re.I)
        if compilepattern.search(string_value):
           return string_value.strip().split(mark)[1]
        return string_value

    def obtainHostname(self, rdict):
        rdictkey = rdict.keys()
        for keyname in rdictkey:
            if re.compile("static hostname",re.I).search(keyname):
               self.outputformat["hostname"] = rdict[keyname]
               continue
            if re.compile("architecture",re.I).search(keyname):
               self.outputformat["osarchitecture"] = rdict[keyname]
               continue

    def obtainOSRelease(self, rdict):
        rdictkey = rdict.keys()
        for keyname in rdictkey:
            if re.compile("^name",re.I).search(keyname) and len(keyname) == 4:
               self.outputformat["osname"] = self.removeMark(rdict[keyname], "\"")
               continue
            if re.compile("^version",re.I).search(keyname) and len(keyname) == 7:
               self.outputformat["osversion"] = self.removeMark(rdict[keyname], "\"")
               continue
            if re.compile("^id",re.I).search(keyname) and len(keyname) == 2:
               self.outputformat["osid"] = self.removeMark(rdict[keyname], "\"")
               continue
            if re.compile("id_like",re.I).search(keyname) and len(keyname) == 7:
               self.outputformat["osidlike"] = self.removeMark(rdict[keyname], "\"")
               continue

    def obtainProduct(self, bash_command, rmsg):
        if re.compile("rpm", re.I).search(bash_command):
           splitedrmsg = rmsg.split("\r\n")
           rlist = []
           for templine in splitedrmsg:
              splitedtempline = templine.split()
              if len(splitedtempline) == 1:
                 rdict = {}
                 rdict["softwarename"] = splitedtempline[0].strip()
                 rdict["version"] = ''
                 rlist.append(rdict)
        elif re.compile("dpkg", re.I).search(bash_command):
           splitedrmsg = rmsg.split("\r\n")
           rlist = []
           for templine in splitedrmsg:
              splitedtempline = templine.split("!!!!!")
              if len(splitedtempline) == 2 and len(splitedtempline[0]) and len(splitedtempline[1]):
                 except_pattern = re.compile("[\(\)\$\?\/]", re.I)
                 if not except_pattern.search(splitedtempline[0]) and not except_pattern.search(splitedtempline[1]):
                    if not re.compile("name",re.I).search(splitedtempline[0]) and not re.compile("version",re.I).search(splitedtempline[1]):
                       rdict = {}
                       rdict["softwarename"] = splitedtempline[0].strip()
                       rdict["version"] = splitedtempline[1].strip()
                       rlist.append(rdict)
        else:
           pass
        self.outputformat["installedapp"] = rlist

    def obtainKernal(self, rmsg):
        #for texts in rmsg.split('\r\n')[1:-1]:
        for texts in rmsg.split('\r\n'):
            splitedtexts = texts.split("=")
            if len(splitedtexts) == 2 and not re.compile("echo",re.I).search(texts):
               tempkeyname = splitedtexts[0].strip()
               if re.compile("oskernal",re.I).search(tempkeyname):
                  self.outputformat[tempkeyname] = splitedtexts[1].strip()

    def installedPackageForLinux(self, targethost, WORKENV):
        # get IP address
        self.outputformat["ipaddress"] = targethost["host"]
        # get HOST name information
        cmdhostname = CMD_GET_HOSTNAME()
        necessary_keynames = ["Static hostname", "Architecture"]
        rdict = cmdhostname.runCmd(targethost, WORKENV, necessary_keynames)
        self.obtainHostname(rdict)
        # clean and make directory for result
        ipstring = str(''.join(targethost['host'].strip().split('.')))
        RESULTFULLPATH = WORKENV['RESULTPATH']+"/"+targethost["ostype"]+"-"+self.outputformat["hostname"]+"-"+ipstring
        if os.path.isdir(RESULTFULLPATH):
          shutil.rmtree(RESULTFULLPATH)
        os.makedirs(RESULTFULLPATH)
        # get OS information
        cmdos = CMD_GET_OS_RELEASE()
        #necessary_keynames = ["NAME", "VERSION", "ID", "ID_LIKE"]
        rdict = cmdos.runCmd(targethost, WORKENV, self.supportedcmd)
        self.obtainOSRelease(rdict)
        # get matched bash command
        bash_command = self.findCmd(rdict)
        cmdinstalled = CMD_GET_INSTALLED_PACKAGES()
        rmsg = cmdinstalled.runCmd(targethost, WORKENV, bash_command)
        self.obtainProduct(bash_command, rmsg)
        # get linux kernal version
        cmdkernal = CMD_GET_KERNAL_VER()
        rmsg = cmdkernal.runCmd(targethost, WORKENV)
        self.obtainKernal(rmsg)
        # write file all result
        changelistformat = [self.outputformat]
        fname = RESULTFULLPATH+"/output.json"
        f = open(fname, 'w')
        f.write(json.dumps(changelistformat))
        f.close()
