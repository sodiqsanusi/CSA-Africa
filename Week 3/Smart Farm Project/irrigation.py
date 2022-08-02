# import required modules
from machine import ADC, Pin
import utime

# use variables instead of numbers:
soil = Pin(26, Pin.IN) # Soil moisture PIN reference
water_pump_relay = Pin(25, Pin.OUT) # Water pump relay PIN reference

# Switching on the relay connection that activates the water pump
def switch_water_on():
    water_pump_relay.on()
    utime.sleep(3)
    

#Calibraton values
min_moisture=0
max_moisture=65535

readDelay = 0.5 # delay between readings

while True:
    # read moisture value and convert to percentage into the calibration range
#     moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
#     # print values
#     print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    print(soil.value())
    if soil.value() == 0:
        switch_water_on()
    if soil.value() == 1 and water_pump_relay:
        water_pump_relay.off()
    utime.sleep(readDelay)
    # set a delay between readings