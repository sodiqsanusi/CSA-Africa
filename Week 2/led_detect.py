from machine import Pin, ADC
from time import sleep

buzz = Pin(16, Pin.OUT)
led_detector = ADC(Pin(4))
led_detector.atten(ADC.ATTN_11DB)

while True:
    how_much_light = led_detector.read()
    how_much_light = int(how_much_light // 4.003)
    percentage_of_light = (how_much_light / 1022) * 100
    if percentage_of_light < 95:
        buzz.on()
    else:
        buzz.off()
    print(percentage_of_light)
    sleep(0.1)