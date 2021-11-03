## Hard-coded input: list of sequence read files (eg SRRXXX or ERRXXX) and prefix (eg .fastq) -- both to avoid other modifications to the files induces by having to use glob; full name essentially hard-coded
## And name of bowtie-indexed (by bowtie-build) genome to align to 
## Code submits one job per file to the cluster to do alignment of reads to specified genome
## Bowtie (1) must be pre-loaded
## Works on Harvard slurm cluster (how general?)


import glob
import numpy as np
import os

filelist = ['ERR906869', 'ERR906862', 'ERR906863', 'ERR906864', 'ERR906872', 'ERR906873', 'ERR906861', 'ERR906866', 'ERR906871', 'ERR906874', 'ERR906876', 'ERR906877', 'ERR906878', 'ERR906865', 'ERR906867', 'ERR906868', 'ERR906875', 'ERR906870']
suffix = '.fastq'

genome = 'C.costata.fasta_bt_indices'

for y in range(0, len(filelist)): 
                print filelist[y]
		sbatchfile = open(filelist[y] + '_align.sh', 'w')
		sbatchfile.write('#!/bin/bash')
		sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -J ' + filelist[y] + '_align.sh')
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
		command = 'bowtie -S ' + genome + ' ' + filelist[y] + suffix + ' ' + filelist[y] + suffix + '.bam' 
		sbatchfile.write(command)
		sbatchfile.write('\n')
		sbatchfile.close()
		runcommand = 'sbatch ' + filelist[y] + '_align.sh'
		print runcommand
		os.system(runcommand)
