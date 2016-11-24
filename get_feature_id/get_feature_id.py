#!/usr/bin/python

import csv

columns = []
features =[]
res = []

with open("features.txt") as f:
	# reader = csv.reader(f, delimiter="\n")
	# features = list(reader)
	for line in f:
		features.append(line.replace('\n', '').replace('.', '[', 1).replace('.', ']', 1))

with open("columns.txt") as f:
	reader = csv.reader(f, delimiter="\t")
	columns = list(reader)

columns = columns[0]

print columns
print features
print len(columns)
print len(features)

for j in features:
	for i in [i for i,x in enumerate(columns) if x == j]:
		res.append(i)

print "column id of the winner's featureres: ", res