# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 19:26:25 2022

@author: oscar
"""

import os
import sys


def get_tree_structure(foldername,dic):
    
    
    file_list = os.listdir(foldername)
    file_list = [os.path.join(foldername, file) for file in file_list]

    
    for file in file_list:

        if os.path.isfile(file):
            dic[file] = file
        else:
            
            dic.update(get_tree_structure(file,dic))
            
    return dic  


# def get_tree_structure_list(foldername,liste):
    
#     file_list = os.listdir(foldername)
#     file_list = [os.path.join(foldername, file) for file in file_list]

#     for file in file_list:
        
#         if os.path.isfile(file):
#             liste = liste + [file]
            
#         else:     
#             liste = liste + get_tree_structure_list(file,liste)
                
#     return liste    




foldername = "C:\\Users\\oscar\\Documents\\GitHub\\Moulinette\\data\\mussels"
tree_structure = list(get_tree_structure(foldername,{}).keys())



if os.path.exists(foldername):
    tree_structure =  list(get_tree_structure(foldername).keys())
        
else :
    sys.stderr.write("The entry data does not exist\n") 

    
for file in tree_structure :
    #sys.stderr.write("{}\n".format(os.path.abspath(file)))
    
    if sys.platform == "linux2":
        file_name = file.split("/")[-1]
        
    else:
        file_name = file.split("\\")[-1]

    folder_name = file.replace(file_name,"")
    file_name = file_name.split('.')[0]