import sys, csv
import numpy as np


if len(sys.argv) != 2:
	sys.stderr.write("Usage: python3 find_min_max_coordinates.py generate_training_data_output_file \n")
	sys.exit(1)
	
inputFilePath = sys.argv[1]

lat = []
lon = []

# Load file
with open(inputFilePath) as f:
	reader = csv.reader(f, delimiter=",")
	#next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} ground truth samples\n".format(len(labeled_data)))
	
	for line in labeled_data:
		data = [ float(h) for h in line]
		lat.append(data[0])
		lon.append(data[1])
		
minLat = min(lat)
minLon = min(lon)
maxLat = max(lat)
maxLon = max(lon)

sys.stdout.write("minLat = {} minLon = {} maxLat = {} maxLon = {}\n".format(minLat, minLon, maxLat, maxLon))
