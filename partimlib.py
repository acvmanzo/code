#This module defines functions for dividing an image up into different ROIs 
#(usually for dividing an aggression or courtship image up into different 
#wells). 

from PIL import Image
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import cmn.cmn as cmn
import pickle
import genplotlib as gpl

WELLPARAMSN = 'wellparams'
WELLCOORDSN = 'wellcoords'

class WellParams():
    
    '''Specifies the regions of the image array that contain wells. Think of 
    the image as an array (rows vs. columns) rather than in xy coordinates.
    '''
    
    def __init__(self, d = {'config':[3, 4], 'r':70, 'c':358, 'rpad':25, 
    'cpad':22, 'nrows':300, 'ncols':300, 'scaling':1, 'rshift':0, 'cshift':0}):
        '''Input: 
        Dictionary with the following items:
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
        self.config = d['config']
        self.r = d['r']
        self.c = d['c']
        self.rpad = d['rpad']
        self.cpad = d['cpad']
        self.nrows = d['nrows']
        self.ncols = d['ncols']
        self.scaling = d['scaling']
        self.rshift = d['rshift']
        self.cshift = d['cshift']
  
    
    def defwells(self):  
        '''Finds the rounded row and column coordinate for each ROI.'''
        vw, hw = map(int, self.config)
        wells = []
        for x in range(hw):
            for y in range(vw):
                r1 = self.r +(self.nrows+self.rpad)*y*self.scaling + self.rshift*x
                r2 = r1 + self.nrows*self.scaling
                c1 = self.c + (self.ncols+self.cpad)*x*self.scaling + self.cshift*y
                c2 = c1 + self.ncols*self.scaling
                rounded = [cmn.myround(z, base=1) for z in [r1, r2, c1, c2]]
                wells.append(rounded)
        return(wells)


    def saveparams(self, pickledir, textdir):
        '''Saves the parameters into a picklefile in the pickledir and a
        text file in the textdir.
        '''
        cmn.makenewdir(pickledir)
        cmn.makenewdir(textdir)
        
        with open(os.path.join(pickledir, WELLPARAMSN), 'w') as e:
            pickle.dump(self, e)
        
        textfile = os.path.join(textdir, WELLPARAMSN+'.txt')
        with open(textfile, 'w') as f:
            pass
        for attr, val in sorted(vars(self).iteritems()):
            attr, val = [str(x) for x in [attr, val]]
            with open(textfile, 'a') as f:
                f.write(cmn.var_str(attr, val.strip('[]'), '\t'))
    
    
    def savewells(self, pickledir, textdir):
        '''Saves the well coordinates into a picklefile in the pickledir and a
        text file in the textdir.
        '''
        wells = self.defwells()
    
        cmn.makenewdir(pickledir)
        cmn.makenewdir(textdir)
        with open(os.path.join(pickledir, WELLCOORDSN), 'w') as e:
            pickle.dump(wells, e)
        
        textfile = os.path.join(textdir, WELLCOORDSN+'.txt')
        with open(textfile, 'w') as f:
            f.write('Well coordinates: r1, r2, c1, c2\n')
        for well in wells:
            with open(textfile, 'a') as f:
                f.write('{0}\n'.format(str(well).strip('[]')))
      
            
def loadptxt(pfile):
    '''Loads the parameters from a parameter text file pfile into a 
    dictionary.'''
    
    d = {}
    with open(pfile, 'r') as f:
        for l in f:
            try:
                d[l.split('\t')[0]] = float(l.split('\t')[1])
            except ValueError:
                d[l.split('\t')[0]] = [float(x) for x in 
                l.split('\t')[1].strip('\n').split(',')]    
    return(d)


def loadppickle(pfile):
    '''Loads the parameters from a parameter pickle file pfile.
    '''
    with open(pfile, 'r') as f:
        m = pickle.load(f)
    return(m)


def checkwells(wells, bgfile, wellsfig='wells.png'):
    '''Plots the wells onto the background image file to check positions.
    Inputs:
    wells = list of well coordinates
    bgfile = background image file
    '''
    
    bg = np.array(Image.open(bgfile)).astype(float)
    plt.figure()
    plt.imshow(bg, cmap=plt.cm.gray)
    for w in wells:
        gpl.plotrect(w)
    plt.savefig(wellsfig)


def defaultwells(bgfile, pickledir, textdir, overwrite):
    '''Generates well coordinates using the default parameters; plots onto a 
    the background image. Saves the parameter and well coordinates.
    Inputs:
    bgfile = name of background image file
    pickledir = directory for picklefiles
    textdir = directory for text parameter files
    '''
    
    picklepfile = os.path.join(pickledir, WELLPARAMSN)
    if os.path.exists(picklepfile) and overwrite == 'no':
        sys.exit('wellparams file already exists')
    
    wp = WellParams()
    wells = wp.defwells()
    checkwells(wells, bgfile)
    
    wp.savewells(pickledir, textdir)
    wp.saveparams(pickledir, textdir)


def b_defaultwells(fdir, bgfile, picklebase, textbase, boverwrite):
    '''Batch function to run defaultwells() on multiple files. Does not run 
    defaultwells() if a pickled wellsparam file is present.
    Input:
    dirlist = list of files on which to run defaultwells
    bgfile = name of background image file
    picklebase = basename for picklefile directory
    textbase = basename for text file directory
     '''
     
    dirlist = cmn.listsortfs(fdir)
    for exptdir in dirlist:
        print(exptdir)
        os.chdir(exptdir)
        pickledir = os.path.join(exptdir, picklebase)
        textdir = os.path.join(exptdir, textbase)
        if os.path.exists(os.path.join(pickledir, WELLPARAMSN)) and \
        boverwrite == 'no':
            continue
        print('Generating default wells')
        defaultwells(bgfile, pickledir, textdir, overwrite='yes')



def findwellstext(bgfile, ptextfile, pickledir):
    '''Generates well coordinates using parameters in ptextfile. Plots onto 
    the background image. Saves the parameter and well coordinates.
    Input:
    bgfile = name of background image file
    ptextfile = name of parameter text file
    pickledir = directory for picklefiles
    '''
    
    d = loadptxt(ptextfile)
    wp = WellParams(d)
    wells = wp.defwells()
    checkwells(wells, bgfile)
    
    textdir = os.path.dirname(os.path.abspath(ptextfile))
    wp.savewells(pickledir, textdir)
    wp.saveparams(pickledir, textdir)

