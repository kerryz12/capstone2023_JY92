from machine import I2C, SoftI2C, Pin
from lib.max30102 import MAX30102
from lib.hr_algorithm import *
from lib.spo2_algorithm import *
from lib.networking import *

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
green_ac = HeartBeat()

# create SPO2 and Heartrate objects
spo2_obj = SPO2()
heartbeat_obj = DetectHeartbeat()

# set up wifi and TCP communication protocols
host, port = '192.168.159.40', 64000
server_address = (host, port)

network_obj = Networking()
network_obj.connect()
network_obj.createTCPSocket(server_address)

# keep track of time elapsed
start_time = time.ticks_ms()
count = 0

# main loop
while(True):
    # check for new readings
    sensor.check()

    if (sensor.available()):
        red = sensor.pop_red_from_storage()
        ir = sensor.pop_ir_from_storage()
        green = sensor.pop_green_from_storage()
        print(red)

        # get the DC value of each LED reading
        red_dc = red_ac.averageDCEstimator(red_ac.ir_avg_reg, red)
        ir_dc = ir_ac.averageDCEstimator(ir_ac.ir_avg_reg, ir)
        green_dc = green_ac.averageDCEstimator(green_ac.ir_avg_reg, green)

        heartbeat_obj.detectHeartbeat(red)
        average_heartbeat = heartbeat_obj.getBeatAverage()

        spo2 = spo2_obj.calculateSPO2(red, red_dc, ir, ir_dc)
        average_spo2 = spo2_obj.calculateAverageSPO2(spo2)

        temperature = sensor.read_temperature() + 8

        # send the data to the TCP server
        current_time = time.ticks_ms() - start_time
        print(str(current_time) + " " + str(average_heartbeat) + " " + str(average_spo2) + " " + str(temperature))
        network_obj.sendTCPPacket("0 " + str(average_heartbeat) + " " + str(average_spo2) + " " + str(temperature))
