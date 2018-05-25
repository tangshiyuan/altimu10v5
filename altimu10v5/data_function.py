import numpy as np
import pandas as pd
import os
from datetime import datetime

def convert_data(data_str):
    data_list = [x.strip() for x in data_str.split(',')]
    data_converted = []
    for ele in data_list:
        data_converted.append(float(ele))
    return (data_converted) # return a float list

def record_data_csv(data_str, path):
    data_list = convert_data(data_str)
    temp_df = pd.DataFrame(np.array(data_list).reshape(-1,len(data_list)), columns = ['accX_R','accY_R','accZ_R'])
    temp_df['time'] = datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")
    temp_df.to_csv(path+'recorded_dataset.csv', mode='a', index = False, header=False)
    #df = df.append(temp_df, ignore_index=True)
    #return df
    return

def floatlist2string(mylist):    
    convert = ''
    for i in range(0,len(mylist)):
        ele = repr(mylist[i])
        convert += ele
        if (i != len(mylist)-1):
            convert +=', '
    return convert