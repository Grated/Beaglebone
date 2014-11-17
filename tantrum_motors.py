from motor import Motor
from motor_driver import MotorDriver

#   We will use the following pins for the front motor:
#   <Func>  <BB Website>   <pin>    <GPIO Num>  <Mapping>
#   FM Dir: gpio_30        p9:11    30          gpio0[30]
#   FM En:  PWM1A          p9:14    50          gpio1[18]
#   [Unsupported] LM SA:  gpio_48        p9:15    48          gpio1[16]
#   [Unsupported] LM SB:  gpio0_5        p9:17    5           gpio0[5]

#   We will use the following pins for the rear motor:
#   <Func>  <BB Website>   <pin>    <GPIO Num>  <Mapping>
#   RM Dir: gpio1_28       p9:12    60          gpio1[28]
#   RM En:  PWM1B          p9:16    51          gpio1[19]
#   [Unsupported] RM SA:  gpio0_31       p9:13    31          gpio0[31]
#   [Unsupported] RM SB:  gpio0_4        p9:18    4           gpio0[4]

class TantrumMotors:
    """
    This class is designed to control the motors of a Tyco Tantrum
    RC car. The Tantrum has a front motor controlling direction and
    a rear motor for moving forwards and backwards.
    """

    _front = 0  # Motor
    _rear = 0  # Motor
    _frontDriver = MotorDriver("P9_11", "P9_14")
    _rearDriver = MotorDriver("P9_12", "P9_16")

    # <public>
    # Initialize motors to forward, stopped
    def __init__(self):
        self._front = Motor(self._frontDriver)
        self._rear = Motor(self._rearDriver)
        self._front.setDirCw()
        self._front.setSpeed(0)
        self._rear.setDirCcw()
        self._rear.setSpeed(0)

    # Set the speed for all motors, if a speed is negative then the
    # motor is put in reverse.
    def setSpeed(self, front, rear):
        front = int(front)
        rear = int(rear)

        self._front.setSpeed(front)
        if (front < 0):
            self._front.setDirCcw()
        else:
            self._front.setDirCw()

        self._rear.setSpeed(rear)
        if (rear < 0):
            self._rear.setDirCcw()
        else:
            self._rear.setDirCw()

    def getFrontSpeed(self):
        return self._front.getSpeed()

    def getRearSpeed(self):
        return self._rear.getSpeed()

    def getFrontDirection(self):
        return self._front.getDirection()

    def getRearDirection(self):
        return self._rear.getDirection()

    def updateMotorState(self):
        self._frontDriver.updateState()
        self._rearDriver.updateState()

    def __exit__(self, type, value, traceback):
        self._frontDriver.shutdown()
        self._rearDriver.shutdown()
