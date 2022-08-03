from hcsr04 import HCSR04
from time import sleep_ms

from machine import Pin, PWM

sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

Door_1 = PWM(Pin(15), 50)
LED = Pin(2, Pin.OUT)

while True:
    distance = sensor.distance_cm()
    print('current Distance is:', distance, 'cm')
    sleep_ms(100)
    
    if 0 < distance < 10:
        LED.value(1)
        Door_1.duty(120)
    else:
        sleep_ms(1000)
        Door_1.duty(20)
        LED.value(0)