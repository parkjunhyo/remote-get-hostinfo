#! /usr/bin/env python
TARGETHOSTS = [
 {
   "host" : "your-ip-address",
   "port" : 22,
   "username" : "ubuntu",
   "method" : "key",
   "option" : {
      "keyname" : "your-private.pem"
   }
 },
 {
   "host" : "your-ip-address",
   "port" : 38300,
   "username" : "root",
   "method" : "password",
   "option" : {
      "password" : "your-password"
   }
 }
]
