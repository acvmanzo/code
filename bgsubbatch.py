#! /usr/bin/env python

# This executable file subtracts the background from multiple movies. Start in 
#folder containing movie folders; see wingdet/README for the requisite file structure.

from bgsublib import *

SUBMOVDIR = 'submovie'
MOVDIR = 'movie'
NFRAMES = 3

subbgmovies('.', SUBMOVDIR, MOVDIR, NFRAMES, fntype='median')

