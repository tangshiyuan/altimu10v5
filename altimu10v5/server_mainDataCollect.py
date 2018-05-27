from Board import *
from lsm6ds33 import LSM6DS33
from bluetooth import *
from threading import Thread

import data_function
import time
import os
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

# Initialise bluetooth socket
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "Rasp Pi3 Master",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

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
        client_sock.send("100") # request sensor data from client
        
        #time.sleep(0.01)
        
        recv_data = client_sock.recv(100).decode("utf-8") #1024 in example
        print("received R data: [%s]" % recv_data)      
        recv_data = data_function.convert_data(recv_data)
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
            client_sock.send("501") # ask client to turn on output
        
        
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
server_sock.close()
print("all done")

