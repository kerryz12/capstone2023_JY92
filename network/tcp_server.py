import socket
import sys
from struct import unpack

# clear data file
f = open('../data/output.txt', 'w')
f.close()

# Create a UDP socket
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

        # continuously receive data
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            decoded_data = data.decode('ascii')
            print(decoded_data)

            # write data to output file
            with open('../data/output.txt', 'a') as f:
                f.write(decoded_data)
