from Board import *
import time

import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin1 = 17 # pin 11 on the RP board
pin2 = 27
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

board = Board()
while (1):
##    print("%s: control:%d light:%d temp:%d custom:%d" % (time.asctime(),
##                                                         board.control(),
##                                                         board.light(),
##                                                         board.temperature(),
##                                                         board.custom()))
    value = board.custom()
    print("%s: force_sensor:%d" % (time.asctime(), value))
    
    if (value >= 3):
        board.output(200) # turn on LED on ADDA board
        #GPIO.output(pin, (GPIO.LOW if state == 0 else GPIO.HIGH))
        GPIO.output(pin1, (GPIO.HIGH))
    #else:
        #GPIO.output(pin2, (GPIO.HIGH))
    #sleep(0.05)
    sleep(0.01)
    GPIO.output(pin1, (GPIO.LOW))
    GPIO.output(pin2, (GPIO.LOW))