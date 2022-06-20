#!/bin/bash

for FILE in $(ls hackel)
do
	FILENAME=${FILE/".hackel"/".xyzC"}
	python3 projets/Moulinette/src/gmm_best_fit.py 'hackel/'$FILE 5 >> xyzC_files/$FILENAME
done
