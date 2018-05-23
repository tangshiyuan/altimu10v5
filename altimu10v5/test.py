from lsm6ds33 import LSM6DS33
from time import sleep

lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

while True:
    print("  ")
    print("Accel_g_force:", lsm6ds33.get_accelerometer_g_forces())
    print("Roll_Pitch:", lsm6ds33.get_accelerometer_angles())
    print("Accel_3_angles:", lsm6ds33.getAccelerometer3Angles())
    #print("Gyro_angular_vel:", lsm6ds33.get_gyro_angular_velocity())
    sleep(1)