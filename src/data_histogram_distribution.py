import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

"""
training data format:
x, y, z, nb_moule, 16 hackel features, gmm class

"""
if len(sys.argv) != 2:
	sys.stderr.write("Usage: data_histogram_distribution.py training-data.csv\n")
	sys.exit(1)

trainingFile = sys.argv[1]

nb_mussel_at_xyz = []

#Load training data
with open(trainingFile) as f:
	reader = csv.reader(f)
	next(reader)
	data = list(reader)
	for x in data:
		nb_mussel_at_xyz.append(int(x[4]))
	sys.stderr.write("[+] Loaded {} training samples\n".format(len(nb_mussel_at_xyz)))

nb_mussel_at_xyz.sort()
print(nb_mussel_at_xyz)

n, bins, patches = plt.hist(x=nb_mussel_at_xyz, bins='auto', color='#0504aa', rwidth=2)
plt.grid(axis='y', alpha=1)
plt.xlabel('nb mussel')
plt.ylabel('Frequency')
plt.title('training data distribution')
#plt.text(23, 45, r'$\mu=15, b=3$')
#maxfreq = n.max()
# Set a clean upper y-axis limit.
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.show()

