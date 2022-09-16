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
groundTruth = []


# Load groundTruth
with open(groundTruthFilePath) as f:
	reader = csv.reader(f, delimiter=" ")
	next(reader)
	labeled_data = list(reader)
	sys.stderr.write("[+] Loaded {} ground truth samples\n".format(len(labeled_data)))
	
	for line in labeled_data:
		data = [ float(h) for h in line]
		#print(data)
		groundTruth.append(data)


# X Y Z 16_hackel_feautres
points = []
features = []


# Load hackel file
with open(hackelFilePath) as f:
	reader = csv.reader(f, delimiter=",")
	hackel_data = list(reader)
	sys.stderr.write("[+] Loaded {} training samples\n".format(len(hackel_data)))
	
	for line in hackel_data:
		data = [ float(h) for h in line ]
		points.append(data[:3])
		features.append(data[3:])
		#print(data[:3], data[3:])
		

kdTree = sp.KDTree(groundTruth)
#trainingData = kdTree.query_ball_point(points[:2], r = radius)
#trainingData = trainingData.nonzero()[0]

#test = [75802, 5067873] # 75802.50288244258 5067873.774412379
#trainingData = kdTree.query_ball_point(test, r = radius)

#print(trainingData)
