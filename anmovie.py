from libs.winglib import *
from wingsettings import *


def an1movie(exptdir, nframes, plotlen):
    # Defines directories.
    exptfiles = exptfiles(os.path.abspath(exptdir))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles
    movsmc, movmmc, movroi = exptint(exptfiles, plotfiles='no', save='yes')
    plotextexpt(exptdir, movsmc, movmmc, plotlen=plotlen, usemovavg='yes', 
    movavgdur=MOVAVGDUR)

an1movie('.', NFRAMES, PLOTLEN)
