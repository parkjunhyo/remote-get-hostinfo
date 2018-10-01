#! /usr/bin/env python
TARGETHOSTS = [
 {
   "host" : "your-host-ip",
   "port" : 22,
   "username" : "ubuntu",
   "method" : "key",
   "ostype" : "linux",
   "option" : {
      "keyname" : "your-private.pem"
   }
 },
 {
   "host" : "your-host-ip",
   "port" : 145,
   "username" : "Administrator",
   "method" : "password",
   "ostype" : "window",
   "option" : {
      "password" : "your-passowrd"
   }
 },
]
