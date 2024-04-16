from machine import Pin
import time

buzzer = Pin(17, Pin.OUT)


while True:
    i=0
    while i<250:
        buzzer.value(1)
        time.sleep(0.00125)
        buzzer.value(0)
        time.sleep(0.00125)
        i=i+1
    time.sleep(1)
