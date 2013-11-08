#!/usr/bin/python
from motor_driver import MotorDriver 

# The motor class is meant for a single motor.
# It provides accessors for setting the speed and direction of a motor.
class Motor:
   """ Controls a single motor """
   # <private>
   _speed = 0
   _direction = "CW"
   _driver = 0

   def __init__(self, driver):
      self._driver = driver

   # <public>
   # Sets the speed for a motor, limited to 0 through 100 inclusive.
   def setSpeed(self, speed):
      speed = abs(speed)
      if (speed > 100):
         self._speed = 100
      else:
         self._speed = speed
      self._driver.setSpeed(self._speed)

   def setDirCw(self):
      self._direction = "CW"

   def setDirCcw(self):
      self._direction = "CCW"

   def getSpeed(self):
      return self._speed

   def getDirection(self):
      return self._direction

class MotorMaster:
   """ Controls multiple motors """
   # <private>
   _left = 0
   _right = 0
   _leftDriver = MotorDriver()
   _rightDriver = 0 #MotorDriver()

   # <public>
   # Initialize motors to forward, stopped
   def __init__(self):
      self._left = Motor(self._leftDriver)
      self._right = Motor(self._rightDriver)
      self._left.setDirCw()
      self._left.setSpeed(0)
      self._right.setDirCcw()
      self._right.setSpeed(0)

   # Set the speed for all motors, if a speed is negative then the 
   # motor is put in reverse.
   def setSpeed(self, left, right):
      left = int(left)
      right = int(right)
      self._left.setSpeed(left)
      if (left < 0):
         self._left.setDirCcw()
      else:
         self._left.setDirCw()

      self._right.setSpeed(right)
      if (right < 0):
         self._right.setDirCw()
      else:
         self._right.setDirCcw()

   def getLeftSpeed(self):
      return self._left.getSpeed()
   def getRightSpeed(self):
      return self._right.getSpeed()

   def getLeftDirection(self):
      return self._left.getDirection()
   def getRightDirection(self):
      return self._right.getDirection()

   def __exit__(self, type, value, traceback):
      self._leftDriver.shutdown()
      #self._rightDriver.shutdown()
