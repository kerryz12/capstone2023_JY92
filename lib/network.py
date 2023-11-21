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

class Network(object):
    def __init__(self):
        self.host = '10.0.0.226'
        self.port = 64000

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        while self.wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        print(self.wlan.ifconfig())

    def createUDPSocket(self):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def createTCPSocket(self):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def testSocket(self, sock, server_address):
        # Send a few messages
        for i in range(10):

            # Pack three 32-bit floats into message and send
            message = "Hello"
            sock.sendto(message.encode(), server_address)

            sleep(1)
