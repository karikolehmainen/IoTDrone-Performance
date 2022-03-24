import socket
import time
import sys

HOST = sys.argv[1]  # The server's hostname or IP address
PORT = sys.argv[2]  # The port used by the server

latency = 0.0
skew = 0.0
count = 0
tests = 100

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	ts1 = 0.0
	ts2 = 0.0
	ts3 = 0.0
	while (count < tests):
		count = count + 1
		ts1 = time.time()
		s.sendall(str.encode(str(ts1)))
		data = s.recv(1024)
		ts3 = time.time()
		ts2 = float(data)
		latency = latency + (ts3-ts1)*1000
		skew = skew + ((ts2-ts1)*1000)-(((ts3-ts1)*1000)/2)

print("latency:"+str(latency/count) + " skew:"+str(skew/count))
