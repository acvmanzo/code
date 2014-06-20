import logging
import correlationlib as cl
import cmn.cmn as cmn
import rnaseqdirlib as rdl
import os
import psycopg2
import glob
import sys
import de_settings


"htseq-count -f bam -s no -t gene -i Name accepted_hits.bam /home/andrea/rnaseqanalyze/references/dmel-all-filtered-r5.57-nofa.gff > htseq_count_results_bam2"


#samtools view -o accepted_hits.sam accepted_hits.bam

ALIGN_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat'
TOPHAT_DIR = 'tophat_out'
EDGER_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR'

GFF_FILE = '/home/andrea/rnaseqanalyze/references/dmel-r5.57/dmel-all-filtered-r5.57-nofa.gff'
ALIGN_FILE_BAM = 'accepted_hits.bam'
INFOFILE = 'htseq.info'

INFODBTABLE = 'autin'




def batch_run_htseq():
    os.chdir(ALIGN_DIR)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])

    for resdir in resdirs:
        os.chdir(os.path.join(resdir, TOPHAT_DIR))
        if os.path.exists(COUNTFILE):
            print('file exists')
            os.remove(COUNTFILE)
        else:
            print('no file')

        cmd = 'htseq-count -f bam -s no -t gene -i Name accepted_hits.bam {} > {}'.format(GFF_FILE, COUNTFILE)
        print(os.path.basename(resdir))
        os.system(cmd)
        with open(INFOFILE, 'w') as f:
            f.write(cmd)


def add_htseq_counts(htseqfile):
    counts = 0 
    with open(htseqfile, 'r') as f:
        for l in f:
            gene, count = l.split('\t')
            #if '__' in gene:
                #continue
            counts += int(count)
    print(counts)


def get_cufflink_path(berkid, exp_results_dir, exp_dir, berkid_fpkm_file):
    '''Returns the path to an experiment fpkm file given a berkid'''
    return(os.path.join(get_sample_results_dir(berkid, exp_results_dir),
        exp_dir, berkid_fpkm_file))



def count_add_berkid():
    if os.path.exists(COUNTFILE):
        cl.add_berkid(berkid, COUNTFILE, COUNTFILE + '_berkid')

def batch_fn(conn, fn):
    os.chdir(ALIGN_DIR)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        cur = conn.cursor()
        print(resdir)
        os.chdir(os.path.join(resdir, TOPHAT_DIR))
        berkid = os.path.basename(resdir)
        print(berkid)
        eval(fn)
        cur.close()

def batch_get_select_genes(conn):
    os.chdir(ALIGN_DIR)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        cur = conn.cursor()
        os.chdir(os.path.join(resdir, TOPHAT_DIR))
        berkid = os.path.basename(resdir)
        print(berkid)
        join_table(cur, berkid, 'htseq', 'prot_coding_genes', 'htseqtemp')
        cur.close()

def batch_copy_to_dbtable(conn):
    os.chdir(ALIGN_DIR)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        cur = conn.cursor()
        os.chdir(os.path.join(resdir, TOPHAT_DIR))
        berkid = os.path.basename(resdir)
        print(berkid)
        cl.copy_to_dbtable(COUNTFILE+'_berkid', 'htseq', cur)
        cur.close()


def gen_joincmd(berkid, dbtable, gene_subset_table, view):
    '''returns a string with a command for joining tables.
    the joined table contains htseq values from the table dbtable for genes 
    specified in the gene_subset_table 
    '''
    
    if gene_subset_table:
        gsstring = 'inner join {} as t2 on t0.gene_name = t2.gene_short_name'.format(gene_subset_table)
    else:
        gsstring = ''

    joinandcopycmd = "drop table {3}; create table {3} as select gene_name, counts, t0.berkid from {0} as t0 {1} where t0.berkid = '{2}' order by gene_short_name;".format(dbtable, gsstring, berkid, view)
    logging.debug('%s', joinandcopycmd)
    return(joinandcopycmd)

def join_table(cur, berkid, dbtable, gene_subset_table, newtable):
    cmd = gen_joincmd(berkid, dbtable, gene_subset_table, newtable)
    print(cmd)
    cur.execute(cmd)
    newfile = 'htseqcount_{}'.format(gene_subset_table)
    with open(newfile, 'w') as f:
        cur.copy_to(f, newtable)
    



#conn = psycopg2.connect("dbname=rnaseq user=andrea")
##batch_copy_to_dbtable(cur)
#batch_get_select_genes(conn)
#conn.commit()
#conn.close()

#batch_edger_pairwise_DE(EXPTLIST, CTRL)
#groups_edger_DE()
#add_htseq_counts('htseq_count_results_bam2')

