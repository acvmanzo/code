# This module contains functions useful for generating a background image 
# from a sequence of image files and then subtracting that image from each file.

from PIL import Image
import os
import sys
import pickle
import numpy as np
import cmn.cmn as cmn
import glob


def genbgim(imdir, nframes, fntype, imext, split=5):
    '''Generates a background image from a sequence of image files.
    Input:
    imdir = directory containing the sequence of image files
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence
    fntype = 'median, 'average'; method for combining nframes.
    imext = extension of image files
    split = how many lists to split the job into
    Output:
    bgnew = numpy array of background image 
    '''
    print "Generating background"
    # Load frames for generating background image.
    imdir = os.path.abspath(imdir)
    files = sorted(os.listdir(imdir))
    moviel = len(files)
    nframes = int(nframes)
    assert moviel > nframes
    
    nummov = np.linspace(1, moviel-1, nframes)
    jobs = np.array_split(nummov, split)
    
    imarr = np.array(Image.open(files[0]))[:,:,0].astype(float)
    medarrs = np.empty((nframes/split,)+np.shape(imarr))
    print(np.shape(medarrs))
        
    for m, job in enumerate(jobs):
        #print(job)
        cont = np.empty((nframes/split,)+np.shape(imarr))
        for n, x in enumerate(job):
            #print(n)
            if imext == 'jpeg':
                c = np.array(Image.open(files[int(x)]))[:,:,0].astype(float)
                print('c', np.shape(c))
            if (imext == 'bmp') or (imext== 'tif'):
                c = np.array(Image.open(files[int(x)])).astype(float)
            print(n)
            cont[n,:,:] = c
            #print('container shape after dstack', np.shape(cont[:,:,1:]))
        if fntype == 'median':
            newc = np.median(cont, 0)
        if fntype == 'average':
            newc = np.average(cont, 0)
        #print('newc', np.shape(newc))
        medarrs[:,:,m] = newc
        
    print('medarrs', np.shape(medarrs))
    #print(medarrs)
    #print(np.sort(medarrs, 2))
    bg = np.median(medarrs, 0)
    
    print(np.shape(bg))
    return(bg)
        
    
            
    #if imext == 'bmp' or "tif":
        #bg = np.array(Image.open(files[0])).astype(float)   
        #for x in np.linspace(1, moviel-1, nframes):
            #c = np.array(Image.open(files[int(x)])).astype(float)
            #bg = np.dstack((bg, c))      
        

    
        
    #return(medarrs)


def savebg(bg, bgfile, bgdir, pickledir):
    '''Saves background image as an image file and as a pickled array.
    Input:
    bg = array of background image
    bgext = extension of background image (e.g., 'tif' or 'jpeg')
    bgdir = directory in which to save background image
    pickledir = directory in which to save the pickled background array
    '''
    
    # Create necessary folders.
    cmn.makenewdir(bgdir)
    cmn.makenewdir(pickledir)
    
    # Save background image.
    bgnew = Image.fromarray(np.uint8(np.absolute(bg)))
    bgnew.save(os.path.join(bgdir, bgfile))
    
    # Save background image as a pickle file.
    with open(os.path.join(pickledir, 'bgarray'), 'w') as h:
        pickle.dump(bg, h)


def genbgimexpt(exptdir, movbase, picklebase, bgfile, nframes, ftype, imext):
    '''Generates and saves background image for a single experiment. 
    Input:
    exptdir = expts/exptxx/ directory
    movbase = name of exptxx/movie directory
    picklebase = name of exptxx/pickle directory
    bgext = extension of background image ('tif' or 'jpeg')
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence
    fntype = 'median, 'average'; method for combining nframes
    Output:
    '''
    
    imdir = os.path.join(exptdir, movbase)
    pickledir = os.path.join(exptdir, picklebase)
    bg = genbgim(imdir, nframes, ftype, imext)
    savebg(bg, bgfile, exptdir, pickledir)
    

def genbgmovies(fdir, movbase, picklebase, bgfile, nframes, fntype, overwrite):
    
    '''Generates and saves background image for multiple experiments in fdir 
    (see wingdet/README.txt).
    Input:
    fdir = extpts/ directory
    movbase = name of exptxx/movie directory
    picklebase = name of exptxx/pickle directory
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence
    fntype = 'median, 'average'; method for combining nframes
    overwrite = 'yes' or 'no'; overwrite background image and bgarray
    '''
    
    dirs = cmn.listsortfs(fdir)
    for exptdir in dirs:
        print(os.path.basename(exptdir))
        os.chdir(exptdir)
        fullbgfile = os.path.join(exptdir, bgfile)
        try:
            cmn.check(bgfile, overwrite)
        except cmn.FileError:
            continue
        movdir = os.path.join(exptdir, movbase)
        os.chdir(movdir)
        try:
            genbgimexpt(exptdir, movbase, picklebase, fullbgfile, nframes, fntype)
        except AssertionError:
            print('Movie length > nframes')
            continue


