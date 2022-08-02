# Complete project details at https://RandomNerdTutorials.com
from machine import Pin, I2C
from time import sleep
from bme280 import BME280

# ESP32 - Pin assignment
sda = machine.Pin(21)
scl = machine.Pin(22)
i2c = I2C(0,sda=sda, scl=scl, freq=400000)
# ESP8266 - Pin assignment
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

while True:
  bme = BME280.BME280(i2c=i2c)
  temp = bme.temperature
#  hum = bme.humidity
  pres = bme.pressure
#   # uncomment for temperature in Fahrenheit
#   #temp = (bme.read_temperature()/100) * (9/5) + 32
#   #temp = str(round(temp, 2)) + 'F'
  print('Temperature: ', temp)
#  print('Humidity: ', hum)
  print('Pressure: ', pres)

  sleep(2)