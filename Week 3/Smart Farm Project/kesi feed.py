import time

import machine
from machine import Pin, PWM
en = Pin(25, Pin.OUT)
IN1 = Pin(32, Pin.OUT)
IN2 = Pin(33, Pin.OUT)
feed = Pin(26, Pin.IN)

#forward
IN1.on()
IN2.on()
en.on()
while True:
    print(feed.value())
    time.sleep(0.5)
# def feed_mill():
pwm2 = PWM(en, freq=100, duty=800)
