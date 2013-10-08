#This module defines functions for dividing an image up into different ROIs 
#(usually for dividing an aggression or courtship image up into different 
#wells). 

from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import cmn.cmn as cmn
import pickle
import genplotlib as gpl


class WellParams():
    
    '''Specifies the regions of the image array that contain wells. Think of 
    the image as an array (rows vs. columns) rather than in xy coordinates.
    Input:
    config = 2-element list: [# wells in vertical direction, # wells in 
    horizontal direction]; for aggression [3, 4]; for courtship [4,10]
    r = Top row of the ROI surrounding the top left well.
    c = Left column of the ROI surrounding the top left well.
    rpad = # rows in between the wells (vertical direction)
    cpad = # columns in between the wells (horizontal direction)
    nrows = # rows in each ROI
    ncols = # cols in each ROI
    rshift = # rows to shift the ROI during each iteration in the horizontal 
    direction; used if image is rotated
    cshift = # columns to shift the ROI during each iteration in the vertical 
    direction; used if image is rotated
    scaling = scalar multiple of each value; used if the zoom is altered
    '''
    
    def __init__(self, config, r, c, rpad, cpad, nrows, ncols, scaling, rshift, 
    cshift):
        self.config = config
        self.r = r
        self.c = c
        self.rpad = rpad
        self.cpad = cpad
        self.nrows = nrows
        self.ncols = ncols
        self.scaling = scaling
        self.rshift = rshift
        self.cshift = cshift
    
    
    def defwells(self):    
        vw, hw = self.config    
        wells = []
        for x in range(hw):
            for y in range(vw):
                r1 = self.r +(self.nrows+self.rpad)*y*self.scaling + self.rshift*x
                r2 = r1 + self.nrows*self.scaling
                c1 = self.c + (self.ncols+self.cpad)*x*self.scaling + self.cshift*y
                c2 = c1 + self.ncols*self.scaling
                wells.append([r1, r2, c1, c2])
        return(wells)


def checkwells(wells, bgfile):
                     
    bg = np.array(Image.open(bgfile)).astype(float)
    plt.figure()
    plt.imshow(bg, cmap=plt.cm.gray)
    for w in wells:
        gpl.plotrect(w)
    plt.savefig('wells.png')

