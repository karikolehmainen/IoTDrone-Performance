import time
import os
import sys


def getDataSet(files, indx):
	dataset = []
	indxstr = str(indx)+"ms"
	for file in files:
		file_str = file.split(".")[0]
		#print(file_str)
		params = file_str.split("-")
		if (indxstr == params[len(params)-1]):
			if (params[0] == "orion" and params[1] == "sub"):
				dataset.append(file)

	return dataset	

def processSet(set,index):
	stage1_lines = []
	for file_str in set:
		f = open(sys.argv[1]+"/"+file_str, "r")
		lines = f.readlines()

	TS1 = 0.0
	TS6 = 0.0
	lat5 = 0.0
	count = 0

	for line in lines:
		elements = line.split(",")
		TS1 = 0.0
		TS6 = 0.0
		lat5 = 0.0
		if (len(elements) == 3):
			TS1 = float(elements[0].split(":")[1])
			TS6 = float(elements[1].split(":")[1])
			lat5 = float(elements[2].split(":")[1])
		
			print(str(TS1)+","+str(TS6)+","+str(lat5))

files = os.listdir(sys.argv[1])
time_index = 0
print("TS1,TS6,lat5")
dataset = getDataSet(files, sys.argv[2])
if (len(dataset) > 0):
	processSet(dataset,time_index)


