import data_function
import time
import os


timestr = time.strftime("%Y%m%d-%H%M%S")
path = timestr+'/'
if not os.path.exists(path):
    os.makedirs(path)

i = 0
while 1:
    data_str = "23, 56, 89" # simulated data string stream # should be receive remote sensor data
    data_function.record_data_csv(data_str, path)
    print('recorded data')
    i +=1
    time.sleep(0.2)
    if i==10:
        break