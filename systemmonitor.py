import psutil
import time
import signal

stat_time = []
stat_cpu = []
stat_mem = []
stat_dsk = []
stat_net = []

def handler(signum, frame):
	# CPU STATS
	cpus = len(stat_cpu[0])
	count = 0
	header = ""
	while (count < cpus):
		count = count +1
		header = header+"cpu"+str(count)+","
	print(header)
	count = 0
	line = ""
	for stat_smpl in stat_cpu:
		while (count < cpus):
			line = line+str(stat_smpl[count])+","
			count = count +1
		print(line)
		count = 0
		line = ""

	# MEM STATS
	print("total,available,percent,used,free,active,inactive,wired")
	for stat_smpl in stat_mem:
		print(str(stat_smpl.total)+","+str(stat_smpl.available)+","+str(stat_smpl.percent)+","+str(stat_smpl.used)+","+str(stat_smpl.free)+","+str(stat_smpl.active)+","+str(stat_smpl.inactive)+","+str(stat_smpl.wired))

	# DSK STAT
	print("read_count,write_count,read_bytes,write_bytes,read_time,write_time")
	for stat_smpl in stat_dsk:
		print(str(stat_smpl.read_count)+","+str(stat_smpl.write_count)+","+str(stat_smpl.read_bytes)+","+str(stat_smpl.write_bytes)+","+str(stat_smpl.read_time)+","+str(stat_smpl.write_time))

	# NET STAT
	count = 0
	header = ""
	for stat_smpl in stat_net:
		line = ""
		for stat in stat_smpl:
			if (count == 0):
				header = header+stat+"_bytes_sent,"+stat+"_bytes_recv,"+stat+"_packets_sent,"+stat+"_packets_recv,"
			line = line + str(stat_smpl[stat].bytes_sent)+","+str(stat_smpl[stat].bytes_recv)+","+str(stat_smpl[stat].packets_sent)+","+str(stat_smpl[stat].packets_recv)+","
		if (count == 0):
			print(header)
		print(line)
		count = 1

	exit(1)

signal.signal(signal.SIGINT, handler)

while True:
	stat_time.append(time.time())
	stat_cpu.append(psutil.cpu_percent(interval=None, percpu=True))
	stat_mem.append(psutil.virtual_memory())
	stat_dsk.append(psutil.disk_io_counters(perdisk=False, nowrap=True))
	stat_net.append(psutil.net_io_counters(pernic=True, nowrap=True))
	#time.sleep(0.1) # minimum interval for psutils
	time.sleep(0.25) # minimum interval for psutils
