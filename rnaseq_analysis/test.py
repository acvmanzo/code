import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.edgeRlib as el
from rnaseq_settings import *
from edgeR_settings import *
import psycopg2
import os

conn = psycopg2.connect("dbname=rnaseq user=andrea")

genefile = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/sfari_r557/lowagg_CS/toptags_edgeR.csv'

fdr_th = 0.05
gene_subset = 'sfari_r557'
group1 = 'lowagg_CS'
group2 = 'ctrlagg_CS'
gff_file = 'dmel-all-filtered-r5.57.gff'
hhfile = 'human_hom_edgeR_{}.csv'.format(fdr_th)

cur = conn.cursor()
el.write_human_homologs(hhfile, fdr_th, gene_subset, group1, group2, gff_file, cur)
#print(len(hh))
#for i in hh:
    #with open('human_hom_edgeR_{}.csv'.format(fdr_th), 'w') as g:
        #g.write('\t'.join(i) + '\n')
cur.close()
#conn.commit()
conn.close()
