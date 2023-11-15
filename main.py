from machine import SoftI2C, I2C, Pin
from utime import sleep
from lib.max30102 import MAX30102
from lib.circular_buffer import CircularBuffer
from lib.hr_algorithm import HeartBeat

import network
import socket

ssid = 'SHAW-6F99'
password = 'cause2233always'

# pin values
SDA_PIN = 8
SCL_PIN = 9

# how many samples to keep to take average of for SPO2 calculation
SPO2_AVERAGE_SAMPLES = 32
