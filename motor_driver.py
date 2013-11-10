import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time


class MotorDriver:
   _pin_dir = 0
   _pin_en = 0
   _pin_sa = 0
   _pin_sb = 0

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

   def setDirection(self, direction):
      # Don't allow a direction change if the motor is on
      print "Direction change not yet supported"

   def setSpeed(self, speed):
      print "Motor driver speed change"
      PWM.set_duty_cycle(self._pin_en, speed)

   def shutdown(self):
      GPIO.cleanup()
      PWM.stop(self._pin_en)
      PWM.cleanup()
      print "Motor driver shutdown complete"

