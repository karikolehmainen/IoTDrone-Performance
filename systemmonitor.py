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
	header = "ts,"
	# Determine common number of samples
	samples = len(stat_time)
	if (samples > len(stat_cpu)):
		samples = len(stat_cpu)
	if (samples > len(stat_mem)):
		samples = len(stat_mem)
	if (samples > len(stat_dsk)):
		samples = len(stat_dsk)
	if (samples > len(stat_net)):
		samples = len(stat_net)

	# Make headers
	count = 0
	cpus = len(stat_cpu[0])
	while (count < cpus):
		count = count +1
		header = header+"cpu"+str(count)+","
	header = header + "total,available,percent,used,free,active,inactive,"
	header = header + "read_count,write_count,read_bytes,write_bytes,read_time,write_time"
	for stat in stat_net[0]:
 		header = header+stat+"_bytes_sent,"+stat+"_bytes_recv,"+stat+"_packets_sent,"+stat+"_packets_recv,"

	print(header)
	cntr = 0
	while (cntr < samples):
		line = str(stat_time[cntr])+","
		stat_smpl = stat_cpu[cntr]
		count = 0
		while (count < cpus):
			line = line+str(stat_smpl[count])+","
			count = count +1
		# MEM STATS
		stat_smpl = stat_mem[cntr]
		line = line + str(stat_smpl.total)+","+str(stat_smpl.available)+","+str(stat_smpl.percent)+","+str(stat_smpl.used)+","+str(stat_smpl.free)+","+str(stat_smpl.active)+","+str(stat_smpl.inactive)+","

		# DSK STAT
		stat_smpl = stat_dsk[cntr]
		line = line + str(stat_smpl.read_count)+","+str(stat_smpl.write_count)+","+str(stat_smpl.read_bytes)+","+str(stat_smpl.write_bytes)+","+str(stat_smpl.read_time)+","+str(stat_smpl.write_time)+","
		
		# NET STAT
		stat_smpl = stat_net[cntr]
		for stat in stat_smpl:
			line = line + str(stat_smpl[stat].bytes_sent)+","+str(stat_smpl[stat].bytes_recv)+","+str(stat_smpl[stat].packets_sent)+","+str(stat_smpl[stat].packets_recv)+","

		print(line)
		line = ""
		cntr = cntr+1

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
