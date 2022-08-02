from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(4))

print('Sensing...')
sleep(2)
try:
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
except:
    print('There is something wrong, try again later!')
else:
    print(f'Temperature is at {t}°C')
    print(f'The atmospheric humidity is at {h}%')
