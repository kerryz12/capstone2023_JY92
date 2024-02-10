from networking import *
import utime

# set up wifi and TCP communication protocols
host, port = '192.168.159.40', 64000
server_address = (host, port)

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    network_obj = Networking()
    network_obj.connect()
    network_obj.createTCPSocket(server_address)
    print(f"[CONNECTED] Client connected to server at {host}:{port}")

    connected = True
    while connected:
        network_obj.sendTCPPacket("1")
        utime.sleep_ms(50)

if __name__ == "__main__":
    main()