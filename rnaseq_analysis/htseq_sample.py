#!/usr/bin/python

#Code for running htseq-count, loading htseq-count results into a database,
#generating files with htseq-count data of different subsets of genes. 
#Settings and file structure are in rnaseq_settings.
#Runs htseq-count on a set of samples given by the user.

import argparse
import datetime
import logging
import psycopg2
import libs.htseqlib as hl
import libs.rnaseqlib as rl
import libs.tuxedolib as tl
from rnaseq_analysis.rnaseq_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('berkidlist', 
        help='list of berkids to align, separated by commas')
parser.add_argument('-ht', '--htseqcount', action='store_true', 
        help='run htseq-count')
parser.add_argument('-c', '--copytodb', action='store_true', 
        help='copy htseq-count results to database')
parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes', 
        'brain_r557', 'bwa_r557', 'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        help='generate new htseq-count results file for the given subset of genes')
args = parser.parse_args()



COLQUERY = ['genotype', 'tube', 'sex', 'frozend', 'rnad', 'rnaconc', 
            'mrnad', 'cdnad', 'indexnum', 'sample', 'seqd', 'thawed',
            'toseq', 'samplenum', 'sentd', 'qbitngul', 'qbitd', 'seq_received']

berkidlist = args.berkidlist.split(',')
print(berkidlist)

def main():

    #curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    #logpath = '{}_{}'.format(curtime, RNASEQDICT['htseq_log_file'])
    #rl.logginginfo(logpath)
    
    seqpaths, respaths = tl.get_berkid_seq_res_paths(berkidlist, \
        SAMPLEINFO_TABLE, COLQUERY,RNASEQDICT['seq_dir'],RNASEQDICT['seq_subdir'], 
        RNASEQDICT['th_resdirpath'])
    print(seqpaths, respaths)
    print(seqpaths, respaths)

    berkid_params = zip(berkidlist, seqpaths, respaths) 
    #run_htseq(HTSEQ_DIR, HTSEQ_FILE, BAM_FILE, GFF_PATH_NOFA, HTSEQ_CMD_FILE):

if __name__ == '__main__':
    main()
