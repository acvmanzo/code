#! /usr/bin/env python

# This executable file subtracts the background from multiple movies. Start in 
#folder containing movie folders; see wingdet/README for the requisite file 
#structure.

from bgsublib import *

SUBMOVDIR = 'submovie'
MOVDIR = 'movie'
PICKLEDIR = 'pickled'
NFRAMES = sys.argv[1] # Number of frames for generating background image

print('1 - nframes')
subbgmovies('.', SUBMOVDIR, MOVDIR, PICKLEDIR, NFRAMES, fntype='median')

