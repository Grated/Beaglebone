import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time


class MotorDriver:
    """
    This class contains low level code for driving PMOD HB5 pins using
    the BeagleBone Black.

    Motor feedback is not supported (Pins SA and SB of PMOD HB5).
    """
    # Pin maps
    _pin_dir = 0
    _pin_en = 0
    _curSpeed = 0      # Current speed
    _curDir = 0         # Current direction
    _targetSpeed = 0  # Target speed
    _targetDir = 0     # Target direction

    # Sensor info
    _sensorA = 0
    _sensorB = 0

    def __init__(self, pin_dir, pin_en):
        print "Initializing motor driver"
        self._pin_dir = pin_dir
        self._pin_en = pin_en

        # First, turn off the enable pin
        #PWM.start(channel, duty, freq=200, polarity=0)
        PWM.start(self._pin_en, 0)

        # I'm concerned about the enable pin not being stable when we startup.
        # For the sake of safety give it a moment to stop.
        time.sleep(0.5)

        # Now set the direction pin as an output and initialize it
        GPIO.setup(self._pin_dir, GPIO.OUT)
        GPIO.output(self._pin_dir, GPIO.LOW)

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
        # Slew to the speed so reduce the sudden power draw
        # from motors, this helps in situations where the device
        # shares the same power source as the motors.

        # We don't need to slew when slowing down.
        if speed > self._curSpeed:
            # Speeding up!
            if (speed - self._curSpeed) > 10:
                # I just picked 10 because it's nice and round
                speed = self._curSpeed + 10

        PWM.set_duty_cycle(self._pin_en, speed)
        self._curSpeed = speed

    def _is_stopped(self):
        """
        Verifies the motor is stopped.

        In the future, this method will use the motor feedback to guarantee
        the motor is stopped. For now, sleeps for a second to allow the
        motor to come to a full stop before.

        :return: True if stopped, False otherwise.
        """
        if self._curSpeed == 0:
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
        # See if we need to change direction
        if self._curDir != self._targetDir:
            # Switching from forwards to backwards
            self._setSpeed(0)
            if self._is_stopped():
                self._setDirection(self._targetDir)

        elif self._curSpeed != self._targetSpeed:
            # No direction change, apply any speed changes
            self._setSpeed(self._targetSpeed)

        # else - Keep doing whatever we were doing

    def shutdown(self):
        GPIO.cleanup()
        PWM.stop(self._pin_en)
        PWM.cleanup()
        print "Motor driver shutdown complete"

