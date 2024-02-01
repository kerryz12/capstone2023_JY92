from flask import Flask, jsonify
from flask_cors import CORS
import socket
import time
from struct import unpack
from random import randint

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
host, port = '0.0.0.0', 64000
server_address = (host, port)

start_time = time.time()

'''
print(f'Starting TCP server on {host} port {port}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()

    # upon receiving a connection
    with conn:
        print(f"Connected by {addr}")
''' 
def getData():
    '''
    data = conn.recv(512)
    if not data:
        print("Error: Not data")
    decoded_data = data.decode('ascii')
    '''

    return [time.time() - start_time, randint(20,100), randint(90,100), randint(20,100)]
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
    app.run()