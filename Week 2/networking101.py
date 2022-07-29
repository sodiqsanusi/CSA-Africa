import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
print(wlan.scan())           # scan for access points
print(wlan.isconnected())      # check if the station is connected to an AP
# wlan.connect('NITDA-ICT-HUB', '6666.2524#') # connect to an AP
# wlan.config('mac')     # get the interface's MAC address
# print(wlan.isconnected())      # 
print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses
