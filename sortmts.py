#! /usr/bin/env python

from mtslib import *

#Run from aggression/newmovies/ folder.
WINGDETDIR = os.path.join(cmn.defpardir(), 'wingdet')

print('1-start (s), 2-dur (s) 3-specdur; yes or no')

START = sys.argv[1] # Number of seconds into movie before conversion begins.
DUR = sys.argv[2] # Duration of conversion in seconds.
SPECDUR = sys.argv[3] # Duration of conversion specified? 'yes' or 'no'


sortmtsdir(params=WINGDETDIR)
os.chdir(WINGDETDIR)
convmovies(fdir=WINGDETDIR, start=START, dur=DUR, specdur=SPECDUR)
