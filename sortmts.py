#! /usr/bin/env python

# This executable file sorts MTS files from the 'newmovies/' folder into 
# individual folders in the directory WINGDETDIR.

from libs.mtslib import *
from wingsettings import *

#Run from aggression/newmovies/ folder.

print('1-image type; 2-overwrite; yes or no')

EXT = sys.argv[1] # Extension of images
OVERWRITE = sys.argv[2] # Overwrite image sequence? 'yes' or 'no'

print("Moving MTS files")
exptsdir = b_sortmtsexpt('.', WINGDETBASE, EXPTSBASE)
os.chdir(exptsdir)
print("Converting movies")
#convmovies(fdir=exptsdir, specdur1='no', start1=0, dur1=0, specdur2='yes', 
#start2=0, dur2=240, ext=EXT, removeavi='yes', movbase=MOVBASE, 
#num=5, qscale=3)

##For testing code
convmovies(fdir=exptsdir, specdur1='yes', start1=0, dur1=60, specdur2='yes', 
start2=0, dur2=60, ext=EXT, overwrite=OVERWRITE, removeavi='no', movbase=MOVBASE, 
num=5, qscale=3)
