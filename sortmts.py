#! /usr/bin/env python

# This executable file sorts MTS files from the 'newmovies/' folder into 
# individual folders in the directory WINGDETDIR.

from mtslib import *

#Run from aggression/newmovies/ folder.
EXPTDIR = os.path.join(cmn.defpardir(),'wingdet', 'expts')

print('1-start (s), 2-dur (s) 3-specdur; yes or no; 4-overwrite; yes or no')

START = sys.argv[1] # Number of seconds into movie before conversion begins.
DUR = sys.argv[2] # Duration of conversion in seconds.
SPECDUR = sys.argv[3] # Duration of conversion specified? 'yes' or 'no'
OVERWRITE = sys.argv[4] # Overwrite image sequence? 'yes' or 'no'

sortmtsdir(params=EXPTDIR)
os.chdir(EXPTDIR)
convmovies(fdir=EXPTDIR, start=START, dur=DUR, specdur=SPECDUR, 
overwrite=OVERWRITE)
