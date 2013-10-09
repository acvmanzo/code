#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the default ROI parameters. This should be run 


from partimlib import *

BGFILE = 'background.tif'
PICKLEBASE = 'pickled'
TEXTBASE = 'text'

b_defaultwells(fdir='.', bgfile=BGFILE, picklebase=PICKLEBASE, textbase=TEXTBASE)
