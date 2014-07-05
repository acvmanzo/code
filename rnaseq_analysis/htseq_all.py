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
        help='make new file of htseq-count results for a subset of genes')
args = parser.parse_args()


logging.basicConfig(filename=RNASEQDICT['th_log_file'], 
        format='%(asctime)s %(levelname)s %(message)s', 
        datefmt='%m/%d/%Y_%I-%M-%S %p', 
        filemode='w', 
        level=logging.INFO)
console = logging.StreamHandler() # Displays output to screen.
logging.getLogger('').addHandler(console)


def batch_run_htseq(conn):
    fn = "run_htseq('{}', '{}', '{}', '{}', '{}')".format(HTSEQ_DIR, HTSEQ_FILE, BAM_FILE, GFF_PATH_NOFA, HTSEQ_CMD_FILE)
    print(fn)
    batch_fn_thdir(TH_RESDIRPATH, TH_DIR, RES_SAMPLE_GLOB, conn, fn)



if args.htseqcount:
    conn = False
    print('Running htseq-count')
    #hl.batch_run_htseq(conn)

if args.copytodb:
    print('Copying to database')
    #conn = psycopg2.connect("dbname=rnaseq user=andrea")
    #hl.batch_ht_add_berkid(conn)
    #hl.batch_ht_copy_to_dbtable(conn)
    #conn.commit()
    #conn.close()

if args.genesubset:
    print('Generating htseq-count file for {}'.format(args.genesubset))
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    hl.batch_ht_gene_subset(conn, args.genesubset)
    conn.commit()
    conn.close()

#batch_edger_pairwise_DE(EXPTLIST, CTRL)
#groups_edger_DE()
#add_htseq_counts('htseq_count_results_bam2')
