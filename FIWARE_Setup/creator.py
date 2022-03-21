import json
import requests

class EntityCreator:

	def __init__(self):
		print("Init Entity Creator")

	def loadEntity(self, file):
		print("EntityCreator.loadEntity: "+file)
		f = open(file)
		data = json.load(f)
		return data

	def createEntity(self, entity, endpoint):
		# Create a new resource
		headers  = {"Accept": "application/json"}
		headers.update({"fiware-service":"flexigrobots"})
		headers.update({"fiware-servicepath":"/"})
		response = requests.post(endpoint, headers = headers, data = json.dumps(entity))
		if response.status_code != 200:
			print('EntityCreator.createEntity error: ' + str(response.status_code))
			print(response.content)
		else:
			print('EntityCreator.createEntity Success')

class DeviceCreator:
	def __init__(self):
		print("Init Device Creator")

	def pruneIoTAgent(self, dev_endpoint, srv_endpoint):
		headers  = {"Content-Type": "application/json"}
		headers.update({"fiware-service":"flexigrobots"})
		headers.update({"fiware-servicepath":"/"})
		# first get all devices
		response = requests.get(dev_endpoint, headers = headers)
		if response.status_code != 200:
			print('EntityCreator.pruneDevice get devs error: ' + str(response.status_code))
			print(response.content)
		else:
			print('EntityCreator.pruneDevice get devs Success')
#                       print(response.content)
			data = response.json()
			for device in data["devices"]:
				print(device["device_id"])
				response = requests.delete(dev_endpoint+"/"+device["device_id"], headers = headers)
				if response.status_code != 204:
					print('EntityCreator.pruneDevice delete dev error: ' + str(response.status_code))
					print(response.content)
				else:
					print('EntityCreator.pruneDevice delete dev Success')
		# second delete service group
		response = requests.get(srv_endpoint, headers = headers)
		if response.status_code != 200:
			print('EntityCreator.pruneIoTAgent get devs error: ' + str(response.status_code))
			print(response.content)
		else:
			print('EntityCreator.pruneIoTAgent get devs Success')
			data = response.json()
			for service in data["services"]:
				print(service["apikey"])
				#headers.update({"apikey":service["apikey"]})
				#headers.update({"resource":service["resource"]})
				response = requests.delete(srv_endpoint+"?resource="+service["resource"]+"&apikey="+service["apikey"], headers = headers)
				if response.status_code != 204:
					print('EntityCreator.pruneIoTAgent delete srv error: ' + str(response.status_code))
					print(response.content)
				else:
					print('EntityCreator.pruneIoTAgent delete srv Success')

	def loadDevice(self, file):
		print("DeviceCreator.loadDevice: "+file)
		f = open(file)
		data = json.load(f)
		return data

	def createService(self, service, endpoint):
		headers  = {"Content-Type": "application/json"}
		headers.update({"fiware-service":"flexigrobots"})
		headers.update({"fiware-servicepath":"/"})
		response = requests.post(endpoint, headers = headers, data = json.dumps(service))
		if response.status_code != 201:
			print('EntityCreator.createService error: ' + str(response.status_code))
			print(response.content)
		else:
			print('EntityCreator.createService Success')

	def createDevice(self, device, endpoint):
		# Create a new resource
		headers  = {"Content-Type": "application/json"}
		headers.update({"fiware-service":"flexigrobots"})
		headers.update({"fiware-servicepath":"/"})
		response = requests.post(endpoint, headers = headers, data = json.dumps(device))
		if response.status_code != 201:
			print('EntityCreator.createDevice error: ' + str(response.status_code))
			print(response.content)
		else:
			print('EntityCreator.createDevice Success')

def main():
	print("FIWARE Entity Creator")	
	entity_creator = EntityCreator()
	device_creator = DeviceCreator()

	endpoint_ent = "http://localhost:1026/v2/entity"
	endpoint_dev = "http://localhost:4041/iot/devices"
	endpoint_srv = "http://localhost:4041/iot/services"

	device_creator.pruneIoTAgent(endpoint_dev, endpoint_srv)

	ent = entity_creator.loadEntity("entity.json")
	dev = device_creator.loadDevice("device.json")
	srv = device_creator.loadDevice("service.json")

	entity_creator.createEntity(ent, endpoint_ent)
	device_creator.createService(srv, endpoint_srv)
	device_creator.createDevice(dev, endpoint_dev)



print("FIWARE Entity Creator")
main()
