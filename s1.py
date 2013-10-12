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

bgpickle = os.path.join(PICKLEDIR, 'bgarray')
#imname = 'mov00009.tif'
#subimname = 'submov00009.tif'
#imfile = os.path.join(MOVBASE, imname)
#subimfile = os.path.join(SUBMOVBASE, subimname)
bgfile = BGFILE


wellcoordpickle = os.path.join(PICKLEBASE, WELLCOORDSN)
wells = wl.loadwells(wellcoordpickle)


IMNUMS = [str(x) for x in np.arange(10, 11, 1)]
IMAGES = ['mov000'+n+'.tif' for n in IMNUMS]


for imfile in IMAGES:
    #subimfile = os.path.join('submovie', 'sub'+imfile)
    #subim = np.array(Image.open(subimfile)).astype(float)
    os.chdir(MOVDIR)
    print(imfile)
    subim = wl.bgsub(bgpickle, imfile)
    for n, well in enumerate(wells):
        #print('Loop', n)
        #try:
        d = wl.findflies(subim, imfile, well, BODY_TH, 'no')
        rotimshape = 0.5*np.array(d['dim'])
        flyoffset = np.array(0.5*rotimshape)
        rotim = wl.orientflies(d['orig_im'], d['label_im'], d['uselab'][0], 
        d['uselab'], 
        d['usecoms'], flyoffset, rotimshape, d['imname'])
        wl.plotrotim(rotim, rotimshape, flyoffset, n, d['uselab'][0], d['imname'],
        ROTFIGDIR)

        #except IndexError:
            #print('No connected components')
            #continue

#pl.showwellpos(wells, 'background.tif')
