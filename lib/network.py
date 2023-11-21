import socket
import sys
from time import sleep
import random
from struct import pack

import network
import socket

# store network information on local computer
f = open("KEY", "r")

ssid = f.readline()
password = f.readline()

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

def createUDPSocket():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '10.0.0.226', 64000
    server_address = (host, port)

def testSocket(sock, server_address):
    # Send a few messages
    for i in range(10):

        # Pack three 32-bit floats into message and send
        message = "Hello"
        sock.sendto(message.encode(), server_address)

        sleep(1)
