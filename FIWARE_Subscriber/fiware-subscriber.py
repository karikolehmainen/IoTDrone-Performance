import falcon
import socket
import time
import json
import requests
import arrow

PORT = 4052  # Port to listen on (non-privileged ports are > 1023)

ORION = "http://localhost:1026/v2/subscriptions"

class NotificationResource(object):
	def on_get(self, req, res):
		print("GOT POST request")
		print(time.time())
		res.status = falcon.HTTP_200  # This is the default status
		res.body = ('Tsuccess')
	def on_post(self, req, resp):
		posted_data = json.loads(req.stream.read())
		ts1 = float(posted_data["data"][0]["velocity"]["value"])
		ts6 = float(time.time())
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = ('Success')
		print("TS1:"+str(ts1)+",TS6:"+str(ts6)+",lat5:"+str((ts6-ts1)*1000))
count = 0
latency = 0.0

local = arrow.utcnow()
print(arrow.utcnow().timestamp())
print(time.time())
print(time.time())
app = falcon.API()
notification_endpoint = NotificationResource()
app.add_route('/notification', notification_endpoint)

