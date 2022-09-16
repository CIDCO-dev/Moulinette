#!/bin/bash

DIR=$1

# echo $folder

for FILE in $(ls $DIR)
do
	FILENAME=${FILE/".txt"/".hackel"}
	cat $DIR/$FILE | ./projets/BenthicClassifier/build/soundings_generate_features 10 >> hackel/$FILENAME
done


for FILE in $(ls hackel)
do
	FILENAME=${FILE/".hackel"/".xyzC"}
	python3 projets/Moulinette/src/gmm_best_fit.py 'hackel/'$FILE 5 >> xyzC_files/$FILENAME
done
