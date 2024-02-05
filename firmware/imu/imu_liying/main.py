import machine
import utime
from networking import *

# UART configuration for Pico W
# This part of the code initializes the Raspberry
# Pi Pico W's UART0 interface, sets the baud rate to 9600, and specifies the UART's TX (transmit) and RX (receive) pins as GPIO 12 and GPIO 13, respectively.
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(12), rx=machine.Pin(13))

# set up wifi and TCP communication protocols
host, port = '206.87.216.92', 64000
server_address = (host, port)

network_obj = Networking()
network_obj.connect()
network_obj.createTCPSocket(server_address)

# Global variables to store the IMU data
# acceleration, gyroscope and angle data read from the IMU.
# These data are initially initialised to zero.
ACCData = [0.0] * 8
GYROData = [0.0] * 8
AngleData = [0.0] * 8
FrameState = 0  # Frame state
Bytenum = 0  # Byte number
CheckSum = 0  # Checksum

a = [0.0] * 3
w = [0.0] * 3
Angle = [0.0] * 3

# DueData function processes the received data
def DueData(inputdata):  # New core procedures, read the data partition, each read to the corresponding array 
    global FrameState    # Declare global variables
    global Bytenum
    global CheckSum
    global acc
    global gyro
    global Angle
    for data in inputdata:  # Traversal the input data
        if FrameState == 0:  # When the state is not determined, enter the following judgment
            if data == 0x55 and Bytenum == 0:  # When 0x55 is the first digit, start reading data and increment bytenum
                CheckSum = data
                Bytenum = 1
                continue
            elif data == 0x51 and Bytenum == 1:  # Change the frame if byte is not 0 and 0x51 is identified
                CheckSum += data
                FrameState = 1
                Bytenum = 2
            elif data == 0x52 and Bytenum == 1:
                CheckSum += data
                FrameState = 2
                Bytenum = 2
            elif data == 0x53 and Bytenum == 1:
                CheckSum += data
                FrameState = 3
                Bytenum = 2
        elif FrameState == 1:  # acc

            if Bytenum < 10:            # Read 8 data
                ACCData[Bytenum-2] = data  # Starting from 0
                CheckSum += data
                Bytenum += 1
            else:
                if data == (CheckSum & 0xff):  # verify check bit
                    acc = get_acc(ACCData)
                CheckSum = 0  # Each data is zeroed and a new circular judgment is made
                Bytenum = 0
                FrameState = 0
        elif FrameState == 2:  # gyro

            if Bytenum < 10:
                GYROData[Bytenum-2] = data
                CheckSum += data
                Bytenum += 1
            else:
                if data == (CheckSum & 0xff):
                    gyro = get_gyro(GYROData)
                CheckSum = 0
                Bytenum = 0
                FrameState = 0
        elif FrameState == 3:  # angle

            if Bytenum < 10:
                AngleData[Bytenum-2] = data
                CheckSum += data
                Bytenum += 1
            else:
                if data == (CheckSum & 0xff):
                    Angle = get_angle(AngleData)
                    result = acc+gyro+Angle
                    network_obj.sendTCPPacket("acc:%10.3f %10.3f %10.3f \ngyro:%10.3f %10.3f %10.3f \nangle:%10.3f %10.3f %10.3f" % result)
                    print(
                        "acc:%10.3f %10.3f %10.3f \ngyro:%10.3f %10.3f %10.3f \nangle:%10.3f %10.3f %10.3f" % result)
                CheckSum = 0
                Bytenum = 0
                FrameState = 0

#from open source
def get_acc(datahex):
    axl = datahex[0]
    axh = datahex[1]
    ayl = datahex[2]
    ayh = datahex[3]
    azl = datahex[4]
    azh = datahex[5]
    k_acc = 16.0
    acc_x = (axh << 8 | axl) / 32768.0 * k_acc
    acc_y = (ayh << 8 | ayl) / 32768.0 * k_acc
    acc_z = (azh << 8 | azl) / 32768.0 * k_acc
    if acc_x >= k_acc:
        acc_x -= 2 * k_acc
    if acc_y >= k_acc:
        acc_y -= 2 * k_acc
    if acc_z >= k_acc:
        acc_z -= 2 * k_acc
    return acc_x, acc_y, acc_z


def get_gyro(datahex):
    wxl = datahex[0]
    wxh = datahex[1]
    wyl = datahex[2]
    wyh = datahex[3]
    wzl = datahex[4]
    wzh = datahex[5]
    k_gyro = 2000.0
    gyro_x = (wxh << 8 | wxl) / 32768.0 * k_gyro
    gyro_y = (wyh << 8 | wyl) / 32768.0 * k_gyro
    gyro_z = (wzh << 8 | wzl) / 32768.0 * k_gyro
    if gyro_x >= k_gyro:
        gyro_x -= 2 * k_gyro
    if gyro_y >= k_gyro:
        gyro_y -= 2 * k_gyro
    if gyro_z >= k_gyro:
        gyro_z -= 2 * k_gyro
    return gyro_x, gyro_y, gyro_z


def get_angle(datahex):
    rxl = datahex[0]
    rxh = datahex[1]
    ryl = datahex[2]
    ryh = datahex[3]
    rzl = datahex[4]
    rzh = datahex[5]
    k_angle = 180.0
    angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle
    angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
    angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >= k_angle:
        angle_z -= 2 * k_angle
    return angle_x, angle_y, angle_z

def main():
    print("Serial is Opened:", uart.any())
    while True:
        if uart.any() > 0:
            datahex = uart.read(33)
            if datahex and len(datahex) == 33:
                DueData(datahex)  # No need to convert to list if DueData can handle bytes
                # Get the current angles
                current_angles = get_angle(AngleData)
                angle_x, angle_y, angle_z = current_angles
                
                # Check the first condition
                if 60 <= angle_y <= 90 :
                    network_obj.sendTCPPacket("\nLying")
                    print("lying")
                elif 60 <= angle_x <= 110 and angle_y < 60:
                    network_obj.sendTCPPacket("\nLying")
                    print("lying")
                elif -180 <= angle_x <= -60 and angle_y < 60:
                    network_obj.sendTCPPacket("\nLying")
                    print("lying")
                else:
                    network_obj.sendTCPPacket("\nNot Lying")
                    print("not lying")

        
        utime.sleep_ms(50)  # Delay to prevent reading too quickly

# Main execution
if __name__ == '__main__':
    main()  # Call the main function
   
