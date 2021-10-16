# input: file extension, eg .fna
# output: esl-translated outputs of all of input files
## does default esl-translate, ie not only starting with AUG; no -m option here 

import glob
import os
import sys

infiles = glob.glob('*' + sys.argv[1])
for i in range(0, len(infiles)): 
	command = 'esl-translate ' + infiles[i] + ' > ' + infiles[i] + '_esltrans'
	print command
	os.system(command)



