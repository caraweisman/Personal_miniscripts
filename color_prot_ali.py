#!/usr/bin/env python3

import sys
import re

# Define a dictionary to map amino acids to their corresponding ANSI escape codes for color
ansi_colors = {
    'G': '\033[37m',  # Gray
    'A': '\033[37m',  # Gray
    'S': '\033[37m',  # Gray
    'T': '\033[37m',  # Gray
    'D': '\033[91m',  # Intense Red
    'E': '\033[91m',  # Intense Red
    'N': '\033[31m',  # Dark Red
    'Q': '\033[31m',  # Dark Red
    'Y': '\033[35m',  # Purple
    'F': '\033[35m',  # Purple
    'W': '\033[35m',  # Purple
    'P': '\033[95m',  # Pink
    'C': '\033[32m',  # Green
    'V': '\033[32m',  # Green
    'I': '\033[32m',  # Green
    'L': '\033[32m',  # Green
    'M': '\033[32m',  # Green
    'K': '\033[34m',  # Blue
    'R': '\033[34m',  # Blue
    'H': '\033[33m'   # Orange
}

# ANSI escape code to reset the text color to the default
reset_color = '\033[0m'

# Font style for larger text (adjust as needed)
larger_font = '\033[1m'

# Function to read a PHYLIP format file and return a list of sequences
def read_phylip(file_path):
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

# Read the list of sequences from the PHYLIP format file
sequences = read_phylip(phylip_file)

# Define a function to print the colored amino acids in the sequences with a larger font style
def print_colored_larger_aligned_sequences(sequences):
    for sequence in sequences:
        colored_sequence = ""
        for aa in sequence:
            color = ansi_colors.get(aa, '\033[0m')  # Default to reset color if not found
            colored_sequence += f'{color}{larger_font}{aa}{reset_color}'
        print(colored_sequence)

# Call the function to print the colored multiple sequence alignment with a larger font style
print_colored_larger_aligned_sequences(sequences)
