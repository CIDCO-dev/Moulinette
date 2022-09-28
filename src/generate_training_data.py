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
	reader = csv.reader(f, delimiter=",")
	next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} ground truth samples\n".format(len(labeled_data)))
	
	for line in labeled_data:
		data = [ float(h) for h in line]
		groundTruthCoordinates.append([data[1], data[0]])
		groundTruthMussels.append(data[2])



# X Y Z 16_hackel_feautres
hackelXY = []
depth = []
features = []


# Load hackel file
with open(hackelFilePath) as f:
	reader = csv.reader(f, delimiter=" ")
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
			features[hackelPointID].append(groundTruthMussels[i])
			trainData.append(features[hackelPointID])
	else:
		continue;
#print(trainData)
model = mixture.GaussianMixture(5, covariance_type = "full") 
model.fit(trainData)
predictions = model.predict(trainData)

if len(predictions) == len(trainData):
	sys.stderr.write("ok")
else:
	sys.stderr.write("predictions : {} != trainData : {}".format(len(predictions), len(trainData)))
	sys.exit(1)

for i in range(len(predictions)):
	sys.stdout.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
				hackelXY[i][0],hackelXY[i][1], depth[i], trainData[i][0],
				trainData[i][1],trainData[i][2],trainData[i][3],trainData[i][4],
				trainData[i][5],trainData[i][6],trainData[i][7],trainData[i][8],
				trainData[i][9],trainData[i][10],trainData[i][11],trainData[i][12],
				trainData[i][13],trainData[i][14],trainData[i][15],trainData[i][16],predictions[i]))
				


