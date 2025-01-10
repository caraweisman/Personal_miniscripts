#!/usr/bin/env python
# much improved relative to v1 - fixes bug that causes failure at high total output file number

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python split_fasta.py <input_fasta_file>")
        sys.exit(1)
    
    input_fasta = sys.argv[1]
    # Number of sequences per output file
    chunk_size = 100
    
    # Keep track of current chunk (file) count and the sequences collected so far
    chunk_counter = 1
    sequences_in_current_chunk = []
    
    # This will temporarily store lines for the current sequence being read
    current_sequence_lines = []

    # Read the input FASTA line by line
    with open(input_fasta, 'r') as infile:
        for line in infile:
            # If we see a '>' this indicates the start of a new sequence
            if line.startswith('>'):
                # If we have lines for a previous sequence, add them to the chunk
                if current_sequence_lines:
                    sequences_in_current_chunk.append(''.join(current_sequence_lines))
                    current_sequence_lines = []
                    
                    # If we've reached 100 sequences, write them out to a file
                    if len(sequences_in_current_chunk) == chunk_size:
                        output_filename = (
                            os.path.splitext(input_fasta)[0]
                            + f"_{chunk_counter}.fasta"
                        )
                        with open(output_filename, 'w') as outfile:
                            for seq in sequences_in_current_chunk:
                                outfile.write(seq)
                        chunk_counter += 1
                        sequences_in_current_chunk = []
                
                # Start a new sequence with the header line
                current_sequence_lines.append(line)
            else:
                # Continue adding lines (sequence data) to the current sequence
                current_sequence_lines.append(line)
        
        # After the loop, there may be a leftover sequence in current_sequence_lines
        if current_sequence_lines:
            sequences_in_current_chunk.append(''.join(current_sequence_lines))
        
        # Also, there may be leftover sequences in sequences_in_current_chunk
        if sequences_in_current_chunk:
            output_filename = (
                os.path.splitext(input_fasta)[0]
                + f"_chunk{chunk_counter}.fasta"
            )
            with open(output_filename, 'w') as outfile:
                for seq in sequences_in_current_chunk:
                    outfile.write(seq)
    
    print("Done splitting FASTA file into chunks of 100 sequences each.")

if __name__ == "__main__":
    main()

