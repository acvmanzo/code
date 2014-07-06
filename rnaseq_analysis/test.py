import libs.rnaseqlib as rl
import libs.htseqlib as hl
import libs.edgeRlib as el
from rnaseq_settings import *
from edgeR_settings import *
import psycopg2
import os

table = 'htseq_prot_coding_genes'

conn = psycopg2.connect("dbname=rnaseq user=andrea")
#cur = conn.cursor()
#cur.close()

def remove_htseqcount_files(conn):
    fn = "print(os.getcwd()), os.remove('htseqcount_brain_aut_will_r557_ralph_mt_excluded')"
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)
    conn.close()

#print(list(el.get_metadata(conn, FEMALES, SAMPLEINFO_TABLE, 'prot_coding_genes')))

#gene_subset = 'prot_coding_genes'
#gene_subset = 'bwa_r557'
gene_subset = 'bwa_r557_ralph_mt_ex'
el.batch_edger_pairwise_DE(MALES, MALES_CTRL, EDGER_DIRPATH, EDGER_METADATA_FILE, 
        SAMPLEINFO_TABLE, gene_subset)
el.batch_edger_pairwise_DE(FEMALES, FEMALES_CTRL, EDGER_DIRPATH, 
        EDGER_METADATA_FILE, SAMPLEINFO_TABLE, gene_subset)
#conn.commit()
conn.close()
