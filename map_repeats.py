## takes in a sequence (fasta) (first cmd line arg) and a reference genome (fasta) (second arg) 
## outputs a list of subsequences in the sequence found more than once by a BLAST hit to the reference genome and their multiplicity
## also outputs a plot of multiplicity per base

import numpy as np
import sys
import glob
import os
from matplotlib import pyplot as plt

threshold = 5

queryseq = sys.argv[1]
dbseq = sys.argv[2]

outfilename = queryseq + '_vs_' + dbseq + '_repeat_map.blastout'

imageoutfilename = queryseq + '_vs_' + dbseq + '_repeat_map.png'

command = 'blastn -task dc-megablast -query ' + queryseq + ' -db ' + dbseq + ' -evalue 0.1  -outfmt="6 qseqid qlen qstart qend sseqid slen sstart send evalue" > ' + outfilename
os.system(command)

blast_results = np.genfromtxt(outfilename, dtype=str, delimiter='\t')
qstart = 2
qend = 3

region_len = int(blast_results[0][1]) # from self-hit


regions = [0]*(int(blast_results[0][1])+1) # vector with n+1 elements, one for each position in query; first one is empty zero for zero indexing
chunked_regions = []
chunked_region_counts = []
for i in range(1, len(blast_results)): # first line will usually be full region, since we're generally blasting it to the same genome 
	startpos = int(blast_results[i][qstart])
	endpos = int(blast_results[i][qend])
	for j in range(startpos, endpos+1): 
		regions[j] = regions[j] + 1
	included = False
	for j in range(0, len(chunked_regions)): 
		if startpos >= chunked_regions[j][0] and endpos <= chunked_regions[j][1]: 
			chunked_region_counts[j] += 1
			included = True
		elif startpos <= chunked_regions[j][0] and endpos >= chunked_regions[j][1]: 
			chunked_regions[j][0] = startpos
			chunked_regions[j][1] = endpos
			chunked_region_counts[j] += 1
			included = True
		elif startpos <= chunked_regions[j][0] and  endpos >= chunked_regions[j][0] and endpos <= chunked_regions[j][1]: 
			chunked_regions[j][0] = startpos
			chunked_region_counts[j] += 1
			included = True
		elif startpos >= chunked_regions[j][0] and startpos <= chunked_regions[j][1] and endpos >= chunked_regions[j][1]: 
			chunked_regions[j][1] = endpos
			chunked_region_counts[j] += 1
			included = True
	if included == False: 
		chunked_regions.append([startpos,endpos])
		chunked_region_counts.append(1)

zipped = zip(chunked_regions, chunked_region_counts)

sortedzipped = sorted(zipped, key=lambda x: x[0])
for i in range(0, len(sortedzipped)):
	print(sortedzipped[i][0], sortedzipped[i][1])


xaxis = np.arange(0, region_len+1)
plt.scatter(xaxis, regions, s=5, color='blue')
#plt.ylim([1,1000])
plt.xlabel(queryseq + ' position ')
plt.ylabel('Number of other loci hit, dc-megablast')
plt.savefig(imageoutfilename + 'TEST.png')
os.system('cp ' + imageoutfilename + 'TEST.png  ~')
