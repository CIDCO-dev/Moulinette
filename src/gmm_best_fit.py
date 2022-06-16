# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np

import sys
import matplotlib.pyplot as plt

from sklearn import mixture

if len(sys.argv) != 3:
	sys.stderr.write("Usage: gmm-best-fit.py equalized-training-data.txt nb-max-class \n")
	sys.exit(1)

trainingFile = sys.argv[1]
maxClusters = int(sys.argv[2])

features = []
points = []


reader = pd.read_csv(trainingFile,delimiter = '\s+',header = 0)
#print(len(reader))
#print(reader.head())
features = reader[["H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12","H13","H14"]]
points = reader[["X","Y","Z"]]
#print(features.head())


sys.stderr.write("[+] Loaded {} training samples\n".format(len(reader)))	
#features = np.array(features)
bic = []
lowest_bic = np.infty

sys.stderr.write("[+] Finding optimal parameters...\n")
n = 1
while n < maxClusters :
    s = "progress: " + str(n) + "/" + str(maxClusters)
    sys.stderr.write(s+"\n")
    sys.stderr.write("calcul du model\n")
    model = mixture.GaussianMixture(n, covariance_type = "full")
    sys.stderr.write("model calculé\n")
    n += 1
    model.fit(features)
    performance = model.bic(features)
    bic.append(performance)
    if performance < lowest_bic:
    	lowest_bic = performance
    	best_model = model
    else:
    	break;


bestFit = 1 + bic.index(min(bic))
sys.stderr.write("best fit: " + str(bestFit) + "\n")

predictions = model.predict(features)
sys.stderr.write("taille features: " + str(len(features)) + "\n")

reader["GMM_Class"] = predictions

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width',None):  # more options can be specified also
   print(reader.to_string(index=False))
   

# for i in range(len(features)):
#    #sys.stderr.write("features= " + str(features[i]) + "\n")
#    #hackel = ' '.join([str(param) for param in features[i]])
#    xyz = points[i]
#    klass = predictions[i]
#    print(str(xyz[0]),str(xyz[1]),str(xyz[2]), klass)
#    #sys.stderr.write(str(xyz[0]),str(xyz[1]),str(xyz[2]), klass)
   
# y = np.arange(1, len(bic)+1)
# x = np.array(bic)
# plt.gca().invert_yaxis()
# plt.gca().invert_xaxis()
# plt.plot(x,y)
# plt.xlabel("best fit")
# plt.xlabel("N clusters")
# plt.ylabel("BIC")
# plt.savefig('GMM.png',format = 'png',dpi = 300)

