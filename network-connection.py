import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("TinTina","tinanguyen")
print(wlan.isconnected())