#!/usr/bin/python

#Code for running edger DE analysis on htseq-count data.

import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.delib as dl
from rnaseq_settings import *
from de_settings import *
import psycopg2
import os
import argparse 
import datetime
import cmn.cmn as cmn


parser = argparse.ArgumentParser()
parser.add_argument('tool', choices=['edger', 'deseq'],
        help='selects DE analysis tool')
parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes', 
        'brain_r557'],
        help='set of genes on which to run DE analysis')
#parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes', 
        #'brain_r557', 'bwa_r557', 'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        #help='set of genes on which to run DE analysis')
parser.add_argument('-r', '--run', action="store_true", 
        help='runs DE analysis')
parser.add_argument('-c', '--copytodb', action="store_true", 
        help='copies DE gene list to database')
parser.add_argument('-m', '--custom', action="store_true", 
        help='runs DE analysis with custom metadata.txt')
args = parser.parse_args()

tool = args.tool

if args.genesubset:
    gene_subset = args.genesubset

if args.copytodb or args.run:
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    exptdir = os.path.join(RNASEQDICT['edger_dirpath'], gene_subset)
    cmn.makenewdir(exptdir)
    logpath = os.path.join(exptdir, '{}_{}'.format(curtime, 
        RNASEQDICT['{}_log_file'.format(tool)]))
    rl.logginginfo(logpath)

if args.run:
#Runs edgeR analysis on the indicated groups.
    dl.batch_pairwise_DE(MALES, MALES_CTRL, gene_subset, RNASEQDICT, tool)
    #dl.batch_pairwise_DE(FEMALES, FEMALES_CTRL, gene_subset, RNASEQDICT, tool)
    #dl.run2groups_DE(AGG_DICT_ALL, gene_subset, RNASEQDICT, tool)
    #dl.run2groups_DE(AGG_DICT_CS, gene_subset, RNASEQDICT, tool)
    #dl.run2groups_DE(MUT_DICT_MALES, gene_subset, RNASEQDICT, tool)
    #dl.run2groups_DE(MUT_DICT_FEMALES, gene_subset, RNASEQDICT, tool)

if args.copytodb:
    #Generates files formatted for database and copies data from that file into 
    #the database. 
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    dl.batch_makecopy_db_degenefile(RNASEQDICT, tool, gene_subset, conn)
    conn.commit()
    conn.close()

if args.custom:
    dl.custom_DE(RNASEQDICT, tool)
