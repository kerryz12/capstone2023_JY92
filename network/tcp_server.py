import socket
import sys
from struct import unpack
import math
import emd
import scipy
import numpy as np
import matplotlib.pyplot as plt

# clear data file
#f = open('data/output.txt', 'w')
#f.close()

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
host, port = '0.0.0.0', 64000
server_address = (host, port)
red_list = []
redrr_start = 0
respRateArray = []


print(f'Starting TCP server on {host} port {port}')

def getData():
    #return [time.time() - start_time, randint(40,120), randint(90,100), randint(30,40)]
    return split_data_main


def getRespiratoryRate():
    raw_red= getData()[4]
    red_list.append(raw_red)
    global redrr_start
    global respRateArray

    if(len(red_list)> 100):
        red_np = np.array(red_list, dtype=int)
        red_norm = red_np -min(red_np)
        imf = emd.sift.sift(red_norm)
        sum_imf = sum(imf)
        max=np.max(plt.psd(sum_imf))
        log_red=10*math.log10(max)
        print("RR = " + str(log_red))
        red_list.pop(0)
        respRateArray.append(log_red)
        print(red_list[0])
        '''
        if(len(respRateArray) == 16):
            finalRR = respRateArray/16
            print(finalRR)
        '''


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    split_data_main = ["0", "-1", "-1", "-1", "-1"]

    # upon receiving a connection
    with conn:
        print(f"Connected by {addr}")

        # continuously receive data
        while True:
            data = conn.recv(512)
            if not data:
                break
            decoded_data = data.decode('ascii')

            split_data_main = decoded_data.split()
            print(split_data_main)
            
            getRespiratoryRate()
            # write data to output file
            #with open('data/output.txt', 'a') as f:
            #    f.write(decoded_data)

