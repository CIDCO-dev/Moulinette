# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:25:54 2022

@author: Hydrograhe
"""

import cv2
import sys


if len(sys.argv) != 4:
	sys.stderr.write("Usage: mask.py image  mask   image_save_directory\n")
	sys.exit(1)


imageFile = sys.argv[1]
maskFile = sys.argv[2]
save_directory = sys.argv[3]


if sys.platform == "linux2":
    file_name = imageFile.split("/")[-1]
    file_name = file_name.split('.')[0]
    
else:
    file_name = imageFile.split("\\")[-1]
    file_name = file_name.split('.')[0]

Output = save_directory + file_name + "_masked.tif"


img = cv2.imread(imageFile,0)
mask = cv2.imread('mask.png',0)
res = cv2.bitwise_and(img,img,mask = mask)

cv2.imwrite(Output, res)