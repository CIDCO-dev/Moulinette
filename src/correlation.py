# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:41:29 2022

@author: Hydrograhe
"""

import sys
import pandas as pd
import numpy as np
import scipy.spatial as sp
import csv


if len(sys.argv) != 4:
	sys.stderr.write("Usage: correlation.py classifiedPoints.xyzC moule_nad.csv radius \n")
	sys.exit(1)
	
classifiedPoints = sys.argv[1]
musselsPoints = sys.argv[2]
radius = sys.argv[3]

#classList = []
# xyz = []

# with open(classifiedPoints) as f:
# 	reader = csv.reader(f, delimiter=' ')
# 	#next(reader)
# 	data = list(reader)
# 	for x in data:
# 		classList.append(int(x[3]))
# 		xyz.append([float(x[0]),float(x[1])])
# 		
# 	sys.stderr.write("[+] Loaded {} classified points\n".format(len(xyz)))
    
df_1 = pd.read_csv(classifiedPoints, delimiter = '\s+', header = 0, names=('X','Y','Z','GMM_Class'),usecols = ('X','Y','GMM_Class'),dtype= {'GMM_Class':np.uint8})
xyz = df_1['X','Y']
classList = df_1['GMM_Class']
sys.stderr.write("[+] Loaded {} classified points\n".format(len(xyz)))


# musselsPoint = []
# musselsQuantity = []
# with open(musselsPoints) as f:
# 	reader = csv.reader(f, delimiter=';')
# 	next(reader)
# 	musselsData = list(reader)
# 	for x in musselsData:
# 		musselsQuantity.append(int(x[2]))
# 		musselsPoint.append([float(x[0]),float(x[1])])
# 	sys.stderr.write("[+] Loaded {} classified points\n".format(len(musselsPoints)))


df_2 = pd.read_csv(musselsPoints, delimiter = ',', header = 0,usecols=('X','Y','Total'),dtype= {'Total':np.uint16})
musselsPoint = df_2['X','Y']
musselsQuantity = df_2['Total']
sys.stderr.write("[+] Loaded {} classified points\n".format(len(xyz)))


kdtree = sp.KDTree(xyz)
points = kdtree.query_ball_point(musselsPoint, radius)
mussels_in_classified_mbes = points.nonzero()[0]

print(mussels_in_classified_mbes)