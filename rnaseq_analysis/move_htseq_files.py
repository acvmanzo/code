# Moves htseq_files from one folder to another.

import libs.htseqlib as htl
from rnaseq_settings import *
import psycopg2

def batch_move_htseq_files(conn):
    fn = "move_htseq_files('{}', '{}')".format(HTSEQ_DIR, HTSEQ_FILE)
    htl.batch_fn_thdir(TH_RESDIRPATH, TH_DIR, RES_SAMPLE_GLOB, conn, fn)

conn = psycopg2.connect("dbname=rnaseq user=andrea")
batch_move_htseq_files(conn)
conn.commit()
conn.close()
