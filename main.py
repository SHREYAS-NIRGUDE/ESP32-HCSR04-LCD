print("Hello, ESP32!")
#importing require modules
import machine
from machine import Pin, I2C 
import time
import utime
import ssd1306
import network
from umqtt.simple import MQTTClient
#Connecting to Wifi
print("Connecting to Wifi.")
server_url = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client",server_url)
write_api_key = "LFSU6YOUXR17SKVH"
Topic ="channels/1663826/publish/" + write_api_key

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST","")
while not wifi.isconnected():
  utime.sleep(0.5)
  print(".",end="")
print(wifi.ifconfig())
#Measuring distance using HCSR04 Ultrsonic sensor
while True:
  trigger = machine.Pin(14,machine.Pin.OUT)
  echo = machine.Pin(27, machine.Pin.IN)
  trigger.value(0)
  utime.sleep_us(2)
  trigger.value(1)
  utime.sleep_us(5)
  trigger.value(0)
  while echo.value() == 0: 
    signaloff = utime.ticks_us()
  while echo.value() ==1: 
    signalon = utime.ticks_us()
  timepassed = signalon-signaloff
  distance = int((timepassed * 0.0330)/2)
  print("The object can be seen from a distance of",distance, "cm")
 
  # ESP32 Pin assignment 
  i2c = I2C(0, scl=Pin(22), sda=Pin(21))

  oled_width = 128
  oled_height = 64
  oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
  oled.text("Distance:",10,10) 
  oled.text(str(distance),90,10)
  oled.show()  
  
  #Sending data to think speak every second
  payload="field1="+ str(distance)
  client.connect()
  client.publish(Topic,payload)
  client.disconnect()
  #Blinking LED at 500ms rate
  pin2=machine.Pin(2, machine.Pin.OUT)
  pin2.value(1)
  time.sleep_ms(500)
  pin2.value(0)

  