import socket
import sys
from time import sleep
import random
from struct import pack

import network
import socket

ssid = 'TinTina'
password = 'tinanguyen'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

connect()

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = '192.168.59.115', 64000
server_address = (host, port)

try:
    sock.connect(server_address)
    print("Connected to TCP server")
except:
    print("Not connected")

# Send a few messages
for i in range(10):

    message = 'hello'
    sock.send(message.encode('ascii'))

    sleep(1)
