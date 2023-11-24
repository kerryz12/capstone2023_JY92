import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("TinTina","tinanguyen")
print(wlan.isconnected())

import mip
mip.install("github:n-elia/MAX30102-MicroPython-driver")