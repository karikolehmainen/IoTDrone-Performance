
import paho.mqtt.client as mqtt
import time
import sys

client = mqtt.Client("tester-pub")
client.username_pw_set("px4","flexigrobots") 
client.connect(sys.argv[1], port=1883, keepalive=60, bind_address="")

counter = 0
topic = "/54321/drone001/attrs"
delay = float(sys.argv[2])
limit = 1000
payload = "lat|0|lon|0|z|0|h|"
while(counter < limit):
	counter = counter+1
	ts1 = time.time()
	print("TS1:"+topic+":"+payload+str(counter)+"|v|"+str(ts1))
	client.publish(topic,payload+str(counter)+"|v|"+str(ts1))
	time.sleep(delay)
