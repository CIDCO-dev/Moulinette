import sys, csv
import numpy as np
import scipy.spatial as sp
from sklearn import mixture

if len(sys.argv) != 4:
	sys.stderr.write("Usage: python generate_trainning_data.py groundTruth.csv hackelFilePath.hackel radius \n")
	sys.exit(1)
	

groundTruthFilePath = sys.argv[1]
hackelFilePath = sys.argv[2]
radius = int(sys.argv[3])

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
		groundTruthCoordinates.append([data[1], data[0]])
		groundTruthMussels.append(data[2])



# X Y Z 16_hackel_feautres gmmClass
hackelXY = []
depth = []
features = []


# Load hackel file
with open(hackelFilePath) as f:
	reader = csv.reader(f, delimiter=",")
	next(reader)
	hackel_data = list(reader)
	sys.stderr.write("[+] Loaded {} training samples\n".format(len(hackel_data)))
	
	for line in hackel_data:
		data = [ float(h) for h in line ]
		hackelXY.append(data[:2])
		depth.append(data[2])
		features.append(data[3:])
		

kdTree = sp.KDTree(groundTruthCoordinates)

trainData = []
for hackelPointID in range(len(hackelXY)):
	indexes = kdTree.query_ball_point(hackelXY[hackelPointID], r = radius)
	if len(indexes) >= 1:
		for i in indexes:
			sys.stdout.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(hackelXY[hackelPointID][0], hackelXY[hackelPointID][1],
							 depth[hackelPointID], features[hackelPointID][0], features[hackelPointID][1], features[hackelPointID][2], features[hackelPointID][3], 
							 features[hackelPointID][4], features[hackelPointID][5], features[hackelPointID][6], features[hackelPointID][7], 
							 features[hackelPointID][8], features[hackelPointID][9], features[hackelPointID][10], features[hackelPointID][11], 
							 features[hackelPointID][12], features[hackelPointID][13], features[hackelPointID][14], features[hackelPointID][15], 
							 features[hackelPointID][16]
							))
	else:
		continue;
