import libs.correlationlib as cl
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

edger_dirpath = os.path.join(rnaset.edger_dirpath, genesubset)
print(edger_dirpath)


os.chdir(edger_dirpath)
for item in degroups.males + degroups.females:
    os.chdir(os.path.join(edger_dirpath, item))
    print(os.getcwd())
    cur = conn.cursor()
    cmd = "COPY (select g.fbgn_id from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = '{}' and d.fdr < 0.1 and gff_file = 'dmel-all-filtered-r5.57.gff' and group1 = '{}' order by fdr) TO STDOUT;".format(genesubset, item)
    with open('toptags_edgeR_0.10fbgn', 'w') as g:
        cur.copy_expert(cmd, g)
    cur.close()

