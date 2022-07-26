from machine import Pin, PWM
from time import sleep

frequency = 5000
led = PWM(Pin(17), frequency)

while True:
    for duty_cycle in range(0, 1024):
        print(duty_cycle)
        led.duty(duty_cycle)
        sleep(0.05)