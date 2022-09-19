import sys, csv
import numpy as np
import scipy.spatial as sp

if len(sys.argv) != 4:
	sys.stderr.write("Usage: python generate_trainning_data.py groundTruth.csv hackelFilePath.hackel radius \n")
	sys.exit(1)
	

groundTruthFilePath = sys.argv[1]
hackelFilePath = sys.argv[2]
radius = int(sys.argv[3])
#csvDelimiter = sys.arv[4]

# X Y nb_Moules
groundTruthCoordinates = []
groundTruthMussels = []

# Load groundTruth
with open(groundTruthFilePath) as f:
	reader = csv.reader(f, delimiter=";")
	next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} ground truth samples\n".format(len(labeled_data)))
	
	for line in labeled_data:
		data = [ float(h) for h in line]
		#print(data[:2], data[2])
		groundTruthCoordinates.append(data[:2])
		groundTruthMussels.append(data[2])



# X Y Z 16_hackel_feautres
xyPoints = []
depth = []
features = []


# Load hackel file
with open(hackelFilePath) as f:
	reader = csv.reader(f, delimiter=",")
	hackel_data = list(reader)
	sys.stderr.write("[+] Loaded {} training samples\n".format(len(hackel_data)))
	
	for line in hackel_data:
		data = [ float(h) for h in line ]
		xyPoints.append(data[:2])
		depth.append(data[2])
		features.append(data[3:])
		#print(data[:2], data[2])
		#print(data[3:])
		

kdTree = sp.KDTree(groundTruthCoordinates)

"""
testPoint = groundTruthCoordinates[0]
testPoint = [testPoint[0]+1, testPoint[1]+1]
test = kdTree.query_ball_point(testPoint, r = 1)
print(groundTruthCoordinates[0], groundTruthCoordinates[test[0]])
"""

for mbesPointID in range(len(xyPoints)):
	indexes = kdTree.query_ball_point(xyPoints[mbesPointID], r = radius)
	if len(indexes[mbesPointID]) >= 1:
		for i in indexes:
			sys.stdout.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
				xyPoints[mbesPointID][0], xyPoints[mbesPointID][1], depth[mbesPointID], features[mbesPointID][0],
				features[mbesPointID][1],features[mbesPointID][2],features[mbesPointID][3],features[mbesPointID][4],
				features[mbesPointID][5],features[mbesPointID][6],features[mbesPointID][7],features[mbesPointID][8],
				features[mbesPointID][9],features[mbesPointID][10],features[mbesPointID][11],features[mbesPointID][12],
				features[mbesPointID][13],features[mbesPointID][14],features[mbesPointID][15],features[mbesPointID][16],
				groundTruthMussels[i]
			))
	else:
		continue;

		
		
