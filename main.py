from machine import SoftI2C, I2C, Pin
from utime import sleep
from lib.max30102 import MAX30102
from lib.circular_buffer import CircularBuffer
from lib.hr_algorithm import *
from lib.spo2_algorithm import *
from lib.network import *

import network
import socket

# pin values
SDA_PIN = 8
SCL_PIN = 9

# how many samples to keep to take average of for SPO2 calculation
SPO2_AVERAGE_SAMPLES = 32

# Create I2C object
i2c = SoftI2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
i2c.scan()

# set up sensor
sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

# using heartbeat library to calculate DC of signals
ir_ac = HeartBeat()
red_ac = HeartBeat()

spo2_obj = SPO2()
heartbeat_obj = DetectHeartbeat()
network_obj = Network()

network_obj.connect()
network_obj.createTCPSocket()

# main loop
while(True):
    # check for new readings
    sensor.check()

    if (sensor.available()):
        red = sensor.pop_red_from_storage()
        ir = sensor.pop_ir_from_storage()

        # get the DC value of each LED reading
        red_dc = red_ac.averageDCEstimator(red_ac.ir_avg_reg, red)
        ir_dc = ir_ac.averageDCEstimator(ir_ac.ir_avg_reg, ir)

        heartbeat_obj.detectHeartbeat(ir)
        average_heartbeat = heartbeat_obj.getBeatAverage()

        spo2 = spo2_obj.calculateSPO2(red, red_dc, ir, ir_dc)
        average_spo2 = spo2_obj.calculateAverageSPO2(spo2)
