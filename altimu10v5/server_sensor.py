# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from lsm6ds33 import LSM6DS33
from bluetooth import *

lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

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

try:
    while True:
        accel_g_force_L = lsm6ds33.get_accelerometer_g_forces()
        print("Local L data:", accel_g_force_L)
        client_sock.send("100") # request sensor data
        sensor_data = client_sock.recv(3000) #1024 in example
        print("received R data: [%s]" % sensor_data)      
      
        client_sock.send("prediction data") # output feedback signal
        #if len(sensor_data) == 0: break
        print("received [%s]" % sensor_data)
        #print(type(data))
        
        time.sleep(0.1)
        
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
