## takes a fasta file WITH ONE SEQUENCE and coordinates within the sequence as input
## outputs the subsequence specified by the coordinates

import numpy as np 
import os
import sys

infilename = sys.argv[1]

infile = np.genfromtxt(infilename, dtype=str, delimiter='\n')

startpos = int(sys.argv[2])
endpos = int(sys.argv[3])

charcount = 0
inseq = False

print infile[0] + '_coords_' + str(startpos) + '_to_' + str(endpos)

seq = ''
for i in range(1, len(infile)): 
        if inseq == True:
                if endpos <= charcount + len(infile[i]):
                        lineend = endpos - charcount
                        #print infile[i][:lineend]
			seq = seq + infile[i][:lineend]
                        inseq = False
                        break
                else:
                     	#print infile[i]
                        charcount += len(infile[i])
			seq = seq + infile[i]	
	if inseq == False and startpos <= charcount + len(infile[i]): 
		linestart = startpos - charcount 
		#print infile[i][linestart:]
		inseq = True
		charcount += len(infile[i])
		seq = seq + infile[i][linestart:]
	if inseq == False: 
		charcount += len(infile[i])


print seq
