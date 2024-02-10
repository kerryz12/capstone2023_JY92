from flask import Flask, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler
import socket
import time
from random import randint
import threading

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

#Routing of functions when a connection is established
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        data = conn.recv(512)
        if not data:
            return
        decoded_data = data.decode('ascii')
        print({addr}, decoded_data)
    conn.close()

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
host, port = socket.gethostbyname(socket.gethostname()), 64000
server_address = (host, port)

print(f'Starting TCP server on {host} port {port}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
#conn, addr = s.accept()

print(f"[LISTENING] Server is listening on {host}:{port}")

#Create threads when there is a new connection
while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


@scheduler.task('interval', id='poll_data', seconds=0.5, misfire_grace_time=2)
def poll_data():
    global split_data

    data = conn.recv(512)
    if not data:
        return
    decoded_data = data.decode('ascii')
    split_data = decoded_data.split()

def getData():
    #return [time.time() - start_time, randint(40,120), randint(90,100), randint(30,40)]
    return split_data  

#APP ROUTES
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
    app.run(port=5000)