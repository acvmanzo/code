import os
import libs.bgblib as bl
import libs.partimlib as pl
import libs.winglib as wl
from wingsettings import *


def an1movie(exptdir, nframes):
    # Defines directories.
    exptfiles = exptfiles(os.path.abspath(exptdir))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles
    
    movsmc, movmmc, movroi = multimint(exptfiles, IMAGES, 'yes', 'yes')

an1movie('.', NFRAMES)
