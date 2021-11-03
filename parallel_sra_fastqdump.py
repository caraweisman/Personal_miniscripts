## Hard-coded input: list of SRA accessions (eg SRRXXX or ERRXXX) 
## Code submits one job per file to the cluster to download from NCBI via fastq-dump in SRA toolkit
## SRA toolkit must be pre-loaded
## Works on Harvard slurm cluster (how general?)


import glob
import numpy as np
import os

filelist = ['ERR906869', 'ERR906862', 'ERR906863', 'ERR906864', 'ERR906872', 'ERR906873', 'ERR906861', 'ERR906866', 'ERR906871', 'ERR906874', 'ERR906876', 'ERR906877', 'ERR906878', 'ERR906865', 'ERR906867', 'ERR906868', 'ERR906875', 'ERR906870']


for y in range(0, len(filelist)): 
                print filelist[y]
		sbatchfile = open(filelist[y] + '_fastqdump.sh', 'w')
		sbatchfile.write('#!/bin/bash')
		sbatchfile.write('\n')
		sbatchfile.write('#SBATCH -J ' + filelist[y] + '_fastqdump.sh')
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
		command = 'fastq-dump ' + filelist[y]
		sbatchfile.write(command)
		sbatchfile.write('\n')
		sbatchfile.close()
		runcommand = 'sbatch ' + filelist[y] + '_fastqdump.sh'
		print runcommand
		os.system(runcommand)
