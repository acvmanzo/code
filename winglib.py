
import os
import numpy as np
from scipy import ndimage
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import pickle


PICKLEBASE = 'pickled'

def loadwells(wcfile):
    with open(wcfile, 'r') as f:
        wells = pickle.load(f)
    return(wells)


def findflies(imfile, well, t, savepickle='no'):
    '''
    Input:
    imfile = raw image file
    well = row and column coords of ROI surrounding well: [r1, r2, c1, c2]
    t = intensity threshold for selecting fly body
    
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
    # Load the image. 
    imname = os.path.splitext(os.path.basename(imfile))[0]
    r1, r2, c1, c2 = well
    orig_im = np.array(Image.open(imfile)).astype(float)[r1:r2, c1:c2]
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
    
    d = {'imname': imname, 'orig_im':orig_im, 'th_im':th_im, 'close_im':close_im, 
    'label_im':label_im, 'nb_labels':nb_labels, 'coms':coms, 
    'dim':list(np.shape(orig_im))}
    
    # Saves output into a picklefile.
    if savepickle == 'yes':
        exptdir = cmn.defpardir('.')
        dpickledir = os.path.join(exptdir, PICKLEBASE, 'images', imname)
        cmn.makenewdir(dpickledir)            
        dpicklefile = os.path.join(dpickledir, 'findflies')
        with open(dpicklefile, 'w') as f:
            pickle.dump(d, f)
    
    return(d)


def plotfindflies(d, figdir):
    '''Plots a figure showing different processing steps in findflies().
    Input:
    d = dictionary; output of findflies()
    figdir = directory to save figure
    '''
    # Plots original image.
    plt.figure()
    plt.subplot2grid((2,3), (0,0), colspan=1)
    plt.imshow(d['orig_im'], cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Original')

    # Plot a histogram of the intensities.
    plt.subplot2grid((2,3), (0,1), colspan=2)
    hist, bin_edges = np.histogram(d['orig_im'], bins=60)
    bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
    plt.plot(bin_centers, hist, lw=2)
    plt.ylim(0, 400)
    plt.title('Intensity histogram')

    # Plot the threshholded image.
    plt.subplot2grid((2,3), (1,0), colspan=1)
    plt.imshow(d['th_im'], cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Thresholded')

    # Plots the smoothed image.
    plt.subplot2grid((2,3), (1,1), colspan=1)
    plt.imshow(d['close_im'], cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Binary closing')
    
    # Plot the connected components and their centers of mass.
    plt.subplot2grid((2,3), (1,2), colspan=1)
    plt.imshow(d['label_im'], cmap=plt.cm.gray)
    print(plt.axis())
    print(d['coms'])
    print(d['coms'].T)
    plt.plot(d['coms'].T[1], d['coms'].T[0], 'ro', mec='r', lw=1, ms=2)
    #plt.plot([0, 290], [290, 0], 'ys', ms=5)
    print(plt.axis())
    rows, cols = d['dim']
    plt.axis((0, cols, rows, 0))
    plt.title('Comp = {0}'.format(d['nb_labels']))
    
    cmn.makenewdir(figdir)
    plt.savefig(os.path.join(figdir, d['imname']+'_fig.png'))
    plt.close()



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
