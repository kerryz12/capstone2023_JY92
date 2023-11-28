import socket
import sys
from max30102 import MAX30102
from machine import SoftI2C, I2C, Pin
import time
from hr_algorithm import *
import random
from struct import pack
from lib.networking import *

#For wifi
import network
import socket


#Define parameters for the sensor and pi pico
my_SDA_pin = 8  # I2C SDA pin number here!
my_SCL_pin = 9  # I2C SCL pin number here!
my_i2c_freq = 400000  # I2C frequency (Hz) here!

#Variables for getting a finger pulse
l_threshold = 7000
u_threshold = 17000
lastBeat = 0
beat = HeartBeat()
beatsPerMinute = 0
beatAvg = 0
prev_beatAvg = 0
rateSpot = 0

start_finger_time = 0
end_finger_time = 0
finger_on = False
count = 0


RATE_SIZE = 16 #Increase this for more averaging. 4 is good.
rates = [RATE_SIZE]

#SPO2
# how many samples to keep to take average of for SPO2 calculation
SPO2_AVERAGE_SAMPLES = 16

ir_ac = HeartBeat()
red_ac = HeartBeat()

# SPO2 Algorithm Values
a = 1.5958422
b = -34.6596622
c = 33.1098759
spo2 = 1
average_spo2 = 0
average_spo2_buffer = []

# set up wifi and TCP communication protocols
host, port = '206.12.45.19', 64000
server_address = (host, port)

network_obj = Networking()
network_obj.connect()
network_obj.createTCPSocket(server_address)

i2c = machine.I2C(0, scl=machine.Pin(my_SCL_pin), sda=machine.Pin(my_SDA_pin))
#Set up the i2c communication from the pi pico to the sensor
i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin),
              freq=my_i2c_freq)

devices = i2c.scan()

sensor = MAX30102(i2c=i2c)

# Setup the sensor with default values
sensor.setup_sensor()

#Set up average buffer
for i in range(SPO2_AVERAGE_SAMPLES):
    average_spo2_buffer.append(float(0))
    
# keep track of time elapsed
start_time = time.ticks_ms()

while (True):
    # The check() method has to be continuously polled, to check if
    # there are new readings into the sensor's FIFO queue. When new
    # readings are available, this function will put them into the storage.
    sensor.check()

    # Check if the storage contains available samples
    if (sensor.available()):
        # Access the storage FIFO and gather the readings (integers)
        red_sample = sensor.pop_red_from_storage()
        ir_sample = sensor.pop_ir_from_storage()

        
        #print(ir_sample, ",", red_sample)
        #Printing the raw LED values for debugging
        #if(ir_sample>0):
        #    print(ir_sample)
        
        if (ir_sample> l_threshold and ir_sample < u_threshold):
            # Print the acquired data (can be plot with Arduino Serial Plotter) - Used for debugging
            #print(ir_sample)
            
            if (finger_on == False):
                start_finger_time = time.ticks_ms()
                finger_on = True
                print("Loading...")
                network_obj.sendTCPPacket("Loading..")
            
            #We sensed a beat!
            #print(beat.checkForBeat(ir_sample))
            if(beat.checkForBeat(ir_sample)):
                count += 1
                delta = time.ticks_ms() - lastBeat
                lastBeat = time.ticks_ms()
 
                beatsPerMinute = 60 / (delta / 1000.0)
                
                prev_beatAvg = beatAvg
                #print(delta)
                #print("Beats Per Minute:", beatsPerMinute)
                #print("Wait")
                red_dc = red_ac.averageDCEstimator(red_ac.ir_avg_reg, red_sample)
                ir_dc = ir_ac.averageDCEstimator(ir_ac.ir_avg_reg, ir_sample)
                
                ratio = (red_sample/red_dc) / (ir_sample/ir_dc)
                spo2 = a*a*ratio + b*ratio + c
                #print("SPO2:", spo2)
                
                for i in range(SPO2_AVERAGE_SAMPLES-1):
                    average_spo2_buffer[i] = average_spo2_buffer[i+1]

                average_spo2_buffer[SPO2_AVERAGE_SAMPLES-1] = spo2

                for i in range(SPO2_AVERAGE_SAMPLES):
                    average_spo2 += average_spo2_buffer[i]
                    
                average_spo2 = average_spo2 / SPO2_AVERAGE_SAMPLES
                
                if(beatsPerMinute <= 255 and beatsPerMinute > 30):
                    rates.append(beatsPerMinute) #Store this reading in the array
                    rateSpot = rateSpot +1
                    rateSpot %= RATE_SIZE #Wrap variable
                    
                    if(count <=16):
                        print("Calibrating..")
                        network_obj.sendTCPPacket("Calibrating..")
                    
                    
                    #Take average of readings
                    beatAvg = 0
                    i = 0
                    for x in rates:
                       #print(x)
                       beatAvg += x
                       i += 1
                       if (i==RATE_SIZE):
                         beatAvg = beatAvg/RATE_SIZE
                         print("Beat Average:", beatAvg)
                         
                         #Die Temp has an inherent resolution of 0.0625°C, but be aware that the accuracy is ±1°C.
                         temperature_C = sensor.read_temperature() 
                         print("Temperature: ", temperature_C, "°C")
                         
                         #print(beatAvg) #For the serial plotter
                         rates.pop(0)
                         #time.sleep_ms(5)
                         
                         #for i in range(SPO2_AVERAGE_SAMPLES-1):
                         #   average_spo2_buffer[i] = average_spo2_buffer[i+1]

                         #average_spo2_buffer[SPO2_AVERAGE_SAMPLES-1] = spo2

                         #for i in range(SPO2_AVERAGE_SAMPLES):
                         #   average_spo2 += average_spo2_buffer[i]

                         #average_spo2 = average_spo2 / SPO2_AVERAGE_SAMPLES
                         spo2_val = min(int(average_spo2*100), 100)
                         print("Blood Oxygenation: ", spo2_val, "%")
                         
                         if (count%2 ==0):
                             # send every second reading to the TCP server
                             current_time = time.ticks_ms() - start_time
                             network_obj.sendTCPPacket(str(current_time) + "\n")
                             network_obj.sendTCPPacket("Temperature: "+ str(temperature_C) + "degC" + "\n")
                             network_obj.sendTCPPacket("Beat Average: " + str(beatAvg) + "\n")
                             network_obj.sendTCPPacket("Blood Oxygenation: "+ str(spo2_val) + "% \n")
                             sleep_ms(1)
                             
                    average_spo2 = 0      
                         
               
#        elif (end_finger_time-start_finger_time>5):
#            rates.clear()
#            finger_on=False
#            end_finger_time =0
#            start_finger_time =0
#            print("Place finger on sensor please!")
        
                
    
            



