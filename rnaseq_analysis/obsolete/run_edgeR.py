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
import cmn.cmn as cmn




parser = argparse.ArgumentParser()
parser.add_argument('-s', '--genesubset', choices=['prot_coding_genes', 
        'bwa_r557', 'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        help='subset of genes on which to run analysis')
parser.add_argument('-c', '--copytodb', action="store_true", 
        help='copies de gene list to database')
parser.add_argument('-r', '--runedger', action="store_true",
        help='run edgeR analysis')
args = parser.parse_args()

tool = 'edger'
if args.genesubset:
    gene_subset = args.genesubset
else:
    gene_subset = '' 

if args.copytodb or args.runedger:
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    exptdir = os.path.join(RNASEQDICT['edger_dirpath'], gene_subset)
    cmn.makenewdir(exptdir)
    logpath = os.path.join(exptdir, '{}_{}'.format(curtime, 
        RNASEQDICT['edger_log_file']))
    rl.logginginfo(logpath)

if args.runedger:
#Runs edgeR analysis on the indicated groups.
    #el.batch_edger_pairwise_DE(MALES, MALES_CTRL, gene_subset, RNASEQDICT)
    #el.batch_edger_pairwise_DE(FEMALES, FEMALES_CTRL, gene_subset, RNASEQDICT)
    #el.edger_2groups_DE(AGG_DICT_ALL, gene_subset, RNASEQDICT)
    #el.edger_2groups_DE(AGG_DICT_CS, gene_subset, RNASEQDICT)
    el.edger_2groups_DE(MUT_DICT_MALES, gene_subset, RNASEQDICT)
    el.edger_2groups_DE(MUT_DICT_FEMALES, gene_subset, RNASEQDICT)

if args.copytodb:
    #Generates files formatted for database and copies data from that file into 
    #the database. 
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    el.batch_makecopy_db_degenefile(RNASEQDICT, tool, gene_subset, conn)
    conn.commit()
    conn.close()

