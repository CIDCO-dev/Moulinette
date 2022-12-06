import os
import sys
import csv
import numpy as np
import pickle


if len(sys.argv) != 3:
	sys.stderr.write("Usage: apply-model.py model-file dataFile\n")
	sys.exit(1)


modelFilename = os.fsencode(sys.argv[1])
dataFilename = os.fsencode(sys.argv[2])
model = pickle.load(open(modelFilename,"rb"))

#Load training data
if model:
	with open(dataFilename,"r") as dataFile:
		reader = csv.reader(dataFile, delimiter=" ")
		#next(reader)
		data = list(reader)
		sys.stderr.write("[+] Loaded {} soundings\n".format(len(data)))

		features = [x[3:] for x in data]

		predictions = model.predict(features);

		for i in range(0,len(predictions)):
			sys.stdout.write("{} {} {} {}\n".format(data[i][0],data[i][1],data[i][2],round(predictions[i])))

else:
	sys.stderr.write("Couldn't load model\n")

