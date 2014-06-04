#! /usr/bin/env python

# For one movie, takes several frames and plots thresholded plots.

from libs.winglib import *
from wingsettings import *
import sys


def testmovie(exptdir, start, stop, secint):
    '''Takes several frames throughout movie and plots thresholded plots.
    Inputs:
    exptdir = expts/exptxx directory
    secint = interval between each analyzed frame, in seconds
    '''
    exptfiles = getexptfiles(os.path.abspath(exptdir))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, extfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    
    frames = cmn.listsortfs(movdir)
    fps = float(getfps(exptdir))
    slices = int(fps*float(secint))
    print(slices)
    multimint(exptfiles=exptfiles, images=frames[start::slices], plotfiles='yes', 
    savemc='no')


SECINT = sys.argv[1] # Interval between frames, in seconds
print('1-interval b/w frames')

testmovie('.', STARTTEST, STOPTEST, SECINT)

