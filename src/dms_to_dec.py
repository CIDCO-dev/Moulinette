import sys

if len(sys.argv) != 2:
		sys.stderr.write("Usage: python dms_to_dec.py inputFilePath \n")
		sys.exit(1)
		
inputFilePath = sys.argv[1]

with open(inputFilePath, 'r') as filein:
	line = filein.readline()
	line = filein.readline()
	while line != '':
		lonLatDepth = line.split(" ")
		lon = lonLatDepth[0].split("-")
		lat = lonLatDepth[1].split("-")
		depth = lonLatDepth[2]
		lonDirection = lon[2][-1]
		latDirection = lat[2][-1]
		lon[2] = lon[2][:-1]
		lat[2] = lat[2][:-1]
		lon = [ float(x) for x in lon]
		lat = [ float(x) for x in lat]
		lonDecimal = lon[0] + lon[1]/60 + lon[2]/3600 
		latDecimal = lat[0] + lat[1]/60 + lat[2]/3600
		sys.stdout.write("{} {} {}".format(-1 * lonDecimal, latDecimal, depth))
		line = filein.readline()
