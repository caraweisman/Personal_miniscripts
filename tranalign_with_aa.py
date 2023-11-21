import sys

# ANSI color codes for nucleotides
COLORS = {
    "A": "\033[91m",  # Red
    "C": "\033[92m",  # Green
    "G": "\033[94m",  # Blue
    "T": "\033[33m",  # Yellow
    "reset": "\033[0m"  # Reset color to default
}

def colorize_nucleotide(nucleotide):
    """
    Wrap the nucleotide with its corresponding ANSI color code.
    """
    return COLORS.get(nucleotide, "") + nucleotide + COLORS["reset"]

def read_fasta(file_path):
    """
    Read a FASTA file and return a dictionary of sequence records.
    """
    records = {}
    with open(file_path, "r") as file:
        current_id = ""
        current_seq = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if current_id and current_seq:
                    records[current_id] = current_seq
                current_id = line[1:]
                current_seq = ""
            else:
                current_seq += line
        if current_id and current_seq:
            records[current_id] = current_seq
    return records

def translate_codon(codon):
    """
    Translate a codon into its corresponding amino acid.
    """
    codon_table = {
        "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
        "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
        "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    }
    return codon_table.get(codon, "X")  # Use "X" for unknown codons

def protein_to_nucleotide_alignment(protein_alignment_file, nucleotide_sequences_file):
    # Read protein alignment
    protein_records = read_fasta(protein_alignment_file)

    # Read nucleotide sequences
    nucleotide_records = read_fasta(nucleotide_sequences_file)

    # Create an empty nucleotide alignment
    nucleotide_alignment = {}

    # Create an empty amino acid alignment
    amino_acid_alignment = {}

    # Iterate through protein alignment and substitute codons
    for protein_id, protein_seq in protein_records.items():
        nucleotide_seq = ""
        amino_acid_seq = ""

        j = 0  # index for nucleotide sequence

        for i in range(len(protein_seq)):
            if protein_seq[i] == "-":  # Handle gaps in the protein alignment
                nucleotide_seq += "--- "  # Assuming a gap is represented by three dashes in the nucleotide sequence
                amino_acid_seq += " -  "
            else:
                codon = nucleotide_records[protein_id][j:j+3]

                # Check for stop codon and adjust the length accordingly
                if "*" in translate_codon(codon):
                    break

                amino_acid = translate_codon(codon)

                nucleotide_seq += codon + ' '
                amino_acid_seq += f"{amino_acid.center(3)}" + ' '# removed space before final quote

                j += 3

        nucleotide_alignment[protein_id] = nucleotide_seq
        amino_acid_alignment[protein_id] = amino_acid_seq

    # Determine the number of groups
    sequence_length = len(list(nucleotide_alignment.values())[0])
    num_groups = (sequence_length // 80) + 1

    # Print the resulting alignment in groups of 60 nucleotides with amino acid sequences
    for group in range(num_groups):
        start = group * 80
        end = (group + 1) * 80
        for protein_id in nucleotide_alignment:
            nucleotide_seq = nucleotide_alignment[protein_id]
            amino_acid_seq = amino_acid_alignment[protein_id]

            # Print sequence identifier to the left of each line
            for i in range(start, min(end, len(nucleotide_seq)), 80):
                formatted_nucleotide_seq = ''.join(colorize_nucleotide(n) for n in nucleotide_seq[i:i+80])
                formatted_amino_acid_seq = amino_acid_seq[i:i+80]

                print(f"{protein_id.ljust(15)} {formatted_amino_acid_seq}")
                print(f"{''.ljust(15)} {formatted_nucleotide_seq}")
        print()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py protein_alignment.fasta nucleotide_sequences.fasta")
        sys.exit(1)

    protein_alignment_file = sys.argv[1]
    nucleotide_sequences_file = sys.argv[2]

    protein_to_nucleotide_alignment(protein_alignment_file, nucleotide_sequences_file)

