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
import libs.winglib as wl
import numpy as np
from wingsettings import *
from PIL import Image

EXPTDIR = os.path.abspath('.')
MOVDIR = os.path.join(EXPTDIR, MOVBASE)
SUBMOVDIR = os.path.join(EXPTDIR, SUBMOVBASE)
PICKLEDIR = os.path.join(EXPTDIR, PICKLEBASE)
TEXTDIR = os.path.join(EXPTDIR, TEXTBASE)
PLOTDIR = os.path.join(EXPTDIR, PLOTBASE)
THFIGDIR = os.path.join(EXPTDIR, THFIGBASE)
ROTFIGDIR = os.path.join(EXPTDIR, ROTFIGBASE)
WINGFIGDIR = os.path.join(EXPTDIR, WINGFIGBASE) 

def find_roi_ints(img, comp_labels, outwingdir):
    
    imfile = img+EXT
    orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTSUBTH, 
    plot='yes')
    fly_roi_int = []
    for comp_label in comp_labels:
        orient_im = orientflies(orig_im, label_im, comp_label, coms, 
        FLY_OFFSET, ROTIMSHAPE, img)
        imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        plot_rotimage(orient_im, ROTIMSHAPE, FLY_OFFSET, comp_label, img, 
        OUTROTDIR)
        w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
        plot_wingimage(w_im, imrois, img, comp_label, WINGFIGDIR)
        roi_int = np.array(roimeans(w_im, imrois))
        #fly_roi_int = np.vstack((fly_roi_int, roi_int[np.newaxis]))
        fly_roi_int.append(roi_int)
   
    return(fly_roi_int)   



bgpickle = os.path.join(PICKLEDIR, 'bgarray')
wellcoordpickle = os.path.join(PICKLEBASE, WELLCOORDSN)
wells = wl.loadwells(wellcoordpickle)


IMNUMS = [str(x) for x in np.arange(10, 12, 1)]
IMAGES = ['mov000'+n+'.bmp' for n in IMNUMS]

#pl.showeachwell(wells, 'background.bmp')

#movsmc = {}
#movmmc = {}

#for n, well in enumerate(wells):
    #movsmc[n] = []
    #movmmc[n] = []

movsmc = np.empty((len(IMAGES),len(wells)))

for frame, imfile in enumerate(IMAGES):
    #subimfile = os.path.join('submovie', 'sub'+imfile)
    #subim = np.array(Image.open(subimfile)).astype(float)
    os.chdir(MOVDIR)
    subim = wl.bgsub(bgpickle, imfile)
    
    for n, well in enumerate(wells):
        d = wl.findflies(subim, imfile, well, BODY_TH, 'no')
        print(d['uselab'])
        if len(d['uselab']) == 0:
            print('No connected components')
            continue
        # Plotting functions.
        wl.plotfindflies(d, n, THFIGDIR)
        plt.close()
        
        flysmc = []
        flymmc = []
        for flyn, comp_label in enumerate(d['uselab']):
            
            rotimshape = 0.5*np.array(d['dim'])
            flyoffset = np.array(0.5*rotimshape)
            
            orient_im = wl.orientflies(d['orig_im'], d['label_im'], comp_label, 
            d['uselab'], d['usecoms'], flyoffset, rotimshape, d['imname'])
            
            tmatflyim = wl.tmatflyim(flyoffset)
            imrois = wl.defrois(CENTER_A, SIDE_AL, MID_L, tmatflyim)
            w_im = wl.findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
            

            # Plotting functions.
            wl.plotrotim(orient_im, rotimshape, flyoffset, n, flyn, d['imname'],
            ROTFIGDIR)
            plt.close()
            wl.plot_wingimage(w_im, imrois, d['imname'], flyn, 
            WINGFIGDIR, n)
            plt.close()

            # Analyzing ROI intensities.
            roi_int = np.array(wl.roimeans(w_im, imrois))
            center_a, center_p, side_a, side_p, med = wl.subroi(roi_int)
            
            if ((center_p+side_p) - (center_a+side_a)) > 0:
                flysmc.append(side_p - center_p)
                flymmc.append(med - center_p)

            else:
                flysmc.append(side_a - center_a)
                flymmc.append(med - center_a)
    
        movsmc[frame,n] = np.max(flysmc)
print(movsmc)
    
            





        
