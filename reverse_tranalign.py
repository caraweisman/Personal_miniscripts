#!/usr/bin/env python3

## TAKES INPUT IN ALIGNED FASTA FORMAT
## TAKES NUCLEOTIDE ALIGNMENT AND DEPICTS A PROTEIN ALIGNMENT BASED ON IT 

import sys

def translate_codon(codon):
    """Translate a single codon to an amino acid."""
    genetic_code = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                 
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'X', 'TAG':'X',
        'TGC':'C', 'TGT':'C', 'TGA':'X', 'TGG':'W',
    }
    return genetic_code.get(codon, '-')


def process_sequence(nucleotide_sequence):
    """Process nucleotide sequence and return aligned protein sequence."""
    protein_seq = ''
    spaced_nucleotide_seq = ''
    codon = ''
    gap_buffer = ''

    for nuc in nucleotide_sequence:
        if nuc != '-':
            codon += nuc
            gap_buffer += nuc
        else:
            gap_buffer += '-'

        if len(codon) == 3:
            amino_acid = translate_codon(codon)
            codon_length = len(gap_buffer)
            left_padding = (codon_length - 1) // 2
            right_padding = codon_length - 1 - left_padding
            protein_seq += '-' * left_padding + amino_acid + '-' * right_padding + ' '
            spaced_nucleotide_seq += gap_buffer + ' '
            codon = ''
            gap_buffer = ''

    return protein_seq.strip(), spaced_nucleotide_seq.strip()

def read_fasta(file_path):
    """Read a FASTA file and return a dictionary of sequences."""
    sequences = {}
    with open(file_path, 'r') as file:
        identifier = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                identifier = line[1:]
                sequences[identifier] = ''
            elif identifier:
                sequences[identifier] += line
    return sequences

def print_interleaved(sequences, processed_data, line_length=60):
    """Print sequences interleaved with their protein translations."""
    for identifier in sequences:
        protein_seq, spaced_nuc_seq = processed_data[identifier]
        protein_lines = [protein_seq[i:i + line_length] for i in range(0, len(protein_seq), line_length)]
        nucleotide_lines = [spaced_nuc_seq[i:i + line_length] for i in range(0, len(spaced_nuc_seq), line_length)]

        for prot_line, nuc_line in zip(protein_lines, nucleotide_lines):
            print(f"{identifier} Protein: {prot_line}")
            print(f"{identifier} DNA    : {nuc_line}")
        print()

# Main execution
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py fasta_file")
        sys.exit(1)

    fasta_file = sys.argv[1]
    nucleotide_sequences = read_fasta(fasta_file)

    # Process and translate each sequence
    processed_data = {id: process_sequence(seq) for id, seq in nucleotide_sequences.items()}

    # Interleave and print sequences with their translations
    print_interleaved(nucleotide_sequences, processed_data)
