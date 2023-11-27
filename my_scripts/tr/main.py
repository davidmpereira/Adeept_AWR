import network, neopixel, time, machine
from machine import Pin
from umqttsimple import MQTTClient
import ubinascii
import micropython
import esp
import gc
import os
esp.osdebug(None)

#define the Neo Pixel Pin and LED number
np = neopixel.NeoPixel(Pin(13), 96)

#SET the MQTT Svariables
mqtt_server = '192.168.0.60'
client_id = ubinascii.hexlify('coolLED')

#define topics to subscribe to
topic_sub = b'/home/ESP32WRMP01/sled'
#topic_sub2 = b'/home/ESP32WRMP01/sledrgb'
#topic_sub3 = b'/home/ESP32WRMP01/sledbright'

#define publish topics
topic_pub = b'/home/ESP32WRMP01/sled/stat'
#topic_pub2 = b'/home/ESP32WRMP01/rgb/stat'
#topic_pub3 = b'/home/ESP32WRMP01/bright/stat'

last_message = 0
counter = 0

#define init settings
status = 'on'
statRed = 255
statGreen = 255
statBlue = 255
statBright = 25

def wifi_connect():

    wlan = network.WLAN(network.STA_IF)
    
    wlan.active(True)
    
    if not wlan.isconnected():
        
        print('connecting to network...')
        
        wlan.connect('PearTreeTop24', '$P0rquinhos7BacoN?')
        
        while not wlan.isconnected():
            
            pass
        
    print('network config:', wlan.ifconfig())

def connect_and_subscribe():
    
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server,user=b'mdevqtt', password=b'hem9CZgKb9[&=7Tf12',keepalive=30)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
    
  return client

# routine to process received message
def sub_cb(topic, msg):
  global status, statRed, statGreen, statBlue, statBright
  print((topic, msg))
  
     
  if topic == b'/home/ESP32WRMP01/sled':
      
      if str(msg).count(',') == 2:
          
          #Parse the message from MTQQ server e.g: b'on,3,255-145-255 or b'on,,255-145-255 or b'on,3,--
          print('ESP received ' + str(msg))
          result = str(msg)
          result = result.replace("'",'')
          result = str(result.replace('b',''))
          result = result.split(',')
          
          if len(result) == 3:
              status = result[0]

              if result[1] != '':
                  statBright = result[1]
                  
              colour = result[2]
              
              if colour.count('-') == 2:
                  colour = colour.split('-')
                  
                  if len(colour) == 3:

                      if colour[0] != '':
                          statRed = int(colour[0])
                          
                      if colour[1] != '':
                          statGreen = int(colour[1])
                          
                      if colour[2] != '':
                          statBlue = int(colour[2])

              if status == 'on':
                       
                  int_val = int(statBright)
                  #print(int_val)
        
                  n = int((int_val*96)/255)
   
                  for i in range(n):
                      np[i] = (statRed, statGreen , statBlue)
                      np.write()
                  time.sleep_ms(10)

                  for i in range(n,96):
                     np[i] = (0, 0, 0)
                     np.write()
                  time.sleep_ms(50)
                        
          #Parse and acknlowdge message with latest settings
          msg = status + ',' + str(statBright) + ',' + str(statRed) + ',' + str(statGreen) + ',' + str(statBlue)
          #print(msg)
          client.publish(topic_pub,msg.encode())
    
      elif msg == b'off':
          
        print('ESP received ' + str(msg))
        soft_off(np)
        client.publish(topic_pub,b'off')
             
      elif msg == b'FADE':
          
        print('ESP received ' + str(msg))
        client.publish(topic_pub,b'ON')
        fade_in(np)
    
      elif msg == b'BONJOUR':
          
        print('ESP received ' + str(msg))
        client.publish(topic_pub,b'ON')
        bonjour(np)
         
      else:
          
         print('ESP unknown ' + str(msg))

def init_on():
    global statRed, statGreen, statBlue, statBright

    for i in range(1,96,5):
        np[i] = (statRed, statGreen, statBlue)
        np.write()
        time.sleep_ms(50)
            
        msg = status + ',' + str(statBright) + ',' + str(statRed) + ',' + str(statGreen) + ',' + str(statBlue)
        #print(msg)
        client.publish(topic_pub,msg.encode())    

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  machine.reset()
  
def soft_reconnect():

      client = connect_and_subscribe()

def soft_on(np):
    global statRed, statGreen, statBlue, statBright
    n = np.n
    
    if statRed == 0:
        statRed = 255
    if statGreen == 0:
        statGreen == 255    
    if statBlue == 0:
        statBlue = 255
        
    for i in range(statBright):
        np[i] = (statRed, statGreen, statBlue)
        np.write()
        time.sleep_ms(100)

def soft_off(np):

    n = np.n
    
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()
        time.sleep_ms(100)
        
def quick_off(np):

    n = np.n
    
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()

def fade_in(np):
    # fade in/out
    n = np.n
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (255, val, 0)
            np.write()

def bonjour(np):
    # Wake up routine
    n = np.n
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (255, val, 0)
            np.write()

def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

''' START OF MAIN PROGRAM '''

wlan = network.WLAN(network.STA_IF)
#wlan.config(reconnects = 5)
#wlan.config(pm=WLAN.PM_PERFORMANCE)
wlan.active(True)

#initiate connection to wifi
wifi_connect()

#initiate mqtt connection
try:
  client = connect_and_subscribe()

except OSError as e:
  restart_and_reconnect()

#initiate LED
init_on()

#demo(np)
start_time = time.ticks_ms()

while True:
     
  try:
      
    if not wlan.isconnected():
        
        print("Soft reconnect!")
        soft_reconnect()
    
    else:
        
        client.check_msg()
      
        if time.ticks_diff(time.ticks_us(), start_time) > 1000:

            msg = status + ',' + str(statBright) + ',' + str(statRed) + ',' + str(statGreen) + ',' + str(statBlue)
            
            #print(msg)
            
            client.publish(topic_pub,msg.encode()) 
            
            start_time = time.ticks_ms()   
 
    time.sleep_ms(50)
    
  except OSError as e:
  
      print("Restart and reconnect!")            
      soft_reconnect()
      
  gc.collect()
    