
import os
import numpy as np
from scipy import ndimage
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import cmn.cmn as cmn
import pickle
import libs.genplotlib as gpl
from wingsettings import *

MIRRY = np.array([[-1, 0], [0, 1]])
MIRRX = np.array([[1, 0], [0, -1]])
START = time.time()

######### FUNCTIONS FOR BACKGROUND SUBTRACTION ########

def arr2im(a):
    #a = np.absolute(a)
    print('-a', time.time()-START)
    a = -a
    #a=a-a.min() # Adds the minimum value to each entry in the array.
    print('ascale', time.time()-START)
    a=a/a.max()*255.0 # Scales each array so that the max value is 255.
    #a = np.uint8(a)
    return a


def bgsub(bgpickle, imfile):
    '''Loads background array from pickle file and image from imfile. 
    Subtracts background from image.
    Inputs:
    bgpickle = pickled file containing background array (pickled/bgarray)
    imfile = one file from the movie image sequence
    '''
    print('load bgpickle', time.time()-START)
    bg = np.load(bgpickle)
    print('load im', time.time()-START)
    im = np.array(Image.open(imfile))[:,:,0].astype(float) # This loads a 3D 
    #array with all the channels identical.
    
    subimarr = arr2im(im-bg)   
    return(subimarr)


############# FUNCTIONS FOR DETECTING FLIES AND WINGS ##############

####### HELPER FUNCTIONS ###########

def loadwells(wcfile):
    with open(wcfile, 'r') as f:
        wells = pickle.load(f)
    return(wells)

def findflies(subimarray, imfile, well, t, savepickle='no'):
    '''
    Input:
    subimarray = array of subtracted image
    imname = name of image (ex., mov00001.jpeg)
    well = row and column coords of ROI surrounding well: [r1, r2, c1, c2]
    t = intensity threshold for selecting fly body]
    savepickle = whether or not to save a picklefile
    
    Output: 
    A dictionary with the following keys, values:
    orig_im = original image
    th_im = thresholded image
    close_im = thresholded image after binary closing is applied
    label_im = array where connected components are labeled by integers; 0 is 
    the background and labeled components start at 1 
    nb_labels = number of connected components (not including the background)
    coms = centers of mass of connected components
    '''
    imname = os.path.splitext(imfile)[0]
    
    # Load the image.
    r1, r2, c1, c2 = well
    nrows = r2-r1
    ncols = c2-c1
    #subimarray = np.array(array2image(subimarray))
    orig_im = subimarray[r1:r2, c1:c2]
    img = np.copy(orig_im)
    onesimage = np.ones(np.shape(orig_im))
    
    # Thresholds the image based on the peaks in the intensity histogram.
    low_values_indices = img < t  # Where values are low
    #high_values_indices = img > 60
    img[low_values_indices] = 0
    th_im = np.copy(img)
    #img[high_values_indices] = 0
    
    # Functions to smooth the connected components.
    #open_img = ndimage.binary_opening(img)
    close_im = ndimage.binary_closing(img, 
    structure=np.ones((5,5)).astype(img.dtype))
    
    # Select the connected components.
    label_im, nb_labels = ndimage.label(close_im)
    sizes = ndimage.sum(onesimage, label_im, np.arange(1, nb_labels+1))
    coms = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, 
    np.arange(1, nb_labels+1)))
    
    # Filter by size of connected component.
    smsizefil = np.array(sizes) > np.tile(0.0011*(nrows*ncols), nb_labels)
    usesizes = smsizefil*sizes
    uselabs = []
    for snum, size in enumerate(usesizes):
        if size > 0:
            uselabs.append(snum+1)
    #uselab = []
    #for size, snum in sorted(lsizes, reverse=True)[:2]:
        #uselab.append(snum)
    usecoms = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, 
    uselabs))

    
    d = {'imfile':imfile, 'imname': imname, 'orig_im':orig_im, 'th_im':th_im, 
    'close_im':close_im, 
    'label_im':label_im, 'nb_labels':nb_labels, 'uselab':uselabs, 'coms':coms,
    'usecoms':usecoms, 'dim':list(np.shape(orig_im))}
    
    # Saves output into a picklefile.
    if savepickle == 'yes':
        exptdir = cmn.defpardir('.')
        dpickledir = os.path.join(exptdir, PICKLEBASE, PIMAGEBASE, imname)
        cmn.makenewdir(dpickledir)            
        dpicklefile = os.path.join(dpickledir, 'findflies')
        with open(dpicklefile, 'w') as f:
            pickle.dump(d, f)

    return(d)


def orientflies(orig_im, label_im, comp_label, labellist, coms, fly_offset, rotimshape, 
imname):
    '''
    Rotates image so that each fly (connected component) is positioned 
    vertically along its AP axis.
    Input:
    orig_im = original image
    label_im = array where connected components are labeled by integers 
    (from findflies())
    comp_label = label designating connected components; starts at 1
    labellist = list of numbers designating connected components
    coms = centers of mass of the connected components
    fly_offset = list of new center coordinates for the oriented image
    rotimshape = tuple with size of the rotated image
    imname = image name
    plot = 'no' (does not plot figure) or 'yes'
    
    Output:
    orient_im = rotated/translated image
    ''' 
    #print('orient flies', time.time()-START)
    # Create an array where each entry is the index.
    origdim = np.shape(orig_im)
    posarray = np.rollaxis(np.mgrid[0:origdim[0], 0:origdim[1]], 0, 3)

    # Find the coordinates of the points comprising each connected component.
    comppos = posarray[label_im == comp_label]
    centroid = np.mean(comppos, axis=0)

    # Check that the centers of mass are equal to the mean of the detected 
    # components.
    assert np.all(centroid == coms[labellist.index(comp_label)])

    # Mean subtract data.
    comppos = comppos - centroid
    #print('svd', time.time()-START)
    # Singular value decomposition
    u, singval, eigenv = np.linalg.svd(comppos, full_matrices=False)
    
    # Plot points in the new axes.
    #flypoints = [[0, 0], [10, 0], [0,5]]
    #origpoints = np.dot(flypoints, eigenv) + centroid
    
    # Orient image.
    flyoffset = fly_offset*-1
    imgoffset = np.dot(flyoffset, 0.5*eigenv)
    #print('rotate',time.time()-START)
    rotimage = ndimage.interpolation.affine_transform(orig_im, 0.5*eigenv.T, 
    centroid + imgoffset, output_shape = rotimshape)
    
    return(rotimage)


def findwings(orient_im, low_value, high_value):
    ''' Thresholds image to pick out wings.
    Input:
    orient_im = image of oriented fly
    low_value = scalar; values below this are set to 0
    high_value = scalar; values above this set to 0
    Output:
    w_im = thresholded image
    '''   
    
    w_im = orient_im
    low_values_indices = w_im < low_value  # Where values are below low_value
    high_values_indices = w_im > high_value
    w_im[low_values_indices] = 0
    w_im[high_values_indices] = 0
    
    return(w_im)

############# FUNCTIONS FOR PLOTTING FLY IMAGES #############
def plotfindflies(d, wellnum, figdir):
    '''Plots a figure showing different processing steps in findflies().
    Input:
    d = dictionary; output of findflies()
    figdir = directory to save figure
    '''
    # Plots original image.
    plt.figure()
    plt.subplot2grid((2,3), (0,0), colspan=1)
    plt.imshow(Image.fromarray(d['orig_im']), cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('BGsub')

    # Plot a histogram of the intensities.
    plt.subplot2grid((2,3), (0,1), colspan=2)
    hist, bin_edges = np.histogram(d['orig_im'], bins=60)
    bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
    plt.plot(bin_centers, hist, lw=2)
    plt.ylim(0, 400)
    plt.xlim(0, 300)
    plt.title('Intensity histogram')

    # Plot the threshholded image.
    plt.subplot2grid((2,3), (1,0), colspan=1)
    plt.imshow(d['th_im'], cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Thresholded')

    ## Plots the smoothed image.
    #plt.subplot2grid((2,3), (1,1), colspan=1)
    #plt.imshow(d['close_im'], cmap=plt.cm.gray)
    #plt.axis('off')
    #plt.title('Binary closing')
    
    # Plot the connected components and their centers of mass.
    plt.subplot2grid((2,3), (1,1), colspan=1)
    plt.imshow(d['label_im'], cmap=plt.cm.gray)
    
    plt.plot(d['coms'].T[1], d['coms'].T[0], 'ro', mec='r', lw=1, ms=2)
    #plt.plot([0, 290], [290, 0], 'ys', ms=5)
    rows, cols = d['dim']
    plt.axis((0, cols, rows, 0))
    plt.title('Comp = {0}'.format(d['nb_labels']))
    
    # Plot the size-filtered connected components and their centers of mass.
    plt.subplot2grid((2,3), (1,2), colspan=1)
    plt.imshow(d['label_im'], cmap=plt.cm.gray)
    
    plt.plot(d['usecoms'].T[1], d['usecoms'].T[0], 'ro', mec='r', lw=1, ms=2)
    #plt.plot([0, 290], [290, 0], 'ys', ms=5)
    rows, cols = d['dim']
    plt.axis((0, cols, rows, 0))
    plt.title('Size-fil comp={0}'.format(len(d['uselab'])))
    
    
    cmn.makenewdir(figdir)
    imname = os.path.splitext(d['imfile'])[0]
    welldir = os.path.join(figdir, 'well{0:02d}'.format(wellnum))
    cmn.makenewdir(welldir)
    # Saves figure in the exptdir/figdir/well##/ folder.
    #plt.savefig(os.path.join(welldir, '{0}_thfig.png'.format(imname)))
    # Saves figure in the exptdir/figdir folder; more convenient for testing.
    plt.savefig('{0}_{1}_thfig.png'.format(welldir, imname))
    plt.close()


def expt_findplotflies(bgpickle, movbase, wells):
    '''Start from experiment folder.
    Input:
    bgpickle = pickled file containing bgarray
    movbase = name of movie/ directory
    wells = list of well coordinates
    '''
    os.chdir(movbase)
    files = cmn.listsortfs(fdir)
    for f in files:
        # To compute for each image:
        subim = bgsub(bgpickle, f)
        # To load from a saved image:
        #subimfile = os.path.join('../'+SUBMOVBASE, 'sub'+f)
        #subim = np.array(Image.open(subimfile)).astype(float)
        for n, well in enumerate(wells):
            print('Well', n)
            try:
                d = findflies(subim, imfile, well, BODY_TH, 'no')
                plotfindflies(d, n, THFIGDIR)
                plt.close()
            except IndexError:
                print('No connected components')
                continue  


def plotrotim(orient_im, rotimshape, fly_offset, wellnum, flynum, imname, outdir):
    # Plot oriented image.
    welldir = os.path.join(outdir, 'well{0:02d}'.format(wellnum))
    cmn.makenewdir(welldir)
    plt.figure()
    plt.imshow(orient_im, cmap=plt.cm.gray)
    plt.plot([0, rotimshape[1]], fly_offset, 'r-') 
    plt.plot(fly_offset, [0, rotimshape[0]], 'r-') 
    # Saves figure in the exptdir/figdir/well##/ folder.
    #plt.savefig(os.path.join(welldir, '{0}_fly{1}.png'.format(imname, 
    #flynum)))
    # Saves figure in the exptdir/figdir/ folder (more convenient for 
    #testing).
    plt.savefig(os.path.join(outdir, '{0}_{1:02d}_fly{2}.png'.format(imname, 
    wellnum, flynum)))

    
def plotrois(imrois):
    cols = np.tile(['b', 'g', 'r', 'c', 'm', 'y', 'w'], 2)
    cols = cols[:np.shape(imrois)[0]+1]
    for x, ((r1,c1), (r2,c2)) in enumerate(np.sort(imrois, axis=1)):
        gpl.plotrect([r1, r2, c1, c2], color=cols[x])
        plt.text(c1, r1, '{0}'.format(x), color=cols[x])


def plot_wingimage(w_im, imrois, imname, flynum, outdir, wellnum):
    cmn.makenewdir(outdir)
    plt.figure()
    plt.imshow(w_im, cmap=plt.cm.gray)
    plotrois(imrois)
    welldir = os.path.join(outdir, 'well{0:02d}'.format(wellnum))
    cmn.makenewdir(welldir)
    # Saves figure in the exptdir/figdir/well##/ folder.
    #figname = os.path.join(welldir, '{0}_{1}.png'.format(imname, flynum))
    # Saves figure in the exptdir/figdir/ folder (more convenient for 
    #testing).
    figname = os.path.join(outdir, '{0}_{1:02d}_fly{2}.png'.format(imname, 
    wellnum, flynum))

    plt.savefig(figname)
    plt.close()


######### FUNCTIONS FOR DEFINING ROIS #################

def tmatflyim(flyoffset):
    
    a = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [flyoffset[0], flyoffset[1], 1]])
    return(a)


def region(center_a, side_al, mid_l):

    ''' Input:
    center: 2x2 numpy array with x, y coordinates of two opposite corners of 
    center rectangle: [[x1, y1], [x2, y2]]
    side: 2x2 numpy array with x, y coordinates of two opposite orners of 
    side rectangle
    
    Ccoordinates are written so that AP axis is x (so that angle 0 is when the
    fly is pointing along x axis, positive is in the anterior direction), and 
    the ML axis is y, positive is going to the left).
    '''
    center_p = np.dot(center_a, MIRRY)
    side_ar = np.dot(side_al, MIRRX)
    side_pl = np.dot(side_al, MIRRY)
    side_pr = np.dot(side_pl, MIRRX)
    mid_r = np.dot(mid_l, MIRRX)
    
    return(center_a, center_p, side_al, side_ar, side_pl, side_pr, mid_l, mid_r)
    

def changecoord(tmat, pts):
    '''
    Inputs: 
    tmat = transformation matrix (homogenous coordinates)
        ex. tmat = np.array([
        [0, 1, 0],
        [-1, 0, 0],
        [offsetx, offsety, 1]])
        where offsetx, offsety are the center of the new axes. This matrix 
        transforms points in fly coordinates to fly image coordinates.
        
    pts = coordinates in original axes (2x2 numpy array)
    '''
    return np.dot(pts, tmat[:-1, :-1]) + tmat[-1, :-1]


def defrois(center_a, side_al, mid_l, tmat):
    '''
    Input: 
    orient_im = image in which fly is aligned vertically along its AP axis; 
    output of orientflies()
    '''
  
    # Define regions of interest in fly coordinates.
    #center_a = [[30, 65], [10, 85]] # In image coordinates
    #side_al = [[40, 40], [20, 60]]

    rois = region(center_a, side_al, mid_l) 
    # center_a, center_p, side_al, side_ar, side_pl, side_pr, mid_l, mid_r  = rois
    
    # Convert regions of interest to fly image coordinates.
    imrois = changecoord(tmat, rois)
    
    return(imrois)

######### FUNCTIONS FOR ANALYZING ROI INTENSITIES #################

def roimeans(w_im, imrois):
    '''
    Input:
    w_im = image of oriented fly, threshholded to isolate wings
    imrois = list of points that define regions of interest in the image 
    coordinates; returned by defrois(); the order or rois are: 
        center_a, center_p, side_al, side_ar, side_pl, side_pr, mid_l, mid_r
    Output:
    roi_int: list of mean intensities 
    '''
       
    ## Measure mean intensity over each ROI.
    roi_int = []
    for (r1,c1), (r2,c2) in np.sort(imrois, axis=1):
        roi_int.append(np.mean(w_im[r1:r2, c1:c2]))
    return(roi_int)


def subroi(roi_int):
    center_a = roi_int[0]
    center_p = roi_int[1]
    side_a = np.sum(roi_int[2:4])
    side_p = np.sum(roi_int[4:6])
    med = np.sum(roi_int[6:8])
    
    return(center_a, center_p, side_a, side_p, med)


########### COMBINED FUNCTIONS FOR ANALYSIS ###################

def wellint(imfile, bgpickle, well, wellnum, plotfiles, thfigdir, rotfigdir, 
wingfigdir):
    '''Finds the difference in ROI intensities for each fly in one well of 
    one movie frame.
    Inputs:
    imfile = image file from movie
    bgpickle = pickled background movie array
    well = coordinates of well
    plotfile = 'yes' or 'no'; indicates whether to plot files
    thfigdir = directory to plot threshold figures
    
    '''
    print('subim', time.time()-START)
    subim = bgsub(bgpickle, imfile)
    #subim = np.array(Image.open(os.path.join('submovie', 'sub'+imfile))).astype(float)
    
    # Finding flies.
    d = findflies(subim, imfile, well, BODY_TH, 'no')
    #print('findflies', time.time()-START)
    if len(d['uselab']) == 0:
        print('No connected components')
    # Plotting functions.
    if plotfiles == 'yes':
        plotfindflies(d, wellnum, thfigdir)
        plt.close()
    
    flysmc = []
    flymmc = []
    flyroi = []
    # Finds data for each fly in the well.
    for flyn, comp_label in enumerate(d['uselab']):
        
        rotimshape = 0.5*np.array(d['dim'])
        flyoffset = np.array(0.5*rotimshape)
        # Orients flies.
        #print('rotate flies', time.time()-START)
        orient_im = orientflies(d['orig_im'], d['label_im'], comp_label, 
        d['uselab'], d['usecoms'], flyoffset, rotimshape, d['imname'])
        
        tmatfly = tmatflyim(flyoffset)
        # Defines roi coordinates.
        imrois = defrois(CENTER_A, SIDE_AL, MID_L, tmatfly)
        # Thresholds fly image to find wings.
        #print('finding wings', time.time()-START)
        w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
        
        # Plotting functions.
        if plotfiles == 'yes':
            plotrotim(orient_im, rotimshape, flyoffset, wellnum, flyn, 
            d['imname'], rotfigdir)
            plt.close()
            plot_wingimage(w_im, imrois, d['imname'], flyn, 
            wingfigdir, wellnum)
            plt.close()

        # Analyzing ROI intensities.
        #print('analyzing roi intensities', time.time()-START)
        roi_int = np.array(roimeans(w_im, imrois))
        center_a, center_p, side_a, side_p, med = subroi(roi_int)
        
        #print('appending rois', time.time()-START)
        
        if ((center_p+side_p) - (center_a+side_a)) > 0:
            flysmc.append(side_p - center_p)
            flymmc.append(med - center_p)

        else:
            flysmc.append(side_a - center_a)
            flymmc.append(med - center_a)
    
        flyroi.append(roi_int)
        
    return(flysmc, flymmc, flyroi)
    

def frameint(exptfiles, imfile, plotfiles):
    '''Finds the difference in ROI intensities for each fly in each well 
    in one movie frame. 
    Inputs:
    exptfiles = exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle (output of 
    wingsettings.exptfiles())
    imfile = image from movie
    plotfiles = 'yes' or 'no'; whether or not to plot files
    '''

    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles

    subim = bgsub(bgpickle, imfile)
    wells = loadwells(wcpickle)
    framesmc = np.empty((1, len(wells)))
    framemmc = np.empty((1, len(wells)))
    frameroi = []
    for n, well in enumerate(wells):
        print(n, time.time()-START)
        try:
            flysmc, flymmc, flyroi = wellint(imfile, bgpickle, well, n, plotfiles, 
            thfigdir, rotfigdir, wingfigdir)
            framesmc[0,n] = np.max(flysmc)
            framemmc[0,n] = np.max(flymmc)
            frameroi.append(flyroi)
        except ValueError:
            continue

    return(framesmc, framemmc, frameroi)


def multimint(exptfiles, images, plotfiles, picklefiles):
    '''Finds the difference in ROI intensities for each fly in each well 
    in multiple images.
    Inputs:
    exptfiles = exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle (output of 
    wingsettings.exptfiles())
    images = list of image names
    plotfiles = 'yes' or 'no'; whether or not to plot files
    picklefiles = 'yes' or 'no'; whether or not to pickle output
    '''
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles
    
    movlen = len(images)
    wells = loadwells(wcpickle)
    movsmc = np.empty((len(images), len(wells)))
    movmmc = np.empty((len(images), len(wells)))
    movroi = []
    
    for frame, imfile in enumerate(images):
        print(imfile, time.time()-START)
        framesmc, framemmc, frameroi = frameint(exptfiles, imfile, plotfiles)
        movsmc[frame,:] = framesmc
        movmmc[frame,:] = framemmc
        movroi.append(frameroi)
    
    if picklefiles == 'yes':
        smcfile = os.path.join(pickledir, 'smc_{0}ims'.format(movlen))
        mmcfile = os.path.join(pickledir, 'mmc_{0}ims'.format(movlen))
        roifile = os.path.join(pickledir, 'roiints_{0}ims'.format(movlen))
        
        with open(smcfile, 'w') as f:
            pickle.dump(movsmc, f)
        with open(mmcfile, 'w') as g:
            pickle.dump(movmmc, g)
        with open(roifile, 'w') as h:
            pickle.dump(movroi, h)
    
    return(movsmc, movmmc, movroi)
        

def exptint(exptfiles, plotfiles, picklefiles):
    '''Finds the difference in ROI intensities for each fly in each well 
    in multiple movieframes.
    '''
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, 
    rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles
    
    os.chdir(movdir)
    frames = cmn.listsortfs()

    movsmc, movmmc, movroi = multiimint(exptfiles, frames, plotfiles)

    return(movsmc, movmmc, movroi)


def plotintd(exptdir, movsmc, movmmc):
    
    plt.figure()
    plt.plot(movsmc, 'r')
    plt.savefig('Side-center.png')
