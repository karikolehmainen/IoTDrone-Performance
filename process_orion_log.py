
import os
import sys
import json

def processFile(filename):
	f = open(filename, "r")
	lines = lines = f.readlines()

	for line in lines:
		split = line.split("{")
		item = 0
		str = ""
		found = False
		for elem in split:
			if "velocity" in elem:
				#print(split[item+1].split(",")[1].split(":")[1])
				str = str + split[item+1].split(",")[1].split(":")[1]
				found = True
			if "\"stream\":\"stdout\",\"time\":" in elem:
				if found:
					#print(split[item].split("\"time\":\"")[1].split("\"}")[0])
					str = str + "," + split[item].split("\"time\":\"")[1].split("\"}")[0]
					found = False

			item = item+1
		if(len(str)>5):
			print(str)			
		


processFile(sys.argv[1])


