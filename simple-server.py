#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from motor import MotorMaster

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
msg = ""
while msg != "quit":
   print 'Server is waiting for connection!'
   c, addr = s.accept()     # Establish connection with client.
   print 'Server got connection from', addr
   c.send('Thank you for connecting')
   while msg != "quit":
      msg = c.recv(1024)
      print 'Server received: ' + msg

c.close()                # Close the connection

