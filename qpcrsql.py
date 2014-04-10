import glob
import itertools
import psycopg2
import numpy as np
import datetime
from libs.qrtpcrlib import primertogene

#exptid = '2014-0226_1'
#FNAME = '2014-0226_1_mut_andrea.csv'
REFERENCE = 'GAPDH'
RESDIR = '/home/andrea/Documents/lab/qRT-PCR/2_results/mut/'

conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

def get_good_primers():
# Get list of good primers 
    dp2g = primertogene()
    cur.execute("select primer from qpcr_primers where used_primer is True;")
    primerlist = [p[0] for p in cur.fetchall()]
    return primerlist


def get_targets(exptid):
    # For one experiment, get a list of targets (i.e., primers).
    cur.execute("SELECT target FROM qpcr_mut WHERE exptid = '{0}';".format(exptid))
    targets = [t[0] for t in cur.fetchall()]
    uniquet = set(targets)
    return uniquet


def getcqdict(gensqlstring, targetlist):
    d = {}
    for t in targetlist:
        print t
        gene = primertogene()[t]
        cur.execute(gensqlstring(exptid, t, gene))
        d[t] = [cq[0] for cq in cur.fetchall()]
    return d


def sqlsearch_t_ref_CS(exptid, t, gene):
    # Getting CQs of target and reference gene expression in CS flies.

    sqlsearch = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* 'CS';".format(exptid, t)
    return sqlsearch

    
def sqlsearch_t_mut(exptid, t, gene):
    # Getting CQs of target gene expression in mutant flies.

    sqlsearch = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptid, t, gene)
    return sqlsearch


def sqlsearch_ref_mut(exptid, t, gene):
 #Getting CQs of reference gene expression in mutant flies.
    sqlsearch = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptid, REFERENCE, gene)
    return sqlsearch
    
#def getcqdict_t_ref_CS():
    #getcqdict(
#ss_cs_cq = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* 'CS';".format(exptid, t)
#d_cs_cq = getcqdict(ss_cs_cq, uniquet)
#print d_cs_cq


#d_mut_cq = {}
#for t in uniquet:
    #gene = dp2g[t]
    #if gene == 'GAPDH':
        #continue
    #cur.execute("SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptid, t, gene))
    #d_mut_cq[t] = [cq[0] for cq in cur.fetchall()]
#print 'Target genes, mutant flies', d_mut_cq

 #Getting CQs of reference gene expression in mutant flies.
#d_ref_mut_cq = {}
#for t in uniquet:
    #gene = dp2g[t]
    #if gene == 'GAPDH':
        #continue
    #cur.execute("SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptid, reference, gene))
    #d_ref_mut_cq[gene] = [cq[0] for cq in cur.fetchall()]

#print 'Ref gene, mutant flies', d_ref_mut_cq

def write_t_ref_CS(d_t_ref_CS):
   
    #Writing the reference gene and target gene CQs in CS flies to a file.
    
    ref_CS = d_t_ref_CS[REFERENCE]
    for t in d_t_ref_CS:
        if t == 'GAPDH':
            continue
        gname = RESDIR + '{0}_{1}_{2}_cs.txt'.format(t, REFERENCE, exptid)
        with open(gname, 'w') as g:
            g.write('Ref_cq,Target_cq\n')
            mut_CS = d_t_ref_CS[t]
            ref_mut_CS = zip(ref_CS, mut_CS)
            for rcq, mcq in ref_mut_CS:
                g.write('{0},{1}\n'.format(rcq, mcq))

def write_t_ref_mut(d_t_mut, d_ref_mut):
    
    #Writing the reference gene and target gene CQs in mutant flies to a file.
    for t in d_t_mut.keys():
        if t == 'GAPDH':
            continue
        gname = RESDIR + '{0}_{1}_{2}_mut.txt'.format(t, REFERENCE, exptid)
        with open(gname, 'w') as g:
            g.write('Ref_cq,Target_cq\n')
            gene = primertogene()[t]
            ref_mut = d_ref_mut[t]
            mut_mut = d_t_mut[t]
            ref_mut_mut = zip(ref_mut, mut_mut)
            for rcq, mcq in ref_mut_mut:                
                g.write('{0},{1}\n'.format(mcq, rcq))

fnames = glob.glob('*.csv')
for fname in fnames:
    exptid = fname.split('_mut_')[0]

    targets = get_targets(exptid)
    write_t_ref_CS(getcqdict(sqlsearch_t_ref_CS, targets))
    d_ref_mut = getcqdict(sqlsearch_ref_mut, targets)
    d_t_mut = getcqdict(sqlsearch_t_mut, targets)
    write_t_ref_mut(d_t_mut, d_ref_mut)


