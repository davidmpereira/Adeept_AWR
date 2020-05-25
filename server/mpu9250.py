from time import sleep
from math import pi, atan, atan2
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import sys                  #import system package

class Gyro:
    
    def __init__(self):
        super().__init__()
        
    
    def getOrientation(self):
        mpu = MPU9250(
        address_ak=AK8963_ADDRESS, 
        address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
        address_mpu_slave=None, 
        bus=1, 
        gfs=GFS_1000, 
        afs=AFS_8G, 
        mfs=AK8963_BIT_16, 
        mode=AK8963_MODE_C100HZ)
    
        mpu.configure() # Apply the settings to the registers.
    
        result = mpu.readMagnetometerMaster()
    
        degree=round(90-atan2(result[1],result[0])*180/pi,1)
        
        return(str(degree))

#mpu = MPU9250(
   # address_ak=AK8963_ADDRESS, 
  #  address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
   # address_mpu_slave=None, 
   # bus=1, 
   # gfs=GFS_1000, 
   # afs=AFS_8G, 
   # mfs=AK8963_BIT_16, 
    #mode=AK8963_MODE_C100HZ)

#mpu.configure() # Apply the settings to the registers.

#print("|.....MPU9250 in 0x68 Address.....|")
#print("Accelerometer", mpu.readAccelerometerMaster())
#print("Gyroscope", mpu.readGyroscopeMaster())
#print("Magnetometer", mpu.readMagnetometerMaster())
#print("Temperature", mpu.readTemperatureMaster())
#result = mpu.readMagnetometerMaster()
        
#degree=90-atan2(result[1],result[0])*180/pi
#print(str(degree))
#print("\n")

