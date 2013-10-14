#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the default ROI parameters. This should be run 

import os
import matplotlib.pyplot as plt
import numpy as np
import cmn.cmn as cmn
import libs.partimlib as pl
import libs.mtslib as ml
import libs.bglib as bl
#import libs.winglib as wl
from libs.winglib import *
import numpy as np
from wingsettings import *
from PIL import Image
import time
import matplotlib as mpl
import time
import cv2


exptfiles = exptfiles(os.path.abspath('.'))
exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles


IMNUMS = [str(x) for x in np.arange(10, 12, 1)]
IMAGES = ['mov000'+n+'.jpeg' for n in IMNUMS]
os.chdir(movdir)
movsmc, movmmc, movroi = multimint(exptfiles, IMAGES, plotfiles='no', 
savemc='no')

#exptint(exptfiles, 'no', 'yes')
#movsmc = np.load(smcfile)
#movmmc = np.load(mmcfile)   

#fps = getfps(exptdir)
#plotextwell(movsmc[:,2], movmmc[:,2], fps=fps, plotlen=60, conv='yes', 
#convdur=0.5)
#saveextwell(2)

#plotextexpt(exptdir, movsmc, movmmc, plotlen=60, usemovavg='yes', movavgdur=MOVAVGDUR)



        
