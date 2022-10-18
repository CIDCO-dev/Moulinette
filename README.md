# Moulinette
Mussel prediction from MBES point cloud
## 1) Prep ground truth data
### Remove useless columns, sort by date
consider epsg 8254 to be equal to epsg 4326
```
cut -d ";" -f 1,2,3,5 data/mussels/merge_of_raw_data.csv | sort -t";" -k4 -r > mussels_sorted_by_date_epsg-8254.csv
```
### Visualize that first 4 lines are not valid -> look at the date
```
cat mussels_sorted_by_date_epsg-8254.csv | sort -t";" -k4 -r | less
```

### Delete first 4 lines
```
sed -i '1,4d' mussels_sorted_by_date_epsg-8254.csv
```

### Keep latest unique data points
```
cut -d ";" -f 1-3 mussels_sorted_by_date_epsg-8254.csv | sort -k1,1 -k2,2 --unique > mussels_epsg-8254.csv
```

## 2) Prep MBES data
### Convert MBES dms to decimal
```
python3 src/dms_to_dec.py data/test/cap-sample-epsg8254-dms.txt > data/test/cap-sample-epsg8254-decimal.txt
```

## 3) Put MBES and ground truth data in same reference system -> ENU
### Compile 
```
cd MBES-lib
mkdir build && cd build
cmake ..
make wgs2lgf
```
```
g++ -I /usr/include/eigen3 src/wgs2lgf_from_lat_lon_eh.cpp -o wgs2lgf_from_lat_lon_eh
```

keep centroid values somewhere
```
cat Cap-Rouge_to_Lac-St-Pierre_epsg-8254-decimal.txt | ./MBES-lib/build/wgs2lgf enu > Cap-Rouge_to_Lac-St-Pierre_enu.txt
```
lat lon Z centroid :  46.527207203821909332 -72.066496911800527414 12.819235715989787394
```
cat mussels_epsg-8254.txt | ./wgs2lgf_from_lat_lon_groundruth enu centroid_Lat centroid_Lon centroid_ellipsoidal_height > mussels_enu.txt
```

### Generate hackel features
```
cat ~/Cap-Rouge_to_Lac-St-Pierre_enu.txt | ./soundings_generate_features 10 > ~/Cap-Rouge_to_Lac-St-Pierre_enu.hackel
```

### Unsupervised MBES classification
```
python3 gmm_best_fit.py ~/Cap-Rouge_to_Lac-St-Pierre_enu.hackel 6 > Cap-Rouge_to_Lac-St-Pierre_enu_gmm_hackel.txt
```

## 4) Generate Trainning data

output xyz hackel_features gmmClass musselGroundTruth
```
python3 generate_training_data.py ../data/mussels/mussels_enu_more_precision_centroid.txt ~/Cap-Rouge_to_Lac-St-Pierre_enu_hackel_gmm.txt 10  > ~/training_data.txt
```

## 5) Optimize model parameter and train
all cpu core will be use for parameter optimisation
```
python3 train_model.py training_data.txt
```

## 6) Apply model
```
python3 apply_model.py trained_mussel_regression.model FILE > ~/result.xyzc
```

## 7) Rasterize result
### Compile utility
```
g++ -I /usr/include/eigen3 lgf2wgs.cpp -o lgf2wgs
```

### convert coordinates back to WGS
```
cat ~/result.xyzc | ./lgf2wgs enu 46.527207203821909332 -72.066496911800527414 12.819235715989787394 > ~/lat_lon_eh_Class.csv
```

### get min max xy to change raster resolution
```
python3 find_min_max_coordinates.py ~/lat_lon_eh_Class.csv
```

### Export result as geotiff
```
bash script/rasterize.bash ~/lat_lon_eh_Class.csv ~/rasters 4326
```
or run a similar command like this
```
gdal_grid -zfield "field_3" -a_srs EPSG:4326 -a invdist -ot Float64 -l lat_lon_eh_Class script/lat_lon_eh_Class.vrt ~/raster_reso_1/mussel_resolution_1.tiff --config GDAL_NUM_THREADS ALL_CPUS -txe -72.6806747039285 -71.41272166174498 -tye 46.26391417288448 46.71285611583465 -tr 0.00001 0.00001
```
