from machine import SoftI2C, I2C, Pin
from utime import sleep
from lib.max30102 import MAX30102
from lib.circular_buffer import CircularBuffer
from lib.hr_algorithm import HeartBeat

# how many samples to keep to take average of for SPO2 calculation
SPO2_AVERAGE_SAMPLES = 32

class SPO2(object):
    def __init__(self):
        # SpO2 Algorithm Values
        self.a = 1.5958422
        self.b = -34.6596622
        self.c = 33.1098759

        # initialize SpO2 variables
        self.spo2 = 1
        self.average_spo2 = 0
        self.average_spo2_buffer = []

    def calculateSPO2(self, red, red_dc, ir, ir_dc):
        # calculate the SpO2 level
        ratio = (red/red_dc) / (ir/ir_dc)
        return self.a*self.a*ratio + self.b*ratio + self.c
    
    def calculateAverageSPO2(self, spo2):
        # if list containing values for average calculation is full
        if (len(self.average_spo2_buffer) == SPO2_AVERAGE_SAMPLES):

            # rotate the list
            for i in range(SPO2_AVERAGE_SAMPLES-1):
                self.average_spo2_buffer[i] = self.average_spo2_buffer[i+1]

            self.average_spo2_buffer[SPO2_AVERAGE_SAMPLES-1] = self.spo2

            # calculate the average SpO2 value
            for i in range(SPO2_AVERAGE_SAMPLES):
                self.average_spo2 += self.average_spo2_buffer[i]

            average_spo2 = self.average_spo2 / SPO2_AVERAGE_SAMPLES

            print(average_spo2)
            average_spo2 = 0

        # otherwise append the samples to the list until the list is full
        else:
            self.average_spo2_buffer.append(self.spo2)

            for i in range(len(self.average_spo2_buffer)):
                self.average_spo2 += self.average_spo2_buffer[i]

            average_spo2 = self.average_spo2 / SPO2_AVERAGE_SAMPLES

            print(average_spo2)
            average_spo2 = 0