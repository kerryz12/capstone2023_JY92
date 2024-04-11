from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler
import socket
import time
from random import randint

# for breathing rate
import numpy as np
import emd
import matplotlib.pyplot as plt
import math

MAIN_PICO = "0"
IMU_SHOULDER_PICO = "1" # will contain BLE
IMU_THIGH_PICO = "2"

red_list = []
respRateArray = []
redrr_start = 0

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

start_time = time.time()

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
#socket.gethostbyname(socket.gethostname())
host, port = '0.0.0.0', 64000
server_address = (host, port)

print(f'Starting TCP server on {host} port {port}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

print(f"[LISTENING] Server is listening on {host}:{port}")

split_data_main = ["0", "-1", "-1", "-1", "-1"]
split_data_shoulder = ["1", "0", "0"]
split_data_thigh = ["2", "0"]
count = 0

# Routing of functions when a connection is established
def handle_client(conn, addr):
    global split_data_main
    global split_data_shoulder
    global split_data_thigh
    
    data = conn.recv(512)
    print("Connected")
    if not data:
        return
    decoded_data = data.decode('ascii')

    print(decoded_data.split())
    if (decoded_data.split()[0] == MAIN_PICO):
        split_data_main = decoded_data.split()
    elif (decoded_data.split()[0] == IMU_SHOULDER_PICO):
        split_data_shoulder = decoded_data.split()
    elif (decoded_data.split()[0] == IMU_THIGH_PICO):
        split_data_thigh = decoded_data.split()
               
# Create threads when there is a new connection
@scheduler.task('interval', id='poll_tcp', seconds=2)
def poll_tcp():
    global scheduler
    global count
    
    conn, addr = s.accept()
    scheduler.add_job(func=handle_client, args=(conn,addr), trigger='interval', id='handle_client'+str(count), seconds=0.5)
    print(f"[NEW CONNECTION] {addr} connected.")
    count += 1

def getData():
    #return [time.time() - start_time, randint(40,120), randint(90,100), randint(30,40)]
    return split_data_main

# POS_NONE = 0
# POS_LYING = 1
# POS_SITTING = 2
# POS_STANDING = 3
def getPosition():
    if (split_data_shoulder[1] == "0" and split_data_thigh[1] == "2"):
        print("2")
        return "2"
    elif (split_data_shoulder[1] == "0" and split_data_thigh[1] == "3"):
        print("3")
        return "3"
    elif (split_data_shoulder[1] == "1" and split_data_thigh[1] == "2"):
        print("1")
        return "1"
    else:
        return "0"

def getRespiratoryRate():
    raw_red = getData()[4]
    global red_list
    global redrr_start
    global respRateArray
    
    red_list.append(raw_red)

    if(len(red_list) > 100):
        red_np = np.array(red_list, dtype=int)
        red_norm = red_np - min(red_np)
        imf = emd.sift.sift(red_norm)
        sum_imf = sum(imf)
        max = np.max(plt.psd(sum_imf))
        log_red = 10*math.log10(max)
        red_list.pop(0)
        respRateArray.append(log_red)
        
        return red_list[0]

# APP ROUTES
@app.route('/heartrate', methods=['GET'])
def heartrate():
    return str(getData()[1])

@app.route('/spo2', methods=['GET'])
def spo2():
    return str(getData()[2])

@app.route('/temperature', methods=['GET'])
def temperature():
    return str(getData()[3])

@app.route('/position', methods=['GET'])
def position():
    return getPosition()

@app.route('/location', methods=['GET'])
def location():
    return split_data_shoulder[2]

@app.route('/br', methods=['GET'])
def br():
    return getRespiratoryRate()

@app.route('dynamic', methods=['GET'])
def dyanmic():
    return split_data_shoulder[3]

if __name__ == '__main__':
    app.run(port=5000)