#! /usr/bin/env python

# This executable file subtracts the background from multiple movies. Start in 
#folder containing movie folders; see wingdet/README for the requisite file 
#structure.

from bglib import *
from wingsettings import *

NFRAMES = sys.argv[1] # Number of frames for generating background image
OVERWRITE = sys.argv[2] # Overwrite- 'yes' or 'no'

print('1-nframes, 2-overwrite? yes or no')
genbgmovies(fdir='.', movbase=MOVBASE, picklebase=PICKLEBASE, bgfile=BGFILE, 
nframes=NFRAMES, fntype='median', overwrite=OVERWRITE)
