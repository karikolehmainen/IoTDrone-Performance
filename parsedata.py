
import os
import sys


def getDataSet(files, indx):
	dataset = []
	indxstr = str(indx)+"ms"
	for file in files:
		file_str = file.split(".")[0]
		#print(file_str)
		params = file_str.split("-")
		if (indxstr == params[2]):
			dataset.append(file)

	return dataset	

def processSet(set,index):
	for file_str in set:
		if (file_str.split("-")[1] == "broker"):
			bkr = open(sys.argv[1]+"/"+file_str, "r")
			bkr_lines = lines = bkr.readlines()
		if (file_str.split("-")[1] == "pub"):
			pub = open(sys.argv[1]+"/"+file_str, "r")
			pub_lines = lines = pub.readlines()
		if (file_str.split("-")[1] == "sub"):
			sub = open(sys.argv[1]+"/"+file_str, "r")
			sub_lines = lines = sub.readlines()
	TS1 = 0.0
	TS2 = 0.0
	TS6 = 0.0
	lat1_min = 100.0
	lat1_max = 0.0
	lat1_avg = 0.0
	lat5_min = 100.0
	lat5_max = 0.0
	lat5_avg = 0.0
	count = 0
	for line in pub_lines:
		elements = line.split(":")
		TS1 = 0.0
		TS2 = 0.0
		TS6 = 0.0
		brk_nfound = True
		sub_nfound = True
		if (len(elements) == 3):
			#count = count + 1
			TS1 = float(elements[2])
			topic = elements[1]
			#print("TS1:"+str(TS1))
			linec = 0
			#print(line)
			bkrline = ""
			for bkrline in bkr_lines:
				bkrset = bkrline.split(",")
				#bkrset = bkrline.split(" ")[1].split(",")
				#print(bkrline)
				linec = linec + 1
				if (len(bkrset) == 3 and bkrset[1] == "TS2"):
					TS2=float(bkrset[2])
					if (bkrset[0] == topic and TS2 > TS1):
						brk_nfound = False
						#print("found brk on line: "+str(linec)+" : "+bkrline)
						break

			if (brk_nfound):
				print("Broker entry not found")
			#print("TS2:"+str(TS2))
			linec = 0
			subline = ""
			for subline in sub_lines:
				sub_set=subline.split(":")
				#print(sub_set)
				linec = linec + 1
				if (len(sub_set) == 3):
					TS6=float(sub_set[2])
					if (sub_set[1] == topic and TS6 > TS1):
						#print(sub_set[1]+":"+topic+":"+str(TS1)+":"+str(TS6))
						sub_nfound = False
						#print("found sub on line: "+str(linec)+" : "+subline)
						break
			if (sub_nfound):
				print("Subscriber entry not found")
			#print("TS6:"+str(TS6))
			if(TS1<TS2<TS6):
				count = count + 1
				if ((TS2-TS1) < lat1_min):
					lat1_min = TS2 - TS1
				if ((TS6-TS1) < lat5_min):
					lat5_min = TS6 - TS1
				if ((TS2-TS1) > lat1_max):
					lat1_max = TS2 - TS1
				if ((TS6-TS1) > lat5_max):
					lat5_max = TS6 - TS1
				lat1_avg = lat1_avg + (TS2-TS1)
				lat5_avg = lat5_avg + (TS6-TS1)
			else:
				#print("Error in timestamps: TS1="+str(TS1)+" TS2="+str(TS2)+" TS6="+str(TS6))
				print("Error in timestamps:")
				print("\t"+line.strip())
				print("\t"+bkrline.strip())
				print("\t"+subline.strip())
	lat1_avg  = lat1_avg / count
	lat5_avg  = lat5_avg / count
	print(str(count)+" good values")	
	print(str(index)+","+str(lat1_min)+","+str(lat1_avg)+","+str(lat1_max)+","+str(lat5_min)+","+str(lat5_avg)+","+str(lat5_max))

files = os.listdir(sys.argv[1])
#print(files)
time_index = 0
print("delay,lat1_min,lat1_avg,lat1_max,lat5_min,lat5_avg,lat5_max")
while (time_index < 100):
	dataset = getDataSet(files, time_index)
	if (len(dataset) > 0):
		processSet(dataset,time_index)
		#print(dataset)
	time_index = time_index+1


