#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the default ROI parameters. This should be run 


from partimlib import *

BGFILE = 'background.tif'
PICKLEBASE = 'pickled'
TEXTBASE = 'text'

print('1-overwrite? yes or no')
OVERWRITE = sys.argv[1] # Overwrite? 'yes' or 'no'


b_defaultwells(fdir='.', bgfile=BGFILE, picklebase=PICKLEBASE, 
textbase=TEXTBASE, boverwrite=OVERWRITE)
