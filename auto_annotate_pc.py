# like auto_annotate, but gives coordinates within the protein for each region
import numpy as np
import re
import sys
import os 

reference_proteome_accession_path = '/n/eddy_lab/users/cweisman/Goddard/3New/Genomes/GCF_000001215.4_Release_6_plus_ISO1_MT_protein.faa_accessionlist'

reference_genome_path = '/n/eddy_lab/users/cweisman/Goddard/3New/Genomes/GCF_000001215.4_Release_6_plus_ISO1_MT_protein.faa'

in_seq = sys.argv[1]

blast_outfile_name = in_seq + '_annotation.out'

blastdbcmd = 'makeblastdb -in ' + in_seq + ' -dbtype nucl'
os.system(blastdbcmd)

print('made blast db')

blastcmd = ' blastx -db ' + reference_genome_path + ' -query ' + in_seq + ' -evalue 1 -outfmt="6 sseqid slen sstart send qstart qend evalue qlen" | sort -k5 -n >> ' + blast_outfile_name
os.system(blastcmd) 

print('performed blast')

blast_outfile = np.genfromtxt(blast_outfile_name, dtype=str, delimiter='\t')

region_length = int(blast_outfile[0][7])

#region_offset = int(sys.argv[3])
region_offset = int(sys.argv[2])

reference_proteome_accession_path = '/n/eddy_lab/users/cweisman/Goddard/3New/Genomes/GCF_000001215.4_Release_6_plus_ISO1_MT_protein.faa_accessionlist'

#region_length = 118001

#region_offset = 00 # this is the distance from the beginning of the contig; the final coordinates at the end are changed to be in reference to this (whole region not included in search so as not to waste time)

## file formatting (hard-coded given above BLAST formatting) and readin
protein_id_col = 0
protein_start_col = 2
protein_end_col = 3
protein_len_col = 1
sequence_start_col = 4
sequence_end_col = 5
evalue_col = 6 

reference_proteome_accession_list = np.genfromtxt(reference_proteome_accession_path, dtype=str, delimiter='\t')


region_ids = ['none']*(region_length+1) # first will be empty because of zero indexing
region_evalues = ['none']*(region_length+1)
region_orientations = ['none']*(region_length+1)
region_protstarts = ['none']*(region_length+1)
region_protends = ['none']*(region_length+1)
region_protlens = ['none']*(region_length+1)

for i in range(0, len(blast_outfile)): 
	hit_start = int(blast_outfile[i][sequence_start_col])
	hit_end = int(blast_outfile[i][sequence_end_col])
	prot_start = int(blast_outfile[i][protein_start_col])
	prot_end = int(blast_outfile[i][protein_end_col])
	prot_len = int(blast_outfile[i][protein_len_col])
	if hit_start < hit_end: 
		orientation = 'plus'
		for j in range(hit_start, hit_end + 1):  # plus one here?
			if region_ids[j] == 'none':
				region_ids[j] = blast_outfile[i][protein_id_col]
				region_evalues[j] = float(blast_outfile[i][evalue_col])
				region_orientations[j] = orientation
				region_protstarts[j] = prot_start
				region_protends[j] = prot_end
				region_protlens[j] = prot_len
			else: 
				if float(region_evalues[j]) > float(blast_outfile[i][evalue_col]):
					region_evalues[j] = float(blast_outfile[i][evalue_col])
					region_ids[j] = blast_outfile[i][protein_id_col]
					region_orientations[j] = orientation
					region_protstarts[j] = prot_start
					region_protends[j] = prot_end
					region_protlens[j] = prot_len

	else: 
		orientation = 'minus'
		for j in range(hit_end, hit_start +1):  # plus one here?
			if region_ids[j] == 'none':
				region_ids[j] = blast_outfile[i][protein_id_col]
				region_evalues[j] = float(blast_outfile[i][evalue_col])
				region_orientations[j] = orientation
				region_protstarts[j] = prot_start
				region_protends[j] = prot_end
				region_protlens[j] = prot_len
			else: 
				if float(region_evalues[j]) > float(blast_outfile[i][evalue_col]):
					region_evalues[j] = float(blast_outfile[i][evalue_col])
					region_ids[j] = blast_outfile[i][protein_id_col]
					region_orientations[j] = orientation
					region_protstarts[j] = prot_start
					region_protends[j] = prot_end
					region_protlens[j] = prot_len

print('finished stage 1')
chunks = []
chunk_positions = []
evalues = []
orientations = []
protstarts = []
protends = []
protlens = []

in_chunk = False
for i in range(1, len(region_ids)): 
	if in_chunk == False:
		if region_ids[i] == region_ids[i-1] and region_ids[i] != 'none':
			in_chunk = True
			start_position = i-1
			hit_name = region_ids[i]
			evalue = region_evalues[i]  
			orientation = region_orientations[i]  
			prot_start = region_protstarts[i]
			prot_end = region_protends[i]
			prot_len = region_protlens[i]
	if in_chunk == True: 
		if i == len(region_ids): 
			end_position = i
			chunk_positions.append((int(start_position) + region_offset, int(end_position)+ region_offset))
			chunks.append(hit_name)
			evalues.append(evalue)
			orientations.append(orientation)
			protstarts.append(prot_start)  
			protends.append(prot_end) 
			protlens.append(prot_len)   
			print('here')        
		if region_ids[i] == hit_name: 
			continue
		else: 
			in_chunk = False
			end_position = i
			chunk_positions.append((int(start_position) + region_offset, int(end_position)+ region_offset))
			chunks.append(hit_name)
			evalues.append(evalue)
			orientations.append(orientation)
			protstarts.append(prot_start)  
			protends.append(prot_end) 
			protlens.append(prot_len)   
            
print('finished stage 2')
hit_list = []
hit_positions = []
hit_evalues = []
hit_orientations = []
hit_protstarts = []
hit_protends = []
hit_protlens = []

for i in range(0, len(chunks)): 
	if chunks[i] not in hit_list:
		hit_list.append(chunks[i])
		running_positions = []
		running_evalues = []
		running_orientations = []
		running_protstarts = []
		running_protends = []
		running_protlens = []
		for j in range(0, len(chunks)): 
			if chunks[i] == chunks[j]: 
				running_positions.append(chunk_positions[j])
				running_evalues.append(evalues[j])
				running_orientations.append(orientations[j])
				running_protstarts.append(protstarts[j])     
				running_protends.append(protends[j])    
				running_protlens.append(protlens[j])                        
		hit_positions.append(running_positions) 
		hit_evalues.append(running_evalues) 
		hit_orientations.append(running_orientations) 
		hit_protstarts.append(running_protstarts)
		hit_protends.append(running_protends)        
		hit_protlens.append(running_protlens)  
        
print('finished stage 3')

for i in range(0, len(hit_list)): 
    accession = hit_list[i]
    for j in range(0, len(reference_proteome_accession_list)): 
        if hit_list[i] in reference_proteome_accession_list[j]:  
            if hit_list[i] == re.split(' ', reference_proteome_accession_list[j])[0][1:]:
                description = reference_proteome_accession_list[j][1:]
                print(description)
            for j in range(0, len(hit_positions[i])): 
                if abs(hit_positions[i][j][0] - hit_positions[i][j][1]) < 60:
                    print(hit_positions[i][j], hit_orientations[i][j], hit_evalues[i][j], 'SHORT HIT')
                    print('Protein (start, stop), len:', '(',hit_protstarts[i][j], ',' , hit_protends[i][j], '),' , hit_protlens[i][j])
                else:
                    print(hit_positions[i][j], hit_orientations[i][j], hit_evalues[i][j])
                    print('Protein (start, stop), len:', '(',hit_protstarts[i][j], ',' , hit_protends[i][j], '),' , hit_protlens[i][j])
print('done')


