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
      self._driver.setTargetSpeed(self._speed)

   def setDirCw(self):
      self._direction = "CW"
      self._driver.setTargetDir(1)

   def setDirCcw(self):
      self._direction = "CCW"
      self._driver.setTargetDir(0)

   def getSpeed(self):
      return self._speed

   def getDirection(self):
      return self._direction


