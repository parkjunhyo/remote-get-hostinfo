#! /usr/bin/env python

from var.common.common import Common
import re, sys

#########################################################################################
class CMD_GET_OS_RELEASE:
    def parseMsg(self, rmsg, tempdict, option):
        for texts in rmsg.split('\r\n')[1:-1]:
            splitedtexts = texts.split("=")
            if len(splitedtexts) == 2 and not re.compile("echo",re.I).search(texts):
               if option == 1:
                  tempdict[splitedtexts[0].strip()] = splitedtexts[1].strip()
               elif option == 2:
                  tempdict[splitedtexts[0].strip()] = splitedtexts[1].strip().lower()
        return tempdict

    def runCmd(self, targethost, WORKENV, supportedcmd):
        commclass = Common()
        # Get ID Like
        IDLIKE_bash_command = "echo ID_LIKE=$(sudo find /etc/ -iname \"*-release\" | awk -F \"[/]\" '{if(NF==3) print $NF;}' | awk -F \"[-]\" '{printf $1\" \"}')\n"
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, IDLIKE_bash_command)
        IDLIKE_rmsg = rmsg
        IDLIKE_rmsg_splited = []
        for linevalue in rmsg.strip().split("\r\n")[1:-1]:
            if re.compile("ID_LIKE=", re.I).search(linevalue):
               splitedline = linevalue.strip().split("=")[-1].strip().split()
               for it in splitedline:
                   if it not in IDLIKE_rmsg_splited:
                      IDLIKE_rmsg_splited.append(it)
        # select command
        tempdict = {}
        if "os" in IDLIKE_rmsg_splited:
           bash_command = "sudo find /etc/ -iname 'os-release' | xargs cat\n"
           c, conn = commclass.connectSSHLogin(targethost, WORKENV)
           rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
           tempdict = self.parseMsg(rmsg, tempdict, 1)
        else:
           # GET ALL DISTRIBUTION FOR LINUX
           distsort = []
           for tempkeyname in supportedcmd.keys():
               for tempvalue in supportedcmd[tempkeyname]: 
                   if tempvalue  not in distsort:
                      distsort.append(tempvalue)
           # Get NAME Field
           namefield = ("system", "redhat", "centos", "lsb")
           for nf in namefield:
               if nf in IDLIKE_rmsg_splited:
                  if re.compile(nf, re.I).search("system"):
                     bash_command = "echo NAME=$(sudo find /etc/ -iname 'system-release' | xargs cat | awk '{if(NR==1) print $0}')\n"
                  elif re.compile(nf, re.I).search("redhat"):
                     bash_command = "echo NAME=$(sudo find /etc/ -iname 'redhat-release' | xargs cat | awk '{if(NR==1) print $0}')\n"
                  elif re.compile(nf, re.I).search("centos"):
                     bash_command = "echo NAME=$(sudo find /etc/ -iname 'centos-release' | xargs cat | awk '{if(NR==1) print $0}')\n"
                  elif re.compile(nf, re.I).search("lsb"):
                     bash_command = "echo NAME=$(sudo find /etc/ -iname 'lsb-release' | xargs cat | grep -i DISTRIB_DESCRIPTION | awk -F\"[=]\" '{if(NR==1) print $2}')\n"
                  else:
                     bash_command = "echo NAME=$(sudo find /etc/ -iname 'issue' | xargs cat | awk '{if(NR==1) print $0}')\n"
                  c, conn = commclass.connectSSHLogin(targethost, WORKENV)
                  rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
                  # validation
                  vstatus = 1
                  for temps in rmsg.strip().split("\r\n")[1:-1]:
                      if re.compile("NAME=", re.I).search(temps):
                         if not len(str(temps.strip().split("NAME=")[-1]).strip()):
                            vstatus = 0
                  if vstatus:
                     tempdict = self.parseMsg(rmsg, tempdict, 1)
                  else:
                     continue 
               else:
                  continue
           # GET ID Like Field
           tempdict = self.parseMsg(IDLIKE_rmsg, tempdict, 2)
           # GET ID
           splitednames = tempdict["NAME"].strip().split()
           if len(splitednames) >= 2:
              parsedstring = str("".join(splitednames[0:2])).lower()
           else:
              parsedstring = splitednames[0].lower()
           for distn in distsort:
               if re.compile(distn, re.I).search(parsedstring):
                  if re.compile("redhat", re.I).search(parsedstring):
                     tempdict["ID"] = "rhel"
                  elif re.compile("suse", re.I).search(parsedstring):
                     tempdict["ID"] = "sles"
                  else:
                     tempdict["ID"] = parsedstring
           # GET VERSION
           tempdict["VERSION"] = str(tempdict["NAME"].strip().split("release")[-1]).lower()
        return tempdict
#########################################################################################
class CMD_GET_INSTALLED_PACKAGES:
    def runCmd(self, targethost, WORKENV, bash_command):
        commclass = Common()
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
        return rmsg
#########################################################################################
class CMD_GET_KERNAL_VER:
    def runCmd(self, targethost, WORKENV):
        bash_command = "echo oskernal=$(cat /proc/version | awk -F\"[(]\" '{print $1}')\n"
        commclass = Common()
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
        return rmsg
#########################################################################################
class CMD_GET_HOSTNAME:
    def parseMsg(self, rmsg, tempdict):
        for texts in rmsg.split('\r\n')[1:-1]:
            splitedtexts = texts.split(":")
            if len(splitedtexts) == 2 and not re.compile("echo",re.I).search(texts):
               tempdict[splitedtexts[0].strip()] = splitedtexts[1].strip()
        return tempdict

    def runCmd(self, targethost, WORKENV, necessary_keynames):
        commclass = Common()
        bash_command = "hostnamectl\n"
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
        tempdict = {}
        tempdict = self.parseMsg(rmsg, tempdict)
        # Confirm main key existance 
        tempdictkeyname = tempdict.keys()
        for keyname in necessary_keynames:
            matchstatus = 0
            for kn in tempdictkeyname:
                if re.compile(keyname, re.I).match(kn):
                   matchstatus = 1 
            if not matchstatus:
                if re.compile(keyname, re.I).match("Static hostname"):
                   bash_command = "echo Static hostname: $(hostname)\n"
                   c, conn = commclass.connectSSHLogin(targethost, WORKENV)
                   rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
                   tempdict = self.parseMsg(rmsg, tempdict)
                elif re.compile(keyname, re.I).match("Architecture"):
                   bash_command = "echo Architecture: $(uname -i)\n"
                   c, conn = commclass.connectSSHLogin(targethost, WORKENV)
                   rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
                   tempdict = self.parseMsg(rmsg, tempdict)
                   # check the status
                   if re.compile("unknown", re.I).search(tempdict['Architecture']):
                      bash_command = "echo Architecture: $(uname -m)\n"
                      c, conn = commclass.connectSSHLogin(targethost, WORKENV)
                      rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
                      tempdict = self.parseMsg(rmsg, tempdict)
        return tempdict

