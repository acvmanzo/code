import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.edgeRlib as el
from rnaseq_settings import *
from edgeR_settings import *
import psycopg2
import os
import argparse 



def remove_htseqcount_files(conn):
    'Removes old htseqcount files.'''
    fn = "print(os.getcwd()), os.remove('htseqcount_brain_aut_will_r557_ralph_mt_excluded')"
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)
    conn.close()


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--genesubset', 
        help='run edgeR analysis on subset of genes')
args = parser.parse_args()


#gene_subset = 'prot_coding_genes'
#gene_subset = 'bwa_r557'
#gene_subset = 'bwa_r557_ralph_mt_ex'

# Runs edgeR.
if args.genesubset:
    gene_subset = args.genesubset
else:
    gene_subset = False

#Runs edgeR analysis on the indicated groups.
#el.batch_edger_pairwise_DE(MALES, MALES_CTRL, gene_subset, RNASEQDICT)
#el.batch_edger_pairwise_DE(FEMALES, FEMALES_CTRL, gene_subset, RNASEQDICT)
#el.edger_2groups_DE(AGG_DICT_ALL, gene_subset, RNASEQDICT)
#el.edger_2groups_DE(AGG_DICT_CS, gene_subset, RNASEQDICT)

#Generates files formatted so they can be copied to the database.
#for params in [male_params, female_params, agg_params]:
    #dirs, group1list, group2list = params
    #batch_db_degenefile(DEGENEDIR, DEGENEFILE, DB_DEGENEFILE, dirs, 
    #group1list, group2list, 'edgeR')

#Copies DE gene data to the database.
#conn = psycopg2.connect("dbname=rnaseq user=andrea")
#batch_copy_dbgenes_to_db(DEGENEDIR, conn, DB_DEGENEFILE, 'degenes')
#conn.commit()
#conn.close()
##conn.commit()
#conn.close()
