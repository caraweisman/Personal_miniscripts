# splits a large fasta file

import numpy as np
import os
import sys
import re 

# parameters

infilename = sys.argv[1]

# seqs per file
nseqs = 100000

# get accession IDs and line numbers

grepcmd = 'grep \> ' + infilename + ' -n > accout'
os.system(grepcmd)

accpositions = np.genfromtxt('accout', dtype=str, delimiter='\n')
print(accpositions)

splitindexes = []
splitstring = ' '
for i in range(0, len(accpositions)): 
	if i % nseqs == 0 and i > 0:
		linenum = re.split(':',accpositions[i])[0]
		splitindexes.append(linenum)
		splitstring = splitstring + linenum + ' '
print(splitstring)

splitcmd = 'csplit --prefix ' + infilename +  ' ' + infilename +  splitstring
print(splitcmd)
os.system(splitcmd)
