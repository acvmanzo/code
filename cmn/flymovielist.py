#! /usr/bin/env python

import os
import glob
import mn.cmn.cmn as cmn

files = []
with open('flymovies.txt', 'r') as f:
   
    for l in f:
        m = l.rstrip('.fmf\n')
        files.append('"'+m+'/" ,')

files.reverse()
with open('movielist.txt', 'w') as g:
    for f in files:
        g.write(f + '\n')
    

