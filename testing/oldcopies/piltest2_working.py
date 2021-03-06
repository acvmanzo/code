from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import misc
from matplotlib.mlab import PCA
import cmn.cmn as cmn
import pickle
from mpl_toolkits.mplot3d import Axes3D
import scipy.signal as scis
import matplotlib as mpl
#from skimage import morphology

##images = ['subm0043']
##imgnums = [14, 17, 18, 19, 21, 23, 26, 28, 36, 37, 40, 41, 42, 43, 44, 46, 47, 48, 50, 52, 55, 57, 60, 67, 75, 78, 82]
##imgnums_upright_closed = [14, 17, 18, 40, 60, 67, 78, 82]
#imgnums_upside_closed = [19, 21, 23, 44, 48, 52, 57, 69, 75]

# File handling options.
EXT = '.tif'
PARDIR = os.path.abspath('.')
OUTRESDIR = PARDIR+'/results/'
OUTSUBTHDIR = PARDIR+'/subth/' 
OUTROTDIR = PARDIR+'/rotimgs/' 
OUTWINGDIR = PARDIR+'/wingimgs/' 
OUTTESTDIR = PARDIR+'/test/'
OUTTHTESTDIR = PARDIR+'/thtest/'
OUTBWTESTDIR = PARDIR+'/bwtest/'
OUTROITESTDIR = PARDIR+'/roitest/'
OUTROITESAMPTDIR = PARDIR+'/roitest_aminusp/'
OUTROITESTCETDIR = PARDIR+'/roitest_cl_ext/'


for outdir in [OUTRESDIR, OUTSUBTHDIR, OUTROTDIR, OUTWINGDIR, OUTTESTDIR, OUTTHTESTDIR, OUTBWTESTDIR, OUTROITESTDIR, OUTROITESAMPTDIR, OUTROITESTCETDIR]:
    cmn.makenewdir(outdir)

IMGDIM = (300, 300)
onesimage = np.ones(IMGDIM)
#areafile = OUTRESDIR+'areameans.txt'
origin = np.array([75, 75], dtype=np.int32)
MIRRY = np.array([[-1, 0], [0, 1]])
MIRRX = np.array([[1, 0], [0, -1]])

IMNUMS = [str(x) for x in [50]]
IMAGES = ['subm 00'+n for n in IMNUMS]
BODY_TH = 120
COMP_LABEL = [1, 2]
FLY_OFFSET = np.array([75, 75])
ROTIMSHAPE = (150, 150)
CENTER_A = np.array([[45, 10], [65, -10]]) # top left corner and bottom diagonal corner of square
#SIDE_AL = np.array([[25, 30], [55, 15]]) 
SIDE_AL = np.array([[25, 40], [45, 25]]) # top left corner and bottom diagonal corner of square
MID_L = np.array([[-15, 65], [15, 25]])
TMAT_FLY_IMG = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [FLY_OFFSET[0], FLY_OFFSET[1], 1]])
WING_TH_LOW = 20
#WING_TH_HIGH = 60
WING_TH_HIGH = 90


'''Note that matplotlib doesn't plot images and points using the same coordinate system (run this code to check:
imshow([[0,1],[0,0]])
plot(0, 1, 'yo')
'''


def region(center_a, side_al, mid_l):

    ''' Input:
    center: 2x2 numpy array with x, y coordinates of two opposite corners of center rectangle: [[x1, y1], [x2, y2]]
    side: 2x2 numpy array with x, y coordinates of two opposite orners of side rectangle
    
    Ccoordinates are written so that AP axis is x (so that angle 0 is when the fly is pointing along x axis, positive is in the anterior direction), and the ML axis is y, positive is going to the left).
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
        where offsetx, offsety are the center of the new axes. This matrix transforms points in fly coordinates to fly image coordinates.
        
    pts = coordinates in original axes (2x2 numpy array)
    '''
    return np.dot(pts, tmat[:-1, :-1]) + tmat[-1, :-1]

    
def plotrect(corners, color='r'):
    '''corners: [a, b, c, d] where a and b define the rows, and c and d define the columns'''
    
    plt.plot(corners[2:4], [corners[0], corners[0]], '{0}-'.format(color))
    plt.plot(corners[2:4], [corners[1], corners[1]], '{0}-'.format(color))
    plt.plot([corners[2], corners[2]], corners[0:2], '{0}-'.format(color))
    plt.plot([corners[3], corners[3]], corners[0:2], '{0}-'.format(color))


def plotrois(imrois):
    cols = np.tile(['b', 'g', 'r', 'c', 'm', 'y', 'w'], 2)
    cols = cols[:np.shape(imrois)[0]+1]
    for x, ((r1,c1), (r2,c2)) in enumerate(np.sort(imrois, axis=1)):
        plotrect([r1, r2, c1, c2], color=cols[x])
        plt.text(c1, r1, '{0}'.format(x), color=cols[x])


def findflies(imfile, t, outdir, plot='yes'):
    '''
    Input:
    imfile = raw image file
    t = intensity threshold for selecting fly body
    plot = 'yes' (plots figure) or 'no'
    
    Output:
    orig_im = original image
    label_im = array where connected components are labeled by integers; 0 is the background and labeled components start at 1
    nb_labels = number of connected components (not including the background)
    coms = centers of mass of connected components
    '''
    

    return(orig_im, label_im, nb_labels, coms)


def orientflies(orig_im, label_im, comp_label, coms, fly_offset, rotimshape, imname):
    '''
    Rotates image so that each fly (connected component) is positioned vertically along its AP axis.
    
    Input:
    orig_im = original image
    label_im = array where connected components are labeled by integers (from findflies())
    comp_label = label designating connected components; starts at 1
    coms = centers of mass of the connected components
    fly_offset = list of new center coordinates for the oriented image
    rotimshape = tuple with size of the rotated image
    imname = image name
    plot = 'no' (does not plot figure) or 'yes'
    
    Output:
    orient_im = rotated/translated image
    ''' 
    # Create an array where each entry is the index.
    posarray = np.rollaxis(np.mgrid[0:IMGDIM[0], 0:IMGDIM[1]], 0, 3)

    # Find the coordinates of the points comprising each connected component.
    comppos = posarray[label_im == comp_label]
    centroid = np.mean(comppos, axis=0)

    # Check that the centers of mass are equal to the mean of the detected components.
    assert np.all(centroid == coms[comp_label-1])

    # Mean subtract data.
    comppos = comppos - centroid

    # Singular value decomposition
    u, singval, eigenv = np.linalg.svd(comppos, full_matrices=False)
    
    # Plot points in the new axes.
    #flypoints = [[0, 0], [10, 0], [0,5]]
    #origpoints = np.dot(flypoints, eigenv) + centroid
    
    # Orient image.
    flyoffset = fly_offset*-1
    imgoffset = np.dot(flyoffset, 0.5*eigenv)
    rotimage = ndimage.interpolation.affine_transform(orig_im, 0.5*eigenv.T, centroid + imgoffset, output_shape = rotimshape)
    
    return(rotimage)

def plot_rotimage(orient_im, rotimshape, fly_offset, comp_label, imname, outdir):
    # Plot oriented image.
    plt.figure()
    plt.imshow(orient_im, cmap=plt.cm.gray)
    plt.plot([0, rotimshape[1]], fly_offset, 'r-') 
    plt.plot(fly_offset, [0, rotimshape[0]], 'r-') 
    plt.savefig('{0}{1}_fly{2}.png'.format(outdir, imname, comp_label))


    # Select head+thorax and abdomen areas. Thought that I could use intensity in these regions to disambiguate direction, but too similar.
    #headthor = orient_im[45:75, 65:85]     
    #plotrect([45, 75, 65, 85], 'y')
    #abd = orient_im[75:110, 65:85]
    #plotrect([75, 110, 65, 85], 'g')


def plot_wingimage(w_im, imrois, img, comp_label, outdir):
    plt.figure()
    plt.imshow(w_im, cmap=plt.cm.gray)
    plotrois(imrois)
    plt.savefig('{0}{1}_fly{2}.png'.format(outdir, img, comp_label))

def defrois(center_a, side_al, mid_l, tmat):
    '''
    Input: 
    orient_im = image in which fly is aligned vertically along its AP axis; output of orientflies()
    '''
  
    # Define regions of interest in fly coordinates.
    #center_a = [[30, 65], [10, 85]] # In image coordinates
    #side_al = [[40, 40], [20, 60]]

    rois = region(center_a, side_al, mid_l) 
    # center_a, center_p, side_al, side_ar, side_pl, side_pr  = rois
    
    # Convert regions of interest to fly image coordinates.
    imrois = changecoord(tmat, rois)
    
    return(imrois)
    
    
def getrc(imrois):
    '''From the array imrois (returned by defrois()), returns the x and y coordinates. These are row and column coordinates if plotted like an image, but are x and y coordinates if plotted using plt.plot.
    '''
    
    x = []
    y = []
    for (r1,c1), (r2,c2) in np.sort(imrois, axis=1):
        x.extend([r1, r2])
        y.extend([c1, c2])
    
    return(x,y)

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




def roimeans(w_im, imrois):
    '''
    Input:
    w_im = image of oriented fly, threshholded to isolate wings
    imrois = list of points that define regions of interest in the image coordinates; returned by defrois(); the order or rois are: 
        center_a, center_p, side_al, side_ar, side_pl, side_pr.
    Output:
    roi_int: list of mean intensities 
    '''
       
    ## Measure mean intensity over each ROI.
    roi_int = []
    for (r1,c1), (r2,c2) in np.sort(imrois, axis=1):
        roi_int.append(np.mean(w_im[r1:r2, c1:c2]))
    return(roi_int)

    
def testareas2(conds):
#with open(areafile, 'w') as f:
    #f.write('Means of various areas\n')

    d = {}
    for cond in conds:
        areasumfile = 'areasum'+cond[0]+'.txt'
        rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_'+cond[0]+'/'
        cmn.makenewdir(rotimgdir)
        
        twc_vals = []
        twl_vals = []
        twr_vals = []

        d[cond[0]] = {}

        for val in cond[1]:      
            imgname = 'subm00{0}'.format(val[0])
            print(imgname)
            orig_im, label_im, nb_labels, coms = findflies(imgname+'.tif')
            rotimage = rotateflies(orig_im, label_im, val[1], coms, imgname)

        # Figuringout how to distinguish fly orientation.
        #plt.plot(rotimage[:, 75].T)

            # Thresholding image to pick out wings.
            throtimage = np.copy(rotimage)
            low_values_indices = throtimage < 20  # Where values are low
            high_values_indices = throtimage > 60
            throtimage[low_values_indices] = 0
            throtimage[high_values_indices] = 0

            #thheadthor = throtimage[45:75, 65:85]
            #print(thheadthor)
            #thabd = throtimage[75:110, 65:85]
            twc = [120, 140, 70, 90]
            twcwing = throtimage[twc[0]:twc[1], twc[2]:twc[3]]
            twc_vals.append(np.mean(twcwing))

            twl = [110, 130, 40, 60]
            twlwing = throtimage[twl[0]:twl[1], twl[2]:twl[3]]
            twl_vals.append(np.mean(twlwing))

            twr = [110, 130, 100, 120]
            twrwing = throtimage[twr[0]:twr[1], twr[2]:twr[3]]
            twr_vals.append(np.mean(twrwing))
                    
            plt.figure()
            plt.subplot(121)
            plt.imshow(throtimage, cmap=plt.cm.gray)
            plotrect(twc, 'g')
            plotrect(twl, 'b')
            plotrect(twr, 'b')

            plt.subplot(122)
            plt.plot(throtimage[:, 75].T)
            plt.savefig('{0}{1}_test_fly{2}.png'.format(rotimgdir, imgname, val[1]))
            plt.close()

            #with open(areafile, 'a') as f:
                #for area in [('twcwing', twcwing), ('twlwing', twlwing), ('twrwing', twrwing)]:
                    #f.write('{0}\tfly {1}\t{2}\t{3}\n'.format(imgname, x, area[0], np.mean(area[1])))
                        
            with open('{0}{1}'.format(outdir, areasumfile), 'w') as g:
                g.write('Summary of area intensity means\n')
                g.write('Mean intensity middle\t{0}\n'.format(np.mean(twc_vals)))
                g.write('Mean intensity left\t{0}\n'.format(np.mean(twl_vals)))
                g.write('Mean intensity right\t{0}\n'.format(np.mean(twr_vals)))

        d[cond[0]]['twc_vals'] = twc_vals
        d[cond[0]]['twl_vals'] = twl_vals
        d[cond[0]]['twr_vals'] = twr_vals

    with open(outdir+'areasumdict', 'w') as h:
        pickle.dump(d, h)
    return(d)





#areasumfile = 'areasum_down_ext.txt'
#rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_down_ext/'




def plot_testareas():
    
    data = [
    ('flies_up_closed', 221),
    ( 'flies_up_ext', 222), 
    ( 'flies_down_ext', 223), 
    ( 'flies_down_closed', 224)
    ]


    plt.figure()
    for datum in data:
        #print(d[datum[0]])
        twc_vals = d[datum[0]]['twc_vals']
        twl_vals = d[datum[0]]['twl_vals']
        twr_vals = d[datum[0]]['twr_vals']

        x_vals = np.hstack((np.tile(1, len(twc_vals)), np.tile(2, len(twl_vals)), np.tile(3, len(twr_vals))))
        print(x_vals)
        y_vals = twc_vals + twl_vals + twr_vals
        print((y_vals))

        plt.subplot(datum[1])
        plt.scatter(x_vals, y_vals)
        plt.xticks([1,2,3], ['center', 'left', 'right'])
        plt.ylabel('Mean_intensity')
        plt.title(datum[0])
        plt.ylim(0, 50)

    plt.savefig(outdir+'compvalues.png')


def plotres_testareas():

    with open(outdir+'areasumdict', 'r') as f:
        d = pickle.load(f)
    #print(d)

    data = [
    ('flies_up_closed', 221),
    ( 'flies_up_ext', 222), 
    ( 'flies_down_ext', 223), 
    ( 'flies_down_closed', 224)
    ]

    #data = [
    #('flies_up_closed', 221)
    #]

    plt.figure()


    for datum in data:
        #print(d[datum[0]])
        twc_vals = d[datum[0]]['twc_vals']
        twl_vals = d[datum[0]]['twl_vals']
        twr_vals = d[datum[0]]['twr_vals']

        x_vals = np.hstack((np.tile(1, len(twc_vals)), np.tile(2, len(twl_vals)), np.tile(3, len(twr_vals))))
        print(x_vals)
        y_vals = twc_vals + twl_vals + twr_vals
        print((y_vals))

        plt.subplot(datum[1])
        plt.scatter(x_vals, y_vals)
        plt.xticks([1,2,3], ['center', 'left', 'right'])
        plt.ylabel('Mean_intensity')
        plt.title(datum[0])
        plt.ylim(0, 50)

    plt.savefig(outdir+'compvalues.png')

def plotresrot_testareas():
    plotres_testareas()

    conds2 = [
    ( 'flies_down_ext', flies_down_ext), 
    ( 'flies_down_closed', flies_down_closed)
    ]
    d = {}
    for cond in conds2:
            areasumfile = 'areasum'+cond[0]+'.txt'
            rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_'+cond[0]+'/'
            cmn.makenewdir(rotimgdir)
            
            twc_vals = []
            twl_vals = []
            twr_vals = []

            d[cond[0]] = {}

            for val in cond[1]:      
                imgname = 'subm00{0}'.format(val[0])
                print(imgname)
                orig_im, label_im, nb_labels, coms = findflies(imgname+'.tif')
                rotimage = orientflies(orig_im, label_im, val[1], coms)
                rotimage = ndimage.interpolation.rotate(rotimage, 180)
            # Figuringout how to distinguish fly orientation.
            #plt.plot(rotimage[:, 75].T)

                # Thresholding image to pick out wings.
                throtimage = np.copy(rotimage)
                low_values_indices = throtimage < 20  # Where values are low
                high_values_indices = throtimage > 60
                throtimage[low_values_indices] = 0
                throtimage[high_values_indices] = 0

                #thheadthor = throtimage[45:75, 65:85]
                #print(thheadthor)
                #thabd = throtimage[75:110, 65:85]
                twc = [120, 140, 70, 90]
                twcwing = throtimage[twc[0]:twc[1], twc[2]:twc[3]]
                twc_vals.append(np.mean(twcwing))

                twl = [110, 130, 40, 60]
                twlwing = throtimage[twl[0]:twl[1], twl[2]:twl[3]]
                twl_vals.append(np.mean(twlwing))

                twr = [110, 130, 100, 120]
                twrwing = throtimage[twr[0]:twr[1], twr[2]:twr[3]]
                twr_vals.append(np.mean(twrwing))
                        
                plt.figure()
                plt.subplot(121)
                plt.imshow(throtimage, cmap=plt.cm.gray)
                plotrect(twc, 'g')
                plotrect(twl, 'b')
                plotrect(twr, 'b')

                plt.subplot(122)
                plt.plot(throtimage[:, 75].T)
                plt.savefig('{0}{1}_test_fly{2}.png'.format(rotimgdir, imgname, val[1]))
                plt.close()

                #with open(areafile, 'a') as f:
                    #for area in [('twcwing', twcwing), ('twlwing', twlwing), ('twrwing', twrwing)]:
                        #f.write('{0}\tfly {1}\t{2}\t{3}\n'.format(imgname, x, area[0], np.mean(area[1])))
                            
                #with open('{0}{1}'.format(outdir, areasumfile), 'w') as g:
                    #g.write('Summary of area intensity means\n')
                    #g.write('Mean intensity middle\t{0}\n'.format(np.mean(twc_vals)))
                    #g.write('Mean intensity left\t{0}\n'.format(np.mean(twl_vals)))
                    #g.write('Mean intensity right\t{0}\n'.format(np.mean(twr_vals)))

            d[cond[0]]['twc_vals'] = twc_vals
            d[cond[0]]['twl_vals'] = twl_vals
            d[cond[0]]['twr_vals'] = twr_vals

        ##with open(outdir+'areasumdictrot', 'w') as h:
            #pickle.dump(d, h)
        
        #return(d)


    data = [
    ( 'flies_down_ext', 221), 
    ( 'flies_down_closed', 222)
    ]

    plt.figure()


    for datum in data:
        #print(d[datum[0]])
        twc_vals = d[datum[0]]['twc_vals']
        twl_vals = d[datum[0]]['twl_vals']
        twr_vals = d[datum[0]]['twr_vals']

        x_vals = np.hstack((np.tile(1, len(twc_vals)), np.tile(2, len(twl_vals)), np.tile(3, len(twr_vals))))
        print(x_vals)
        y_vals = twc_vals + twl_vals + twr_vals
        print((y_vals))

        plt.subplot(datum[1])
        plt.scatter(x_vals, y_vals)
        plt.xticks([1,2,3], ['center', 'left', 'right'])
        plt.ylabel('Mean_intensity')
        plt.title(datum[0])
        plt.ylim(0, 120)

    plt.savefig(outdir+'compvalues_rot.png')

def plot3d():
    with open(outdir+'areasumdict', 'r') as f:
        d = pickle.load(f)
    print(d)

    data = [
    ('flies_up_closed', 'k', 'o'),
    ( 'flies_up_ext', 'r', '*'), 
    ( 'flies_down_ext', 'b', 's'), 
    ( 'flies_down_closed', 'y', '^')
    ]

    #data = [
    #('flies_up_closed', 221)
    #]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #twc_vals = []
    #twl_vals = []
    #twr_vals = []

    for datum in data:
        twc_vals = d[datum[0]]['twc_vals']
        twl_vals = d[datum[0]]['twl_vals']
        twr_vals = d[datum[0]]['twr_vals']

        ax.scatter(twc_vals, twr_vals, twl_vals, zdir=twl_vals, c=datum[1], marker=datum[2])

    #plt.subplot(datum[1])
    #plt.scatter(x_vals, y_vals)
    #plt.xticks([1,2,3], ['center', 'left', 'right'])
    #plt.ylabel('Mean_intensity')
    #plt.title(datum[0])
    #plt.ylim(0, 50)

    plt.savefig(outdir+'3dplot.png')
    plt.show()



