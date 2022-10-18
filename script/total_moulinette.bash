#!/bin/bash

echo 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18 > total.hackel

for FILE in $(ls hackel)
do
	cat hackel/$FILE | sed 1d >> total.hackel
	
done

python3 projets/Moulinette/src/gmm_best_fit.py total.hackel 5 >> total.xyzC
