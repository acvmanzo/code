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


exptfiles = exptfiles(os.path.abspath('.'))
exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles


#IMNUMS = [str(x) for x in np.arange(10, 60, 1)]
#IMAGES = ['mov000'+n+'.bmp' for n in IMNUMS]
#os.chdir(movdir)
#START = time.time()
#movsmc, movmmc, movroi = multimint(exptfiles, IMAGES, 'no')

#exptint(exptfiles, 'no', 'yes')

smcfile = os.path.join(pickledir, SMCFILE+'.npy')
mmcfile = os.path.join(pickledir, MMCFILE+'.npy')

movsmc = np.load(smcfile)
movmmc = np.load(mmcfile)


def window(winlen):    
    wind = list(np.ones(winlen)/winlen)
    return(wind)

def getfps(exptdir):
    info = os.path.basename(exptdir).split('_')
    if info.count('PF24') == 1:
        fps = 24
    if info.count('PF30') == 1:
        fps = 30
    return(fps)

def movavg(t, fps, trace):
    frames = t*fps
    wind = window(frames)
    ctrace = np.convolve(trace/max(trace), wind, 'same')
    return(ctrace)

def plotextwell(smc, mmc, wellnum):
    plt.figure()
    smc = smc-np.mean(smc)
    mmc = mmc-np.mean(mmc)
    plt.plot(smc, 'r', label='side-center')
    plt.plot(mmc, 'b', label='middle-center')
    plt.title('Well {0}'.format(wellnum))
    plt.legend()
    plt.savefig('wingext_well{0:02d}.png'.format(wellnum))
    plt.close()

def plotextexpt(wells, movsmc, movmmc):
    for well in range(wells):
        smc = movsmc[:, well]
        mmc = movmmc[:, well]
        plotextwell(smc, mmc, well)


#fps = getfps(exptdir)
#csmc = movavg(1, fps, movsmc[:,4])
#cmmc = movavg(1, fps, movmmc[:,4])
#plotwingext(csmc, cmmc)
plotextexpt(12, movsmc, movmmc)



                





        
