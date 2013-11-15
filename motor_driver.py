import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time

# This class contains low level code for driving PMOD HB5 pins
# using the BeagleBone Black
class MotorDriver:
   # Pin maps
   _pin_dir = 0
   _pin_en = 0
   _pin_sa = 0
   _pin_sb = 0
   _curSpeed = 0     # Current speed
   _curDir = 0       # Current direction
   _targetSpeed = 0  # Target speed
   _targetDir = 0    # Target direction

   # Sensor info
   _sensorA = 0
   _sensorB = 0

   def __init__(self, pin_dir, pin_en, pin_sa, pin_sb):
      print "Initializing motor driver"
      self._pin_dir = pin_dir
      self._pin_en = pin_en
      self._pin_sa = pin_sa
      self._pin_sb = pin_sb

      # First, turn off the enable pin
      #PWM.start(channel, duty, freq=200, polarity=0)
      PWM.start(self._pin_en, 0)

      # I'm concerned about the enable pin not being stable when we startup.
      # For the sake of safety give it a moment to stop.
      # TODO: Enable the feedback pins first and verify the motor
      # is stopped before setting the direction.
      time.sleep(0.5)

      # Now set the direction pin as an output and initialize it
      GPIO.setup(self._pin_dir, GPIO.OUT)
      GPIO.output(self._pin_dir, GPIO.LOW)

      # Set up feedback pins as inputs
      GPIO.setup(self._pin_sa, GPIO.IN)
      GPIO.setup(self._pin_sb, GPIO.IN)
      print "Motor driver init complete"

   # The motor MUST be stopped prior to calling this method.
   def _setDirection(self, direction):
      print "Motor driver direction set"
      # Set the direction!
      if (direction > 0):
         GPIO.output(self._pin_dir, GPIO.HIGH)
         self._curDir = 1
      else:
         GPIO.output(self._pin_dir, GPIO.LOW)
         self._curDir = 0

   # speed must be between 0 and 100 inclusive
   def _setSpeed(self, speed):
      assert speed <= 100
      assert speed >= 0
      print "Motor driver speed change"
      PWM.set_duty_cycle(self._pin_en, speed)
      self._curSpeed = speed

   def _isStopped(self):
      # TODO
      # Check the current speed.
      if (self._curSpeed == 0):
         # Is the hbridge sensor information reporting that the motor
         # is stopped?  
         # If both agree, then the motor is stopped.
         # TODO: Actually do this
         time.sleep(1)
         return True
      return False

   # Updates the target speed
   def setTargetSpeed(self, speed):
      self._targetSpeed = speed

   # Sets the target direction
   def setTargetDir(self, direction):
      self._targetDir = direction

   # Performs any pending speed or direction changes.
   # Reads motor feedback sensors.
   def updateState(self):
      # Update hbridge sensor feedback
      # TODO Update the sensor

      # See if we need to change direction
      if (self._curDir != self._targetDir):
         # Switching from forwards to backwards
         self._setSpeed(0)
         if (self.isStopped()):
            self._setDirection(self._targetDir)
      elif (self._curSpeed != self._targetSpeed):
         # No direction change, apply any speed changes
         self._setSpeed(self._targetSpeed)
      # else - Keep doing whatever we were doing
     

   def shutdown(self):
      GPIO.cleanup()
      PWM.stop(self._pin_en)
      PWM.cleanup()
      print "Motor driver shutdown complete"

