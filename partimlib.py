from piltest2 import *

# Code for first attempt at dividing images into wells.


def window(winlen):
    
    wind = list(np.ones(winlen)/winlen)
    return(wind)

imfile = 'background.tif'
t1 = 140
t2 = 215
imgdim = (1080, 1920)
onesimage = np.ones(imgdim)
WINLEN = 50


orig_im = np.array(Image.open(imfile)).astype(float)

## Plots histogram
#hist, bin_edges = np.histogram(orig_im, bins=60)
#bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
#plt.plot(bin_centers, hist, lw=2)
#plt.savefig('histogram.png')
#plt.close()

## Thresholds the image based on the peaks in the intensity histogram.
#low_values_indices = img < t1  # Where values are low
#high_values_indices = img > t2
#img[low_values_indices] = 0
#img[high_values_indices] = 0

## Functions to smooth the connected components.
#open_img = ndimage.binary_opening(img, structure=np.ones((10,10)).astype(img.dtype))
##close_img = ndimage.binary_closing(img, structure=np.ones((3,3)).astype(img.dtype))
#close_img = img
## Select the connected components.
#label_im, nb_labels = ndimage.label(close_img)
#sizes = ndimage.sum(onesimage, label_im, np.arange(1, nb_labels+1))
#coms = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, np.arange(1, nb_labels+1)))

plt.figure()
plt.imshow(orig_im, cmap=plt.cm.gray)

# Parameters for 20131006_movie1
#r = 70
#c = 358
#rpad = 25
#cpad = 22
#nrows = 300
#ncols = 300

# Parameters for 20131006_movie2
#r = 80
#c = 325
#rpad = 25
#cpad = 22
#nrows = 300
#ncols = 300

# Parameters for 20131006_movie3
#r = 75
#c = 315
#rpad = 22
#cpad = 20
#nrows = 300
#ncols = 300
#scaling = 1

# Parameters for 20131006_movie4
#r = 73
#c = 350
#rpad = 22
#cpad = 18
#nrows = 300
#ncols = 300
#scaling = 1

#Parameters for 20131006_movie5
#r = 55
#c = 310
#rpad = 32
#cpad = 30
#nrows = 300
#ncols = 300
#scaling = 1.015
#rshift = 3
#cshift = -5

#Parameters for 20131006_movie6
r = 35
c = 345
rpad = 25
cpad = 23
nrows = 300
ncols = 300
scaling = 0.98
rshift = 20
cshift = -20

for x in [0, 1, 2, 3]:
    for y in [0, 1, 2]:
        r1 = r +(nrows+rpad)*y*scaling + rshift*x
        r2 = r1 + nrows*scaling
        c1 = c + (ncols+cpad)*x*scaling + cshift*y
        c2 = c1 + ncols*scaling
        plotrect([r1, r2, c1, c2])

plt.savefig('wells.png')


# Plot the connected components and their centers of mass.
#plt.figure()
#plt.imshow(img, cmap=plt.cm.gray)
##plt.plot(coms. T[1], coms.T[0], 'ro', lw=1)
##plt.title('Connected comp = {0}'.format(nb_labels))
##plt.axis((0, 2000, 0, 1200))
#plt.savefig('conn_comp.png')
#plt.close()


#plt.figure()
#plt.subplot(211)
#plt.plot(orig_im[900,:], 'r')
#plt.plot(orig_im[500,:], 'g')
#plt.plot(orig_im[200,:], 'b')
#plt.subplot(212)
#plt.plot(img[900,:], 'r')
#plt.plot(img[500,:], 'g')
#plt.plot(img[200,:], 'b')
#plt.savefig('int_r.png')
#plt.close()


#plt.figure()
#plt.subplot(211)
#plt.plot(orig_im[:,500], 'r')
#plt.plot(orig_im[:,800], 'g')
#plt.plot(orig_im[:,1100], 'b')
#plt.plot(orig_im[:,1400], 'k')
#plt.subplot(212)
#plt.plot(img[:,500], 'r')
#plt.plot(img[:,800], 'g')
#plt.plot(img[:,1100], 'b')
#plt.plot(img[:,1400], 'k')
#plt.savefig('int_c.png')
#plt.close()


#wind = window(WINLEN)
#conv_c500 = np.convolve(img[:,500], wind, 'same')
#plt.plot(conv_c500, 'r')
#plt.savefig('conv_c500.png')      

