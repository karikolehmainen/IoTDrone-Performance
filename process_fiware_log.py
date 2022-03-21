
import os
import sys
import json

def processFile(filename):
	f = open(filename, "r")
	lines = lines = f.readlines()

	for line in lines:
		split = line.split("|")
		if(len(split) > 8):
			if "msg=stringMessage" in split[8]:
				str = split[8].split("[")[1]+"|"+split[9]+"|"+split[10]+"|"+split[11]+"|"+split[12]+"|"+split[13]+"|"+split[14]+"|"+split[15]+"|"+split[16]+"|"+split[17].split("]")[0]+"|"+split[18].split("time\":")[1].split("\"")[1]
				print(str)
		


print("delay,lat1_min,lat1_avg,lat1_max,lat5_min,lat5_avg,lat5_max")
processFile(sys.argv[1])


