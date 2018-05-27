from Board import *
from lsm6ds33 import LSM6DS33
from bluetooth import *
from threading import Thread

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
board = Board()

# Initialise (accelerometer)
lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

# Initialise bluetooth socket
#addr = None
addr = "B8:27:EB:B6:17:14"

# search for the RaspPi service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("connected")
while True:
    #data = raw_input()
    #if len(data) == 0: break
    #sock.send(data)
    receive = sock.recv(3000).decode("utf-8")  #1024 in example #convert byte to string
    #print(type(receive))
    print("Receive command: [%s]" % receive)
    if (receive == "100"): # sensor data requested
        force = board.custom() # force sensor data
        float_list = data_function.round_floatlist(lsm6ds33.get_accelerometer_g_forces(),3) # accel data
        float_list.append(data_function.rss_floatlist(float_list))
        float_list.append(force)
        
        # convert float list to string
        data = data_function.floatlist2string(float_list)
        
        #accel_g_force_R = lsm6ds33.get_accelerometer_g_forces()
        #accelX_R = accel_g_force_R[0]
        #data = '%.5f' % accel_g_force_R[0]
        #print(data)
        
        # send data
        sock.send(data)
        
    elif (receive == "501"): # command to output signal
        board.output(200) # turn on LED on ADDA board
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

