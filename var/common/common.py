#! /usr/bin/env python

import paramiko
import re, time, sys
import os, json, shutil, random
from multiprocessing import Process

#from var.app.installedSoftwareForWindow import InstalledSoftwareForWindow

class Common:
   
    paramiko_out_waittimeout = 1000 * 60 * 1
    paramiko_receive_buffer = 2097152
    response_max_waittime = 60
    response_min_waittime = 10
    garbage_min_waittime = 5
    def connectSSHLogin(self, targethost, WORKENV):
        try:
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # access with private key (RSA)
            if re.match(targethost['method'], 'key'):
               KEYPATH = WORKENV["WORKPATH"]+"/key.d/"+targethost['option']['keyname']
               k = paramiko.RSAKey.from_private_key_file(KEYPATH)
               c.connect(hostname=targethost['host'], port=targethost['port'], username=targethost['username'], pkey = k)
            # access with ID and Password
            else:
               c.connect(hostname=targethost['host'], port=targethost['port'], username=targethost['username'], password = targethost['option']['password'])
            # setting options
            conn = c.invoke_shell()
            conn.settimeout(self.paramiko_out_waittimeout)
            # banner info received
            time.sleep(self.garbage_min_waittime)
            conn.recv(self.paramiko_receive_buffer)
        except:
            print "Error:Common Class:connectSSHLogin"
            c.close()
            sys.exit()
            c.close()
        # after SSH access, excute command
        return c, conn

    def runBashAfterSSHLogin(self, c, conn, bash_command):
        conn.send(bash_command)
        time.sleep(self.response_min_waittime)
        rmsg = conn.recv(self.paramiko_receive_buffer)
        conn.send("exit\n")
        return rmsg

    def disconnectSSHLogin(self, c, conn):
        conn.send("exit\n")

    def testPrintOut(self):
        print "Common Class are included!"

#    def mergeJsonOut(self, TARGETHOSTS, WORKENV):
#        # search used os type
#        alllistostype = []
#        for itemname in TARGETHOSTS:
#           if itemname["ostype"] not in alllistostype:
#             alllistostype.append(itemname["ostype"])
#        # search output directory
#        alllistdir = os.listdir(WORKENV["RESULTPATH"])
#        matchedlist = []
#        for dirname in alllistdir:
#           for prefixstring in alllistostype:
#              if re.compile("^"+prefixstring+"-").search(dirname):
#                 if dirname not in matchedlist:
#                    matchedlist.append(dirname)
#        # find file and read
#        returnalllist = []
#        for dirname in matchedlist:
#           OUTPUTFILEFULLPATH = WORKENV["RESULTPATH"]+"/"+dirname+"/output.json"
#           if os.path.isfile(OUTPUTFILEFULLPATH):
#              f = open(OUTPUTFILEFULLPATH, 'r')
#              rmsg = f.read()
#              f.close()
#              changed_json = json.loads(rmsg)
#              for tempitem in changed_json:
#                 returnalllist.append(tempitem)
#        # create single file
#        OUTPUTJSON = WORKENV["RESULTPATH"]+"/remote-get-hostinfo-output.json"
#        f = open(OUTPUTJSON, 'w')
#        f.write(json.dumps(returnalllist))
#        f.close() 
#
#    def conditionmatchfilelist(self, filenameslist, comppattern, targetdirname):
#        matchedlist = []
#        stringstartercomp = re.compile(": begin result from script :")
#        for fname in filenameslist:
#            if comppattern.search(fname):
#               fpath = targetdirname+"/"+fname
#               f = open(fpath, 'r')
#               msglist = f.readlines()
#               f.close()
#               if stringstartercomp.search(msglist[0]):
#                  matchedlist.append(fname)
#        return matchedlist
#
#    def findListWithPattern(self, msglist, begincpt, endcpt):
#        indexcount = 0
#        beginindex = 0
#        endindex = len(msglist)
#        for rline in msglist:
#            if re.compile(begincpt, re.I).search(rline):
#               beginindex = indexcount
#            if re.compile(endcpt, re.I).search(rline):
#               endindex = indexcount
#               break
#            indexcount = indexcount + 1
#        return msglist[beginindex+1:endindex]
#
#    def changeDictWithMark(self, tmpList, marks):
#        tempDict = {}
#        for item_i in tmpList:
#            splited_list = item_i.strip().split(marks)
#            if len(splited_list) == 2:
#               matchkey = splited_list[0].strip()
#               matchvalue = splited_list[1].strip()
#               if matchkey not in tempDict.keys():
#                  tempDict[matchkey] = matchvalue 
#        return tempDict
#
#    def readASCIIstring(self, targethost, WORKENV):
#        fpath = WORKENV['LOCALRUNUTILSRCPATH']+"/"+targethost
#        tempfilename = "/tmp/"+str(random.random() + os.getpid())
#        bash_cmd = "iconv -c -t ASCII "+fpath+" > "+tempfilename+"\n"
#        os.system(bash_cmd)
#        bash_cmd = "col -b < "+tempfilename+" > "+tempfilename+".bak\n"
#        os.system(bash_cmd)
#        bash_cmd = "mv "+tempfilename+".bak "+fpath
#        os.system(bash_cmd)
#        bash_cmd = "rm -rf "+tempfilename+"*\n"
#        os.system(bash_cmd)
#        # read file
#        f = open(fpath, 'r')
#        msglist = f.readlines()
#        f.close()
#        return fpath, msglist
#
#    def parseWindowOrigin(self, targethost, WORKENV):
#        fpath, msglist = self.readASCIIstring(targethost, WORKENV) 
#        # computersystem search
#        tmpList = self.findListWithPattern(msglist, ": begin computersystem :", ": end computersystem :")
#        csList = [self.changeDictWithMark(tmpList, "=")]
#        # operatingsystem search
#        tmpList = self.findListWithPattern(msglist, ": begin operatingsystem :",": end operatingsystem :")
#        osList = [self.changeDictWithMark(tmpList, "=")]
#        # product search
#        tmpList = self.findListWithPattern(msglist, ": begin product :",": end product :")
#        filteredlist = []
#        for tempstring in tmpList:
#            if re.compile("caption=",re.I).search(tempstring) or re.compile("version=",re.I).search(tempstring):
#               filteredlist.append(tempstring)
#        indexcount = 0
#        prdList = []
#        for tempstring in filteredlist:
#            if re.compile("caption=",re.I).search(tempstring):
#               splitedtempstring = tempstring.strip().split("=")
#               if len(splitedtempstring) == 2:
#                  tempdict = {}
#                  matchkey = splitedtempstring[0].strip() 
#                  matchvalue = splitedtempstring[1].strip() 
#                  tempdict[matchkey] = matchvalue
#                  nextstrings = filteredlist[indexcount+1]
#                  if re.compile("version=",re.I).search(nextstrings):
#                     splitednextstrings = nextstrings.strip().split("=")
#                     if len(splitednextstrings) == 2:
#                        matchkey = splitednextstrings[0].strip()
#                        matchvalue = splitednextstrings[1].strip()
#                        tempdict[matchkey] = matchvalue
#                        prdList.append(tempdict)
#                     else:
#                        prdList.append(tempdict)
#                  else:
#                     prdList.append(tempdict)
#            indexcount = indexcount + 1
#        # run to parse
#        c = InstalledSoftwareForWindow()
#        c.obtainWin32Computersystem(csList)
#        c.obtainWin32Operatingsystem(osList)
#        c.obtainWin32Product(prdList)
#        # Get IP address.
#        removeOringTxtstring = targethost.strip().split(".origin.txt")[0]
#        removeMarkstring = removeOringTxtstring.strip().split("-")[-1]
#        c.outputformat["ipaddress"] = removeMarkstring
#        # OutPut Path  
#        changelistformat = [c.outputformat]
#        fdir = WORKENV['RESULTPATH']+"/"+removeOringTxtstring
#        if os.path.isdir(fdir):
#           shutil.rmtree(fdir)
#        os.makedirs(fdir)
#        fname = fdir+"/output.json"
#        f = open(fname, 'w')
#        f.write(json.dumps(changelistformat))
#        f.close()
# 
#    def parseLinuxOrigin(self, targethost, WORKENV):
#        fpath, msglist = self.readASCIIstring(targethost, WORKENV) 
#        tmpList = self.findListWithPattern(msglist, ": begin hostnamectl :", ": end hostnamectl :")
#        hostList = [self.changeDictWithMark(tmpList, ":")]
#        tmpList = self.findListWithPattern(msglist, ": begin /etc/os-release :", ": end /etc/os-release :")
#        osList = [self.changeDictWithMark(tmpList, "=")]
#        tmpList = self.findListWithPattern(msglist, ": begin product :", "----- : end product : -----")
#        # run to parse
#        #c = InstalledPackageForLinux()
#        #sys.exit()
#
#
#    def convertOriginJson(self, WORKENV):
#        filenameslist = os.listdir(WORKENV['LOCALRUNUTILSRCPATH'])
#        matchedlinuxlist = self.conditionmatchfilelist(filenameslist, re.compile("linux-", re.I), WORKENV['LOCALRUNUTILSRCPATH'])
#        matchedwindowlist = self.conditionmatchfilelist(filenameslist, re.compile("window-", re.I), WORKENV['LOCALRUNUTILSRCPATH'])
#        pList = []
#        for targethost in matchedlinuxlist:
#            p = Process(target=self.parseLinuxOrigin, args=(targethost, WORKENV,))
#            p.start()
#            pList.append(p)
#        for targethost in matchedwindowlist:
#            p = Process(target=self.parseWindowOrigin, args=(targethost, WORKENV,))
#            p.start()
#            pList.append(p)
#        for p in pList:
#            p.join()
