from machine import Pin, PWM
from time import sleep

frequency = 5000
led = PWM(Pin(17), frequency)

for duty_cycle in range(1024):
    print(duty_cycle)
    led.duty(duty_cycle)
    sleep(0.05)
led.duty(1)
