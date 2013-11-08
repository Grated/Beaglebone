#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import threading           # Import threads
import time                # for sleep

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

# Routine for receiving messages from the server.
def receive_thread(conn):
   print 'Receive thread started'
   rec_msg = "temp"
   while rec_msg:
      rec_msg = conn.recv(1024)
      print rec_msg
   print 'Receive thread closed'

print 'Client is attempting connection...'
s.connect((host, port))
print 'MOTD: ' + s.recv(1024)
msg = ""
receiveThread = threading.Thread(target = receive_thread, args = [s])
receiveThread.start()
while msg.lower() != "quit" and msg.lower() != "disconnect":
   msg = raw_input('Input message: ')
   s.send(msg)
   # Best idea so far for letting receive thread print
   # TODO: What's better?
   time.sleep(1)

print 'Client disconnecting'
s.close                     # Close the socket when done
receiveThread.join()
print 'Client closed'

