# This module contains functions useful for generating a background image 
# from a sequence of image files and then subtracting that image from each file.

from PIL import Image
import os
import sys
import pickle
import numpy as np
import cmn.cmn as cmn


def genbgim(imdir, nframes, fntype):
    '''Generates a background image from a sequence of image files.
    Input:
    imdir = directory containing the sequence of image files
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence
    fntype = 'median, 'average'; method for combining nframes.
    Output:
    bgnew = numpy array of background image 
    '''
    
    # Load frames for generating background image.
    imdir = os.path.abspath(imdir)
    files = sorted(os.listdir(imdir))
    moviel = len(files)
    nframes = int(nframes)
    
    bg = np.array(Image.open(files[0])).astype(float)

    assert moviel > nframes
    
    for x in np.linspace(1, moviel-1, nframes):
        print(x)
        c = np.array(Image.open(files[int(x)])).astype(float)
        bg = np.dstack((bg, c))

    if fntype == 'median':
        bgnew = np.median(bg, 2)
    if fntype == 'average':
        bgnew = np.average(bg, 2)
        
    return(bgnew)


def savebg(bg, bgdir, pickledir):
    '''Saves background image as a tif file and as a pickled array.
    Input:
    bg = array of background image
    bgdir = directory in which to save background image
    pickledir = directory in which to save the pickled background array
    '''
    
    # Create necessary folders.
    cmn.makenewdir(bgdir)
    cmn.makenewdir(pickledir)
    
    # Save background image.
    bgnew = Image.fromarray(np.uint8(np.absolute(bg)))
    bgnew.save(os.path.join(bgdir, 'background.tif'))
    
    # Save background image as a pickle file.
    with open(os.path.join(pickledir, 'bgarray'), 'w') as h:
        pickle.dump(bg, h)


def subbgim(bg, submoviedir, imdir='.'):
    '''Subtracts background from each file in an image sequence.
    bg = numpy array of background image
    imdir = directory containing the sequence of image files; default is 
    current directory
    submoviedir = directory to deposit the background-subtracted image files
    '''
    
    imdir = os.path.abspath(imdir)
    files = sorted(os.listdir(imdir))
    cmn.makenewdir(submoviedir)
    
    # Loads each image, subtracts the background then saves new image into 
    # submovie folder.
    for x in np.arange(0, len(files), 1):
        outfile = os.path.join(submoviedir, 'sub'+files[int(x)])
        c = np.array(Image.open(files[int(x)])).astype(float)
        subarr = c-bg
        subim = Image.fromarray(np.uint8(np.absolute(subarr)))
        subim.save(outfile)


def subbgmovie(imdir, bgdir, pickledir, submovdir, nframes, 
fntype, overwrite='no'):
    '''Generates background image from nframes of movie and saves in bgdir. 
    Subtracts background from each file in movie image sequence.
    Input:
    imdir = directory containing the sequence of image files
    bgdir = directory in which to save background image
    pickledir = directory in which to save pickled background image
    submoviedir = directory to deposit the background-subtracted image files
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence
    fntype = 'median, 'average'; method for combining nframes
    '''
    
    bgfile = os.path.join(bgdir, 'background.tif')
    if os.path.exists(bgfile) and overwrite == 'no':
        sys.exit('Background image already generated.')

    os.chdir(imdir)
    bg = genbgim(imdir, nframes, fntype)
    savebg(bg, bgdir, pickledir)
    subbgim(bg, submovdir, imdir)
    
    
def subbgmovies(fdir, submovbase, movbase, picklebase, nframes, fntype, 
boverwrite):
    '''Start in folder containing movie folders; see wingdet/README.txt.
    For each movie, generates background image and subtracts background from 
    each image.
    '''
    dirs = cmn.listsortfs(fdir)
    for exptdir in dirs: 
        print(os.path.basename(exptdir))
        movdir = os.path.join(exptdir, movbase)
        submovdir = os.path.join(exptdir, submovbase)
        pickledir = os.path.join(exptdir, picklebase)
        
        if os.path.exists(submovdir) and boverwrite == 'no':
            print('Images are already background-subtracted')
            continue

        os.chdir(movdir)
        try:
            subbgmovie(imdir=movdir, bgdir=exptdir, pickledir=pickledir, 
            submovdir=submovdir, nframes=nframes, fntype=fntype, overwrite='yes')
        except AssertionError:
            print('AssertionError')
            continue
