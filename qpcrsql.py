import itertools
import psycopg2
import numpy as np
import datetime


conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()



def primertogene():
    d = {}
    cur.execute("SELECT gene, primer FROM qpcr_primers WHERE primer is not Null ORDER BY gene;")
    allrows = cur.fetchall()
    for r in allrows:
        d[r[1]] = r[0]

    d['cg34127-gp1'] = 'CG34127'
    d['nrxi-gp1'] = 'NrxI'
    d['betaintnu3'] = 'Bintnu'
    d['bintnu-M'] = 'Bintnu'
    d['pten-R'] = 'pten'
    d['bintnu-gp1'] = 'Bintnu'
    d['pten-Ryan'] = 'pten' 
    d['NrxI-Takeo'] = 'NrxI' 
    return d

dp2g = primertogene()
cur.execute("select primer from qpcr_primers where used_primer is True;")
primerlist = cur.fetchall()
print primerlist


reference = 'GAPDH'
exptd = '2014-02-26'

fname = '2014-0226_1_mut_andrea.csv'
cur.execute("SELECT target FROM qpcr_mut WHERE exptd = '{0}';".format(exptd))
targets = [t[0] for t in cur.fetchall()]
uniquet = set(targets)

#def getcqdict(sqlstring, targetlist):
    #d = {}
    #for t in targetlist:
        #print t
        #cur.execute(sqlstring)
        #d[t] = [cq[0] for cq in cur.fetchall()]
    #return d



# Getting CQs of target and reference gene expression in CS flies.
d_cs_cq = {}

for t in uniquet:
    cur.execute("SELECT cq FROM qpcr_mut WHERE exptd = '{0}' AND target = '{1}' AND sample ~* 'CS';".format(exptd, t))
    d_cs_cq[t] = [cq[0] for cq in cur.fetchall()]
print 'CS flies', d_cs_cq

#ss_cs_cq = "SELECT cq FROM qpcr_mut WHERE exptd = '{0}' AND target = '{1}' AND sample ~* 'CS';".format(exptd, t)
#d_cs_cq = getcqdict(ss_cs_cq, uniquet)
#print d_cs_cq


# Getting CQs of target gene expression in mutant flies.
d_mut_cq = {}
for t in uniquet:
    gene = dp2g[t]
    if gene == 'GAPDH':
        continue
    cur.execute("SELECT cq FROM qpcr_mut WHERE exptd = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptd, t, gene))
    d_mut_cq[t] = [cq[0] for cq in cur.fetchall()]
print 'Target genes, mutant flies', d_mut_cq

# Getting CQs of reference gene expression in mutant flies.
d_ref_mut_cq = {}
for t in uniquet:
    gene = dp2g[t]
    if gene == 'GAPDH':
        continue
    cur.execute("SELECT cq FROM qpcr_mut WHERE exptd = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptd, reference, gene))
    d_ref_mut_cq[gene] = [cq[0] for cq in cur.fetchall()]

print 'Ref gene, mutant flies', d_ref_mut_cq

# Writing the reference gene and target gene CQs in CS flies to a file.
ref_CS = d_cs_cq[reference]
for t in uniquet:
    if t == 'GAPDH':
        continue
           
    gname = '{0}_{1}_{2}_cs.txt'.format(reference, t, exptd)
    with open(gname, 'w') as g:
        mut_CS = d_cs_cq[t]
        ref_mut_CS = zip(ref_CS, mut_CS)
        for rcq, mcq in ref_mut_CS:
            g.write('{0},{1}\n'.format(rcq, mcq))

# Writing the reference gene and target gene CQs in mutant flies to a file.
for t in uniquet:
    if t == 'GAPDH':
        continue
    gname = '{0}_{1}_{2}_mut.txt'.format(reference, t, exptd)
    with open(gname, 'w') as g:
        
        gene = dp2g[t]
        ref_mut = d_ref_mut_cq[gene]
        mut_mut = d_mut_cq[t]
        ref_mut_mut = zip(ref_CS, mut_CS)
        for rcq, mcq in ref_mut_mut:                
            g.write('{0},{1}\n'.format(rcq, mcq))
                                     
