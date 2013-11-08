#!/usr/bin/python          # This is server.py file

import socket              # Import socket module
import threading           # Import threads
import Queue               # Queue to pass data safely between threads

class RobotNetworkService(threading.Thread):
   _recvQueue = 0
   _sendQueue = 0

   def __init__(self, recv_queue, send_queue):
      super(RobotNetworkService, self).__init__()
      self._recvQueue = recv_queue
      self._sendQueue = send_queue
      self.alive = threading.Event()
      self.alive.set()
   
   # Routine for handling messages from the client.
   def receive_thread(self, conn):
      print 'Receive thread started'
      rec_msg = ""

      # Client disconnect is handled here, not sure how I feel about it.
      while (self.alive.isSet() and rec_msg.lower() != "disconnect" and rec_msg.lower() != "quit"):
         # TODO: Add a timeout! 
         rec_msg = conn.recv(1024)

         # recv returns an empty string when the client disconnects
         if rec_msg:
            print 'Server received: ' + rec_msg
            self._recvQueue.put(rec_msg)
         else:
            # Client is gone
            print 'Client disconnected, exiting receive_thread'
            self._recvQueue.put("Client disconnected: broken pipe")
            return

      # Client responsibly told us it was disconnecting
      if (rec_msg.lower() == "quit"):
         print 'Client issued quit, exiting receive_thread'
      elif (rec_msg.lower() == "disconnect"):
         print 'Client issued disconnect, exiting receive_thread'
      else:
         print 'Exiting receive_thread on join request'

   # Routine for accepting a connection and starting the server.
   def send_thread(self):
      print 'Send thread started'

      s = socket.socket()         # Create a socket object
      s.settimeout(1)             # Default timeout of 1 second
      host = socket.gethostname() # Get local machine name
      port = 12345                # Reserve a port for your service.
      try:
         s.bind((host, port))        # Bind to the port
         s.listen(1)                 # Now wait for client connection.
      except socket.error as msg:
         s.close()
         print 'Server socket error, exiting'
         return

      while (self.alive.isSet()):
   
         # Holds message received from the remote
         msg = ""

         print 'Server is waiting for connection!'

         # Try making a connection. If we timeout waiting check the
         # while loop exit condition and keep trying.
         # A timeout here prevents the server thread from blocking
         # even when the program is trying to exit.
         try:
            c, addr = s.accept()     # Establish connection with client.
         except socket.timeout as msg:
            print 'Server timeout on listen'
            continue

         print 'Server received connection from', addr
         c.send('Robot server ready! Starting receive thread')

         # Kick off the thread that will receive messages from the client.
         receiveThread = threading.Thread(target = self.receive_thread, args = [c])
         receiveThread.start()

         # This loop will check for messages to transmit and send them.
         # If the connection is lost, we are told to stop, or the receive
         # thread quits, then break out of the loop.
         # TODO: 'c' check may not be useful here
         while (c and self.alive.isSet() and receiveThread.isAlive()):
            # See if there are messages on the queue, block for a while
            # and bail out if nothing is received.  This allows us to check
            # the stop condition on occasion.
            try:
               msg = self._sendQueue.get(True, 1)
            except Queue.Empty:
               # Not a bad thing, just need to check the exit conditions.
               pass
            else:
               c.send(msg)

         if (receiveThread.isAlive() == False):
            print 'Server disconnected on receive thread death'
         elif (self.alive.isSet() == False):
            print 'Server exiting on join request'
         elif (not c):
            print 'Server disconnected on broken pipe'

         # Left the loop
         c.close()                # Close the connection
         receiveThread.join()

      # Received a quit
      print 'Server closed (Asked to quit)'

   def run(self):
      self.send_thread()

   def join(self, timeout = None):
      self.alive.clear()
      threading.Thread.join(self, timeout)

