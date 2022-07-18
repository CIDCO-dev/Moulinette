# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:55:49 2022

@author: Hydrograhe
"""

import numpy as np
import pandas as pd
import sys
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import Affine
from rasterio.crs import CRS

if len(sys.argv) != 3:
	sys.stderr.write("Usage: rasterization.py  csv_file  save_directory\n")
	sys.exit(1)
    
Datafile = sys.argv[1]
save_directory = sys.argv[2]

if sys.platform == "linux2":
    file_name = Datafile.split("/")[-1]
    file_name = file_name.split('.')[0]
    
else:
    file_name = Datafile.split("\\")[-1]
    file_name = file_name.split('.')[0]


#open the chemistry data
#Datafile = "C:\\Users\\Hydrograhe\\Documents\\GitHub\\Moulinette\\data\\Models\\applied\\classification_trained_model_training_data_5m_freq74.csv"
df = pd.read_csv(Datafile,index_col=None,header = 0,nrows = None, names =['X','Y','Z','Classes'])
df = df.dropna() #delete missing data rows

print(df.describe())


#define interpolation inputs
points = list(zip(df.X,df.Y))
values = df.Classes.values
# print(points[:5])
# print(values[:5])


#define raster resolution
rRes = 50

#create coord ranges over the desired raster extension
xRange = np.arange(df.X.min(),df.X.max()+rRes,rRes)
yRange = np.arange(df.Y.min(),df.Y.max()+rRes,rRes)
#print(xRange[:5],yRange[:5])



#create arrays of x,y over the raster extension
gridX,gridY = np.meshgrid(xRange, yRange)

#interpolate over the grid
gridClasses = griddata(points, values, (gridX,gridY), method='nearest')
gridClasses = gridClasses.astype('float64')
print(gridClasses.dtype)  ##

#show interpolated values
#plt.imshow(gridClasses)

#definition of the raster transform array

transform = Affine.translation(gridX[0][0]-rRes/2, gridY[0][0]-rRes/2)*Affine.scale(rRes,rRes)
print(transform)

# #get crs as wkt

rasterCrs = CRS.from_epsg(32187)
# print(rasterCrs.data)
# rasterCrs = CRS.from_proj4("+proj=tmerc +lat_0=0 +lon_0=-70.5 +k=0.9999 +x_0=304800 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs ")
# rasterCrs = CRS.from_wkt("")

#definition, register and close of interpolated raster
interpRaster = rasterio.open('{}{}_rasterise.tif'.format(save_directory,file_name),
                                'w',
                                driver='GTiff',
                                height=gridClasses.shape[0],
                                width=gridClasses.shape[1],
                                count=1,
                                dtype=gridClasses.dtype,
                                crs=rasterCrs,
                                transform=transform,
                                )
interpRaster.write(gridClasses,1)
interpRaster.close()

