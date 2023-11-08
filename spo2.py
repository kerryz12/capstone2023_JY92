from machine import SoftI2C, I2C, Pin
from utime import sleep
from max30102 import MAX30102

# pin values
SDA_PIN = 8
SCL_PIN = 9

# device i2c address
I2C_ADDRESS = 0x57

# register addresses
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

# Create I2C object
i2c = SoftI2C(sda=Pin(SDA_PIN),
              scl=Pin(SCL_PIN),
              freq=400000)

# set up sensor
sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()

while(True):
    sensor.check()

    if (sensor.available()):
        red = sensor.pop_red_from_storage()
        ir = sensor.pop_ir_from_storage()

        print("Red="+repr(red)+" IR="+repr(ir))

