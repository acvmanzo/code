from libs.winglib import *
from wingsettings import *


def an1movie(exptdir, plotlen):
    # Defines directories.
    exptfilesd = exptfiles(os.path.abspath(exptdir))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfilesd
    
    movsmc, movmmc, movroi = exptint(exptfilesd, plotfiles='no', save='yes')
    plotextexpt(exptdir, movsmc, movmmc, plotlen=plotlen, usemovavg='yes', 
    movavgdur=MOVAVGDUR)

an1movie('.', PLOTLEN)


