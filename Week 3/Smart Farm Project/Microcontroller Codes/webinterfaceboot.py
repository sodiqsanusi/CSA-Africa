try:
  import usocket as socket
except:
  import socket
  
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

station = network.WLAN(network.STA_IF)

network_name = 'NITDA-ICT-HUB'
network_password = '6666.2524#'

station.active(True)
station.connect(network_name, network_password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())