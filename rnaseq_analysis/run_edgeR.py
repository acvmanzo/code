#!/usr/bin/python

#Code for running edger DE analysis on htseq-count data.

import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.edgeRlib as el
from rnaseq_settings import *
from edgeR_settings import *
import psycopg2
import os
import argparse 
import datetime


def remove_htseqcount_files(conn):
    'Removes old htseqcount files.'''
    fn = "print(os.getcwd()), os.remove('htseqcount_brain_aut_will_r557_ralph_mt_excluded')"
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)
    conn.close()


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--genesubset', choices=['prot_coding_genes', 
        'bwa_r557', 'bwa_r557_ralph_mt_ex'], 
        help='run edgeR analysis on subset of genes')
args = parser.parse_args()

tool = 'edger'
if args.genesubset:
    gene_subset = args.genesubset
else:
    gene_subset = '' 

curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
logpath = os.path.join(RNASEQDICT['edger_dirpath'], gene_subset, '{}_{}'.format(curtime, RNASEQDICT['edger_log_file']))
#logpath = 'testr.log'
print(logpath)
#rl.logginginfo(logpath)


##Runs edgeR analysis on the indicated groups.
#el.batch_edger_pairwise_DE(MALES, MALES_CTRL, gene_subset, RNASEQDICT)
#el.batch_edger_pairwise_DE(FEMALES, FEMALES_CTRL, gene_subset, RNASEQDICT)
#el.edger_2groups_DE(AGG_DICT_ALL, gene_subset, RNASEQDICT)
#el.edger_2groups_DE(AGG_DICT_CS, gene_subset, RNASEQDICT)

##Generates files formatted for database and copies data from that file into 
##the database. 
#conn = psycopg2.connect("dbname=rnaseq user=andrea")
#el.batch_makecopy_db_degenefile(RNASEQDICT, tool, gene_subset, conn)
#conn.commit()
#conn.close()
