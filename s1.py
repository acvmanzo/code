#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the default ROI parameters. This should be run 

import cmn.cmn as cmn
import partimlib as pl
import mtslib as ml
import bgsublib as bl
import winglib as wl

import os
import matplotlib.pyplot as plt
import numpy as np

BGFILE = 'background.tif'
PICKLEBASE = 'pickled'
TEXTBASE = 'text'
#exptdir = os.path.abspath('.')
exptdir = cmn.defpardir('.')
submovdir = os.path.join(exptdir, 'submovie')
movdir = os.path.join(exptdir, 'movie')
pickledir = os.path.join(exptdir, 'pickled')
textdir = os.path.join(exptdir, 'text')
plotdir = os.path.join(exptdir, 'plots')
thfigdir = os.path.join(plotdir, '0_thfigs')
wellcoordpickle = os.path.join(pickledir, 'wellcoords')

BODY_TH = 120
imfile = os.path.join(submovdir, 'submov00010.tif')

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
        plot_wingimage(w_im, imrois, img, comp_label, outwingdir)
        roi_int = np.array(roimeans(w_im, imrois))
        #fly_roi_int = np.vstack((fly_roi_int, roi_int[np.newaxis]))
        fly_roi_int.append(roi_int)
   
    return(fly_roi_int)   



#defaultwells(bgfile=BGFILE, pickledir=PICKLEBASE, textdir=TEXTBASE)
#ml.convmovies('.', 0, 1, 'yes', 'no')
#ml.convmovie('cs_20130619_ag_A_l_1.MTS', 'cs_20130619_ag_A_l_1.MTS.avi', 0, 
#60, 'yes')
#bl.subbgmovies()
#(fdir, submovbase, movbase, picklebase, nframes, fntype, 
#boverwrite='no'):
#pl.defaultwells(BGFILE, pickledir, textdir, overwrite='yes')
#print(cmn.myround(129.923, base=1))



wells = wl.loadwells(wellcoordpickle)
d = wl.findflies(imfile, wells[0], BODY_TH, 
'no')
wl.plotfindflies(d, thfigdir)
