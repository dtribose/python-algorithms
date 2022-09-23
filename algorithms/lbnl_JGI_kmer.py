# kmer.py

import os
import numpy as np
import matplotlib.pyplot as plt
import time

def process_kmer_file(filename, kmer_len, show_contigs=True):

    print(f"Reading file {os.path.split(filename)[-1]}...")

    with open(filename, 'r') as fp:

        contig_bits = []
        contig_dict = {}

        # Get first contig name
        for line in fp:
            if line.startswith('#'):
                continue
            elif line.startswith('>'):
                contig_name = line[1:].strip()
                break

        # for line in fp.readline():  # why doesn't this work?

        # Read file and get contig_name and contig string.
        for line in fp:
            if line.startswith('>'):
                next_contig_name = line[1:].strip()
                # Process previous results
                contig = ''.join(contig_bits)
                if show_contigs:
                    print(f"contig_name: '{contig_name}'")
                    print(f"contig: '{contig}'")
                contig_dict[contig_name] = contig
                
                contig_name = next_contig_name
                contig_bits = []
                continue

            contig_bits.append(line.strip())

        # join together contig_bits
        contig = ''.join(contig_bits)
        if show_contigs:
            print(f"contig_name: '{contig_name}'")
            print(f"contig: '{contig}'")
        contig_dict[contig_name] = contig

        print("Done reading in data\n")
        print("Processing contigs!")

        # Get kmers and counts for each kmer.
        kmer_dict = {}
        for contig_name,contig in contig_dict.items():
            print(f"For contig, '{contig_name}'")
            for i in range(len(contig)//kmer_len):
                kmer = contig[kmer_len*i:kmer_len*i+kmer_len]
                # print(kmer)
                if kmer in kmer_dict:
                    kmer_dict[kmer] += 1
                else:
                    kmer_dict[kmer] = 1

        print(f"kmer_dict = {kmer_dict}")
        vals = list(kmer_dict.values())
        print(f"kmer_dict.values() = {vals}")

        # Get a tuple of unique values and their frequency in numpy array
        uni, freq = np.unique(vals, return_counts=True)

        print(f"uni, freq = {uni}, {freq}")
          
        # convert both into one numpy array
        counts = np.asarray((uni, freq))
        kmer_counts_dict = {u:f for u,f in zip(uni, freq)}

        print(f"kmer_counts_dict = {kmer_counts_dict}")

        # And Plot, using Matplotlib
        #fig, ax = plt.subplots()
        #ax.plot(uni, freq)
        #plt.show()

        # Try implementing as a histogram.
        fig, axs = plt.subplots(tight_layout=True)
        axs.hist(vals, bins=[.5,1.5, 2.5, 3.5, 4.5])
        axs.plot()
        plt.show()

if __name__ == "__main__":

    filename = r'C:\Users\David\dev\toy-algorithms\algorithms\a.fasta'
    process_kmer_file(filename, 3)
