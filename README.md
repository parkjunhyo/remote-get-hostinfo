# remote-get-hostinfo

This code is utilized to obtain information from remote Linux Hosts. 
There are some important files to use this script.

1. key.d
   you need insert RSA private key to access Linux hosts
2. env.py
   you need change with your directory path
3. hosts.py
   this is host imformation
   method type should be "key" or "password"


Version 
  - 0.1 : 201809, Installed Package information GET Possible

How to Use

1. chagne to env.py for your enviromment.
   WORKENV = {
        "WORKPATH" : "/root/remote-get-hostinfo",
        "RESULTPATH" : "/tmp"
   }
   "RESULTPATH" are used to get the result after complete this script.

2. Add to hosts information to access in hosts.py
   {
   "host" : "54.180.9.144",
   "port" : 22,
   "username" : "ubuntu",
   "method" : "key",
   "option" : {
      "keyname" : "aws-seoul-junhyo2.park-kp1.pem"
   }
   }
   Most of variables are necessary. "method" should be one of "key" or "password"
   
3. Run "./runMain.py"

4. After this script. I can get the result in "RESULTPATH", In default case, I use "/tmp" directory.
   There are serveral directory. The name of directory is combined with IP address and Port number. For example, 
   your host IP address is "175.192.3.124" and SSH port is "3294", the directory name should 17519231242394.

5. Look at the reuslt directory.
   There are some file. (Look at the Version Information) Every files are seperated by the feature.
   


