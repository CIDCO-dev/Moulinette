# Moulinette
Mussel prediction from MBES point cloud
## 1) Prep ground truth data
### Remove useless columns, sort by date
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

## 2) Train regression model
```
python3 src/train_model.py data/train_data/training_data.txt
```
## 3) Generate hackel file
### Mbes file must be in a projected or orthogonal reference system on a 1*1 M grid
### The utility soundings_generate_features is from Benthinc_classifier : https://github.com/CIDCO-dev/BenthicClassifier
```
cat MBES_FILE.txt | ./soundings_generate_features 10 > outputFilePath.hackel
```

## 6) Apply model
```
python3 apply_model.py trained_mussel_regression.model FILE.hackel > outputFilePath_result.csv
```
