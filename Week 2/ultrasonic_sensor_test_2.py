from machine import Pin
import utime

trigger = Pin(4, Pin.OUT)
echo = Pin(18, Pin.IN)

def ultra():
    trigger.off()
    utime.sleep_us(2)
    trigger.on()
    utime.sleep_us(10)
    trigger.off()
#     while echo.value() == 0:
#         continue
#     time_end = utime.ticks_us()
#     duration = time_end - time_start
#     distance = (duration * 0.034) / 2
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print(f"The distance from object is {distance} cm")
    
while True:
    ultra()
    utime.sleep(0.05)