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
			dataset.append(file)

	return dataset	
def convertTime(str):
	p = '%Y-%m-%dT%H:%M:%S.%fZ'
	str = str[0:23]
	micro = float(str.split(".")[1])
	str = str+"Z"
	#print(str)
	ts = time.strptime(str.strip(), p)
	#print(float(time.mktime(ts))+micro/1000)
	return float(time.mktime(ts)+micro/1000)+7200

def processSet(set,index):
	stage1_lines = []
	for file_str in set:
		fileparts = file_str.split("-")
		#print(file_str)
		if (fileparts[0] == "mqtt"):
			if (fileparts[1]=="pub"):
				stage1 = open(sys.argv[1]+"/"+file_str, "r")
				stage1_lines = stage1.readlines()
			else:
				stage2 = open(sys.argv[1]+"/"+file_str, "r")
				stage2_lines = stage2.readlines()
		if (file_str.split("-")[0] == "iotagent"):
			stage3 = open(sys.argv[1]+"/"+file_str, "r")
			stage3_lines = stage3.readlines()
		if (file_str.split("-")[0] == "orion"):
			if (fileparts[1]=="sub"):
				stage5 = open(sys.argv[1]+"/"+file_str, "r")
				stage5_lines = stage5.readlines()
			else:
				stage4 = open(sys.argv[1]+"/"+file_str, "r")
				stage4_lines = stage4.readlines()

	TS1 = 0.0
	TS2 = 0.0
	TS3 = 0.0
	TS4 = 0.0
	TS6 = 0.0
	lat1_min = 100.0
	lat1_max = 0.0
	lat1_avg = 0.0
	lat2_min = 100.0
	lat2_max = 0.0
	lat2_avg = 0.0
	lat3_min = 100.0
	lat3_max = 0.0
	lat3_avg = 0.0
	lat5_min = 100.0
	lat5_max = 0.0
	lat5_avg = 0.0
	count = 0
	stage2_miss = 0
	stage3_miss = 0
	stage4_miss = 0
	stage5_miss = 0

	for line in stage1_lines:
		elements = line.split(":")
		TS1 = 0.0
		TS2 = 0.0
		TS3 = 0.0
		TS4 = 0.0
		TS6 = 0.0
		stage2_nfound = True
		stage3_nfound = True
		stage4_nfound = True
		stage5_nfound = True
		if (len(elements) == 3):
			TS1 = float(elements[2].split("|")[9])
			topic = elements[1]
			bkrline = ""
			for bkrline in stage2_lines:
				bkrset = bkrline.split(",")
				#print(bkrline)
				if (len(bkrset) == 3 and bkrset[1] == "TS2"):
					TS2=float(bkrset[2])
					if (bkrset[0] == topic and TS2 > TS1):
						stage2_nfound = False
						#print("found brk on line: "+str(linec)+" : "+bkrline)
						break


			#print("TS2:"+str(TS2))
			for iotline in stage3_lines:
				sub_set=iotline.split("|")
				#print(sub_set)
				if (len(sub_set) == 11):
					if (float(sub_set[9]) == TS1):
						TS3=convertTime(sub_set[10])
						#print(str(TS3))
						stage3_nfound = False
						#print("found sub on line: "+str(linec)+" : "+subline)
						break

			for orionline in stage4_lines:
				sub_set=orionline.split(",")
				#print(sub_set)
				if (len(sub_set) == 2):
					if (float(sub_set[0]) == TS1):
						TS4=convertTime(sub_set[1])
						stage4_nfound = False
						#print("found sub on line: "+str(linec)+" : "+subline)
						break

			for appline in stage5_lines:
				sub_set=appline.split(",")
				#print(sub_set)
				if (len(sub_set) == 3):
					if (float(sub_set[0].split(":")[1]) == TS1):
						TS6=float(sub_set[1].split(":")[1])
						stage5_nfound = False
						break
			if (stage2_nfound):
				#print("MQTT Broker entry not found for TS1: "+ str(TS1))
				stage2_miss = stage2_miss+1
			if (stage3_nfound):
				#print("IoTAgent entry not found for TS1: "+ str(TS1))
				stage3_miss = stage3_miss+1
			if (stage4_nfound):
				#print("Orion entry not found for TS1: "+ str(TS1))
				stage4_miss = stage4_miss+1
			if (stage5_nfound):
				#print("Orion Subscriber entry not found for TS1: "+ str(TS1))
				stage5_miss = stage5_miss+1

			if (not stage2_nfound and not stage3_nfound and not stage4_nfound and not stage5_nfound):
				lat1 = TS2-TS1
				lat2 = TS3-TS1			
				lat3 = TS4-TS1
				lat5 = TS6-TS1
				count = count + 1
				if (lat1 < lat1_min):
					lat1_min = lat1
				if (lat2 < lat2_min):
					lat2_min = lat2
				if (lat3 < lat3_min):
					lat3_min = lat3
				if (lat5 < lat5_min):
					lat5_min = lat5
				if (lat1 > lat1_max):
					lat1_max = lat1
				if (lat2 > lat2_max):
					lat2_max = lat2
				if (lat3 > lat3_max):
					lat3_max = lat3
				if (lat5 > lat5_max):
					lat5_max = lat5
				lat1_avg = lat1_avg + lat1
				lat2_avg = lat2_avg + lat2
				lat3_avg = lat3_avg + lat3
				lat5_avg = lat5_avg + lat5

	lat1_avg = lat1_avg / count
	lat2_avg = lat2_avg / count
	lat3_avg = lat3_avg / count
	lat5_avg = lat5_avg / count
	lat1_min = float(int(lat1_min*10000))/10.0
	lat2_min = float(int(lat2_min*10000))/10.0
	lat3_min = float(int(lat3_min*10000))/10.0
	lat5_min = float(int(lat5_min*10000))/10.0
	lat1_avg = float(int(lat1_avg*10000))/10.0
	lat2_avg = float(int(lat2_avg*10000))/10.0
	lat3_avg = float(int(lat3_avg*10000))/10.0
	lat5_avg = float(int(lat5_avg*10000))/10.0
	lat1_max = float(int(lat1_max*10000))/10.0
	lat2_max = float(int(lat2_max*10000))/10.0
	lat3_max = float(int(lat3_max*10000))/10.0
	lat5_max = float(int(lat5_max*10000))/10.0
	#print(str(count)+" good values")	
	print(str(index)+","+str(lat1_min)+","+str(lat1_avg)+","+str(lat1_max)+","+str(lat2_min)+","+str(lat2_avg)+","+str(lat2_max)+","+str(lat3_min)+","+str(lat3_avg)+","+str(lat3_max)+","+str(lat5_min)+","+str(lat5_avg)+","+str(lat5_max)+","+str(stage2_miss)+","+str(stage3_miss)+","+str(stage5_miss)+","+str(count))

files = os.listdir(sys.argv[1])
#print(files)
time_index = 0
print("delay,lat1_min,lat1_avg,lat1_max,lat2_min,lat2_avg,lat2_max,lat3_min,lat3_avg,lat3_max,lat5_min,lat5_avg,lat5_max,s2_mis,s3_mis,s4_mis,count")
while (time_index < 100):
	dataset = getDataSet(files, time_index)
	if (len(dataset) > 0):
		processSet(dataset,time_index)
		#print(dataset)
	time_index = time_index+1


