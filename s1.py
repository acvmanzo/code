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


IMNUMS = [str(x) for x in np.arange(20, 22, 1)]
IMAGES = ['mov000'+n+'.bmp' for n in IMNUMS]
exptfiles = exptfiles(os.path.abspath('.'))

exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles
os.chdir(movdir)
#START = time.time()
movsmc, movmmc, movroi = multimint(exptfiles, IMAGES, 'no', 'yes')

#smcfile = os.path.join(pickledir, 'smc_5ims')
#mmcfile = os.path.join(pickledir, 'mmc_5ims')

#with open(smcfile, 'r') as f:
    #movsmc = pickle.load(f)
#with open(mmcfile, 'r') as g:
    #movmmc = pickle.load(g)  

#plt.figure()
#print(np.shape(movsmc))
#plt.plot(movsmc[:,1], 'r')
#plt.savefig('Side-center.png')

            





        
