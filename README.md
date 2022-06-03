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

Based on the mbes data, we generate Hackel features and clean lines with NaN:
```
cat mbes.xyz | soundings_generate_features radius >> outputfile.Hackel
sed -i '/nan/d' "${WORKDIR}/WithFeatures/outputfile.Hackel"
```
With radius = 10m

The Hackel file can be found on the server "indien" at the address "/home/oscar/moules/BenthicClassifier/data/hackel_features/Hackel_Features.Hackel"



### Nearest neighbor search and selection of mbes data

Using a kd-tree we select the mbes points within a given radius of the mussels points.  
The points are labeled with the corresponding information (mussels_id + number of mussels).   
If a point is near two mussels, only the nearest is considered.  
It should be noted that in the mussels data, the number of mussels listed at each point, varies from 0 to 269.  

```
python src/generate_pre_training_data.py moules_nad.csv mbes_file_no_header.xyz radius  >> pre_training_data.txt
```

The file can be found in "data/pre_training_data.txt"


## Step 3: Obtening the dataset.

### Merging the pre-processing data


Using "generate_training_data.py" we merge the files genereted in the step 2.
```
python src/generate_training_data.py pre_training_data.txt hackel.Hackel  >> training_data.txt
```

The file can be found in "data/raining_data.txt"

### Truncation of the training_data

The distribution of the number of mussels being very variable, we need to truncate the over-represented number of mussels.

```
python src/remove_overrepresented.py training_data.txt maximum_frequency_allowed >> valid_training_data.txt
```
In order to determine a suitable maximum_frequency_allowed, you can use the program "histo.py" (see below)

### Visualisation of the distribution

It should be noted that the distribution of the number of mussels and of others parameters can be viewed using the program "histo.py"


```
python src/histo.py training_data.txt 
```

The histograms are saved in the src directory.

