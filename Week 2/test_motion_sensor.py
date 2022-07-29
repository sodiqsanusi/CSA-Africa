from machine import Pin
from time import sleep

sensor = Pin(13, Pin.IN)
led = Pin(14, Pin.OUT)

led.off()
def detect_motion():
    if sensor.value() == 1:
        led.on()
        sleep(2)
    else:
        led.off()
        sleep(0.05)
while True:
    detect_motion()