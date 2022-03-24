import socket
import time
import sys

HOST = sys.argv[1]  # Standard loopback interface address (localhost)
PORT = sys.argv[2]  # Port to listen on (non-privileged ports are > 1023)

count = 0
latency = 0.0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, int(PORT)))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            ts = time.time()
    #        print("TS1:"+ str(ts))
            conn.sendall(str.encode(str(ts)))
            latency = latency + (ts-float(data))*1000
            count = count + 1

print("latency :" + str(latency/count))
