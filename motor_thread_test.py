#!/usr/bin/python

import Queue
import time
from motor_thread import MotorThread

motorQueue = Queue.Queue()
motorControl = MotorThread(motorQueue)
motorControl.stop()
motorControl.start()
print 'Main is sleeping'
motorControl.putCmd("Entry 1")
time.sleep(1)
motorControl.putCmd("Entry 2")
time.sleep(1)
motorControl.putCmd("Entry 3")
time.sleep(1)
motorControl.putCmd("Entry 4")
time.sleep(1)
motorControl.putCmd("Entry 5")
time.sleep(2)
print 'Awake, stop motor controller'
motorControl.join()

