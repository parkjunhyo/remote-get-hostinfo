#! /usr/bin/env python

from var.common.common import Common
from var.common.bash_command import CMD_GET_OS_RELEASE
from var.common.bash_command import CMD_GET_INSTALLED_PACKAGES
from var.common.bash_command import CMD_GET_HOSTNAME
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
            "installedapp":[]
        }
        self.supportedcmd = {
                "rpm -qa\n" : [
                    "centos",
                    "rhel",
                    "fedora",
                    "suse"
                ],
                "dpkg -l | awk \'{print $2\"!!!!!\"$3}\'\n" : [
                    "debian"
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
                 rdict["softwarename"] = splitedtempline[0]
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
                       rdict["softwarename"] = splitedtempline[0]
                       rdict["version"] = splitedtempline[1]
                       rlist.append(rdict)
        else:
           pass
        self.outputformat["installedapp"] = rlist

    def installedPackageForLinux(self, targethost, WORKENV):
        # get IP address
        self.outputformat["ipaddress"] = targethost["host"]
        # get HOST name information
        cmdhostname = CMD_GET_HOSTNAME()
        rdict = cmdhostname.runCmd(targethost, WORKENV)
        self.obtainHostname(rdict)
        #rdictkey = rdict.keys()
        #for keyname in rdictkey:
        #    if re.compile("static hostname",re.I).search(keyname):
        #       self.outputformat["hostname"] = rdict[keyname]
        #       continue
        #    if re.compile("architecture",re.I).search(keyname):
        #       self.outputformat["osarchitecture"] = rdict[keyname]
        #       continue
        # clean and make directory for result
        ipstring = str(''.join(targethost['host'].strip().split('.')))
        RESULTFULLPATH = WORKENV['RESULTPATH']+"/"+targethost["ostype"]+"-"+self.outputformat["hostname"]+"-"+ipstring
        if os.path.isdir(RESULTFULLPATH):
          shutil.rmtree(RESULTFULLPATH)
        os.makedirs(RESULTFULLPATH)
        # get OS information
        cmdos = CMD_GET_OS_RELEASE()
        rdict = cmdos.runCmd(targethost, WORKENV)
        self.obtainOSRelease(rdict)
        #rdictkey = rdict.keys()
        #for keyname in rdictkey:
        #    if re.compile("^name",re.I).search(keyname) and len(keyname) == 4:
        #       self.outputformat["osname"] = self.removeMark(rdict[keyname], "\"")
        #       continue
        #    if re.compile("^version",re.I).search(keyname) and len(keyname) == 7:
        #       self.outputformat["osversion"] = self.removeMark(rdict[keyname], "\"")
        #       continue
        #    if re.compile("^id",re.I).search(keyname) and len(keyname) == 2:
        #       self.outputformat["osid"] = self.removeMark(rdict[keyname], "\"")
        #       continue
        #    if re.compile("id_like",re.I).search(keyname) and len(keyname) == 7:
        #       self.outputformat["osidlike"] = self.removeMark(rdict[keyname], "\"")
        #       continue
        # write file
        #fname = RESULTFULLPATH+"/os-release"
        #f = open(fname, 'w')
        #f.write(str(rdict))
        #f.close()
        # get matched bash command
        bash_command = self.findCmd(rdict)
        cmdinstalled = CMD_GET_INSTALLED_PACKAGES()
        rmsg = cmdinstalled.runCmd(targethost, WORKENV, bash_command)
        #
        self.obtainProduct(bash_command, rmsg)
        #
        #if re.compile("rpm", re.I).search(bash_command):
        #   splitedrmsg = rmsg.split("\r\n")
        #   rlist = []
        #   for templine in splitedrmsg:
        #      splitedtempline = templine.split()
        #      if len(splitedtempline) == 1:
        #         rdict = {}
        #         rdict["softwarename"] = splitedtempline[0]
        #         rdict["version"] = ''
        #         rlist.append(rdict)
        #elif re.compile("dpkg", re.I).search(bash_command):
        #   splitedrmsg = rmsg.split("\r\n")
        #   rlist = []
        #   for templine in splitedrmsg:
        #      splitedtempline = templine.split("!!!!!")
        #      if len(splitedtempline) == 2 and len(splitedtempline[0]) and len(splitedtempline[1]):
        #         except_pattern = re.compile("[\(\)\$\?\/]", re.I)
        #         if not except_pattern.search(splitedtempline[0]) and not except_pattern.search(splitedtempline[1]):
        #            if not re.compile("name",re.I).search(splitedtempline[0]) and not re.compile("version",re.I).search(splitedtempline[1]):
        #               rdict = {}
        #               rdict["softwarename"] = splitedtempline[0]
        #               rdict["version"] = splitedtempline[1]
        #               rlist.append(rdict)
        #else:
        #   pass
        # 
        #splitedrmsg = rmsg.split()
        #rlist = []
        #for templine in splitedrmsg:
        #   splitedby = templine.split("!!!!!")
        #   if len(splitedby) == 2 and not len(splitedby[0]) and not len(splitedby[1]):
        #     rdict = {}
        #     rdict['softwarename'] = splitedby[0]
        #     rdict['version'] = splitedby[-1]
        #     rlist.append(rdict)
        #self.outputformat["installedapp"] = rlist
        # write file
        #fname = RESULTFULLPATH+"/installed-packages"
        #f = open(fname, 'w')
        #f.write(str(rlist))
        #f.write(rmsg)
        #f.close()
        # write file all result
        changelistformat = [self.outputformat]
        fname = RESULTFULLPATH+"/output.json"
        f = open(fname, 'w')
        f.write(json.dumps(changelistformat))
        f.close()
