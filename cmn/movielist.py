#! /usr/bin/env python

import os
import glob
import mn.cmn.cmn as cmn

files = []
with open('moviematch.txt', 'r') as f:
    f.next()
    for l in f:
        f, m24, m32 = l.split(',')[0:3]
        m24 = m24.rstrip('.fmf')
        m32 = m32.rstrip('.fmf')
        files.append('"'+m24 +'/" ,')
        files.append('"'+m32 +'/" ,')

files.reverse()
with open('movielist.txt', 'w') as g:
    for f in files:
        g.write(f + '\n')
    

cmn.makenewdir('data_cibarea')
cmn.makenewdir('cibroijpgs')
