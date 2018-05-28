import socket               

s = socket.socket()        
host = '192.168.1.108'# ip of raspberry pi 
port = 12345               
s.connect((host, port))


print(s.recv(1024))
s.close()