from machine import SoftI2C, I2C, Pin
from utime import sleep
from lib.max30102 import *
from lib.hr_algorithm import HeartBeat

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

ir_ac = HeartBeat()
red_ac = HeartBeat()

# SPO2 Algorithm Values
ratio = 1
a = 1
b = 1
c = 1
spo2 = 1
average_spo2 = 1
average_spo2_buffer = CircularBuffer(SPO2_AVERAGE_SAMPLES)

while(True):
    sensor.check()

    if (sensor.available()):
        red = sensor.pop_red_from_storage()
        ir = sensor.pop_ir_from_storage()

        red_dc = red_ac.averageDCEstimator(red_ac.ir_avg_reg, red)
        ir_dc = ir_ac.averageDCEstimator(ir_ac.ir_avg_reg, ir)

        #print("AC: Red="+repr(red)+" IR="+repr(ir))
        #print("DC: Red="+repr(red_dc)+" IR="+repr(ir_dc))

        ratio = (red/red_dc) / (ir/ir_dc)
        spo2 = a*a*ratio + b*ratio + c

        average_spo2_buffer.append(spo2)

        for i in range(len(average_spo2_buffer)):
            average_spo2 += i

        average_spo2 = average_spo2 / len(average_spo2_buffer)

        print(average_spo2)



