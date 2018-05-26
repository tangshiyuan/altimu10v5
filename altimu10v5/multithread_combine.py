from Board import *
from lsm6ds33 import LSM6DS33
from threading import Thread
import time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin1 = 17 # pin 11 on the RP board
#pin2 = 27
GPIO.setup(pin1, GPIO.OUT)
#GPIO.setup(pin2, GPIO.OUT)


def turn_on(pin):
    GPIO.output(pin, (GPIO.HIGH))
    print('on')
    time.sleep(0.1)
    
    GPIO.output(pin, (GPIO.LOW))
    print('off')
    #time.sleep(0.01)

board = Board()

lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

while (1):
##    print("%s: control:%d light:%d temp:%d custom:%d" % (time.asctime(),
##                                                         board.control(),
##                                                         board.light(),
##                                                         board.temperature(),
##                                                         board.custom()))
    value = board.custom()
    accel_g_force_L = lsm6ds33.get_accelerometer_g_forces()
    
    print("%s: force_sensor:%d" % (time.asctime(), value))
    #print(type(value))
    print("Accel_g_force:" , accel_g_force_L)
    #print(type(accel_g_force_L))
    float_list = accel_g_force_L
    float_list.append(value)
    print(float_list)
    #print("Roll_Pitch:", lsm6ds33.get_accelerometer_angles())
    #print("Accel_3_angles:", lsm6ds33.getAccelerometer3Angles())
    
    if (value >= 3):
        board.output(200) # turn on LED on ADDA board
        #GPIO.output(pin, (GPIO.LOW if state == 0 else GPIO.HIGH))
        #t1.start()
        #turn_on(pin1)
        t1 = Thread(target=turn_on, args=(pin1,))
        if not t1.is_alive():
          t1.start()
        
        #GPIO.output(pin1, (GPIO.HIGH))
    #else:
        #GPIO.output(pin2, (GPIO.HIGH))
    #sleep(0.05)
    #sleep(0.01)
    
    #GPIO.output(pin1, (GPIO.LOW))
    #GPIO.output(pin2, (GPIO.LOW))
