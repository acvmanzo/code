#! /usr/bin/env python

# This executable file subtracts the background from multiple movies. Start in 
#folder containing movie folders; see wingdet/README for the requisite file 
#structure.

from bgsublib import *
from wingsettings import *

BGEXT = sys.argv[1] # Extension for background image
NFRAMES = sys.argv[2] # Number of frames for generating background image
OVERWRITE = sys.argv[3] # Overwrite- 'yes' or 'no'

print('1-image extension 2-nframes, 3-overwrite? yes or no')
genbgmovies(fdir='.', movbase=MOVBASE, picklebase=PICKLEBASE, bgext=BGEXT, 
nframes=NFRAMES, fntype='median', overwrite=OVERWRITE)
