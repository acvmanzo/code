# Rename files for use with Ryan's correlation script.

import os
import sys
import glob
import itertools
import psycopg2
import numpy as np
import datetime
import shutil
import cmn.cmn as cmn

conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

def renamefiles():
    cur.execute("select berkid, sample from autin where sample is not null order by berkid;")
    berksample = cur.fetchall()
    print berksample
    print len(berksample)
    d = {}
    for b, s in berksample:
        d[b] = s

    for k in sorted(d.keys()):
        print k, d[k]
        

    fnames = glob.glob('*.*')
    newdir = 'renamed_files'
    cmn.makenewdir(newdir)

    for fname in fnames:
        print fname
        new1fname = fname.replace('_report', '')
        berkid = fname.split('_')[0]
        sample = d[berkid]
        newfname = sample + '_' + new1fname
        newpath = os.path.join(newdir, newfname)
        print newpath 
        shutil.copy(fname, newpath)

def sepfiles(ext):
    
    pardir = '/home/andrea/Documents/lab/rsanalyze_me/'
    fnames = glob.glob('*.{0}'.format(ext))

    for fname in fnames:
        newdir = fname.split('_')[0] + fname.split('_')[1][0]
        newpath = os.path.join(pardir, newdir)
        cmn.makenewdir(newpath)
        shutil.copy(fname, newpath) 

#renamefiles()
sepfiles('txt')
sepfiles('xls')
