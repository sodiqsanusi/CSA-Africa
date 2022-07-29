from machine import Pin, ADC, PWM
from time import sleep

#led = PWM(Pin(17), 5000)
pot = ADC(Pin(36))
pot.atten(ADC.ATTN_11DB)

while True:
    pot_value = pot.read()
    pot_value = int(pot_value // 4.005)
    print(pot_value)
    #led.duty(pot_value)
    sleep(0.05)