
import os
import numpy as np
from scipy import ndimage
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import pickle




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
