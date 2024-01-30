from flask import Flask, jsonify
from flask_cors import CORS
import socket
import sys
from struct import unpack

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
'''
print(f'Starting TCP server on {host} port {port}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()

    # upon receiving a connection
    with conn:
        print(f"Connected by {addr}")

        # continuously receive data
        while True:
            data = conn.recv(512)
            if not data:
                break
            decoded_data = data.decode('ascii')
            data = decoded_data.split(" ")
'''
@app.route('/', methods=['GET'])
def index():
    test_data = '{"time":0, "heartrate":-1, "spo2":-2, "temperature":-3}'
    return test_data
    #return data

if __name__ == '__main__':
    app.run()