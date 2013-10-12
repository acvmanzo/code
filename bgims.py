#! /usr/bin/env python

# This executable file generates the background image for multiple movies. Start in 
#folder containing movie folders; see wingdet/README for the requisite file 
#structure.

from libs.bglib import *
from wingsettings import *

NFRAMES = sys.argv[1] # Number of frames for generating background image
OVERWRITE = sys.argv[2] # Overwrite- 'yes' or 'no'

print('1-nframes, 2-overwrite? yes or no')
genbgmovies(fdir='.', movbase=MOVBASE, picklebase=PICKLEBASE, bgfile=BGFILE, 
nframes=NFRAMES, fntype='median', overwrite=OVERWRITE)
