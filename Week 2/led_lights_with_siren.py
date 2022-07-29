from machine import Pin, PWM
from time import sleep
import dht

red = Pin(16, Pin.OUT)
amber = Pin(17, Pin.OUT)
green = Pin(19, Pin.OUT)
sensor = dht.DHT11(Pin(4))
freq = 5000
buzzer = PWM(Pin(18), freq)

print('Sensing...')
buzzer.duty(0)
sleep(2)
try:
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
except:
    print('There is something wrong, try again later!')
else:
    print(f'{t}°C')
    if t < 26:
        green.on()
        amber.off()
        red.off()
        buzzer.duty(0)
    elif t < 29:
        green.off()
        amber.on()
        red.off()
        buzzer.duty(0)
    else:
        green.off()
        amber.off()
        red.on()
        for i in range(1024):
            print(i)
            buzzer.duty(i)
            sleep(0.05)
    buzzer.duty(0)
    sleep(2)
    green.off()
    red.off()
    amber.off()
        
        


