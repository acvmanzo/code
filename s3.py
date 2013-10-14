from libs.bglib import *
from wingsettings import *
from libs.mtslib import *
from libs.partimlib import *
from libs.winglib import *

EXPTDIR = os.path.abspath('.')
MOVDIR = os.path.join(EXPTDIR, MOVBASE)
SUBMOVDIR = os.path.join(EXPTDIR, SUBMOVBASE)
PICKLEDIR = os.path.join(EXPTDIR, PICKLEBASE)
TEXTDIR = os.path.join(EXPTDIR, TEXTBASE)
PLOTDIR = os.path.join(EXPTDIR, PLOTBASE)
THFIGDIR = os.path.join(EXPTDIR, THFIGBASE)
ROTFIGDIR = os.path.join(EXPTDIR, ROTFIGBASE)

exptfiles = exptfiles(os.path.abspath('.'))
exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles

#avitoim('cs_20130619_ag_PF30_A_l_1.avi', 'bmp', 'yes', 5, 3)
convmovies(fdir=exptdir, specdur1='yes', start1=0, dur1=180, specdur2='yes', 
start2=0, dur2=0, newxdim=1920, newydim=1080, ext='jpeg', overwrite='no', 
scale = 'yes', removeavi='no', movbase=MOVBASE, num=5, qscale=3)

os.chdir(MOVDIR)
#genbgimexpt(EXPTDIR, MOVBASE, PICKLEBASE, BGFILE, 100, 'median', 'bmp')

#defaultwells(BGFILE, PICKLEDIR, TEXTDIR, WELLPARAMSN, WELLCOORDSN, 'no')

