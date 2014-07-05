import libs.rnaseqlib as rl
import libs.htseqlib as hl
from rnaseq_settings import *
import psycopg2
import os

table = 'htseq_prot_coding_genes'

#conn = psycopg2.connect("dbname=rnaseq user=andrea")
#cur = conn.cursor()
#cmd = "SELECT EXISTS( SELECT 1 FROM   pg_catalog.pg_class c JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE  n.nspname = 'public' AND    c.relname = '{}');;".format(table)
#cur.execute(cmd)
#r = cur.fetchone()[0]
#print(r)
#print(r == True)

#r = rl.check_table_exists(table, cur)
#if r:
    #print('yup')

#cur.close()
#conn.commit()
#conn.close()

def batch_fn_thdir(th_resdirpath, tophat_dir, globstring, conn, fn):
    logging.info('running batch')
    os.chdir(th_resdirpath)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob(globstring)])
    for resdir in resdirs:
        cur = conn.cursor()
        logging.info(resdir)
        os.chdir(os.path.join(resdir, tophat_dir))
        berkid = os.path.basename(resdir)
        logging.info(berkid)
        cur.close()

def remove_htseqcount_files(conn):
    fn = "print(os.getcwd()), os.remove('htseqcount_brain_aut_will_r557_ralph_mt_excluded')"
    hl.batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)
    conn.close()
