import numpy as np
import os

WINGDETBASE = 'wingdet'
EXPTSBASE = 'expts'
MOVBASE = 'movie'
SUBMOVBASE = 'submovie'
PICKLEBASE = 'pickled'
PIMAGEBASE = 'images'
TEXTBASE = 'text'
PLOTBASE = 'plots'
WELLIDBASE = 'wellid'
THFIGBASE = '0_thfigs'
ROTFIGBASE = '1_rotims'
WINGFIGBASE = '2_wingims'

BGFILE = 'background.bmp'
#BGFILE = 'background.tif'
BGNP = 'bgarray.npy'
WELLPARAMSN = 'wellparams'
WELLCOORDSN = 'wellcoords'
SMCFILE = 'movsmc'
MMCFILE = 'movmmc'
ROIFILE = 'movroi_int'

CONFIG = (3,4)
#BODY_TH = 150
BODY_TH = 120
#WING_TH_LOW = 20
WING_TH_LOW = 25
#WING_TH_HIGH = 90
WING_TH_HIGH = 120
CENTER_A = np.array([[45, 10], [65, -10]]) # top left corner and bottom diagonal corner of square
SIDE_AL = np.array([[25, 40], [45, 25]]) # top left corner and bottom diagonal corner of square
MID_L = np.array([[-15, 65], [15, 25]])

WINLEN = 1


def exptfiles(fdir):
    exptdir = os.path.abspath(fdir)
    movdir = os.path.join(exptdir, MOVBASE)
    submovdir = os.path.join(exptdir, SUBMOVBASE)
    pickledir = os.path.join(exptdir, PICKLEBASE)
    textdir = os.path.join(exptdir, TEXTBASE)
    plotdir = os.path.join(exptdir, PLOTBASE)
    thfigdir = os.path.join(exptdir, THFIGBASE)
    rotfigdir = os.path.join(exptdir, ROTFIGBASE)
    wingfigdir = os.path.join(exptdir, WINGFIGBASE)
    
    bgpickle = os.path.join(pickledir, BGNP)
    wcpickle = os.path.join(pickledir, WELLCOORDSN)
    
    return(exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, 
    rotfigdir, wingfigdir, bgpickle, wcpickle)



