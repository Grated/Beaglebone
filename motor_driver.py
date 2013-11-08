import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time


#   We will use the following GPIOs:
#   <Func>  <BB Website>   <pin>    <GPIO Num>  <Mapping>
#   M1 Dir: gpio_30        p9:11    30          gpio0[30]
#   M1 En:  PWM1A          p9:14    50          gpio1[18]
#   M1 SA:  gpio_48        p9:15    48          gpio1[16]
#   M1 SB:  gpio_4         p9:17    5           gpio0[4]

class MotorDriver:
   def __init__(self):
      print "Initializing motor driver"
      # First, turn off the enable pin
      #PWM.start(channel, duty, freq=200, polarity=0)
      PWM.stop("P9_14")

      # Now set the direction pin as an output and initialize it
      GPIO.setup("P9_11", GPIO.OUT)
      GPIO.output("P9_11", GPIO.LOW)

      # Set up feedback pins as inputs
      GPIO.setup("P9_15", GPIO.IN)
      GPIO.setup("P9_17", GPIO.IN)
      print "Motor driver init complete"

   def setDirection(self, left, right)
      # Don't allow a direction change if the motor is on
      print "Direction change not yet supported"

   def setSpeed(self, left, right)
      print "Motor driver speed change"
      PWM.set_frequency("P9_14", left)

   def shutdown(self):
      GPIO.cleanup()
      PWM.stop("P9_14")
      PWM.cleanup()
      print "Motor driver shutdown complete"

