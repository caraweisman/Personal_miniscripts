## input: list of sam files
## Code submits one job per file to the cluster to use samtools to convert to bam format
## Samtools (1) must be pre-loaded
## Works on Harvard slurm cluster (how general?)


import glob
import numpy as np
import os

filelist = glob.glob('*fastq.sam')


for y in range(0, len(filelist)): 
                print filelist[y]
		sbatchfile = open(filelist[y] + '_samtobam.sh', 'w')
		sbatchfile.write('#!/bin/bash')
		sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -J ' + filelist[y] + '_samtobam.sh')
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
		command = 'samtools view -S -b ' + filelist[y] + ' > ' + filelist[y][:-4] + '.bam'
		sbatchfile.write(command)
		sbatchfile.write('\n')
		sbatchfile.close()
		runcommand = 'sbatch ' + filelist[y] + '_samtobam.sh'
		print runcommand
		os.system(runcommand)
