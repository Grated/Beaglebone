#!/usr/bin/python

import Queue
import time
import threading           # Import threads
from motor_thread import MotorThread
from server import RobotNetworkService

def help(sendQueue):
   sendQueue.put('~~Robot server help~~\n')
   sendQueue.put('Commands:\n')
   sendQueue.put('help - displays this menu\n')
   sendQueue.put('quit - Quits client and server\n')
   sendQueue.put('disconnect - Disconnect client only\n')

# Instantiate queues
motorQueue = Queue.Queue()
cmdQueue = Queue.Queue()
sendQueue = Queue.Queue()

# Kick off motorControl thread
motorControl = MotorThread(motorQueue, sendQueue)
motorControl.start()

# Start server
netService = RobotNetworkService(cmdQueue, sendQueue)
netService.start()

msg = ""
while (msg != "quit"):
   # TODO: Verify threads stay alive.
   if (motorControl.isAlive() == False):
      print 'Motor control thread died!'
      break
   if (netService.isAlive() == False):
      print 'Network service thread died!'
      break

   # TODO: Require a heartbeat message from the remote
   try:
      msg = cmdQueue.get(True, 1)
   except Queue.Empty:
      # Not a bad thing, just need to check the exit conditions.
      pass
   else:
      print 'Received command: ' + msg
      words = msg.split()
      if (words[0] == "motor"):
         motorControl.putCmd(msg)

#####################################################################
# Stop the motors and anything else we don't want running after the
# program exits.
#####################################################################
# TODO: Stop the motors and whatever else
motorQueue.put("motor 0 0")
# Let the motor thread get the message
# TODO: Is there a better way to guarantee this?
time.sleep(1)

#####################################################################
# Clean up all the threads
#####################################################################
netService.join()
motorControl.join()
print 'Robot exit'


