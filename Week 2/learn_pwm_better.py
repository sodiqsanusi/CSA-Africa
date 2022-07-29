from machine import Pin, PWM
from time import sleep

frequency = 1000
led = PWM(Pin(4), frequency)
brightness = 0
for i in range(0, 1024, 3):
    if int(f'{((i / 1023) * 100):.0f}') > brightness:
        print(f'{((i / 1023)):.0%} Brightness')
    led.duty(i)
    sleep(0.05)
