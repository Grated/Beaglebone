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

#   We will use the following pins for the left motor:
#   <Func>  <BB Website>   <pin>    <GPIO Num>  <Mapping>
#   LM Dir: gpio_30        p9:11    30          gpio0[30]
#   LM En:  PWM1A          p9:14    50          gpio1[18]
#   LM SA:  gpio_48        p9:15    48          gpio1[16]
#   LM SB:  gpio0_5        p9:17    5           gpio0[5]

#   We will use the following pins for the right motor:
#   <Func>  <BB Website>   <pin>    <GPIO Num>  <Mapping>
#   RM Dir: gpio1_28       p9:12    60          gpio1[28]
#   RM En:  PWM1B          p9:16    51          gpio1[19]
#   RM SA:  gpio0_31       p9:13    31          gpio0[31]
#   RM SB:  gpio0_4        p9:18    4           gpio0[4]

class MotorMaster:
   """ Controls multiple motors """
   # <private>
   _left = 0
   _right = 0
   _leftDriver = MotorDriver("P9_11", "P9_14", "P9_15", "P9_17")
   _rightDriver = MotorDriver("P9_12", "P9_16", "P9_13", "P9_18")

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

   def updateMotorState(self):
      self._leftDriver.updateState()
      self._rightDriver.updateState()

   def __exit__(self, type, value, traceback):
      self._leftDriver.shutdown()
      self._rightDriver.shutdown()

