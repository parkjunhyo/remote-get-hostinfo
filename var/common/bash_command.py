#! /usr/bin/env python

from var.common.common import Common
import re

#########################################################################################
class CMD_GET_OS_RELEASE:
    def runCmd(self, targethost, WORKENV):
        commclass = Common()
        bash_command = "cat /etc/os-release\n"
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
        tempdict = {}
        for texts in rmsg.split('\r\n')[1:-1]:
            splitedtexts = texts.split("=")
            if len(splitedtexts) == 2:
               tempdict[splitedtexts[0].strip()] = splitedtexts[1].strip()
        return tempdict
#########################################################################################
class CMD_GET_INSTALLED_PACKAGES:
    def runCmd(self, targethost, WORKENV, bash_command):
        commclass = Common()
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
        return rmsg
#########################################################################################
class CMD_GET_HOSTNAME:
    def runCmd(self, targethost, WORKENV):
        commclass = Common()
        bash_command = "hostnamectl\n"
        c, conn = commclass.connectSSHLogin(targethost, WORKENV)
        rmsg = commclass.runBashAfterSSHLogin(c, conn, bash_command)
        tempdict = {}
        for texts in rmsg.split('\r\n')[1:-1]:
            splitedtexts = texts.split(":")
            if len(splitedtexts) == 2:
               tempdict[splitedtexts[0].strip()] = splitedtexts[1].strip()
        return tempdict

