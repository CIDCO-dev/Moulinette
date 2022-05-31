# Moulinette
Prédiction des distributions de moules d'eau douce


## Step 1: Selecting the data

The project requires various data:

### MBES data

The multibeam data are stored in the server "indien" at the address "/home/oscar/moules/BenthicClassifier/data/mbes/Combine_secteur_Quebec_no_header.xyz".  
The points are in the SRS "NAD83 / MTM  zone 7".

### Mussels data

Locations of mussels are listed in the 4 excel files in the directory "data/mussels/raw data".  
The merge of those files was done manually and can be found in the file "listing_moules.csv" in the directory "data/mussels/raw data".   
The points are in the SRS "WGS 84" (Lat/Long).  
However, some rows have the same coordinates but different dates and different number of mussels. Those duplicates were treated with the code "mussels_sorting.py".   
Then the coordinates are converted in the SRS "NAD83 / MTM  zone 7" thanks to QGIS.   
The final data are listed in the file "moules_nad.csv" in the directory "data/mussels".  


## Step 2: Pre-processing

### Hackel features

Based on the mbes data, we  generate Hackel features and clean lines with NaN:
```
cat mbes.xyz | soundings_generate_features radius >> outputfile.Hackel
sed -i '/nan/d' "${WORKDIR}/WithFeatures/outputfile.Hackel"
```
With radius = 10m

The Hackel file can be found on the server "indien" at the address "/home/oscar/moules/BenthicClassifier/data/hackel_features/Hackel_Features.Hackel"


### Gaussian Mixture Model (GMM)

From those Hakel Features we make an unsupervised clasification of the mbes points based on the GMM algorithm. 
```
python src/gmm_best_fit.py Hackel_Features.Hackel nb-max-class  >> GMM.txt
```
With nb-max-class = 5

The GMM file an be found on the server "indien" at the address "/home/oscar/moules/BenthicClassifier/data/GMM/GMM.txt"

### Nearest neighbor search and selection

Using a kd-tree we select the mbes points within a given radius of the mussels points.  
The points are labeled with the corresponding information (mussels_id + number of mussels).   
If a point is near two mussels, only the nearest is considered.  
It should be noted that in the mussels data, the number of mussels listed at each point, varies from 0 to 269.  

```
python src/plus_proche_voisin.py moules_nad.csv mbes_file_no_header.xyz radius  >> plus_proche_voisin.csv
```
With radius = 3m

he file can be found in "data/plus_proche_voisin.csv"


## Step 3: Merging the data

Using "merge.py" we merge the3 files genereted in the step 2.
```
python src/merge.py plus_proche_voisin.csv GMM.txt hackel.Hackel  >> trained_data.csv
```

The file can be found in "data/trained_data.csv"

