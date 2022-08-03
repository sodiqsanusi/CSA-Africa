import machine, time
from machine import Pin


__version__ = '0.2.0'
__author__ = 'Roberto Sánchez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

class HCSR04:
    
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        pulse_time = self._send_pulse_and_wait()
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms


intruder_alarm_active = Pin(14, Pin.IN)
lights = Pin(26, Pin.IN)

ultrasonic = HCSR04(trigger_pin=22, echo_pin=23, echo_timeout_us=1000000)
led = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(machine.Pin(21, machine.Pin.OUT))
buzzer.freq(4186)
buzzer.duty(0)

intruder_distance = 7

while True:
    distance = ultrasonic.distance_cm()
    print(intruder_alarm_active.value())
#     print(lights.value())
    print('Distance:', distance, 'cm')
    if distance <= intruder_distance and intruder_alarm_active.value() == 1:
        buzzer.duty(512)
        led.on()
    elif distance <= intruder_distance and intruder_alarm_active.value() == 0:
        lights = True
        buzzer.duty(0)
        led.off()
    else:
        buzzer.duty(0)
        led.off()
    time.sleep_ms(1000)
feed()   