## inputs: 1) phylip alignment; 2) list of sequence names, as many as there are sequences in alignment
## outputs: the same alignment but with the sequence names changed to those in file 2)

import numpy as np 
import sys
import re

infilename = sys.argv[1]

seqnames = np.genfromtxt(sys.argv[2], dtype=str, delimiter='\n')

# assumes phylip format 

infile = np.genfromtxt(infilename, dtype=str, delimiter='\n') 

numseqs = int(re.split('\s+', infile[0])[0])

outfile = open(infilename + '_renamed', 'w')


if numseqs != len(seqnames): 
	print ' Warning: Number of names in file does not match number of sequences in alignment'

namecount = 0
for i in range(1, len(infile)): 
	if ' ' in infile[i]: # identifies lines with sequence names by containing white space
        	newname = seqnames[namecount]
        	newnametouse = re.split('from', newname)[1][1:] # modifying slightly for my weird case; if name in sequence new name file isn't exactly what you want
		namepart = re.split('\s+', infile[i])[0] # find part before white space, ie sequence name 
		newline = infile[i].replace(namepart, newnametouse)
		outfile.write(newline + '\n')
	else: 
		outfile.write(infile[i] + '\n')
	namecount += 1
outfile.close()
