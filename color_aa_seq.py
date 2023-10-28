#!/usr/bin/env python3

import sys

# Define a dictionary to map amino acids to their corresponding ANSI escape codes for color
ansi_colors = {
    'A': '\033[92m',  # Green for Alanine
    'R': '\033[94m',  # Blue for Arginine
    'N': '\033[94m',  # Blue for Asparagine
    'D': '\033[91m',  # Red for Aspartic Acid
    'C': '\033[33m',  # Brown for Cysteine
    'E': '\033[91m',  # Red for Glutamic Acid
    'Q': '\033[94m',  # Blue for Glutamine
    'G': '\033[92m',  # Green for Glycine
    'H': '\033[94m',  # Blue for Histidine
    'I': '\033[92m',  # Green for Isoleucine
    'L': '\033[92m',  # Green for Leucine
    'K': '\033[94m',  # Blue for Lysine
    'M': '\033[33m',  # Brown for Methionine
    'F': '\033[33m',  # Brown for Phenylalanine
    'P': '\033[33m',  # Brown for Proline
    'S': '\033[91m',  # Red for Serine
    'T': '\033[91m',  # Red for Threonine
    'W': '\033[33m',  # Brown for Tryptophan
    'Y': '\033[33m',  # Brown for Tyrosine
    'V': '\033[92m'   # Green for Valine
}

# ANSI escape code to reset the text color to the default
reset_color = '\033[0m'

# Font style for larger text (adjust as needed)
larger_font = '\033[1m'

# Function to read a FASTA file and return the protein sequence
def read_fasta(file_path):
    sequence = ""
    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            if line.startswith(">"):
                continue  # Skip the header line
            sequence += line.strip()
    return sequence

if len(sys.argv) != 2:
    print("Usage: python script.py input.fasta")
    sys.exit(1)

fasta_file = sys.argv[1]

# Read the protein sequence from the FASTA file
protein_sequence = read_fasta(fasta_file)

# Define a function to print the colored amino acids in the sequence with a larger font style
def print_colored_larger_protein_sequence(sequence):
    colored_sequence = ""
    for aa in sequence:
        color = ansi_colors.get(aa, '\033[0m')  # Default to reset color if not found
        colored_sequence += f'{color}{larger_font}{aa}{reset_color}'
    print(colored_sequence)

# Call the function to print the colored protein sequence with a larger font style
print_colored_larger_protein_sequence(protein_sequence)
