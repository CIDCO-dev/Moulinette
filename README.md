
# Prep data
### remove useless columns, sort by date, remove date column, keep uniq rows only
```
cut -d ";" -f 1,2,3,5 data/mussels/merge_of_raw_data.csv | sort -t";" -k4 -r | cut -d ";" -f 1-3 | sort -k1,1 -k2,2 --unique > mussels_epsg-4326.csv

```
### visualize that first 4 lines are not valid -> look at the date
```
cut -d ";" -f 1,2,3,5 data/mussels/merge_of_raw_data.csv | sort -t";" -k4 -r | less
```

### delete first 4 lines
```
sed -i '1,4d' mussels_epsg-4326.csv
```



# Generate Trainning data

### keep MBES points near mussels data
```
python3 src/generate_trainning_data.py data/mussels/mussels_epsg-32187.csv data/test/cap-sample.hackel
```




