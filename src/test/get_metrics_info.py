# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 15:42:44 2022

@author: Hydrograhe
"""
import sys
import os



def get_tree_structure(foldername,dic = {}):    
    
    file_list = os.listdir(foldername)
    file_list = [os.path.join(foldername, file) for file in file_list]
    
    for file in file_list:

        if os.path.isfile(file):
            dic[file] = file
        else:  
            dic.update(get_tree_structure(file,dic))
           
    return dic  
################################################################################
# Main                                                                         #
################################################################################

if __name__ == "__main__":
    
    dic = {}
        
    if len(sys.argv) != 2:
     	sys.stderr.write("Usage: train_model.py Metrics_data_folder  \n")
     	sys.exit(1)
    
    foldername = sys.argv[1]
    
    
    
    
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
        
        
        # sys.stderr.write("Loading file : {} \n".format(file_name))
        # sys.stderr.write("Loading from folder : {} \n".format(folder_name))
        
        with open('{}'.format(file),'r') as f:
            line = f.readline()
            accuracy = line.split(' ')[-1]
            accuracy = accuracy.split('\n')[0]
            
            dic[file] = float(accuracy)
            

max_key = max(dic, key=dic.get)
print("\n Maximum accuracy: {} in file {} \n".format(dic[max_key],max_key))

