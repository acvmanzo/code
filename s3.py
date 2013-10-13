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


avitoim('cs_20130619_ag_PF30_A_l_1.avi', 'bmp', 'yes', 5, 3)
os.chdir(MOVDIR)
genbgimexpt(EXPTDIR, MOVBASE, PICKLEBASE, BGFILE, 20, 'median', 'bmp')

#defaultwells(BGFILE, PICKLEDIR, TEXTDIR, WELLPARAMSN, WELLCOORDSN, 'no')

