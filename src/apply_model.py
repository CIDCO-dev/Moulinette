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
		print("[+] Loaded {} soundings".format(len(data)))

		features = [x[:-1] for x in data]

		classes = model.predict(features);

		for i in range(0,len(classes)):
			print("{},{},{},{}".format(data[i][0],data[i][1],data[i][2],classes[i]))

else:
	sys.stderr.write("Couldn't load model\n")

