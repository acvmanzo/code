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
    
    return d


cur.execute("select primer from qpcr_primers where used_primer is True;")
primerlist = cur.fetchall()
print primerlist

reference = 'GAPDH'
sample = 'CG34127'
exptd = '2014-02-26'

fname = '2014-0226_1_mut_andrea.csv'
cur.execute("SELECT target FROM qpcr_mut WHERE exptd = '{0}';".format(exptd))
targets = [t[0] for t in cur.fetchall()]


uniquet = set(targets)
print uniquet

for t in uniquet:
    cur.execute("SELECT target, cq FROM qpcr_mut WHERE exptd = '{0}' AND target = '{1}';".format(exptd, t))
    cqs = cur.fetchall()
    print cqs
