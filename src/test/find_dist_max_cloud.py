# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 11:38:17 2022

@author: Hydrograhe
"""


import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import time




plt.figure()

file = "C:\\Users\Hydrograhe\Documents\GitHub\Moulinette\data\\ppv_1m.txt"

df = pd.read_csv(file, delimiter = '\s+', header = 0)

start_time = time.time()

length = np.bincount(df['id_moules'])   
id_moule = np.argmax(length)
df = df.loc[df['id_moules'] == id_moule]
if len(df) >= 3:
    points = df[['X','Y']].values
    hull = ConvexHull(points)
    
    # Extract the points forming the hull
    hullpoints = points[hull.vertices,:]
    
    # Naive way of finding the best pair in O(H^2) time if H is number of points on
    # hull
    hdist = cdist(hullpoints, hullpoints, metric='euclidean')
               
    
plt.plot(points[:,0], points[:,1], 'o')
for simplex in hull.simplices:

    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

plt.show()

dist_max = int((np.max(hdist)+1)/2)

print(dist_max)

print("--- %s seconds ---" % (time.time() - start_time))