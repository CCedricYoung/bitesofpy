import os
from urllib.request import urlretrieve
import pandas as pd
from textwrap import wrap
from collections import Counter

"""
The genetic code of all organisms uses a 3 base (codon), 4 letter encoding (A, G, C or T/U) to represent the 20* amino acids used in proteins. This yields 43 = 4*4*4 = 64 different possible three base codons. Of these, one is used as an initiator called "start codon", three are used to signal the end of a protein and are called "stop codons" (*). The residual 60 codons + the start/methionine codon encode the 20 proteinogenic amino acids. Some amino acids are encoded by up to 6 different codons, whereas other amino acids are only encoded by a single codon. This is known as the degenerate code and is often visualized by a codon wheel. Every organism has a different set of preferred codons which helps to optimize and balance protein production.

In this bite you are provided with a list of all coding sequences of the bacterium Staphyloccocus aureus.

Calculate the average codon usage table for all sequences using the supplied translation table. Please note that the coding sequences are supplied as an RNA sequence, whereas the codon usage table is provided as a DNA sequence. To convert a DNA sequence to an RNA sequence, replace all Ts to Us. Disregard sequences that are not valid coding sequences.
  
bacterium Staphyloccocus aureus

(<codon>?[AGCT/U][AGCT/U][AGCT/U])
(<amino acid>?{start codon}{codon}*)(3x{stop codon})
1. given codon usage table in DNA -> convert to RNA (T->U)
2. ignore invalid amino acid sequences

1. %3 == 0
2. first codon is M
3. last 3 codons are *

A | S | 1 | 2 | 3 | Count
F | - | T | T | T | 0
F | - | T | T | C | 0
L | - | T | T | A | 0
L | M | T | T | G | 0



3. calculate average codon usage table
"""

# Translation Table:
# https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG11
# Each column represents one entry. Codon = {Base1}{Base2}{Base3}
# All Base 'T's need to be converted to 'U's to convert DNA to RNA
TRANSL_TABLE_11 = """
    AAs  = FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
  Starts = ---M------**--*----M------------MMMM---------------M------------
  Base1  = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
  Base2  = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
  Base3  = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG
"""

# Converted from http://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Staphylococcus_aureus_Newman_uid58839/NC_009641.ffn  # noqa E501
URL = "https://bites-data.s3.us-east-2.amazonaws.com/NC_009641.txt"

# Order of bases in the table
BASE_ORDER = ["U", "C", "A", "G"]


def _preload_sequences(url=URL):
    """
    Provided helper function
    Returns coding sequences, one sequence each line
    """
    filename = os.path.join(os.getenv("TMP", "/tmp"), "NC_009641.txt")
    if not os.path.isfile(filename):
        urlretrieve(url, filename)
    with open(filename, "r") as f:
        return f.readlines()


def return_codon_usage_table(
    sequences=_preload_sequences(), translation_table_str=TRANSL_TABLE_11
):
    """
    Receives a list of gene sequences and a translation table string
    Returns a string with all bases and their frequencies in a table
    with the following fields:
    codon_triplet: amino_acid_letter frequency_per_1000 absolute_occurrences

    Skip invalid coding sequences:
       --> must consist entirely of codons (3-base triplet)
    """
    # M - start, * - end

    table_map = {}
    for line in translation_table_str.replace("T", "U").split("\n"):
        if "=" in line:
            key, val = line.strip().split("=")
            table_map[key.strip()] = val.strip()

    df = pd.DataFrame()
    df['Starts'] = list(table_map['Starts'])
    df['AAs'] = list(table_map['AAs'])
    df['Codon'] = list(map(''.join, zip(table_map['Base1'], table_map['Base2'], table_map['Base3'])))

    def starts(codon):
        return df[df["Codon"] == codon]['Starts'].values[0]

    def is_start(codon):
        return starts(codon) == 'M'
    
    def is_end(codon):
        return starts(codon) == '*'

    counter = Counter()
    for sequence in sequences:
        line = sequence.strip()
        if not (len(line) % 3 == 0 and len(line) > 1):
            continue
        codons = wrap(line, 3)
        if not is_start(codons[0]):
            continue
        if not is_end(codons[-1]):
            continue
        
        counter += Counter(codons)

        print(codons)

    print(df)





if __name__ == "__main__":
    print(return_codon_usage_table())
