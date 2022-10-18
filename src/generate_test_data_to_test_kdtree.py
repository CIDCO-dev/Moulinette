import sys, csv
import numpy as np
import scipy.spatial as sp
from sklearn import mixture

if len(sys.argv) != 2:
	sys.stderr.write("Usage: python3 generate_test_data_to_test_kdtree.py groundTruth.csv \n")
	sys.exit(1)
	

groundTruthFilePath = sys.argv[1]

# X Y nb_Moules
groundTruthCoordinates = []
groundTruthMussels = []

# Load groundTruth
with open(groundTruthFilePath) as f:
	reader = csv.reader(f, delimiter=" ")
	#next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} ground truth samples\n".format(len(labeled_data)))
	
	for line in labeled_data:
		data = [ float(h) for h in line]
		groundTruthCoordinates.append([data[0], data[1]])
		groundTruthMussels.append(data[2])

groundTruthCoordinates = sorted(groundTruthCoordinates, key=lambda k: [k[0], k[1]])

for i in range(len(groundTruthCoordinates)):
	if i % 100 == 0:
		sys.stdout.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(groundTruthCoordinates[i][0]+1, groundTruthCoordinates[i][1]+1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))



