import os
import bgsublib as bl
import partimlib as pl

NFRAMES = 10

def an1movie(fdir, nframes):
    # Start in expt/moviexx directory.
    
    # Defines directories.
    exptdir = os.path.abspath(fdir)
    submovdir = os.path.join(exptdir, 'submovie')
    movdir = os.path.join(exptdir, 'movie')
    pickledir = os.path.join(exptdir, 'pickled')
    textdir = os.path.join(exptdir, 'text')
    
    # Generates background image and subtracts it from every image file.
    bl.subbgmovie(imdir=movdir, bgdir=exptdir, pickledir=pickledir, 
    submovdir=submovdir, nframes=nframes, fntype='median', overwrite='no')

    # Finds ROIs surrounding wells.
    pl.defaultwells('background.txt', pickledir, textdir, overwrite='no')

an1movie('.', NFRAMES)
