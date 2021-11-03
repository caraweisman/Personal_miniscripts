## input: list of sam files
## Code submits one job per file to the cluster to use samtools to index a bam file
## Samtools (1) must be pre-loaded
## Works on Harvard slurm cluster (how general?)


import glob
import numpy as np
import os

filelist = glob.glob('*fastq_sorted.bam')


for y in range(0, len(filelist)): 
                print filelist[y]
		sbatchfile = open(filelist[y] + '_indexbam.sh', 'w')
		sbatchfile.write('#!/bin/bash')
		sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -J ' + filelist[y] + '_indexbam.sh')
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
		command = 'samtools index ' + filelist[y]
		sbatchfile.write(command)
		sbatchfile.write('\n')
		sbatchfile.close()
		runcommand = 'sbatch ' + filelist[y] + '_indexbam.sh'
		print runcommand
		os.system(runcommand)
