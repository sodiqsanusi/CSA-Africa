from machine import Pin, PWM, ADC
from time import sleep

analog_device = ADC(Pin(36))
analog_device.atten(ADC.ATTN_11DB)
led = PWM(Pin(17), 5000)

collected_signals = []

led.duty(0)
for i in range(50):
    ADC_value = analog_device.read()
    collected_signals.append(int(ADC_value // 4.005))
    sleep(0.2)
print('Done with reading the analog signals')
sleep(1)

for signal in collected_signals:
    led.duty(signal)
    sleep(0.05)
print('Used the collected analog signals in the Pulse-Width-Modulation effect completed just now.')
    