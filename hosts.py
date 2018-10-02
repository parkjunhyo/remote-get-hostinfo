#! /usr/bin/env python
TARGETHOSTS = [
 {
   "host" : "172.22.0.216",
   "port" : 38300,
   "username" : "ubuntu",
   "method" : "key",
   "ostype" : "linux",
   "option" : {
      "keyname" : "your-private.pem"
   }
 },
 {
   "host" : "172.22.0.151",
   "port" : 22,
   "username" : "centos",
   "method" : "key",
   "ostype" : "linux",
   "option" : {
      "keyname" : "your-private.pem"
   }
 },
 {
   "host" : "172.22.0.123",
   "port" : 145,
   "username" : "your-id",
   "method" : "password",
   "ostype" : "window",
   "option" : {
      "password" : "your-password"
   }
 },
]
