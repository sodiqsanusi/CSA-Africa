# import required modules
from machine import ADC, Pin
import utime

# use variables instead of numbers:
soil = ADC(Pin(36))
soil.atten(ADC.ATTN_11DB)
#soil = Pin(26, Pin.IN) # Soil moisture PIN reference
irrigate = Pin(25, Pin.OUT) # Water pump relay PIN reference


#Calibraton values
min_moisture=0
max_moisture=65535

readDelay = 0.5 # delay between readings

while True:
    read = soil.read()
    percentage = (read / 4095) * 100
    print(read, percentage)
    if percentage > 87:
        print('Water pump on')
        irrigate.on()
    else:
        irrigate.off()
        print('Water pump off')
    # read moisture value and convert to percentage into the calibration range
#     moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
#     # print values
#     print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
#     print(soil.value())
#     if soil.value() == 1:
#         water_pump_relay.on()
#         continue
#     water_pump_relay.off()
    utime.sleep(readDelay)
    # set a delay between readings

