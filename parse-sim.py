import time
import os
import sys

def processSet(file_str):
	lines = []

	f = open(file_str, "r")
	lines = f.readlines()

	TS1 = 0.0
	TS6 = 0.0
	lat5 = 0.0
	count = 0
	drones = {}
	for line in lines:
		elements = line.split(",")
		TS1 = 0.0
		TS6 = 0.0
		lat5 = 0.0
		if (len(elements) == 4):
			drone = elements[0]
			TS1 = int(float(elements[1].split(":")[1]))
			TS6 = int(float(elements[2].split(":")[1]))
			lat5 = float(elements[3].split(":")[1])

			if (drone not in drones):
				drones[drone] = []

			drones[drone].append(drone+","+str(TS1)+","+str(TS6)+","+str(lat5))
	for drone in drones:
		timeslot = 0
		cntr = 0
		lat = 0.0
		for line in drones[drone]:
			ts = int(float(line.split(",")[1]))
			if (timeslot == 0):
				timeslot = ts
			if (timeslot == ts):
				cntr = cntr + 1
				lat = lat + float(line.split(",")[3])
			else:
				lat = lat/cntr
				line = line.split(",")[0]+","+str(timeslot)+","+str(lat)+","+str(cntr)
				print(line)
				lat = 0.0
				cntr = 0
				timeslot = 0


print("Drone,TS1,TS6,lat5")
processSet(sys.argv[1])


