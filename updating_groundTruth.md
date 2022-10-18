# Adding new ground truth to previous file
## instruction
### 1) format data with unique : lon lat nb_mussel
### 2) append old data to new
```
cp new_data.txt new_data.bak
cat old_data.txt > new_data.txt
```

### 3) keep unique data between new and old
```
cut -d ";" -f 1-3 new_data.csv | sort -k1,1 -k2,2 --unique > updated_mussels_epsg-4326.csv
```
