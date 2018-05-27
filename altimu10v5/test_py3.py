from lsm6ds33 import LSM6DS33
from time import sleep
import data_function

lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

while True:
    accel_g_force_L = data_function.round_floatlist(lsm6ds33.get_accelerometer_g_forces(),3)
    accel_g_force_L.append(data_function.rss_float_list(accel_g_force_L))
    print("  ")
    print("Accel_g_force:", accel_g_force_L)
    print("Roll_Pitch:", lsm6ds33.get_accelerometer_angles())
    print("Accel_3_angles:", lsm6ds33.getAccelerometer3Angles())
    #print("Gyro_angular_vel:", lsm6ds33.get_gyro_angular_velocity())
    sleep(1)