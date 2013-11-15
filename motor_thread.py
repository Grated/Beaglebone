#!/usr/bin/python

import threading
import Queue                  # Queue to pass data safely between threads
import time                   # for sleep
from motor import MotorMaster # Import motor module

# Contains the thread used to update motor state.
# 

# Slews to a speed
def _slew(self, target, current):
   if (target < current):

# Accepts a queue that sends motor commands.
# Commands are used to update the motor state, if no command
# is available will sleep a bit and see if anything needs to 
# be done.

class MotorThread:
   #<private>
   _cmdQueue = 0
   _respQueue = 0
   _motors = MotorMaster()
   _running = False
   _TheThread = 0

   def __init__(self, cmdQueue, respQueue):
      self._cmdQueue = cmdQueue
      self._respQueue = respQueue

   def _run(self):
      print 'Motor thread running'
      
      while (self._running == True):
         time.sleep(0.5)
         if (self._cmdQueue.empty() == False):
            cmd = self._cmdQueue.get_nowait()
            print 'Motor thread received: ' + cmd
            words = cmd.split()
            if (words[0] == "motor"):
               if (len(words) == 3):
                  self._motors.setSpeed(words[1], words[2])
               elif (len(words) == 2 and words[1] == "status"):
                  outstring = 'Left speed: ' + str(self._motors.getLeftSpeed())
                  outstring += '\n'
                  outstring += 'Left dir: ' + self._motors.getLeftDirection()
                  outstring += '\n'
                  outstring += 'Right speed: ' + str(self._motors.getRightSpeed())
                  outstring += '\n'
                  outstring += 'Right dir: ' + self._motors.getRightDirection()
                  outstring += '\n'
                  self._respQueue.put(outstring)
               else:
                  print 'Motor thread: Incorrect arguments for motor command'
            else:
               print 'Motor thread: Invalid command'
         # Done processing the command queue
         # Call the motor update routine
         self._motors.updateMotorState()
      print 'Motor thread exit'

   # Starts the thread
   def start(self):
      print 'Starting motor thread'
      self._running = True
      self._TheThread = threading.Thread(target = self._run)
      print 'Motor thread start!'
      self._TheThread.start()

   # Stops the thread
   def join(self):
      if (self._running == True):
         print 'Requesting motor thread stop'
         self._running = False
         self._TheThread.join()
      else:
         print 'Motor thread is not running...'

   # Puts an entry on the queue for processing
   def putCmd(self, cmd):
      self._cmdQueue.put(cmd)

   # Call to check that the motorThread is still running
   def isAlive(self):
      return self._running

