import os
import bgsublib as bl
import partimlib as pl

EXPTDIR = os.path.abspath(os.getcwd())
SUBMOVDIR = os.path.join(EXPTDIR, 'submovie')
MOVDIR = os.path.join(EXPTDIR, 'movie')
PICKLEDIR = os.path.join(EXPTDIR, 'pickled')

NFRAMES = 10

def an1movie():
    # Start in expt/moviexx directory.
    
    bl.subbgmovie(imdir=MOVDIR, bgdir=EXPTDIR, pickledir=PICKLEDIR, 
    submovdir=SUBMOVDIR, nframes=NFRAMES, fntype='median', overwrite='no')
