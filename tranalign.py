import sys
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment

def protein_to_nucleotide_alignment(protein_alignment_file, nucleotide_sequences_file):
    # Read protein alignment
    protein_alignment = AlignIO.read(protein_alignment_file, "fasta")

    # Read nucleotide sequences
    nucleotide_records = SeqIO.to_dict(SeqIO.parse(nucleotide_sequences_file, "fasta"))

    # Create an empty nucleotide alignment
    nucleotide_alignment = MultipleSeqAlignment([])

    # Iterate through protein alignment and substitute codons
    for protein_record in protein_alignment:
        protein_seq = str(protein_record.seq)
        nucleotide_seq = ""

        i = 0  # index for protein sequence
        j = 0  # index for nucleotide sequence

        while i < len(protein_seq):
            if protein_seq[i] == "-":  # Handle gaps in the protein alignment
                nucleotide_seq += "---"  # Assuming a gap is represented by three dashes in the nucleotide sequence
                i += 1
            else:
                codon = str(nucleotide_records[protein_record.id].seq[j:j+3])

                # Check for stop codon and adjust the length accordingly
                if "*" in Seq(codon).translate():
                    break

                nucleotide_seq += codon
                i += 1
                j += 3

        nucleotide_record = SeqRecord(Seq(nucleotide_seq), id=protein_record.id, description=protein_record.description)
        nucleotide_alignment.append(nucleotide_record)

    # Print the resulting nucleotide alignment to the terminal
    AlignIO.write(nucleotide_alignment, sys.stdout, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py protein_alignment.fasta nucleotide_sequences.fasta")
        sys.exit(1)

    protein_alignment_file = sys.argv[1]
    nucleotide_sequences_file = sys.argv[2]

    protein_to_nucleotide_alignment(protein_alignment_file, nucleotide_sequences_file)
