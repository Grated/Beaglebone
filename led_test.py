import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time

print "Starting test"

PWM.start("P9_14", 0)
PWM.start("P9_16", 100)
GPIO.setup("P9_11", GPIO.OUT)
GPIO.output("P9_11", GPIO.LOW)
GPIO.setup("P9_15", GPIO.OUT)
GPIO.output("P9_15", GPIO.LOW)
GPIO.setup("P9_17", GPIO.OUT)
GPIO.output("P9_17", GPIO.LOW)
GPIO.setup("P9_12", GPIO.OUT)
GPIO.output("P9_12", GPIO.LOW)
GPIO.setup("P9_13", GPIO.OUT)
GPIO.output("P9_13", GPIO.LOW)
GPIO.setup("P9_18", GPIO.OUT)
GPIO.output("P9_18", GPIO.LOW)
time.sleep(1)

PWM.set_duty_cycle("P9_14", 10)
PWM.set_duty_cycle("P9_16", 90)
time.sleep(1)

PWM.set_duty_cycle("P9_14", 40)
PWM.set_duty_cycle("P9_16", 60)
time.sleep(1)

PWM.set_duty_cycle("P9_14", 80)
PWM.set_duty_cycle("P9_16", 20)
time.sleep(1)

PWM.set_duty_cycle("P9_14", 100)
PWM.set_duty_cycle("P9_16", 10)
time.sleep(1)

PWM.stop("P9_14")
PWM.stop("P9_16")
GPIO.cleanup()
PWM.cleanup()

print "Test complete"

