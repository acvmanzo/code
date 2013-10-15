#! /usr/bin/env python

from libs.winglib import *
from wingsettings import *


def an1movie(exptdir, plotlen):
    # Defines directories.
    exptfiles = getexptfiles(os.path.abspath(exptdir))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, extfigdir, bgpickle, wcpickle, smcfile, mmcfile = \
    exptfiles
    
    #movsmc, movmmc, movroi = exptint(exptfiles, plotfiles='no', save='yes')
    #os.chdir(exptdir)
    
    plotextexpt(exptdir=exptdir, smcfile=smcfile, mmcfile=mmcfile, 
    figdir=extfigdir, plotlen=plotlen, usemovavg='yes', movavgdur=MOVAVGDUR)
    
    

an1movie('.', PLOTLEN)


