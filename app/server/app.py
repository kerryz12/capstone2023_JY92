from flask import Flask, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler
import socket
import time
from random import randint

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
host, port = '0.0.0.0', 64000
server_address = (host, port)

print(f'Starting TCP server on {host} port {port}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()

    # upon receiving a connection
    with conn:
        print(f"Connected by {addr}")

@scheduler.task('interval', id='poll_data', seconds=0.5, misfire_grace_time=2)
def poll_data():
    global decoded_data

    data = conn.recv(512)
    if not data:
        return
    decoded_data = data.decode('ascii')

def getData():
    #return [time.time() - start_time, randint(40,120), randint(90,100), randint(30,40)]
    return decoded_data  

@app.route('/time', methods=['GET'])
def getTime():
    return str(getData()[0])

@app.route('/heartrate', methods=['GET'])
def heartrate():
    return str(getData()[1])

@app.route('/spo2', methods=['GET'])
def spo2():
    return str(getData()[2])

@app.route('/temperature', methods=['GET'])
def temperature():
    return str(getData()[3])

if __name__ == '__main__':
    app.run(debug=True, port=5000)