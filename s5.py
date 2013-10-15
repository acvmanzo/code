from libs.winglib import *
from wingsettings import *
import cv2
import cv

def arr2imtest(a):
    #a = np.absolute(a)
    #print('-a', time.time()-START)
    #a = -a
    #a=a-a.min() # Adds the minimum value to each entry in the array.
    #print('ascale', time.time()-START)
    #a=a/a.max()*255.0 # Scales each array so that the max value is 255.
    #a = np.uint8(a)
    return a


def bgsubtest(bgarray, imfile):
    '''Loads background array from pickle file and image from imfile. 
    Subtracts background from image.
    Inputs:
    bgpickle = pickled file containing background array (pickled/bgarray)
    imfile = one file from the movie image sequence
    '''
    
    bg = bgarray
    print('bg max', np.max(bg))
    print('bg min', np.min(bg))
    #print('load im', time.time()-START)
    #im = np.array(Image.open(imfile))[:,:,0].astype(float) # This loads a 3D 
    im = cv2.imread(imfile, 0)
    print('im max', np.max(im))
    print('im min', np.min(im))
    #array with all the channels identical.
    #print('Subtracting array', time.time()-START)
    #print('-a', time.time()-START)
    #subimarr = arr2imtest(im-bg)
    subimarr = bg - im
    print('subim max', np.max(subimarr))
    print('subim min', np.min(subimarr))
    return(subimarr)


def findfliestest(subimarray, well, t):

    # Load the image.
    r1, r2, c1, c2 = well
    nrows = r2-r1
    ncols = c2-c1
    #subimarray = np.array(array2image(subimarray))
    orig_im = subimarray[r1:r2, c1:c2]
    print('subim well max', np.max(orig_im))
    print('subim well min', np.min(orig_im))
    orig_im = orig_im - np.min(orig_im)
    print('subim well max', np.max(orig_im))
    print('subim well min', np.min(orig_im))
    orig_im = orig_im/np.max(orig_im)*255
    print('subim well max', np.max(orig_im))
    print('subim well min', np.min(orig_im))
    

    img = np.copy(orig_im)
    img = img - np.min(img)
    print('img max', np.max(img))
    print('img min', np.min(img))
    
    img = np.uint8(img)
    onesimage = np.ones(np.shape(orig_im))
   
    th_im = np.copy(img)
    retval, th_im = cv2.threshold(src=img, thresh=175, maxval=255, 
    type=cv2.THRESH_BINARY, dst=th_im)
    
    ## Thresholds the image based on the peaks in the intensity histogram.
    #floator = np.copy(orig_im)
    #low_values_indices = floator < 120  # Where values are low
    ##high_values_indices = img > 60
    #floator[low_values_indices] = 0
    #th_im = np.copy(floator)
    #img[high_values_indices] = 0
    
    # Functions to smooth the connected components.
    #open_img = ndimage.binary_opening(img)
    # binary image closing
    close_im = np.copy(th_im)
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    cv2.morphologyEx(src=th_im, op=cv2.MORPH_CLOSE, kernel=structure, 
    dst=close_im)


    # Select the connected components.
    contim = np.copy(close_im)
    contours, hier = cv2.findContours(contim, mode=cv2.RETR_LIST, 
    method=cv2.CHAIN_APPROX_NONE)
    #print(np.shape(contours))
    #print(np.shape(contours[0]))
    #print(np.shape(contours[0][0]))
    #print(contours[0][0][0][0])
    #print(contours[80,0,0])
    
    contpic = np.empty(np.shape(close_im))
    cv2.drawContours(image=contpic, contours=contours, contourIdx=1, 
    color=(255,0,0), thickness=cv.CV_FILLED)
    print(np.max(contpic))
    li = contpic > 254
    
    origdim = np.shape(contpic)
    posarray = np.rollaxis(np.mgrid[0:origdim[0], 0:origdim[1]], 0, 3)
    #print('compute centroid', time.time()-START)
    # Find the coordinates of the points comprising each connected component.
    comppos = posarray[contpic == 255]
    centroid = np.mean(comppos, axis=0)

    print(np.mean(comppos, axis=0))
        #ca1 = cv2.contourArea(contours[0])
    #ca2 = cv2.contourArea(contours[1])
    ##ca3 = cv2.contourArea(contours[2])
    #ca = ca1 + ca2
    #print('contour area', ca)
    
    ccom = cv2.moments(contours[0])
    print('ccom', ccom)
    
    label_im, nb_labels = ndimage.label(close_im)
    sizes = ndimage.sum(onesimage, label_im, np.arange(1, nb_labels+1))
    #print('ndimage.com', time.time()-START)
    coms = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, 
    np.arange(1, nb_labels+1)))
    #print('end ndimage.com', time.time()-START)
    
    #print('Size filter', time.time()-START)
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

    d = {'orig_im':orig_im, 'th_im':th_im, 'centroid':centroid, 
    'close_im':close_im, 'contim':contim, 'contours':contours, 'contpic':contpic, \
    'label_im':label_im, 'nb_labels':nb_labels, 'uselab':uselabs, 'coms':coms,
    'usecoms':usecoms, 'dim':list(np.shape(orig_im))}
    
    return(d)

def plotfindfliestest(d, imname, wellnum):
    '''Plots a figure showing different processing steps in findflies().
    Input:
    d = dictionary; output of findflies()
    figdir = directory to save figure
    '''
    
    # Plots original image.
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

    # Plots the smoothed image.
    plt.subplot2grid((2,3), (1,1), colspan=1)
    plt.imshow(d['close_im'], cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Binary closing')
    
    # Plots the contours image.
    plt.subplot2grid((2,3), (1,2), colspan=1)
    plt.imshow(d['contpic'], cmap=plt.cm.gray)
    plt.plot(d['centroid'][1], d['centroid'][0], 'ro', markersize=3)
    plt.axis('off')
    plt.title('Contours')
    rows, cols = d['dim']
    plt.axis((0, cols, rows, 0))
    
    ## Plot the connected components and their centers of mass.
    #plt.subplot2grid((2,3), (1,1), colspan=1)
    #plt.imshow(d['close_im'], cmap=plt.cm.gray)
    
    #plt.plot(d['coms'].T[1], d['coms'].T[0], 'ro', mec='r', lw=1, ms=2)
    ##plt.plot([0, 290], [290, 0], 'ys', ms=5)
    #rows, cols = d['dim']
    #plt.axis((0, cols, rows, 0))
    #plt.title('Comp = {0}'.format(d['nb_labels']))
    
    ## Plot the size-filtered connected components and their centers of mass.
    #plt.subplot2grid((2,3), (1,2), colspan=1)
    #plt.imshow(d['label_im'], cmap=plt.cm.gray)
    
    #plt.plot(d['usecoms'].T[1], d['usecoms'].T[0], 'ro', mec='r', lw=1, ms=2)
    ##plt.plot([0, 290], [290, 0], 'ys', ms=5)
    #rows, cols = d['dim']
    #plt.axis((0, cols, rows, 0))
    #plt.title('Size-fil comp={0}'.format(len(d['uselab'])))


def testff():
    
    exptfiles = getexptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    imfile = os.path.join(movdir, 'mov02313.jpeg')
    imname = 'mov02313'
    wells = loadwells(wcpickle)
    wellnum = 1
    well = wells[wellnum]
    bgarray = np.load(bgpickle)
    subim = bgsubtest(bgarray, imfile)
    t = BODY_TH

    #plt.figure(figsize=(10,8), dpi=400)
    d = findfliestest(subim, well, t)
    plotfindfliestest(d, imname, wellnum)
    savetestfig(thfigdir, imname, wellnum, 'none')
    #d = findflies(subim, well, t)
    #plotfindflies(d, imname, wellnum)
    #savetestfig(thfigdir, imname, wellnum, 'none')

testff()

#import cProfile
#cProfile.run('testff()', 'profcl_cv2')


#import pstats
#p = pstats.Stats('profcl_cv2')
#q = pstats.Stats('profcl_ndim')
#p.strip_dirs().sort_stats('cumulative').print_stats(15)
#q.strip_dirs().sort_stats('cumulative').print_stats(15)

#if __name__ == '__main__':
    #import timeit
    #print(timeit.timeit("testff()", setup="from __main__ import testff", 
    #number=10))


