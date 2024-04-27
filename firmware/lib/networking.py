import network
import socket
from time import sleep
from machine import Pin, Timer


class Networking(object):
    def __init__(self):
        self.ssid = ''
        self.password = ''
        self.led = Pin("LED", Pin.OUT)

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while self.wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        print(self.wlan.ifconfig())
        self.led.toggle()
        sleep(1)
        self.led.toggle()

    def createUDPSocket(self):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def createTCPSocket(self, server_address):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect(server_address)
            self.led.toggle()
            self.led.toggle()
            self.led.toggle()
            print("Connected to TCP server")
        except:
            print("Not connected")

    def sendTCPPacket(self, data):
        self.sock.send(data.encode('ascii'))
        
        

