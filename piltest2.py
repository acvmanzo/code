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
#from skimage import morphology

##images = ['subm0043']
##imgnums = [14, 17, 18, 19, 21, 23, 26, 28, 36, 37, 40, 41, 42, 43, 44, 46, 47, 48, 50, 52, 55, 57, 60, 67, 75, 78, 82]
##imgnums_upright_closed = [14, 17, 18, 40, 60, 67, 78, 82]
#imgnums_upside_closed = [19, 21, 23, 44, 48, 52, 57, 69, 75]
#images = ['subm00{0}'.format(n) for n in imgnums_upside_closed]
##images = ['subm0025', 'subm0069', 'subm0027', 'subm0043', 'subm0082']

ext = '.tif'
outdir = '/home/andrea/Documents/auto/results/'
outdirrotimg = '/home/andrea/Documents/auto/results/rotimgs/'
imgdim = (290, 300)
onesimage = np.ones(imgdim)
areafile = outdir+'areameans.txt'
origin = np.array([75, 75], dtype=np.int32)
MIRRY = np.array([[-1, 0], [0, 1]])
MIRRX = np.array([[1, 0], [0, -1]])


def region(center_a, side_al):

    ''' Input:
    center: 2x2 numpy array with x, y coordinates of two opposite corners of center rectangle: [[x1, y1], [x2, y2]]
    side: 2x2 numpy array with x, y coordinates of two opposite orners of side rectangle
    
    Ccoordinates are written so that AP axis is x (so that angle 0 is when the fly is pointing along x axis, positive is in the anterior direction), and the ML axis is y, positive is going to the left).
'''
    center_p = np.dot(center, MIRRY)
    side_ar = np.dot(side, MIRRX)
    side_pl = np.dot(side, MIRRY)
    side_pr = np.dot(side_pl, MIRRX)
    
    return(center_a, center_p, side_al, side_ar, side_pl, side_pr)
    

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

    
def plotrect(corners, color):
    '''corners: [a, b, c, d] where a and b define the y coordinates, and c and d define the x coordinates'''
    
    plt.plot(corners[2:4], [corners[0], corners[0]], '{0}-'.format(color))
    plt.plot(corners[2:4], [corners[1], corners[1]], '{0}-'.format(color))
    plt.plot([corners[2], corners[2]], corners[0:2], '{0}-'.format(color))
    plt.plot([corners[3], corners[3]], corners[0:2], '{0}-'.format(color))


def findflies(imfile, plot='no'):
    '''
    Input:
    imfile = raw image file
    plot = 'yes' (plots figure) or 'no'
    
    Output:
    orig_im = original image
    label_im = array where connected components are labeled by integers
    nb_labels = number of connected components
    coms = centers of mass of connected components
    '''
    # Load the image. 
    orig_im = np.array(Image.open(imfile)).astype(float)
    img = np.array(Image.open(imfile)).astype(float)
    
    # Thresholds the image based on the peaks in the intensity histogram.
    low_values_indices = img < 120  # Where values are low
    #high_values_indices = img > 60
    img[low_values_indices] = 0
    #img[high_values_indices] = 0
    
    # Functions to smooth the connected components.
    #open_img = ndimage.binary_opening(img)
    close_img = ndimage.binary_closing(img, structure=np.ones((5,5)).astype(img.dtype))
    
    # Select the connected components.
    label_im, nb_labels = ndimage.label(close_img)
    sizes = ndimage.sum(onesimage, label_im, np.arange(1, nb_labels+1))
    coms = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, np.arange(1, nb_labels+1)))
    
    
    if plot == 'yes':
        # Plots images into a figure.
        plt.figure()
        plt.subplot(231)
        plt.imshow(orig_im, cmap=plt.cm.gray)
        plt.axis('off')
        plt.title('Original image')

        # Plot a histogram of the intensities.
        plt.subplot(232)
        hist, bin_edges = np.histogram(img, bins=60)
        bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
        plt.plot(bin_centers, hist, lw=2)
        plt.ylim(0, 500)
        plt.title('Histogram of intensities')

        # Plot the threshholded image.
        plt.subplot(233)
        plt.imshow(img, cmap=plt.cm.gray)
        plt.axis('off')
        plt.title('Threshholded image')

        # Plots the smoothed image.
        plt.subplot(234)
        plt.imshow(close_img, cmap=plt.cm.gray)
        plt.axis('off')
        plt.title('Binary closing')
        
        # Plot the connected components and their centers of mass.
        plt.subplot(235)
        plt.imshow(label_im, cmap=plt.cm.gray)
        plt.plot(coms.T[1], coms.T[0], 'rx', lw=1)
        plt.title('Connected comp = {0}'.format(nb_labels))
        plt.axis((0, 300, 0, 300))
        imgname = os.path.splitext(imfile)[0]
        plt.savefig(outdir+imgname+'_fig.png')
        plt.close()

    return(orig_im, label_im, nb_labels, coms)


def orientflies(orig_im, label_im, comp_label, coms, imgname):
    '''
    Input:
    orig_im = 
    label_im = array where connected components are labeled by integers (from findflies())
    comp_label = label designating connected components (one of the numbers in nb_labels from findflies())
    ''' 
    # Create an array where each entry is the index.
    posarray = np.rollaxis(np.mgrid[0:imgdim[0], 0:imgdim[1]], 0, 3)

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
    flypoints = [[0, 0], [10, 0], [0,5]]
    origpoints = np.dot(flypoints, eigenv) + centroid
    
    # Rotate image.
    flyoffset = [-75, -75]
    imgoffset = np.dot(flyoffset, 0.5*eigenv)
    rotimage = ndimage.interpolation.affine_transform(orig_im, 0.5*eigenv.T, centroid + imgoffset, output_shape = (150, 150))
    plt.figure()
    plt.imshow(rotimage, cmap=plt.cm.gray)
    plt.plot([0, 150], [75, 75], 'r-') 
    plt.plot([75, 75], [0, 150], 'r-') 

    # Select head+thorax and abdomen areas.
    #print(rotimage)
    #print(np.shape(rotimage))
    headthor = rotimage[45:75, 65:85]     
    plotrect([45, 75, 65, 85], 'y')
    
    abd = rotimage[75:110, 65:85]
    plotrect([75, 110, 65, 85], 'g')

    #print('headthor', np.mean(headthor))
    #print('abdomen', np.mean(abd))
    
    plt.savefig('{0}{1}_fly{2}.png'.format(outdir, imgname, comp_label))
    plt.close()
    return(rotimage)

def testareas(conds):
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
            orig_img, label_im, nb_labels, coms = findflies(imgname+'.tif')
            rotimage = rotateflies(orig_img, label_im, val[1], coms, imgname)

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



flies_up_closed = [
(14, 1), 
(14, 2), 
(17, 1), 
(17, 2), 
(18, 1), 
(18, 2), 
(40, 1), 
(40, 2), 
(60, 1), 
(60, 2), 
(67, 1), 
(67, 2), 
(78, 1), 
(78, 2), 
(82, 1), 
(82, 2)
]

#areasumfile = 'areasum_up_closed.txt'
#rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_up_closed/'

flies_up_ext = [
(36, 2), 
(41, 2), 
(42, 2), 
(43, 2), 
(44, 2), 
(52, 2), 
(55, 2), 
(57, 2),
]

#areasumfile = 'areasum_up_ext.txt'
#rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_up_ext/'


flies_down_closed = [
(19, 1), 
(21, 1), 
(21, 2), 
(23, 1), 
(44, 1), 
(48, 2), 
(52, 1), 
(55, 1), 
(57, 1), 
(69, 1), 
(75, 1)
]

#areasumfile = 'areasum_down_closed.txt'
#rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_down_closed/'



flies_down_ext = [
(23, 2), 
(25, 2), 
(26, 2), 
(27, 2), 
(28, 2), 
(47, 1), 
(48, 1), 
(50, 1)
]

#areasumfile = 'areasum_down_ext.txt'
#rotimgdir = '/home/andrea/Documents/auto/results/rotimgs_down_ext/'


conds = [
('flies_up_closed', flies_up_closed),
( 'flies_up_ext', flies_up_ext), 
( 'flies_down_ext', flies_down_ext), 
( 'flies_down_closed', flies_down_closed)
]


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
        plt.ylim(0, 50)

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

