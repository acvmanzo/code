from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import misc
from matplotlib.mlab import PCA
#from skimage import morphology

#images = ['subm0043']
images = ['subm0025', 'subm0069', 'subm0027', 'subm0043', 'subm0082']
ext = '.tif'
outdir = '/home/andrea/Documents/auto/results/'
imgdim = (290, 300)
onesimage = np.ones(imgdim)
areafile = outdir+'areameans.txt'




def plotrect(corners, color):
    '''corners: [a, b, c, d] where a and b define the y coordinates, and c and d define the x coordinates'''
    
    plt.plot(corners[2:4], [corners[0], corners[0]], '{0}-'.format(color))
    plt.plot(corners[2:4], [corners[1], corners[1]], '{0}-'.format(color))
    plt.plot([corners[2], corners[2]], corners[0:2], '{0}-'.format(color))
    plt.plot([corners[3], corners[3]], corners[0:2], '{0}-'.format(color))


with open(areafile, 'w') as f:
    f.write('Means of various areas\n')

for imgname in images:

    imgfile = imgname+ext
  
    plt.figure()
    plt.subplot(231)

    # Load the image. Plots into a figure.
    img1 = np.array(Image.open(imgfile)).astype(float)
    img = np.array(Image.open(imgfile)).astype(float)
    plt.imshow(img1, cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Original image')

    # Plot a histogram of the intensities.
    plt.subplot(232)
    hist, bin_edges = np.histogram(img, bins=60)
    bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
    plt.plot(bin_centers, hist, lw=2)
    plt.ylim(0, 500)
    plt.title('Histogram of intensities')

    # Thresholds the image based on the peaks in the histogram.
    low_values_indices = img < 120  # Where values are low
    #high_values_indices = img > 60
    img[low_values_indices] = 0
    #img[high_values_indices] = 0

    # Plot the threshholded image.
    plt.subplot(233)
    plt.imshow(img, cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Threshholded image')

    # Functions to smooth the connected components.
    #open_img = ndimage.binary_opening(img)
    close_img = ndimage.binary_closing(img, structure=np.ones((5,5)).astype(img.dtype))
    plt.subplot(234)
    plt.imshow(close_img, cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Binary closing')

    # Label the connected components.
    label_im, nb_labels = ndimage.label(close_img)
    sizes = ndimage.sum(onesimage, label_im, np.arange(1, nb_labels+1))
    #print(sizes)
    coms = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, np.arange(1, nb_labels+1)))
    #print(coms)

    # Label their centers of mass.
    plt.subplot(235)
    plt.imshow(label_im, cmap=plt.cm.gray)
    plt.plot(coms.T[1], coms.T[0], 'rx', lw=1)
    plt.title('Connected comp = {0}'.format(nb_labels))
    plt.axis((0, 300, 0, 300))
    plt.savefig(outdir+imgname+'_fig.png')
    plt.close()

    # Create an array where each entry is the index.
    #y = np.arange(0, 290, 1)
    #x = np.arange(0, 300, 1)
    #ycoords = []
    #xcoords = []
    #for row in y:
        #ycoords.append(np.tile(row, 300))
    #for col in x:
        #xcoords.append(np.tile(col, 290))
    #posarray = np.dstack((ycoords, np.array(xcoords).T))   

    posarray = np.rollaxis(np.mgrid[0:imgdim[0], 0:imgdim[1]], 0, 3)

    # For each connected component:
    for x in np.arange(nb_labels):
    #for x in [0]:
    # Find the coordinates of the points comprising each connected component.
        print(x)
        comppos = posarray[label_im == x+1]
        centroid = np.mean(comppos, axis=0)
        #print(comppos)
        #print(np.shape(comppos))
        #print(comppos.T[1])
        #print(np.mean(comppos, axis=0))
        #print(comppos.T[0])
        #print(coms)

        # Check that the centers of mass are equal to the mean of the detected components.
        assert np.all(centroid == coms[x])

        # Mean subtract data.
        comppos = comppos - centroid

        # Singular value decomposition
        u, singval, eigenv = np.linalg.svd(comppos, full_matrices=False)
        
        # Plot points in the new axes.
        flypoints = [[0, 0], [10, 0], [0,5]]
        origpoints = np.dot(flypoints, eigenv) + centroid
        #print(origpoints)
        #plt.plot(origpoints.T[1], origpoints.T[0], 'ro', lw=2)
        #plt.savefig(outdir+imgname+'_fig2.png')
        
        # Rotate image.
        flyoffset = [-75, -75]
        imgoffset = np.dot(flyoffset, 0.5*eigenv)
        rotimage = ndimage.interpolation.affine_transform(img1, 0.5*eigenv.T, centroid + imgoffset, output_shape = (150, 150))
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
        
        plt.savefig('{0}{1}_fly{2}.png'.format(outdir, imgname, x))
        plt.close()
        #plt.figure()
        #plt.imshow(headthor, cmap=plt.cm.gray)
        
        # Figuringout how to distinguish fly orientation.
        #plt.plot(rotimage[:, 75].T)

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
        
        twl = [110, 130, 40, 60]
        twlwing = throtimage[twl[0]:twl[1], twl[2]:twl[3]]
        
        twr = [110, 130, 100, 120]
        twrwing = throtimage[twr[0]:twr[1], twr[2]:twr[3]]
                
        plt.figure()
        plt.subplot(121)
        plt.imshow(throtimage, cmap=plt.cm.gray)
        
        plotrect(twc, 'g')
        plotrect(twl, 'b')
        plotrect(twr, 'b')
        
        #plt.title(' Mean = {0:f}'.format(thwingmean))
        
        plt.subplot(122)
        plt.plot(throtimage[:, 75].T)
       
        plt.savefig('{0}{1}_test_fly{2}.png'.format(outdir, imgname, x))
        plt.close()
        
        with open(areafile, 'a') as f:
            for area in [('twcwing', twcwing), ('twlwing', twlwing), ('twrwing', twrwing)]:
                f.write('{0}\tfly {1}\t{2}\t{3}\n'.format(imgname, x, area[0], np.mean(area[1])))
            
        
    #plt.show()
