#!/usr/bin/python

#Code for running goseq

import argparse 
import cmn.cmn as cmn
import datetime
import glob
import libs.goseqlib as gl
import libs.rnaseqlib as rl
import rnaseq_settings as rs
import os
import psycopg2


parser = argparse.ArgumentParser()
parser.add_argument('tool', choices=['edger', 'deseq'],
        help='selects DE analysis tool used')
parser.add_argument('alignment', choices=['unstranded', '2str', 'r6_2str'], 
        help='Option for which data to analyze')
parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes',
        'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        'bwa_r557_ralph_mt_ex', 'sfari_r557', 'bwa_r601', 'sfari_r601', 
        'pcg_r601'], 
        help='set of genes on which DE analysis was run')
parser.add_argument('-r', '--run', action="store_true", 
        help='runs goseq analysis')
parser.add_argument('-c', '--copytodb', action="store_true", 
        help='copies goseq results to database')

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
        rnaseqdict['goseq_log_file']))
    rl.logginginfo(logpath)

if args.run:
#Runs DE analysis on the indicated groups.
    exptlist = sorted(glob.glob('*/'))
    gl.batch_run_goseq(exptlist, rnaset, tool)

if args.copytodb:
    #Generates files formatted for database and copies data from that file into 
    #the database. 
    conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
    gl.batch_makecopy_db_goseqfile(rnaset, tool, gene_subset, conn)
    conn.commit()
    conn.close()

