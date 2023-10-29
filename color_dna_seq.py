#!/usr/bin/env python3
import sys
import re

# Define a dictionary to map DNA bases to their corresponding ANSI escape codes for color
ansi_colors = {
    'A': '\033[91m',   # Red
    'C': '\033[92m',   # Green
    'G': '\033[34m',   # Blue
    'T': '\033[93m',   # Intense Yellow
}

# ANSI escape code to reset the text color to the default
reset_color = '\033[0m'

# Font style for larger text (adjust as needed)
larger_font = '\033[1m'

# Function to read a FASTA file and return a list of DNA sequences
def read_fasta_dna(file_path):
    sequences = []
    current_sequence = ''
    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            if line.startswith(">"):
                if current_sequence:
                    sequences.append(current_sequence)
                    current_sequence = ''
            else:
                current_sequence += line.strip()
        if current_sequence:  # Append the last sequence
            sequences.append(current_sequence)
    return sequences

if len(sys.argv) != 2:
    print("Usage: python script.py input.fasta")
    sys.exit(1)

fasta_file = sys.argv[1]

# Read the list of DNA sequences from the FASTA file
sequences = read_fasta_dna(fasta_file)

# Define a function to print the colored DNA bases in the sequence with a larger font style
def print_colored_larger_aligned_sequence(sequence):
    colored_sequence = ""
    for base in sequence:
        color = ansi_colors.get(base, '\033[0m')  # Default to reset color if not found
        colored_sequence += f'{color}{larger_font}{base}{reset_color}'
    print(colored_sequence)

# Call the function to print the colored DNA sequence with a larger font style
if sequences:
    for sequence in sequences:
        print_colored_larger_aligned_sequence(sequence)
else:
    print("No DNA sequences found in the input file.")
