import machine
import time
door = machine.Pin(27, machine.Pin.IN)
p23 = machine.Pin(12)
pwm = machine.PWM(p23)
pwm.freq(50)
pwm.duty(0)
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))

def open_door():
    for i in range(170, 30, -10):
        servo(pwm, i)
        time.sleep(0.5)
    time.sleep(2)
def close_door():
    for i in range(30, 170, 10):
        servo(pwm, i)
        time.sleep(0.5)
    time.sleep(2)

is_open = False
opened = 0
closed = 0

while True:
    if door.value() == 1 and opened == 0:
        opened += 1
        open_door()
        is_open = True
    elif door.value() == 0 and closed == 0 and is_open:
        closed += 1
        close_door()
        is_open = False
    if opened == 1 and closed == 1:
        opened = 0
        closed = 0