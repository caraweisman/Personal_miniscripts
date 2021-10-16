##input: header from jackhmmmer output file containing the sequence ID information in a terrible format, WITH LEADING POUND SIGNS REMOVED
## (This is so that numpy can read the file .can do this with some awk command? cut? -c? can't remember.)
## output: list of sequences info in slightly cleaner format
import numpy as np 
import re
import sys

infile = sys.argv[1]


infiledata = np.genfromtxt(infile, dtype=str, delimiter='\t') 

for i in range(0, len(infiledata)): 
	currline = infiledata[i]
	tax = re.split('\[', currline)[-1][:-1]
	genus = re.split(' ', tax)[0][0]
	species = re.split(' ', tax)[1][0:3]
	abbrevtax = genus + '.' + species

	name = re.split('\[',re.split('\[subseq from\]', currline)[1])[0]
	coords = re.split('/', re.split(' ', currline)[1])[1]

	final = name + '(' + coords + ') ' + abbrevtax
	print final
