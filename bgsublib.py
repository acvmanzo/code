from PIL import Image
import os
import numpy as np
import cmn.cmn as cmn

def genbgim(imdir='.', bgdir='.', nframes=100, fntype='median'):
    '''Generates a background image from a sequence of image files.
    Input:
    imdir = directory containing the sequence of image files; default is 
    current directory
    outdir = directory in which to save background image; default is current 
    directory
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence; default is 100
    fntype = 'median, 'average'; method for combining nframes; default is 'median'.
    Output:
    bgnew = numpy array of background image 
    '''
    
    # Load frames for generating background image.
    imdir = os.path.abspath(imdir)
    files = sorted(os.listdir(imdir))
    moviel = len(files)
    
    bg = np.array(Image.open(files[0])).astype(float)

    for x in np.linspace(1, moviel-1, nframes):
        c = np.array(Image.open(files[int(x)])).astype(float)
        bg = np.dstack((bg, c))

    if fntype == 'median':
        bgnew = np.median(bg, 2)
    if fntype == 'average':
        bgnew = np.average(bg, 2)

    # Save background image.
    bgnew1 = Image.fromarray(np.uint8(np.absolute(bgnew)))
    bgnew1.save(os.path.join(bgdir, 'background.tif'))
    return(bgnew)
    

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
    
    for x in np.arange(0, len(files), 1):
        outfile = os.path.join(submoviedir, 'sub'+files[int(x)])
        c = np.array(Image.open(files[int(x)])).astype(float)
        subarr = c-bg
        subim = Image.fromarray(np.uint8(np.absolute(subarr)))
        subim.save(outfile)


def subbgmovie(submoviedir, imdir='.', bgdir='.', nframes=100, 
fntype='median'):
    '''Generates background image from nframes of movie and saves in outdir. 
    Subtracts background from each file in movie image sequence.
    Input:
    submoviedir = directory to deposit the background-subtracted image files
    imdir = directory containing the sequence of image files; default is 
    current directory
    outdir = directory in which to save background image; default is current 
    directory
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence; default is 100
    fntype = 'median, 'average'; method for combining nframes; default is 'median'.
    '''
    
    os.chdir(imdir)
    bg = genbgim(imdir, bgdir, nframes, fntype)
    subbgim(bg, submoviedir, imdir)
    
    
def subbgmovies(fdir, submovbase, movbase, nframes=100, fntype='median'):
    '''Start in folder containing movie folders; see wingdet/README.txt.
    '''
    dirs = cmn.listsortfs(fdir)
    for exptdir in dirs: 
        movdir = os.path.join(exptdir, movbase)
        submovdir = os.path.join(exptdir, submovbase)
        os.chdir(movdir)
        subbgmovie(submovdir, imdir=movdir, bgdir=exptdir, nframes=nframes, 
        fntype=fntype)
    
