## input: extension of fastq files in the current directory
## output: fastq files in fasta format

import glob
import os
import sys

ext = sys.argv[1]

infiles = glob.glob('*' + ext)

for i in range(0, len(infiles)): 
	command = ''' cat ''' + infiles[i] + ''' | awk '{if(NR%4==1) {printf(">%s\\n",substr($0,2));} else if(NR%4==2) print;}' > ''' + infiles[i][:-len(ext)] + ".fa"
	os.system(command)
