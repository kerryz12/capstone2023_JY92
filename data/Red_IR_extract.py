from max30102 import MAX30102
from machine import SoftI2C, I2C, Pin
import time

#Define parameters for the sensor and pi pico
my_SDA_pin = 8  # I2C SDA pin number here!
my_SCL_pin = 9  # I2C SCL pin number here!
my_i2c_freq = 400000  # I2C frequency (Hz) here!

#Variables for getting a finger pulse
l_threshold = 7000
u_threshold = 17000
num_samps = 1000

i2c = machine.I2C(0, scl=machine.Pin(my_SCL_pin), sda=machine.Pin(my_SDA_pin))
#Set up the i2c communication from the pi pico to the sensor
i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin),
              freq=my_i2c_freq)

devices = i2c.scan()

sensor = MAX30102(i2c=i2c)

# Setup the sensor with default values
sensor.setup_sensor()
    
# keep track of time elapsed
start_time = time.ticks_ms()
count = 0

while (count<num_samps):
    # The check() method has to be continuously polled, to check if
    # there are new readings into the sensor's FIFO queue. When new
    # readings are available, this function will put them into the storage.
    sensor.check()
    

    # Check if the storage contains available samples
    if (sensor.available()):
        count +=1
        # Access the storage FIFO and gather the readings (integers)
        red_sample = sensor.pop_red_from_storage()
        ir_sample = sensor.pop_ir_from_storage()
        
        current_time = time.ticks_ms() - start_time
        print(str(count) +","+str(current_time) + "," + str(red_sample) + "," + str(ir_sample) + ",")

