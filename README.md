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
  - 0.2 : 201810, Local running case Possible 

How to Use for remote access mode

1. chagne to env.py for your enviromment.
   - WORKENV = {
        "WORKPATH" : "/home/ubuntu/applications/remote-get-hostinfo",
        "RESULTPATH" : "/tmp",
        "LOCALRUNUTILSRCPATH" : "/home/ubuntu/applications/remote-get-hostinfo/utils/local-run-scripts/src"
     }
   - "RESULTPATH" are used to get the result after complete this script.
   - "LOCALRUNUTILSRCPATH" are used to convert and merge local result files which are copied from local host after running locally.

2. Add to hosts information to access in hosts.py
   - TARGETHOSTS = [{
   "host" : "172.22.0.216",
   "port" : 38300,
   "username" : "ubuntu",
   "method" : "key",
   "ostype" : "linux",
   "option" : {
      "keyname" : "your-private.pem"
   }
   }]
   - "method" should be one of "key" or "password"
   - "ostype" should be one of "linux" or "window"
   - "option" should has "keyname" (SSH Case, key mode) or "password" (Passowrd Case, password mode)

3. Run one of command below.
   - "./runMain.py" : remote access and get the result
   - "./runMain.py convertOriginJson" : convert and parse the file which are copied from local hosts.
   - "./runMain.py mergeJsonOut" : conver and merge all result file to create single file.
   - For remote-run, Just run "./runMain.py" and "./runMain.py mergeJsonOut"

4. After this script. I can get the result in "RESULTPATH", By default, I use "/tmp" directory for the result.
   - Directory name should be similar with "<linux- or window->". 

How to Use for local run mode

1. Copy and locate the files which are obtained on local hosts after running in "LOCALRUNUTILSRCPATH"

2. The bash script and batch file is located in upper directory of "LOCALRUNUTILSRCPATH".
   There are "run-linux.sh" and "run-window.cmd". Download these file on local hosts, and run this.
   I will get the "<linux-local or window-local>" files. I need to copy and move these file into the server.

3. "./runMain.py convertOriginJson" and "./runMain.py mergeJsonOut"


