import numpy as np
import pandas as pd
import os
import math
from datetime import datetime

##def convert_data(data_str):
##    data_list = [x.strip() for x in data_str.split(',')]
##    data_converted = []
##    for ele in data_list:
##        data_converted.append(float(ele))
##    return (data_converted) # return a float list

def convert_data(data_str, variables):
    data_list = [x.strip() for x in data_str.split(',')]
    if (data_list[-1]==''):
        data_list = data_list[:-1]
    data_converted = []
    for ele in data_list:
        data_converted.append(float(ele))
        
    while True:
        if (len(data_converted)%variables == 0):
            result = data_converted[-variables:]
            break
        else :
            data_converted = data_converted[:-1]
        
    return result

def convert_data2(data_str, variables):
    data_list = [x.strip() for x in data_str.split(',')]
    if (data_list[-1]==''):
        data_list = data_list[:-1]
    data_converted = []
    for ele in data_list:
        data_converted.append(float(ele))
    
    while True:
        last = data_converted[-1]
        #print(last)
        if (last == int(last)):
            result = data_converted[-variables:]

            break
        else :
            data_converted = data_converted[:-1]
        
    return result

def record_data_csv(data_str, path):
    #data_list = convert_data(data_str)
    data_list = data_str
    temp_df = pd.DataFrame(np.array(data_list).reshape(-1,len(data_list)), columns = ['acLX_R','accY_L','accZ_L','acc_L','Force_L'])
    temp_df['time'] = datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")
    temp_df.to_csv(path+'recorded_dataset.csv', mode='a', index = False, header=False)
    return

def combine_record_data_csv(data_floatlist, data_str, path):
    #data_list = convert_data(data_str)
    data_list = data_str
    data_floatlist.extend(data_list)
    temp_df = pd.DataFrame(np.array(data_floatlist).reshape(-1,len(data_floatlist)), 
                           columns = ['accX_L','accY_L','accZ_L','acc_L','Force_L','accX_R','accY_R','accZ_R','acc_R','Force_R'])
    temp_df['time'] = datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")
    temp_df.to_csv(path+'recorded_dataset.csv', mode='a', index = False, header=False)
    return

def floatlist2string(mylist):    
    convert = ''
    for i in range(0,len(mylist)):
        ele = repr(mylist[i])
        convert += ele
        if (i != len(mylist)-1):
            convert +=', '
    return convert

def round_floatlist(mylist, dec):
    convert = []
    for ele in mylist:
        ele = round(ele, dec)
        convert.append(ele)
    return convert

def rss_floatlist(mylist):
    sum = 0
    for ele in mylist:
        sum += ele*ele
    return  round(math.sqrt(sum),3)