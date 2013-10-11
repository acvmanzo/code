#! /usr/bin/env python

# This executable file sorts MTS files from the 'newmovies/' folder into 
# individual folders in the directory WINGDETDIR.

from mtslib import *
from wingsettings import *

#Run from aggression/newmovies/ folder.

print('1-start (s), 2-dur (s) 3-specdur; yes or no; 4-overwrite; yes or no')

EXT = sys.argv[1] # Extension of images
OVERWRITE = sys.argv[2] # Overwrite image sequence? 'yes' or 'no'

exptsdir = b_sortmtsexpt('.', WINGDETBASE, EXPTSBASE)
os.chdir(exptsdir)
#convmovies(fdir=exptsdir, specdur1='no', start1=0, start1=0, specdur2='yes', 
#start2=0, dur2=240, ext=EXT, removeavi='yes', movbase=MOVBASE, 
#num=5, qscale=3)
convmovies(fdir=exptsdir, specdur1='yes', start1=0, dur1=1, specdur2='yes', 
start2=0, dur2=1, ext=EXT, overwrite=OVERWRITE, removeavi='yes', movbase=MOVBASE, 
num=5, qscale=3)
