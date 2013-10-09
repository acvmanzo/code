#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the default ROI parameters. This should be run 


from partimlib import *
import mtslib as ml
import bgsublib as bl

BGFILE = 'background.tif'
PICKLEBASE = 'pickled'
TEXTBASE = 'text'

#defaultwells(bgfile=BGFILE, pickledir=PICKLEBASE, textdir=TEXTBASE)
#ml.convmovies('.', 0, 1, 'yes', 'no')
#ml.convmovie('cs_20130619_ag_A_l_1.MTS', 'cs_20130619_ag_A_l_1.MTS.avi', 0, 
#60, 'yes')
bl.subbgmovies()
(fdir, submovbase, movbase, picklebase, nframes, fntype, 
boverwrite='no'):
