import shutil
import logging
import libs.rnaseqlib as rl
import cmn.cmn as cmn
import libs.rnaseqlib as rl
import os
import psycopg2
import glob
import sys
from rnaseq_analysis.rnaseq_settings import *


"htseq-count -f bam -s no -t gene -i Name accepted_hits.bam /home/andrea/rnaseqanalyze/references/dmel-all-filtered-r5.57-nofa.gff > htseq_count_results_bam2"


#samtools view -o accepted_hits.sam accepted_hits.bam

#ALIGN_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat'
#TH_DIR = 'tophat_out'
#EDGER_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR'

#GFF_FILE = '/home/andrea/rnaseqanalyze/references/dmel-r5.57/dmel-all-filtered-r5.57-nofa.gff'
#ALIGN_FILE_BAM = 'accepted_hits.bam'
#INFOFILE = 'htseq.info'

#INFODBTABLE = 'autin'

#SAMPLE_GLOB = 'RG*'


def batch_fn_thdir(th_resdirpath, tophat_dir, globstring, conn, fn):
    print('running batch')
    os.chdir(th_resdirpath)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob(globstring)])
    for resdir in resdirs:
        cur = conn.cursor()
        print(resdir)
        os.chdir(os.path.join(resdir, tophat_dir))
        berkid = os.path.basename(resdir)
        print(berkid)
        eval(fn)
        cur.close()

#def batch_fn(conn, fn):
    #os.chdir(ALIGN_DIR)
    #resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    #for resdir in resdirs:
        #cur = conn.cursor()
        #print(resdir)
        #os.chdir(os.path.join(resdir, TH_DIR))
        #berkid = os.path.basename(resdir)
        #print(berkid)
        #eval(fn)
        #cur.close()

def run_htseq(htseq_dir, htseq_file, bamfile, gff_file, htseq_cmd_file):
    '''Runs htseq-count from inside the tophat_out directory.
    htseq_dir = directory with results of htseq-count
    htseq_file = name of file with htseq-count results
    bamfile = alignment bam file output by Tophat
    gff_file = gff file used for counts
    htseq_cmd_file = file with htseq command used
    '''
    htseq_dirpath = os.path.join(os.path.dirname(os.getcwd()), htseq_dir)
    cmn.makenewdir(htseq_dirpath)
    htseq_path = os.path.join(htseq_dirpath, htseq_file)

    if os.path.exists(htseq_path):
        pass
        #print('Removing existing file')
        #os.remove(htseq_path)
    else:
        print('Creating new file')

        cmd = 'htseq-count -f bam -s no -t gene -i Name {} {} > {}'.format(bamfile, gff_file, htseq_path)

        os.system(cmd)
        with open(htseq_cmd_file, 'w') as f:
            f.write(cmd)


def batch_run_htseq(conn):
    fn = "run_htseq('{}', '{}', '{}', '{}', '{}')".format(HTSEQ_DIR, HTSEQ_FILE, BAM_FILE, GFF_PATH_NOFA, HTSEQ_CMD_FILE)
    print(fn)
    batch_fn_thdir(TH_RESDIRPATH, TH_DIR, RES_SAMPLE_GLOB, conn, fn)

#def batch_run_htseq(conn):
    #os.chdir(ALIGN_DIR)
    #resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])

    #for resdir in resdirs:
        #os.chdir(os.path.join(resdir, TH_DIR))
        #if os.path.exists(COUNTFILE):
            #print('file exists')
            #os.remove(COUNTFILE)
        #else:
            #print('no file')

        #cmd = 'htseq-count -f bam -s no -t gene -i Name accepted_hits.bam {} > {}'.format(GFF_FILE, COUNTFILE)
        #print(os.path.basename(resdir))
        #os.system(cmd)
        #with open(INFOFILE, 'w') as f:
            #f.write(cmd)


def add_htseq_counts(htseqfile):
    '''Adds up the counts found in the htseq-count file.
    '''
    counts = 0 
    with open(htseqfile, 'r') as f:
        for l in f:
            gene, count = l.split('\t')
            #if '__' in gene:
                #continue
            counts += int(count)
    print(counts)


def htseq_add_berkid(berkid, htseq_file):
    if os.path.exists(htseq_file):
        rl.add_berkid(berkid, htseq_file)

def batch_ht_add_berkid(conn):
    fn = "htseq_add_berkid(berkid, '{}')".format(HTSEQ_FILE)
    batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)

#def batch_get_select_genes(conn):
    #os.chdir(ALIGN_DIR)
    #resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    #for resdir in resdirs:
        #cur = conn.cursor()
        #os.chdir(os.path.join(resdir, TH_DIR))
        #berkid = os.path.basename(resdir)
        #print(berkid)
        #join_table(cur, berkid, 'htseq', 'prot_coding_genes', 'htseqtemp')
        #cur.close()

def ht_copy_to_dbtable(htseqfile, htseqdbtable, cur):
    '''Copies the results of htseqcount from the file htseqpath into the table
    htseqdbtable using the cursor cur'''
    rl.copy_to_dbtable(htseqfile+'_berkid', htseqdbtable, cur)

def batch_ht_copy_to_dbtable(conn):
    fn = "ht_copy_to_dbtable('{}', '{}', cur)".format(HTSEQ_FILE, HTSEQ_TABLE)
    batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)


def gen_joincmd(berkid, dbtable, gene_subset_table):
    '''Returns a string with a command for joining tables.
    The joined table newtable contains htseq values from sample berkid
    from the table dbtable containing htseq data for genes specified in the 
    gene_subset_table.
    '''
   
    if gene_subset_table:
        gsstring = 'inner join {} as t2 on t0.gene_name = t2.gene_short_name'.format(gene_subset_table)
    else:
        gsstring = ''
    
    newtable = dbtable + '_' + gene_subset_table
    joinandcopycmd = "drop table {3}; create table {3} as select gene_name, counts, t0.berkid from {0} as t0 {1} where t0.berkid = '{2}' order by gene_short_name;".format(dbtable, gsstring, berkid, newtable)
    logging.debug('%s', joinandcopycmd)
    return(joinandcopycmd, newtable)


def join_table(cur, berkid, dbtable, gene_subset_table):
    '''Executes the join command given by gen_joincmd, and writes table to 
    file.
    '''
    cmd, newtable = gen_joincmd(berkid, dbtable, gene_subset_table)
    print(cmd)
    cur.execute(cmd)
    newfile = 'htseqcount_{}'.format(gene_subset_table)
    with open(newfile, 'w') as f:
        cur.copy_to(f, newtable)
    

def batch_ht_gene_subset(conn, gene_subset_table):
    fn = "join_table(cur, berkid, '{}', '{}')".format(HTSEQ_TABLE,
        gene_subset_table)
    batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)


def move_htseq_files(htseq_dir, htseq_file):
    '''Initially saved htseqcount files in the tophat_out directory in each
    sample directory. Script moves files into a htseq_out directory at the
    same level as tophat_out. Run from the tophat_out/ directory.'''

    htseq_dirpath = os.path.join(os.path.dirname(os.getcwd()), htseq_dir)
    cmn.makenewdir(htseq_dirpath)
    htseq_path = os.path.join(htseq_dirpath, htseq_file)
    
    htfiles = glob.glob('htseq*')
    for ht in htfiles:
        shutil.move(ht, htseq_dirpath)

def batch_move_htseq_files():
    fn = "move_htseq_files('{}', '{}')".format(HTSEQ_DIR, HTSEQ_FILE)
    batch_fn_thdir(TH_RESDIRPATH, HTSEQ_DIR, RES_SAMPLE_GLOB, conn, fn)
