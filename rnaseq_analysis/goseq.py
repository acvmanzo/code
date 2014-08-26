#!/usr/bin/python

#Code for running goseq analysis.

import argparse 
import cmn.cmn as cmn
import datetime
import glob
import libs.goseqlib as gl
import libs.rnaseqlib as rl
import rnaseq_settings as rs
import os
import psycopg2
import shutil


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
parser.add_argument('-c', '--copytodb', action="store_true", 
        help='copies goseq results to database')
parser.add_argument('-w', '--write_go_cat', action="store_true",
        help='gets GO catgories corresponding to GO IDs')

args = parser.parse_args()
tool = args.tool

rnaset = rs.RNASeqData(alignment=args.alignment, genesubset=args.genesubset)
rnaseqdict = rnaset.__dict__
degroups = rs.DEGroups()

exptdir = os.path.join(rnaseqdict['{}_dirpath'.format(tool)], args.genesubset)
os.chdir(exptdir)

if args.expts == 'all':
    exptlist = sorted([os.path.abspath(e) for e in glob.glob('*/')])
else:
    exptlist = args.expts.split(',')

if args.copytodb or args.run or args.write_go_cat:
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    cmn.makenewdir(exptdir)
    logpath = os.path.join(exptdir, '{}_{}'.format(curtime, 
        rnaseqdict['goseq_log_file']))
    rl.logginginfo(logpath)
    setpath = os.path.join(exptdir, rnaseqdict['goseq_set_file_copy'])
    shutil.copy(rnaseqdict['set_path_orig'], '{}_{}'.format(setpath, curtime))

if args.run:
    #Runs goseq analysis on the indicated groups.
    gl.batch_run_goseq(exptlist, rnaset, tool)

if args.copytodb:
    #Generates files formatted for database and copies data from that file into 
    #the database. 
    conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
    gl.batch_makecopy_db_goseqfile(exptlist, rnaset, tool, conn)
    conn.commit()
    conn.close()

if args.write_go_cat:
    #Writes new results file with the GO categories associated with GO IDs
    conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
    gl.batch_write_full_go_results(exptlist, rnaset, tool, conn)
    conn.commit()
    conn.close()
