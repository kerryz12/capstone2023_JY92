import network
import socket
from time import sleep

class Network(object):
    def __init__(self):
        # store network information on local computer
        f = open("KEY", "r")

        self.ssid = f.readline()
        self.password = f.readline()
        self.host = '10.0.0.226'
        self.port = 64000

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
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

    def testSocket(self, server_address):
        # Send a few messages
        for i in range(10):

            # Pack three 32-bit floats into message and send
            message = "Hello"
            self.sock.sendto(message.encode(), server_address)

            sleep(1)
