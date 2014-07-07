import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.edgeRlib as el
from rnaseq_settings import *
from edgeR_settings import *
import psycopg2
import os
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('-fdr', '--fdr_threshold', default=0.05, help='Level at which to control the FDR')
parser.add_argument('-s', '--genesubset', choices=['prot_coding_genes', 
        'bwa_r557', 'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        help='run edgeR analysis on subset of genes')
parser.add_argument('-G', '--gff_file', default='dmel-all-filtered-r5.57.gff',
        help='gff file used')
parser.add_argument('-t', '--tool', default='edger', help='DE analysis tool')
args = parser.parse_args()

fdr_th = args.fdr_threshold
if args.genesubset:
    gene_subset = args.genesubset
else:
    gene_subset = ''
gff_file = args.gff_file
tool = args.tool

conn = psycopg2.connect("dbname=rnaseq user=andrea")
cur = conn.cursor()
el.batch_write_human_homologs(RNASEQDICT, fdr_th, tool, gene_subset, gff_file, conn)
cur.close()
#conn.commit()
conn.close()
