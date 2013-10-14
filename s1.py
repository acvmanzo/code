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
    info = os.path.basename(os.path.abspath(exptdir)).split('_')
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

def plotextwell(smc, mmc, fps, plotlen):
    '''
    plotlen = duration of each subplot, in minutes
    '''
    
    # ======== SET INITIAL FIGURE PROPERTIES =============
    mpl.rc('axes', linewidth=2)

    # Sets font to Arial and assigns font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(25)
    
    plt.figure(figsize=(20,20), dpi=600)
    smc = smc-np.mean(smc)
    mmc = mmc-np.mean(mmc)
    
    
    dur = len(smc)/fps/60.
    
    print('dur', dur)
    numplots = range(np.int(np.ceil(dur/plotlen)))
    print('numplots', numplots)
    subplots = (len(numplots), 1)
    
    xvals = np.linspace(0, dur, len(smc))
    plotmax = np.max([np.max(smc), np.max(mmc)])
    
    for x in numplots:
        li = 0 + x*plotlen*60*fps
        ri = plotlen*60*fps + x*plotlen*60*fps
        ax = plt.subplot2grid(subplots, (x,0), colspan=1)    
    
        plt.plot(xvals[li:ri], smc[li:ri], 'r', lw=2, label='side-center')  
        plt.plot(xvals[li:ri], mmc[li:ri], 'b', lw=2, label='middle-center')

        xmin = xvals[li]
        xmax = plotlen*x+plotlen
        print((xmax-xmin)/4)
        plt.xlim(xmin, xmax)    
        plt.ylim(0, 1.2*plotmax)
        
        xlist = np.linspace(xmin, xmax, 5)
        print(xlist)
        xtime = [time.strftime('%M:%S', time.gmtime(x*60)) for x in xlist]
        plt.xticks(xlist, xtime, fontproperties=fontv)
        #ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))

    plt.suptitle('Wing extension', fontsize=30)
    plt.legend()



def saveextwell(wellnum):
    
    plt.savefig('wingext_well{0:02d}.png'.format(wellnum))
    plt.close()


def plotextexpt(movsmc, movmmc):
    for well in range(np.shape(movsmc)[1]):
        smc = movsmc[:, well]
        mmc = movmmc[:, well]
        plotextwell(smc, mmc, well)
        
def plotextexptconv(exptdir, movsmc, movmmc, conv, convt=3):
    fps = getfps(exptdir)
    for well in range(np.shape(movsmc)[1]):
        smc = movsmc[:,well]
        mmc = movmmc[:,well]
        if conv == 'yes':
            smc, mmc = [movavg(convt, fps, x) for x in [smc, mmc]]
        
        plotextwell(smc, mmc, fps)
        saveextwell(well)
        

#fps = getfps(exptdir)
#csmc = movavg(1, fps, movsmc[:,4])
#cmmc = movavg(1, fps, movmmc[:,4])
#plotwingext(csmc, cmmc)

#plotextexptconv('.', movsmc, movmmc, 1)
plotextwell(movsmc[:,2], movmmc[:,2], 30, 0.5)
saveextwell(2)

                





        
