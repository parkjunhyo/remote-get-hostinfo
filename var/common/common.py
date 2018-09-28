#! /usr/bin/env python

import paramiko
import re, time, sys

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
        #conn.send("dpkg -l | awk '{print $2\"@\"$3}'\n")
        #time.sleep(self.response_min_waittime)
        #receivemsg = conn.recv(self.paramiko_receive_buffer)
        #conn.send("exit\n")
        #print receivemsg