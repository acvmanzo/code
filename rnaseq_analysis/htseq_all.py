#!/usr/bin/python

#Code for running htseq-count, loading htseq-count results into a database,
#generating files with htseq-count data of different subsets of genes. 
#Settings and file structure are in rnaseq_settings.

import argparse
import datetime
import logging
import os
import psycopg2
import libs.htseqlib as hl
import libs.rnaseqlib as rl
import rnaseq_settings as rs

parser = argparse.ArgumentParser()
parser.add_argument('alignment', choices=['unstranded', '2str', 'r6_2str'], 
        help='Option for which data to analyze')
#parser.add_argument('genesubset', choices=['all', 'prot_coding_genes',
        #'brain_r557'], 
        #help='make new file of htseq-count results for the given subset of genes')
parser.add_argument('genesubset', choices=['all', 'prot_coding_genes',
        'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        'bwa_r557_ralph_mt_ex', 'sfari_r557', 'bwa_r601', 'sfari_r601'], 
        help='make new file of htseq-count results for the given subset of genes')
parser.add_argument('-ht', '--htseqcount', action='store_true', 
        help='run htseq-count')
parser.add_argument('-c', '--copytodb', action='store_true', 
        help='copy htseq-count results to database')
#parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes',
        #'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        #'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        #help='make new file of htseq-count results for the given subset of genes')
args = parser.parse_args()

rnaset = rs.RNASeqData(alignment=args.alignment, genesubset=args.genesubset)
rnaseqdict = rnaset.__dict__
curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
if args.genesubset == 'all':
    args.genesubset = False


def batch_run_htseq(conn):
    fn = "run_htseq('{}', '{}', '{}', '{}', '{}')".format(rnaset.htseq_dir, 
            rnaset.htseq_file, rnaset.bam_file, rnaset.gff_path_nofa, 
            rnaset.htseq_cmd_file)
    hl.batch_fn_thdir(rnaset.th_resdirpath, rnaset.th_dir, 
            rnaset.res_sample_glob, conn, fn)

def batch_ht_add_berkid(conn):
    fn = "htseq_add_berkid(berkid, '{}')".format(rnaset.htseq_file)
    hl.batch_fn_thdir(rnaset.th_resdirpath, rnaset.htseq_dir, rnaset.res_sample_glob, conn, fn)

def batch_ht_copy_to_dbtable(conn):
    fn = "ht_copy_to_dbtable('{}', '{}', cur)".format(rnaset.htseq_file, 
            rnaset.htseq_table)
    hl.batch_fn_thdir(rnaset.th_resdirpath, rnaset.htseq_dir, rnaset.res_sample_glob, conn, fn)

def batch_ht_gene_subset(conn, gene_subset_table):
    fn = "join_table(cur, berkid, '{}', '{}')".format(rnaset.htseq_table,
        gene_subset_table)
    print(fn)
    hl.batch_fn_thdir(rnaset.th_resdirpath, rnaset.htseq_dir, rnaset.res_sample_glob, conn, fn)

def main():
    # Settings for logging.
    logpath = os.path.join(rnaset.th_resdirpath,  '{}_{}'.format(curtime, 
        rnaset.htseq_log_file))
    rl.logginginfo(logpath)
    
    if args.htseqcount:
        #conn = False
        conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
        logging.info('Running htseq-count')
        batch_run_htseq(conn)

    if args.copytodb:
        logging.info('Copying to database')
        #conn = psycopg2.connect("dbname=rnaseq user=andrea")
        conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
        batch_ht_add_berkid(conn)
        batch_ht_copy_to_dbtable(conn)
        conn.commit()
        conn.close()

    if args.genesubset:
        logging.info('Generating htseq-count file for {}'.format(args.genesubset))
        #conn = psycopg2.connect("dbname=rnaseq user=andrea")
        conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
        batch_ht_gene_subset(conn, args.genesubset)
        conn.commit()
        conn.close()

print('Type -h for help')
if __name__ == '__main__':
    main()

#batch_edger_pairwise_DE(EXPTLIST, CTRL)
#groups_edger_DE()
#add_htseq_counts('htseq_count_results_bam2')
