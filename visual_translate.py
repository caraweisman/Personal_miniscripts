#!/usr/bin/env python3

import sys
from Bio import SeqIO
from Bio.Seq import Seq

def translate_dna_to_protein(dna_sequence):
    """
    Translates a DNA sequence to a protein sequence.
    """
    dna_seq = Seq(dna_sequence)
    protein_seq = dna_seq.translate()
    return protein_seq

def colorize_nucleotide(nucleotide):
    """
    Returns a colorized representation of a nucleotide.
    """
    colors = {'A': '\033[91m',  # Red
              'C': '\033[92m',  # Green
              'G': '\033[94m',  # Blue
              'T': '\033[93m'}  # Yellow
    reset_color = '\033[0m'  # Reset color

    return colors.get(nucleotide, nucleotide) + nucleotide + reset_color

def display_alignment(dna_sequence, protein_sequence):
    """
    Displays the alignment of nucleotides and amino acids with colored nucleotides.
    """
    alignment_length = max(len(dna_sequence), len(protein_sequence) * 3)

    print("Amino Acid Sequence:  ", protein_sequence)

    codons = [dna_sequence[i:i+3] for i in range(0, alignment_length, 3)]
    amino_acids = [protein_sequence[i//3] for i in range(0, alignment_length, 3)]

    for i in range(0, len(codons), 20):
        codon_line = "".join("".join(colorize_nucleotide(nt) for nt in codon) for codon in codons[i:i+20])
        amino_acid_line = " " + " ".join(f"{aa:^2}" for aa in amino_acids[i:i+20])

        # Print nucleotide and amino acid lines separately to maintain spacing
        print("Codons:               ", codon_line)
        print("Amino Acids:          ", amino_acid_line)
        print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py fasta_filename")
        sys.exit(1)

    fasta_filename = sys.argv[1]

    # Read the FASTA file
    try:
        with open(fasta_filename, 'r') as fasta_file:
            record = list(SeqIO.parse(fasta_file, 'fasta'))[0]
    except FileNotFoundError:
        print(f"Error: File '{fasta_filename}' not found.")
        sys.exit(1)

    # Get the DNA sequence
    dna_sequence = str(record.seq)

    # Translate DNA to protein sequence
    protein_sequence = translate_dna_to_protein(dna_sequence)

    # Display the alignment
    display_alignment(dna_sequence, protein_sequence)
