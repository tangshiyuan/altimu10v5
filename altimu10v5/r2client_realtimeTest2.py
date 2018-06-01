#from Board import *
from lsm6ds33 import LSM6DS33
from threading import Thread

import socket
import data_function
import time
import RPi.GPIO as GPIO
import sys

def turn_on(pin):
    GPIO.output(pin, (GPIO.HIGH))
    #print('on')
    time.sleep(0.1)
    
    GPIO.output(pin, (GPIO.LOW))
    #print('off')
    
# Initialise GPIO components
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin1 = 17 # pin 11 on the RP board
#pin2 = 27
GPIO.setup(pin1, GPIO.OUT)
#GPIO.setup(pin2, GPIO.OUT)

# Initialise ADDA component (force sensor)
#board = Board()

# Initialise (accelerometer)
lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

# Initialise socket
#addr = None

sock = socket.socket()
host = sys.argv[1]
#host = '192.168.1.238'# ip of host
port = 12345               
sock.connect((host, port))

print("connected")
while True:
    #data = raw_input()
    #if len(data) == 0: break
    #sock.send(data)
    receive = sock.recv(3000).decode("utf-8")  #1024 in example #convert byte to string
    receive = data_function.convert_data(receive,1)
    #print(type(receive))
    print("Receive command:" ,receive)
    #if (receive == "100"): # sensor data requested
    
    #force = board.custom() # force sensor data
    float_list = data_function.round_floatlist(lsm6ds33.get_accelerometer_g_forces(),3) # accel data
    float_list.append(data_function.rss_floatlist(float_list))
    #float_list.append(force)
        
        # convert float list to string
    data = data_function.floatlist2string(float_list)+','
        
        #accel_g_force_R = lsm6ds33.get_accelerometer_g_forces()
        #accelX_R = accel_g_force_R[0]
        #data = '%.5f' % accel_g_force_R[0]
        #print(data)
        
        # send data
    sock.send(data.encode("utf-8"))
        
    if (int(receive[0])== 501): # command to output signal
        #board.output(200) # turn on LED on ADDA board
        #GPIO.output(pin1, (GPIO.HIGH)) # turn on buzzer
        t1 = Thread(target=turn_on, args=(pin1,))
        if not t1.is_alive():
            t1.start()
        
        
    else :
        pass

    
    #time.sleep(0.1)
    #time.sleep(0.01)
    
    #GPIO.output(pin1, (GPIO.LOW))
    
sock.close()

