#!/usr/bin/python

from motor import Motor, MotorMaster

# Read speed from command line and then verify the input is an integer.
leftSpeed = raw_input('Input left motor speed: ')

try:
   leftSpeed = int(leftSpeed)
except ValueError:
   print "Speed must be an integer, forcing to 0"
   leftSpeed = 0
else:
   print 'User input is: ', leftSpeed

rightSpeed = raw_input('Input right motor speed: ')

try:
   rightSpeed = int(rightSpeed)
except ValueError:
   print "Speed must be an integer, forcing to 0"
   rightSpeed = 0
else:
   print 'User input is: ', rightSpeed

# Set the speed using the input values
master = MotorMaster()
print 'Left Previous speed: ', master.getLeftSpeed()
print 'Right Previous speed: ', master.getRightSpeed()
master.setSpeed(leftSpeed, rightSpeed)
print 'Left New speed: ', master.getLeftSpeed()
print 'Right New speed: ', master.getRightSpeed()

print 'Left Direction: ', master.getLeftDirection()
print 'Right Direction: ', master.getRightDirection()


