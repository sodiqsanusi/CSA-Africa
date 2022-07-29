from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(4))

print('Sensing...')
led = Pin(2, Pin.OUT)
led.on()
sleep(2)
try:
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
except:
    print('There is something wrong, try again later!')
else:
    led.off()
    print(f'Temperature is at {t}°C')
    print(f'The atmospheric humidity is at {h}%')
