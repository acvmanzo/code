
#!/usr/bin/python

#Code for running goseq

import argparse 
import cmn.cmn as cmn
import datetime
import glob
import libs.decountlib as dl
import libs.rnaseqlib as rl
import rnaseq_settings as rs
import os
import psycopg2


parser = argparse.ArgumentParser()
parser.add_argument('expts', 
        help="'all' = all DE directories, else list of directories separated \
        by commas")
parser.add_argument('tool', choices=['edger', 'deseq'],
        help='selects DE analysis tool used')
parser.add_argument('alignment', choices=['unstranded', '2str', 'r6_2str'], 
        help='Option for which data to analyze')
parser.add_argument('genesubset', choices=['all', 'prot_coding_genes',
        'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        'bwa_r557_ralph_mt_ex', 'sfari_r557', 'bwa_r601', 'sfari_r601', 
        'pcg_r601'], 
        help='set of genes on which DE analysis was run')
parser.add_argument('-r', '--run', action="store_true", 
        help='runs goseq analysis')

args = parser.parse_args()
tool = args.tool

rnaset = rs.RNASeqData(alignment=args.alignment, genesubset=args.genesubset)
rnaseqdict = rnaset.__dict__
degroups = rs.DEGroups()
cmn.makenewdir(rnaset.decount_dirpath)

exptdir = os.path.join(rnaseqdict['{}_dirpath'.format(tool)], args.genesubset)
os.chdir(exptdir)
if args.expts == 'all':
    exptlist = sorted([os.path.abspath(e) for e in glob.glob('*/')])
else:
    exptlist = sorted([os.path.abspath(e) for e in args.expts.split(',')])

conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))


#for fdr in [0.01, 0.05, 0.10]:
for fdr in [0.01]:
    #dl.create_decount_tables(conn, rnaset, tool, fdr)
    #dl.write_decount_samples_mf(conn, rnaset, tool, fdr)
    #dl.write_group_decount(conn, exptlist, rnaset, fdr, tool)
    for sex in ['M', 'F']:
        #dl.write_decount_gene_counts(conn, rnaset, degroups, sex, fdr, tool, 
                #minfdr=True)
        dl.write_decount_fc_cv(conn, rnaset, degroups, sex, fdr, tool, 
                minfdr=True)
