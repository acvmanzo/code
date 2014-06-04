#! /usr/bin/env python

# Script for combining multiple files containing behaviorl data into one 
# file (more general than combineagdata.py)

import numpy as np
import os
import sys

print('newfile, basename, #files+1')
COMBFILE = sys.argv[1] # Name of combined file
BNAME = sys.argv[2] # Base name of the data files
NFILES = sys.argv[3] # Number of files to combine + 1

def combinedata(newfile, basename, nfiles):

    nums = np.arange(1, int(nfiles)) # Number of data files.
    files = ['{0}{1}.csv'.format(basename, n) for n in nums] # List of data files.

    if os.path.exists(newfile) == True:
        os.remove(newfile)

    # Rewrites the content of the data files into 1 combined file.
    with open(newfile, 'a') as g:
        for fil in files:
            
            with open(fil) as f:
                #f.next()
                #f.next()
                for l in f:
                    g.write(l)
            g.write('\n')
                    


combinedata(COMBFILE, BNAME, NFILES)
