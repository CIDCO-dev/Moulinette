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
	next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} ground truth samples\n".format(len(labeled_data)))
	
	for line in labeled_data:
		data = [ float(h) for h in line]
		groundTruthCoordinates.append([data[0], data[1]])
		groundTruthMussels.append(data[2])


for i in range(len(groundTruthCoordinates)):
	sys.stdout.write("{} {} {}\n".format(groundTruthCoordinates[i][0]+9, groundTruthCoordinates[i][1]+9, groundTruthMussels[i]))



