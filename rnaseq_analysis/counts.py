import libs.correlationlib as cl
import libs.htseqlib as hl
import libs.rnaseqlib as rl
import libs.delib as dl
import matplotlib.pyplot as plt
import os
import shutil
import glob
import psycopg2
import rnaseq_settings as rs 
import sys

align = '2str'
genesubset = 'prot_coding_genes'

conn = psycopg2.connect("dbname=rnaseq user=andrea")
rnaset = rs.RNASeqData(alignment=align, 
        genesubset=genesubset)
degroups = rs.DEGroups()
htseqtable = 'htseq_2str'

edger_dirpath = os.path.join(rnaset.edger_dirpath, genesubset)
print(edger_dirpath)


#os.chdir(edger_dirpath)
#for item in degroups.males + degroups.females:
    #os.chdir(os.path.join(edger_dirpath, item))
    #print(os.getcwd())
    #cur = conn.cursor()
    #cmd = "COPY (select g.fbgn_id from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = '{}' and d.fdr < 0.1 and gff_file = 'dmel-all-filtered-r5.57.gff' and group1 = '{}' order by fdr) TO STDOUT;".format(genesubset, item)
    #with open('toptags_edgeR_0.10fbgn', 'w') as g:
        #cur.copy_expert(cmd, g)
    #cur.close()

gene = 'klu'
berkid = 'RGAM009A'
group1 = 'NrxIV_M'
group2 = 'CS_M'
detable = 'degenes_2str'
tool = 'edger'
cur = conn.cursor()

#print(hl.get_gene_count(cur, htseqtable, gene, berkid))
#print(hl.get_counts(cur=cur, genotype='NrxIV_M', gene='klu', 
    #sampleinfo_table='autin', htseqtable=htseqtable))
print(hl.compare_replicate_counts(cur, degroups.females + ['CS_F'], 'klu', 
    sampleinfo_table='autin', htseqtable=htseqtable))
#dl.get_de_info(cur, gene, group1, group2, detable, tool, genesubset)
print(dl.compare_replicate_de(cur, degroups.females, 'CS_F', gene, detable, tool, genesubset))

cur.close()
conn.close()
