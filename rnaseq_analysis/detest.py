#!/usr/bin/python

#Code for running edger DE analysis on htseq-count data.

import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.delib as dl
import rnaseq_settings as rs
import psycopg2
import os
import argparse 
import datetime
import cmn.cmn as cmn


parser = argparse.ArgumentParser()
parser.add_argument('tool', choices=['edger', 'deseq'],
        help='selects DE analysis tool')
parser.add_argument('alignment', choices=['unstranded', '2str', 'r6_2str'], 
        help='Option for which data to analyze')
parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes',
        'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        'bwa_r557_ralph_mt_ex', 'sfari_r557', 'bwa_r601', 'sfari_r601', 
        'pcg_r601'], 
        help='set of genes on which to run DE analysis')
parser.add_argument('-r', '--run', action="store_true", 
        help='runs DE analysis')
parser.add_argument('-c', '--copytodb', action="store_true", 
        help='copies DE gene list to database')
parser.add_argument('-m', '--custom', action="store_true", 
        help='runs DE analysis with custom metadata.txt')
args = parser.parse_args()

tool = args.tool

rnaset = rs.RNASeqData(alignment=args.alignment, genesubset=args.genesubset)
rnaseqdict = rnaset.__dict__
degroups = rs.DEGroups()


if args.genesubset:
    gene_subset = args.genesubset

if args.copytodb or args.run:
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    exptdir = os.path.join(rnaseqdict['edger_dirpath'], gene_subset)
    cmn.makenewdir(exptdir)
    logpath = os.path.join(exptdir, '{}_{}'.format(curtime, 
        rnaseqdict['{}_log_file'.format(tool)]))
    rl.logginginfo(logpath)

if args.run:
#Runs DE analysis on the indicated groups.
    dl.batch_pairwise_DE(degroups.males, degroups.males_ctrl, rnaset, 
            gene_subset, rnaseqdict, tool)
    dl.batch_pairwise_DE(degroups.females, degroups.females_ctrl, rnaset,
            gene_subset, rnaseqdict, tool)
    #dl.run2groups_DE(degroups.agg_dict_all, rnaset, gene_subset, rnaseqdict, tool)
    #dl.run2groups_DE(degroups.agg_dict_cs, rnaset, gene_subset, rnaseqdict, tool)
    #dl.run2groups_DE(degroups.mut_dict_males, rnaset, gene_subset, rnaseqdict, tool)
    #dl.run2groups_DE(degroups.mut_dict_females, rnaset, gene_subset, rnaseqdict, tool)

if args.copytodb:
    #Generates files formatted for database and copies data from that file into 
    #the database. 
    conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
    dl.batch_makecopy_db_degenefile(rnaseqdict, tool, gene_subset, conn)
    conn.commit()
    conn.close()

if args.custom:
    dl.custom_DE(rnaseqdict, tool)
