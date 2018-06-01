from Board import *
from lsm6ds33 import LSM6DS33
from threading import Thread

import socket
import data_function
import time
import os
import sys
import RPi.GPIO as GPIO

def turn_on(pin):
    GPIO.output(pin, (GPIO.HIGH))
    #print('on')
    time.sleep(0.05)
    
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

# Initialise socket
sock = socket.socket()
host = sys.argv[1]
#host = '192.168.1.238' #ip of host
port = 12345
sock.bind((host, port))

sock.listen(100)
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = sock.accept()
print("Accepted connection from ", client_info)

# show ready
board.output(150)
time.sleep(1)
board.output(200)
time.sleep(1)

# create folder to store data
timestr = time.strftime("%Y%m%d-%H%M%S")
path = '/home/pi/Desktop/Data/'+timestr+'/'
if not os.path.exists(path):
    os.makedirs(path)

try:
    while True:
        t1 = Thread(target=turn_on, args=(pin1,))
        
        force = board.custom() # force sensor data
        float_list = data_function.round_floatlist(lsm6ds33.get_accelerometer_g_forces(),3) # accel data
        float_list.append(data_function.rss_floatlist(float_list))
        float_list.append(force)
        print("Local L data:", float_list)
        client_sock.send("100,".encode("utf-8")) # request sensor data from client
        
        #time.sleep(0.01)
        
        recv_data = client_sock.recv(3000).decode("utf-8") #1024 in example
        print("received R data: [%s]" % recv_data)      
        #recv_data = data_function.convert_data(recv_data,5)
        recv_data = data_function.convert_data2(recv_data,5)
        #print("received R data:", recv_data) 
        
        
        # model prediction
        if (recv_data[-1] >= 3):
            board.output(200) # turn on LED on ADDA board

            #GPIO.output(pin1, (GPIO.HIGH)) # turn on buzzer
            #t1 = Thread(target=turn_on, args=(pin1,))
            if not t1.is_alive():
                t1.start()
        
        # output feedback signal
        if (float_list[-1]>=3):
            print('ask R output')
            client_sock.send("501,".encode("utf-8")) # ask client to turn on output
        
        
        # save data
        data_function.combine_record_data_csv(float_list, recv_data, path)
        
        #print(float_list[-1])
        
        #client_sock.send("prediction data")
        #if len(sensor_data) == 0: break
        
        #time.sleep(0.1)
        #time.sleep(0.01)
        
        #GPIO.output(pin1, (GPIO.LOW))
        
except IOError:
    pass

print("disconnected")

client_sock.close()
sock.close()
print("all done")

