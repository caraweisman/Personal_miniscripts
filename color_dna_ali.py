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

# Function to read a PHYLIP format file and return a list of DNA sequences
def read_phylip_dna(file_path):
    sequences = []
    with open(file_path, 'r') as phylip_file:
        lines = phylip_file.readlines()
        num_sequences, seq_length = map(int, re.findall(r'\d+', lines[0]))
        for i in range(1, len(lines)):
            sequence = lines[i].strip()
            sequences.append(sequence)
    return sequences

if len(sys.argv) != 2:
    print("Usage: python script.py input.phy")
    sys.exit(1)

phylip_file = sys.argv[1]

# Read the list of DNA sequences from the PHYLIP format file
sequences = read_phylip_dna(phylip_file)

# Define a function to print the colored DNA bases in the sequences with a larger font style
def print_colored_larger_aligned_sequences(sequences):
    for sequence in sequences:
        colored_sequence = ""
        for base in sequence:
            color = ansi_colors.get(base, '\033[0m')  # Default to reset color if not found
            colored_sequence += f'{color}{larger_font}{base}{reset_color}'
        print(colored_sequence)

# Call the function to print the colored DNA alignment with a larger font style
print_colored_larger_aligned_sequences(sequences)
