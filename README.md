# Moulinette
Mussel prediction from MBES point cloud
## Prep ground truth data
### remove useless columns, sort by date
```
cut -d ";" -f 1,2,3,5 data/mussels/merge_of_raw_data.csv | sort -t";" -k4 -r > mussels_sorted_by_date_epsg-4326.csv
```
### visualize that first 4 lines are not valid -> look at the date
```
cat mussels_sorted_by_date_epsg-4326.csv | sort -t";" -k4 -r | less
```

### delete first 4 lines
```
sed -i '1,4d' mussels_sorted_by_date_epsg-4326.csv
```

### keep latest unique data points
```
cut -d ";" -f 1-3 mussels_sorted_by_date_epsg-4326.csv | sort -k1,1 -k2,2 --unique > mussels_epsg-4326.csv
```

## prep MBES data
### convert MBES dms to decimal
```
python3 src/dms_to_dec.py data/test/cap-sample-epsg8254-dms.txt > data/test/cap-sample-epsg8254-decimal.txt
```

### put MBES and ground truth data in same reference system -> ENU
```
cat Cap-Rouge_to_Lac-St-Pierre_epsg-8254-decimal.txt | ./wgs2lgf enu > Cap-Rouge_to_Lac-St-Pierre_enu.txt
```
lat lon Z centroid :  46.527207203821909332 -72.066496911800527414 12.819235715989787394
```
cat mussels_epsg-8254.txt | ./wgs2lgf_from_lat_lon_eh enu centroid_Lat centroid_Lon centroid_ellipsoidal_height > mussels_enu.txt
```

### generate hackel features
```
cat ~/Cap-Rouge_to_Lac-St-Pierre_enu.txt | ./soundings_generate_features 10 > ~/Cap-Rouge_to_Lac-St-Pierre_enu.hackel
```

### unsupervised MBES classification
```
python3 gmm_best_fit.py ~/Cap-Rouge_to_Lac-St-Pierre_enu.hackel 6
```

## Generate Trainning data

output xyz hackel_features gmmClass musselGroundTruth
```
python3 generate_training_data.py ~/Documents/Cap-Rouge_to_Lac-St-Pierre_enu.hackel ../data/mussels/mussels_enu_more_precision_centroid.txt 10
```




