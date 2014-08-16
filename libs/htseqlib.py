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

def batch_fn_thdir(th_resdirpath, tophat_dir, globstring, conn, fn):
    logging.info('running batch')
    os.chdir(th_resdirpath)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob(globstring)])
    print(conn)
    for resdir in resdirs:
        cur = conn.cursor()
        logging.info(resdir)
        os.chdir(os.path.join(resdir, tophat_dir))
        berkid = os.path.basename(resdir)
        logging.info(berkid)
        print(fn)
        eval(fn)
        cur.close()

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
    htseq_cmd_path = os.path.join(htseq_dirpath, htseq_cmd_file)

    if os.path.exists(htseq_path):
        pass
        #logging.info('Removing existing file')
        #os.remove(htseq_path)
    else:
        logging.info('Creating new file')

        #cmd = 'htseq-count -f bam -s no -t gene -i Name {} {} > {}'.format(bamfile, gff_file, htseq_path)
        #cmd = 'htseq-count -f bam -s no -t exon -i Name {} {} > {}'.format(bamfile, gff_file, htseq_path)
        #cmd = 'htseq-count -f bam -s yes -t gene -i Name {} {} > {}'.format(bamfile, gff_file, htseq_path)
        cmd = 'htseq-count -f bam -s yes -t Parent -i Name {} {} > {}'.format(bamfile, gff_file, htseq_path)
        logging.debug(cmd)
        os.system(cmd)
        with open(htseq_cmd_path, 'w') as f:
            f.write(cmd)


def htseq_add_berkid(berkid, htseq_file):
    berkidfile = htseq_file + '_berkid'
    if os.path.exists(htseq_file):
        rl.add_berkid(berkid, htseq_file, berkidfile)

def ht_copy_to_dbtable(htseqfile, htseqdbtable, cur):
    '''Copies the results of htseqcount from the file htseqpath into the table
    htseqdbtable using the cursor cur'''
    rl.copy_to_dbtable(htseqfile+'_berkid', htseqdbtable, cur)


def gen_joincmd(berkid, dbtable, gene_subset_table):
    '''Returns a string with a command for joining tables.
    The joined table newtable contains htseq values from sample berkid
    from the table dbtable containing htseq data for genes specified in the 
    gene_subset_table.
    '''
   
    if gene_subset_table:
        gsstring = 'inner join {} as t2 on t0.gene_short_name = t2.gene_short_name'.format(gene_subset_table)
    else:
        gsstring = ''
    
    newtable = dbtable + '_' + gene_subset_table


    joinandcopycmd = "create table {3} as select gene_short_name, counts, t0.berkid from {0} as t0 {1} where t0.berkid = '{2}' order by gene_short_name;".format(dbtable, gsstring, berkid, newtable)
    logging.debug('%s', joinandcopycmd)
    return(joinandcopycmd, newtable)


def join_table(cur, berkid, dbtable, gene_subset_table):
    '''Executes the join command given by gen_joincmd, and writes table to 
    file.
    '''
    cmd, newtable = gen_joincmd(berkid, dbtable, gene_subset_table)
    if rl.check_table_exists(newtable, cur):
        cmd = "drop table {};".format(newtable) + cmd

    logging.debug(cmd)
    cur.execute(cmd)
    newfile = 'htseqcount_{}'.format(gene_subset_table)
    with open(newfile, 'w') as f:
        cur.copy_to(f, newtable)
    

def move_htseq_files(htseq_dir, htseq_file):
    '''Initially saved htseqcount files in the tophat_out directory in each
    sample directory. Script moves files into a htseq_out directory at the
    same level as tophat_out. Run from the tophat_out/ directory.'''

    htseq_dirpath = os.path.join(os.path.dirname(os.getcwd()), htseq_dir)
    cmn.makenewdir(htseq_dirpath)
    htseq_path = os.path.join(htseq_dirpath, htseq_file)
    print(htseq_dirpath)
    
    htfiles = glob.glob('htseq*')
    print(htfiles)
    for ht in htfiles:
        shutil.move(ht, htseq_dirpath)

def get_gene_count(cur, htseqtable, gene, berkid):
    '''For the given gene and berkid, finds the counts from the table 
    htseqtable.
    '''
    cmd = "SELECT * from {} where gene_short_name = '{}' and berkid = '{}';".format(htseqtable, gene, berkid)
    cur.execute(cmd)
    gene, count, berkid = cur.fetchall()[0]
    return(gene, count, berkid)
    #return(count)

def get_replicate_counts(cur, genotype, gene, sampleinfo_table, htseqtable):
    '''Gets the counts for each replicate of the given genotype, for the
    given gene from the given htseqtable.
    '''
    berkids = rl.get_replicate_berkid_dict(cur, genotype, sampleinfo_table)
    countslist = []
    for berkid in berkids:
        countslist.append(get_gene_count(cur, htseqtable, gene, berkid))
    return(countslist)

def compare_replicate_counts(cur, genotypes, gene, sampleinfo_table, htseqtable):
    '''For each genotype in the genotypes list, gives the counts for each
    replicate for the given gene.
    '''
    d = {}
    for gen in genotypes:
        d[gen] = get_replicate_counts(cur, gen, gene, sampleinfo_table, htseqtable)
    return(d)

    
