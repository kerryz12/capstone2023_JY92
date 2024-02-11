from flask import Flask, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler
import socket
import time
from random import randint
import threading

MAIN_PICO = "0"
IMU_PICO = "1"
BLE_PICO = "2"

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
host, port = "0.0.0.0", 64000
server_address = (host, port)

print(f'Starting TCP server on {host} port {port}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

print(f"[LISTENING] Server is listening on {host}:{port}")

split_data_main = [0, -1, -1, -1]
split_data_imu = [1, 0]
split_data_ble = [2, 0]
count = 0

# Routing of functions when a connection is established
def handle_client(conn, addr):
    global split_data_main
    global split_data_imu
    global split_data_ble
    
    data = conn.recv(512)
    if not data:
        return
    decoded_data = data.decode('ascii')
    
    if (decoded_data.split()[0] == MAIN_PICO):
        split_data_main = decoded_data.split()
    elif (decoded_data.split()[0] == IMU_PICO):
        split_data_imu = decoded_data.split()
    elif (decoded_data.split()[0] == BLE_PICO):
        split_data_ble = decoded_data.split()    
               
# Create threads when there is a new connection
@scheduler.task('interval', id='poll_tcp', seconds=2)
def poll_tcp():
    global scheduler
    global count
    
    conn, addr = s.accept()
    scheduler.add_job(func=handle_client, args=(conn,addr), trigger='interval', id='test'+str(count), seconds=0.5)
    print(f"[NEW CONNECTION] {addr} connected.")
    count += 1

def getData():
    #return [time.time() - start_time, randint(40,120), randint(90,100), randint(30,40)]
    return split_data_main

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
    return str(split_data_imu[1])

if __name__ == '__main__':
    app.run(port=5000)