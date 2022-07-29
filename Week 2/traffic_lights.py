import time
from machine import Pin

def traffic_light_on_off(color, seconds):
    possibilities = {
        'red': 4,
        'amber': 16,
        'green': 17
    }
    Pin(possibilities[color], Pin.OUT).on()
    time.sleep(seconds)
    if color == 'red':
        traffic_light_on_off('amber', 1.5)
    Pin(possibilities[color], Pin.OUT).off()
    
times = 1
while times <= 10:
    traffic_light_on_off('red', 3)
    time.sleep_ms(500)
    traffic_light_on_off('green', 3)
    traffic_light_on_off('amber', 1.5)
    print(f'Traffic light is going thorough sequence {times}')
    times += 1