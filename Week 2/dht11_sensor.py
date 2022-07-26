from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(16))

while True:
    print('Sensing...')
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
    except:
        print('There is something wrong, try again later!')
    else:
        print(f'Temperature is at {t}°C')
        print(f'The atmospheric humidity is at {h}%')
        sleep(10)
