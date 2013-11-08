#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

print 'Client is attempting connection...'
s.connect((host, port))
print 'MOTD: ' + s.recv(1024)
msg = ""
while msg != "quit":
   msg = raw_input('Input message: ')
   s.send(msg)
s.close                     # Close the socket when done

