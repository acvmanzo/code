#! /usr/bin/env python

import numpy as np
import os
import glob

#COMBFILE = '20131119_agdata_wms_all.csv' # Name of combined file
#BNAME = '20131119_agdata_wms_part' # Base name of the data files

COMBFILE = '../2014-0416_agdata_autlines_all.csv' # Name of combined file
#BNAME = '20131024_agdata_autlines_part' # Base name of the data files

#nums = np.arange(1, 3) # Number of data files.
#files = ['{0}{1}.csv'.format(BNAME, n) for n in nums] # List of data files.


if os.path.exists(COMBFILE) == True:
    os.remove(COMBFILE)

files = sorted(glob.glob('*.csv'))
# Rewrites the content of the data files into 1 combined file.

with open(COMBFILE, 'a') as g:
    for fil in files:
        
        with open(fil) as f:
            f.next()
            f.next()
            for l in f:
                g.write(l)
        g.write('\n')
                
            

