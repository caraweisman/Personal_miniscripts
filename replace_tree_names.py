# this takes an input tree with taxids that are <str>.<n> and an input file of actual names and replaces the names in the tree with the names in the input file, IN THAT ORDER (eg seq.1 goes to the first name in the file) 
# useful when using esl-reformat --rename option to avoid terrible phylip cutoff of names in processing, duplicate taxids, etc; this switches them back at the end

import sys
import numpy as np
import re 

intree = np.genfromtxt(sys.argv[1], dtype=str) 

seqids = np.genfromtxt(sys.argv[2], dtype=str, delimiter='\t') 

print(intree)

for i in range(0, len(intree)): 
	treetest = intree[i]
	firstbreak = re.split(':', treetest)
	reconline = ''
	for i in range(0, len(firstbreak)): 
		secondbreak = re.split('\(', firstbreak[i])
		if len(secondbreak) > 1: 
			if len(secondbreak[-1]) > 0: 
				taxnum = re.split('\.',secondbreak[-1])[1] # assumes sequence ids in tree are in the form <s>.x, where s is a string and x is the number CORRESPONDING TO ORDER IN SEQIDS file; this is based on esl-reformat-based renaming
				taxid = seqids[int(taxnum)-1][1:] # numbers in esl-reformatted renamed file start at 1 for sequence ids; file starts at 0 ; 1: excludes first bracket which is carryover from fasta
				for j in range(0, len(secondbreak)-1): 
					reconline = reconline + secondbreak[j] + '('
				reconline = reconline + taxid
			else: 
				reconline = reconline + secondbreak[0] + '('
		else: 
			secondbreak = re.split(',', firstbreak[i])
			if len(secondbreak) > 1:
				if len(secondbreak[-1]) > 0: 
					taxnum = taxnum = re.split('\.',secondbreak[-1])[1]
					taxid =	seqids[int(taxnum)-1][1:]
	  		              	for j in range(0, len(secondbreak)-1):
	                	        	reconline = reconline +	secondbreak[j] + ','
	                		reconline = reconline +	taxid
				else: 
					reconline = reconline + secondbreak[0] + ','
			else: 
				if ',' not in secondbreak[0] and ':' not in secondbreak[0] and '(' not in secondbreak[0] and ')' not in secondbreak[0]: 
					taxnum = re.split('\.', secondbreak[0])[1]
					taxid =	seqids[int(taxnum)-1][1:]
					reconline = reconline + taxid
				else: 
					reconline = reconline + firstbreak[i]
		
		if i < len(firstbreak)-1: 
			reconline = reconline + ':'
		else: 
			reconline = reconline
	print reconline
