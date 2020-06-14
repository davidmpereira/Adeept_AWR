'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
from time import sleep
import sys                  #import system package


class GPSmodule:
    
    def __init__(self):
        super().__init__()
          
    def getCoord(self):
        
        gpgga_info = "$GPGGA,"
        ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
        #GPGGA_buffer = 0
        #NMEA_buff = 0
        lat_in_degrees = 0
        long_in_degrees = 0
    
        bFlag = False
    
        try:
            while bFlag == False:
                #print("getting serial") 
                received_data = (str)(ser.readline())                   #read NMEA string received
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                if (GPGGA_data_available>0):
                    #print("got data")  
                    GPGGA_buffer = received_data.split("$GPGGA,",1)[1] #store data coming after "$GPGGA," string 
                    #print(GPGGA_buffer)
                    NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                    #print("get GPS info!")
                    result = getGPSInfo(NMEA_buff)
                    #print(result)
                    lat_in_degrees = result[0]
                    long_in_degrees = result[1]                                          #get time, latitude, longitude
 
                    #print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
                    #print("------------------------------------------------------------\n")
                    if float(lat_in_degrees) > 0 and float(long_in_degrees) > 0:
                        bFlag = True
                    else:
                        print("err:" + str(lat_in_degrees) + "," + str(long_in_degrees))
        except:
            bFlag = False
            lat_in_degrees = 0
            long_in_degrees = 0
            #print("Error on coord")
        
        result = str(lat_in_degrees)+","+str(long_in_degrees)
        return result
    
def getGPSInfo(nmea):
    #print("here")
    NMEA_buff1=nmea
    #lat_in_degrees
    #long_in_degrees

    nmea_time = []
    nmea_latitude = []
    mea_longitude = []
    nmea_time = NMEA_buff1[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff1[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff1[3]               #extract longitude from GPGGA string
    
    #print("NMEA Time: ", nmea_time,'\n')
    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    return lat_in_degrees,long_in_degrees 
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    #print("pos res=" + str(position))
    position = "%.4f" %(position)
    return position
