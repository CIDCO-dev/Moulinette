import os
import sys
import csv
import numpy as np
import pickle


if len(sys.argv) != 3:
	sys.stderr.write("Usage: apply-gmm-model.py model-file hackelDataFile\n")
	#sys.stderr.write("{}\n".format(sys.argv))
	sys.exit(1)


modelFilename = os.fsencode(sys.argv[1])
dataFilename = os.fsencode(sys.argv[2])
model = pickle.load(open(modelFilename,"rb"))

features = []
classes = []
data = []

#Load training data
if model:
	with open(dataFilename,"r") as dataFile:
		reader = csv.reader(dataFile, delimiter=",")
		next(reader)
		data = list(reader)
		sys.stderr.write("[+] Loaded {} soundings\n".format(len(data)))
		
		#print(data)
		
		for line in data:
			y = [float(x) for x in line[3:]]
			features.append(y)
		
		classes = model.predict(features);

else:
	sys.stderr.write("Couldn't load model\n")
	sys.exit(1)


for i in range(0,len(classes)):
	sys.stdout.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],data[i][7],data[i][8],data[i][9],data[i][10],data[i][11],data[i][12],data[i][13],data[i][14],data[i][15],data[i][16],data[i][17],data[i][18], classes[i]))





