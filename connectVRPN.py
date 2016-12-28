#!/usr/bin/python
## This is a python script for udp connection to VRPN server

import socket
import sys

ip = "127.0.0.1"
port = 3883

print("Start to connect to VRPN server")
s = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP

while True:
    try:
        data = s.recvfrom(500)
        data = data.decode("utf-8")
        print("data = "+data)
    
    except s.error, msg:
        print 'socket error:' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
