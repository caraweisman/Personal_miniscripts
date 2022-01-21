### takes as input 1. a tree in newick format; 2. a scalar. 
### returns the same tree with all branches scaled by the scalar. 
import numpy as np 
import sys
import re

treefile = sys.argv[1]
factor = float(sys.argv[2])


tree = open(treefile, 'r').read()
print tree


broken = re.split('(:|,|\(|\))', tree)

def isfloat(str): 
	try: 
		float(str)
		return True
	except: 
		return False

tojoin = []
for i in range(0, len(broken)): 
	if isfloat(broken[i]) == True: 
		tojoin.append(str(float(broken[i])*factor))
	else: 
		tojoin.append(broken[i])


joined = ''.join(tojoin)
print joined
