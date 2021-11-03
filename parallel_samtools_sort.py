## input: list of sam files
## Code submits one job per file to the cluster to use samtools to sort the output (how to make bowtie do this in the first place???)
## Samtools (1) must be pre-loaded
## Works on Harvard slurm cluster (how general?)

import glob
import numpy as np
import os

filelist = glob.glob('*fastq.sam')


for y in range(0, len(filelist)): 
                print filelist[y]
		sbatchfile = open(filelist[y] + '_sortsam.sh', 'w')
		sbatchfile.write('#!/bin/bash')
		sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -J ' + filelist[y] + '_samsortsam.sh')
                sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -c 4')
                sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -N 1')
                sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -p eddy')
                sbatchfile.write('\n')
		sbatchfile.write('#SBATCH --mem 15000')
                sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -t 0-500:00')
                sbatchfile.write('\n')
		command = 'samtools sort -o ' + filelist[y][:-4] + '_sorted' + '.sam' + ' ' + filelist[y] 
		sbatchfile.write(command)
		sbatchfile.write('\n')
		sbatchfile.close()
		runcommand = 'sbatch ' + filelist[y] + '_sortsam.sh'
		print runcommand
		os.system(runcommand)
