import machine
import utime
from lib.networking import *
from micropython import const
from lib.ble_advertising import decode_services, decode_name
import struct
import bluetooth
import time

# Patient states
POS_NONE = 0
POS_LYING = 1
POS_SITTING = 2
POS_STANDING = 3

# UART configuration for Pico W
# This part of the code initializes the Raspberry
# Pi Pico W's UART0 interface, sets the baud rate to 9600, and specifies the UART's TX (transmit) and RX (receive) pins as GPIO 12 and GPIO 13, respectively.
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(12), rx=machine.Pin(13))

# set up wifi and TCP communication protocols
host, port = '172.20.10.4', 64000 # 172.20.10.7 Chis hotspot  192.168.159.115 Tina hotspot
server_address = (host, port)

network_obj = Networking()
network_obj.connect()
network_obj.createTCPSocket(server_address)

current_room = 1

#Localization states
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GAP_RSSI_RESULT = const(20)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

class BLESimpleCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._reset()

    def _reset(self):
        self._name = None
        self._addr_type = None
        self._addr = None
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None
        self._notify_callback = None
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._tx_handle = None
        self._rx_handle = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND) and _UART_SERVICE_UUID in decode_services(adv_data):
                self._addr_type = addr_type
                self._addr = bytes(addr)
                self._name = decode_name(adv_data) or "?"
                self._rssi = rssi
                self._ble.gap_scan(None)
        elif event == _IRQ_SCAN_DONE:
            if self._scan_callback:
                if self._addr:
                    self._scan_callback(self._addr_type, self._addr, self._name, self._rssi)
                    self._scan_callback = None
                else:
                    self._scan_callback(None, None, None, None)
        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                self._reset()
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            print("service", data)
            if conn_handle == self._conn_handle and uuid == _UART_SERVICE_UUID:
                self._start_handle, self._end_handle = start_handle, end_handle
        elif event == _IRQ_GATTC_SERVICE_DONE:
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(self._conn_handle, self._start_handle, self._end_handle)
            else:
                print("Failed to find uart service.")
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _UART_RX_CHAR_UUID:
                self._rx_handle = value_handle
            if conn_handle == self._conn_handle and uuid == _UART_TX_CHAR_UUID:
                self._tx_handle = value_handle
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            if self._tx_handle is not None and self._rx_handle is not None:
                if self._conn_callback:
                    self._conn_callback()
            else:
                print("Failed to find uart rx characteristic.")
        elif event == _IRQ_GATTC_WRITE_DONE:
            conn_handle, value_handle, status = data
            print("TX complete")
        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle and value_handle == self._tx_handle:
                if self._notify_callback:
                    self._notify_callback(notify_data)
        elif event == _IRQ_GAP_RSSI_RESULT:
            conn_handle, rssi = data
            if conn_handle == self._conn_handle:
                print("RSSI:", rssi)

    def is_connected(self):
        return self._conn_handle is not None and self._tx_handle is not None and self._rx_handle is not None

    def scan(self, callback=None):
        self._addr_type = None
        self._addr = None
        self._scan_callback = callback
        self._ble.gap_scan(2000, 30000, 30000)

    def connect(self, addr_type=None, addr=None, callback=None):
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        self._conn_callback = callback
        if self._addr_type is None or self._addr is None:
            return False
        self._ble.gap_connect(self._addr_type, self._addr)
        return True

    def disconnect(self):
        if self._conn_handle is None:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    def write(self, v, response=False):
        if not self.is_connected():
            return
        self._ble.gattc_write(self._conn_handle, self._rx_handle, v, 1 if response else 0)

    def on_notify(self, callback):
        self._notify_callback = callback

def on_scan(addr_type, addr, name, rssi):
    if addr_type is not None:
        global current_room
    
    if addr_type is not None:
        #print(name,rssi)
        if(name == "Room 1" and rssi > -65):
            print("Inside",name)
            current_room = 1
        elif(name == "Room 2" and rssi > -73):
            print("Inside",name)
            current_room = 2
        elif(name == "Room 1" and rssi <= -65 and current_room == 1):
            print("Corridor")
            current_room = 3
        elif(name == "Room 2" and rssi <= -73 and current_room == 2):
            print("Corridor")
            current_room = 3
        elif(current_room == 3):
            print("Corridor")
        else:
            print("Inside Room",current_room)
        #Need to onvert rssi to distance
        #Distance = 10^((Measured Power - Instant RSSI)/(10*N))
        #Measured Power: rssi at a distance of 1m (need to measure), normally N=2
        #or find a rssi_threshold
    else:
        print("Nothing Found")

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
    acc = get_acc(ACCData)
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
                    network_obj.sendTCPPacket("%10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f" % result)
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
    acc_x = (int(axh) << int(8) | int(axl)) / 32768.0 * k_acc
    acc_y = (int(ayh) << int(8) | int(ayl)) / 32768.0 * k_acc
    acc_z = (int(azh) << int(8) | int(azl)) / 32768.0 * k_acc
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
    gyro_x = (int(wxh) << int(8) | int(wxl)) / 32768.0 * k_gyro
    gyro_y = (int(wyh) << int(8) | int(wyl)) / 32768.0 * k_gyro
    gyro_z = (int(wzh) << int(8) | int(wzl)) / 32768.0 * k_gyro
    if gyro_x >= k_gyro:
        gyro_x -= 2 * k_gyro
    if gyro_y >= k_gyro:
        gyro_y -= 2 * k_gyro
    if gyro_z >= k_gyro:
        gyro_z -= 2 * k_gyro
    return gyro_x, gyro_y, gyro_z


def get_angle(datahex):
    global current_room
    
    rxl = datahex[0]
    rxh = datahex[1]
    ryl = datahex[2]
    ryh = datahex[3]
    rzl = datahex[4]
    rzh = datahex[5]
    k_angle = 180.0
    angle_x = float(int(rxh) << int(8) | int(rxl)) / 32768.0 * k_angle
    angle_y = float(int(ryh) << int(8) | int(ryl)) / 32768.0 * k_angle
    angle_z = float(int(rzh) << int(8) | int(rzl)) / 32768.0 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >= k_angle:
        angle_z -= 2 * k_angle
    return angle_x, angle_y, angle_z

def detect_falling(acc_data, threshold=4.0):
    """
    Detects falling based on sudden changes in acceleration.
    :param acc_data: List of acceleration data [ax, ay, az]
    :param threshold: Threshold value for detecting twitching
    :return: True if twitching is detected, False otherwise
    """
    # Calculate the magnitude of acceleration
    acc_magnitude = (acc_data[0] ** 2 + acc_data[1] ** 2 + acc_data[2] ** 2) ** 0.5
    
    # Check if acceleration exceeds the threshold
    if acc_magnitude > threshold:
        return True
    return False

def detect_twitching(acc_data, threshold=1.0):
    """
    Detects twitching based on sudden changes in acceleration.
    :param acc_data: List of acceleration data [ax, ay, az]
    :param threshold: Threshold value for detecting twitching
    :return: True if twitching is detected, False otherwise
    """
    # Calculate the magnitude of acceleration
    acc_magnitude = (acc_data[0] ** 2 + acc_data[1] ** 2 + acc_data[2] ** 2) ** 0.5
    
    # Check if acceleration exceeds the threshold
    if acc_magnitude > threshold:
        return True
    return False

def main():
    global current_room
    print("Serial is Opened:", uart.any())
    ble = bluetooth.BLE()
    central = BLESimpleCentral(ble)
    not_found = False
    
    while True:
        central.scan(on_scan)
        
        if uart.any() > 0:
            datahex = uart.read(33)
            if datahex and len(datahex) == 33:
                DueData(datahex)  # No need to convert to list if DueData can handle bytes
                # Get the current angles
                current_angles = get_angle(AngleData)
                angle_x, angle_y, angle_z = current_angles
                current_gyros = get_gyro(GYROData)
                gyro_x, gyro_y, gyro_z = current_gyros
                current_accs = get_acc(ACCData)
                acc_x, acc_y, acc_z = current_accs
                
                
                
                # Check the nromal lying condition ( face up)
                if -40 <= angle_y <= 0 :
                    #network_obj.sendTCPPacket("1 " + str(POS_LYING) + " " + str(current_room) + " ")
                    print("lying")
                    
                #Check the normal lying but with tilting (face up)
                elif -110 <= angle_x <= -60 and -60 <= angle_y <= 40:
                   # network_obj.sendTCPPacket("1 " + str(POS_LYING) + " " + str(current_room) + " ")
                    print("lying")
                    
                #Check the lying on the left side
                elif 120 <= angle_x <= 170 and -80 <= angle_y < -30:
                    #network_obj.sendTCPPacket("1 " + str(POS_LYING) + " " + str(current_room) + " ")
                    print("lying")
                    
                #Check the lying on the right side
                elif -125 <= angle_x <= -70 and 0 <= angle_y <= 70 :
                   # network_obj.sendTCPPacket("1 " + str(POS_LYING) + " " + str(current_room) + " ")
                    print("lying")
                    
                elif -180 <= angle_x <= -90 and -85 <= angle_y < -40 :
                  # network_obj.sendTCPPacket("1 " + str(POS_LYING) + " " + str(current_room) + " ")
                    print("lying")
                    
                elif 100 <= angle_x <= 180 and -85 <= angle_y < -50 :
                   # network_obj.sendTCPPacket("1 " + str(POS_LYING) + " " + str(current_room) + " ")
                    print("lying")
                    
                else:
                   # network_obj.sendTCPPacket("1 " + str(POS_NONE) + " " + str(current_room) + " ")
                    print("not lying")
                    
                #Body Dynamics:
                # Check the twitching condition
                if detect_twitching(current_accs):
                    network_obj.sendTCPPacket("Twitching detected")
                    print("Twitching detected")
                # Check the twitching condition
                if detect_falling(current_accs):
                    network_obj.sendTCPPacket("Falling detected")
                    print("Falling detected")

        utime.sleep_ms(200)  # Delay to prevent reading too quickly

# Main execution
if __name__ == '__main__':
    main()  # Call the main function
   
