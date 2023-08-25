## takes output from a lastz run and turns into a dotplot
## assumes highly nonstandard output format from lastz, corresponding to: 
## lastz TARGET.fna QUERY.fna --format=general:name1,size1,start1,end1,length1,name2,size2,start2,end2,length2,nmatch,nmismatch,ngap,identity,continuity

import numpy as np
from matplotlib import pyplot as plt

lastz_infile = sys.argv[1]
lastz_data = np.genfromtxt(lastz_infile, dtype=str, delimiter='\t')

target_name = lastz_data[0][0]
target_length = int(lastz_data[0][1])
query_name = lastz_data[0][5]
query_length = int(lastz_data[0][6])

ali_target_starts = []
ali_target_ends = []
ali_query_starts = []
ali_query_ends = []

for i in range(0, len(lastz_data)): 
    #print(lastz_data[i])
    #ali_target_starts.append(lastz_data[i][2])
    #ali_target_ends.append(lastz_data[i][3])
    target_start = float(lastz_data[i][2])
    target_end = float(lastz_data[i][3])
    
    query_start = float(lastz_data[i][7])
    query_end = float(lastz_data[i][8])
    #ali_query_starts.append(lastz_data[i][7])
    #ali_query_ends.append(lastz_data[i][8])
    
    plt.plot([query_start, query_end], [target_start, target_end], color='black')
#plt.xlim([0, query_length])
#plt.ylim([0, target_length])
plt.xlabel(query_name)
plt.ylabel(target_name)
plt.show()
