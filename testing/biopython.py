import os
from Bio import SeqIO

GENE_FASTA_FILE = '/home/andrea/rnaseqanalyze/references/dmel-all-gene-r5.57.fasta'

fbgn_ids = []
gene_names = []
n = 0 

for seq_record in SeqIO.parse(GENE_FASTA_FILE, "fasta"):
    if n < 10:
        desc = seq_record.description
        desclist = desc.split('; ')
        gene_name = desclist[3].split('=')[1]

        fbgn_ids.append(seq_record.id)
        gene_names.append(gene_name)
        n+=1

print(fbgn_ids)
print(gene_names)
