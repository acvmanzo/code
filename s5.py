from libs.winglib import *
from wingsettings import *
import cv2


def findfliestest(subimarray, well, t):

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

    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    #print(structure)
    cv2.morphologyEx(img, cv2.MORPH_CLOSE, structure, img)
    close_im = img
    
    # Select the connected components.
    #print('ndimage.label', time.time()-START)
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

    d = {'orig_im':orig_im, 'th_im':th_im, 
    'close_im':close_im, 
    'label_im':label_im, 'nb_labels':nb_labels, 'uselab':uselabs, 'coms':coms,
    'usecoms':usecoms, 'dim':list(np.shape(orig_im))}
    
    return(d)


def testff():
    
    exptfiles = getexptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    imfile = os.path.join(movdir, 'mov02313.jpeg')
    imname = 'mov02313'


    wells = loadwells(wcpickle)
    wellnum = 0
    well = wells[wellnum]
    bgarray = np.load(bgpickle)
    subim = bgsub(bgarray, imfile)
    t = BODY_TH


    #plt.figure(figsize=(10,8), dpi=400)
    d = findflies(subim, well, t)
    #plotfindflies(d, imname, wellnum)
    #savetestfig(thfigdir, imname, wellnum, 'none')


#import cProfile
#cProfile.run('testff()', 'profcl_cv2')


#import pstats
#p = pstats.Stats('profcl_cv2')
#q = pstats.Stats('profcl_ndim')
#p.strip_dirs().sort_stats('cumulative').print_stats(15)
#q.strip_dirs().sort_stats('cumulative').print_stats(15)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("testff()", setup="from __main__ import testff", 
    number=10))


#Results:
#timeit, cv2: 0.486644029617
#timeit, ndimage: 0.5499
