# Moulinette
Mussel prediction from MBES point cloud
## Prep data
### remove useless columns, sort by date, remove date column, keep uniq points only
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


## Generate Trainning data

### keep MBES points near mussels data
```
python3 src/generate_trainning_data.py data/mussels/mussels_epsg-32187.csv data/test/cap-sample.hackel
```




