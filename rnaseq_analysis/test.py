#import libs.rnaseqlib as rl
#import libs.htseqlib as hl
#import libs.edgeRlib as el
import rnaseq_settings as rs
import libs.rnaseqlib as rl
#from edgeR_settings import *
import psycopg2
import os
import libs.htseqlib as hl

#conn = psycopg2.connect("dbname=rnaseq user=andrea")

#genefile = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/sfari_r557/lowagg_CS/toptags_edgeR.csv'

#fdr_th = 0.05
#gene_subset = 'sfari_r557'
#group1 = 'lowagg_CS'
#group2 = 'ctrlagg_CS'
#gff_file = 'dmel-all-filtered-r5.57.gff'
#hhfile = 'human_hom_edgeR_{}.csv'.format(fdr_th)

#cur = conn.cursor()
#el.write_human_homologs(hhfile, fdr_th, gene_subset, group1, group2, gff_file, cur)
##print(len(hh))
##for i in hh:
    ##with open('human_hom_edgeR_{}.csv'.format(fdr_th), 'w') as g:
        ##g.write('\t'.join(i) + '\n')
#cur.close()
##conn.commit()
#conn.close()
#file_path = 'genes.fpkm_tracking_test'
#new_file_path = 'test'
#rl.remove_blank_trackid(file_path, new_file_path)



print(hl.add_htseq_counts('htseqcount'))
#print(hl.add_clc_counts('pten_MA_RGAM009G_RNA-Seq.txt'))
