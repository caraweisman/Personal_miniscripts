## inputs: 1. file with many fasta sequences; 2. name of one of the sequences
## outputs: Just the named sequence

import numpy as np 
import sys
import re 

infile = np.genfromtxt(sys.argv[1], dtype=str, delimiter='\t')

seqname = sys.argv[2]

count = 0
inseq = False
for i in range(0, len(infile)): 
	if inseq == True and '>' in infile[i]:
		# print count
                inseq = False
		count = 0
	if '>' in infile[i]: 
		#print infile[i]
		#print re.split(' ', infile[i])
		if seqname.lower() == re.split(' ', infile[i])[0][1:].lower(): 
			inseq = True
			print infile[i]
	if inseq == True and '>' not in infile[i]: 
		print infile[i]
		count = count + 1

