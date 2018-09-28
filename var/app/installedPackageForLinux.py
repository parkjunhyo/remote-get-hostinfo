#! /usr/bin/env python

from var.common.common import Common
from var.common.bash_command import CMD_GET_OS_RELEASE
from var.common.bash_command import CMD_GET_INSTALLED_PACKAGES
import os, shutil, re

class InstalledPackageForLinux:
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

    def findCmd(self, rdict):
        commandlist = self.supportedcmd.keys()
        returnmsg = "exit\n"
        for tempcmd in commandlist:
            for osname in self.supportedcmd[tempcmd]:
                recomp = re.compile(osname, re.I)
                if recomp.search(rdict['ID_LIKE']):
                    return tempcmd
        return returnmsg

    def installedPackageForLinux(self, targethost, WORKENV):
        # clean and make directory for result
        ipstring = str(''.join(targethost['host'].strip().split('.')))
        RESULTFULLPATH = WORKENV['RESULTPATH']+"/"+ipstring+str(targethost['port'])
        if os.path.isdir(RESULTFULLPATH):
          shutil.rmtree(RESULTFULLPATH)
        os.mkdir(RESULTFULLPATH)
        # get OS information
        cmdos = CMD_GET_OS_RELEASE()
        rdict = cmdos.runCmd(targethost, WORKENV)
        # write file
        fname = RESULTFULLPATH+"/os-release"
        f = open(fname, 'w')
        f.write(str(rdict))
        f.close()
        # get matched bash command
        bash_command = self.findCmd(rdict)
        cmdinstalled = CMD_GET_INSTALLED_PACKAGES()
        rmsg = cmdinstalled.runCmd(targethost, WORKENV, bash_command)
        # write file
        fname = RESULTFULLPATH+"/installed-packages"
        f = open(fname, 'w')
        f.write(rmsg)
        f.close()
