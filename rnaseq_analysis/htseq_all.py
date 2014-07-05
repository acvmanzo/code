import libs.htseqlib as hl
import psycopg2
import argparse
import logging
from rnaseq_analysis/rnaseq_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('-ht', '--htseqcount', action='store_true', 
        help='run htseq-count')
parser.add_argument('-c', '--copytodb', action='store_true', 
        help='copy htseq-count results to database')
parser.add_argument('-s', '--genesubset', 
        help='make new file of htseq-count results for the given subset of genes')
args = parser.parse_args()


def batch_run_htseq(conn):
    fn = "run_htseq('{}', '{}', '{}', '{}', '{}')".format(HTSEQ_DIR, HTSEQ_FILE, BAM_FILE, GFF_PATH_NOFA, HTSEQ_CMD_FILE)
    hl.batch_fn_thdir(TH_RESDIRPATH, TH_DIR, RES_SAMPLE_GLOB, conn, fn)

def batch_ht_add_berkid(conn):
    fn = "htseq_add_berkid(berkid, '{}')".format(HTSEQ_FILE)
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)

def batch_ht_copy_to_dbtable(conn):
    fn = "ht_copy_to_dbtable('{}', '{}', cur)".format(HTSEQ_FILE, HTSEQ_TABLE)
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)

def batch_ht_gene_subset(conn, gene_subset_table):
    fn = "join_table(cur, berkid, '{}', '{}')".format(HTSEQ_TABLE,
        gene_subset_table)
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)

def main():
    logging.basicConfig(filename=RNASEQDICT['htseq_log_file'], 
            format='%(asctime)s %(levelname)s %(message)s', 
            datefmt='%m/%d/%Y_%I-%M-%S %p', 
            filemode='w', 
            level=logging.DEBUG)
    console = logging.StreamHandler() # Displays output to screen.
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    if args.htseqcount:
        conn = False
        logging.info('Running htseq-count')
        hl.batch_run_htseq(conn)

    if args.copytodb:
        logging.info('Copying to database')
        conn = psycopg2.connect("dbname=rnaseq user=andrea")
        hl.batch_ht_add_berkid(conn)
        hl.batch_ht_copy_to_dbtable(conn)
        conn.commit()
        conn.close()

    if args.genesubset:
        logging.info('Generating htseq-count file for {}'.format(args.genesubset))
        conn = psycopg2.connect("dbname=rnaseq user=andrea")
        hl.batch_ht_gene_subset(conn, args.genesubset)
        conn.commit()
        conn.close()

if __name__ == '__main__':
    main()

#batch_edger_pairwise_DE(EXPTLIST, CTRL)
#groups_edger_DE()
#add_htseq_counts('htseq_count_results_bam2')
