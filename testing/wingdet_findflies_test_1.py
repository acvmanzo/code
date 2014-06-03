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
    #print('bg max', np.max(bg))
    #print('bg min', np.min(bg))
    #print('load im', time.time()-START)
    #im = np.array(Image.open(imfile))[:,:,0].astype(float) # This loads a 3D 
    im = cv2.imread(imfile, 0)
    #print('im max', np.max(im))
    #print('im min', np.min(im))
    #array with all the channels identical.
    #print('Subtracting array', time.time()-START)
    #print('-a', time.time()-START)
    #subimarr = arr2imtest(im-bg)
    subimarr = np.clip(bg-im, 0, 255).astype(np.uint8)
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
    #print('subim well max', np.max(orig_im))
    #print('subim well min', np.min(orig_im))
    #orig_im = orig_im - np.min(orig_im)
    #print('subim well max', np.max(orig_im))
    #print('subim well min', np.min(orig_im))
    #orig_im = orig_im/np.max(orig_im)*255
    #print('subim well max', np.max(orig_im))
    #print('subim well min', np.min(orig_im))
  
    img = np.copy(orig_im)
    # Threshold image.
    th_im = np.copy(img)
    cv2.threshold(src=img, thresh=150, maxval=255, 
    type=cv2.THRESH_BINARY, dst=th_im)
    # Binary closing.
    close_im = np.copy(th_im)
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    cv2.morphologyEx(src=th_im, op=cv2.MORPH_CLOSE, kernel=structure, 
    dst=close_im)
    # Find contours.
    contim = np.copy(close_im)
    contours, hier = cv2.findContours(contim, mode=cv2.RETR_LIST, 
    method=cv2.CHAIN_APPROX_NONE)
    # Find areas and centers of mass of contours.
    contpics = []
    ccoms = []
    #careas = []
    careascv = []
    for x, contour in enumerate(contours):
        contpic = np.zeros(np.shape(img))
        cv2.drawContours(image=contpic, contours=contours, contourIdx=x, 
        color=(255,0,0), thickness=cv.CV_FILLED)
               
        cmean = np.mean(contour, axis=0)
        #carea = np.sum(contpic)/255.
        careacv = cv2.contourArea(contours[x])
        contpics.append(contpic)
        #if carea > 0.0011*(nrows*ncols):
            #contpics.append(contpic)
            #ccoms.extend(cmean)
            #careas.append(carea)
        if careacv > 0.0011*(nrows*ncols):
            contpics.append(contpic)
            ccoms.extend(cmean)
            careascv.append(careacv)
        #print('contour', np.shape(contour))
        #print('contour mean', np.mean(contour, axis=0))
    
    #print('contpics shape', np.shape(contpics))
    #print('ccoms', ccoms)
    #print('careas', careas)
    print('careascv', careascv)
    
    #allcontpic = np.sum(contpics, axis=0)
        
    d = {'orig_im':orig_im, 'th_im':th_im, 'close_im':close_im, 
    'contim':contim, 'contpics':contpics,
    'coms':np.array(ccoms), 'contours':contours, 'dim':np.shape(orig_im)}
    
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
    #plt.imshow(d['allcontpic'], cmap=plt.cm.gray)
    plt.plot(d['coms'].T[0], d['coms'].T[1], 'ro', markersize=3)
    #plt.axis('off')
    plt.title('Comp={0}'.format(len(d['coms'])))
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

def orientfliestest(orig_im, contpics, coms, flynum, fly_offset, rotimshape):

    #print('orient flies', time.time()-START)
    # Create an array where each entry is the index.
    #print('Create posarray', time.time()-START)
    origdim = np.shape(orig_im)
    #print('orig', np.shape(orig_im))
    #print('contpic', np.shape(contpics[0]))
    posarray = np.rollaxis(np.mgrid[0:origdim[0], 0:origdim[1]], 0, 3)
    #print(posarray[:,0])
    #print('compute centroid', time.time()-START)
    # Find the coordinates of the points comprising each connected component.
    comppos = posarray[contpics[flynum] == 255]
    #print(np.mean(comppos, axis=0))
    
    #centroid = np.mean(comppos, axis=0)
    centroid = [coms[flynum][1], coms[flynum][0]]
    #print(centroid)
    #print('end compute centroid', time.time()-START)
    # Check that the centers of mass are equal to the mean of the detected 
    # components.
    #print('assertion', time.time()-START)
    #assert np.all(centroid == coms[labellist.index(comp_label)])

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
    centroid + imgoffset, output_shape = rotimshape, order=1)
    
    
    return(rotimage)

def testff():
    
    exptfiles = getexptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    imfile = os.path.join(movdir, 'mov02313.jpeg')
    imname = 'mov02313'
    wells = loadwells(wcpickle)
    wellnum = 1
    well = wells[wellnum]
    bgarray = np.load(bgpickle).astype(np.int16) + 5
    subim = bgsubtest(bgarray, imfile)
    t = BODY_TH
    flynum = 0

    #plt.figure(figsize=(10,8), dpi=400)
    d = findflies(subim, well, t)
    plt.figure()
    
    plt.subplot(121)
    plt.imshow(d['contpics'][0], cmap=plt.cm.gray)
    plt.subplot(122)
    plt.imshow(d['contpics'][1], cmap=plt.cm.gray)
    plt.savefig('contpics.png')
        
    #d = findflies(subim, well, t)
    #plotfindfliestest(d, imname, wellnum)
    #plotfindflies(d, imname, wellnum)
    #savetestfig(thfigdir, imname, wellnum, 'none')
    #rotimshape = 0.5*np.array(d['dim'])
    #flyoffset = np.array(0.5*rotimshape)        
    #rotim = orientfliestest(d['orig_im'], d['contpics'], d['coms'], flynum, 
    #flyoffset, rotimshape)
    #rotim = orientflies(d['orig_im'], d['label_im'], flynum+1, 
    #d['uselab'], d['usecoms'], flyoffset, rotimshape)
    #plotrotim(rotim, rotimshape, flyoffset, wellnum, flynum, imname, 
    #rotfigdir)
    #savetestfig(rotfigdir, imname, wellnum, flynum)
    
    #d = findflies(subim, well, t)
    #plotfindflies(d, imname, wellnum)
    #savetestfig(thfigdir, imname, wellnum, 'none')

testff()

#import cProfile
#cProfile.run('testff()', 'profall_ndim_comp')
#cProfile.run('testff()', 'profall_cv2_careascv')


#import pstats
#p = pstats.Stats('profall_cv2')
#q = pstats.Stats('profall_ndim')
#p.strip_dirs().sort_stats('cumulative').print_stats(15)
#q.strip_dirs().sort_stats('cumulative').print_stats(15)

#if __name__ == '__main__':
    #import timeit
    #print(timeit.timeit("testff()", setup="from __main__ import testff", 
    #number=10))


