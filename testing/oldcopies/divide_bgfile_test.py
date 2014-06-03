############### TESTING CODE FOR DIVIDING BACKGROUND FILE INTO WELLS ###############

from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import cmn.cmn as cmn
import pickle


# Code for dividing image into wells.

imfile = 'background.tif'
orig_im = np.array(Image.open(imfile)).astype(float)

# Coordinates in chamber coordinates, with (0,0) at the bottom left corner of the bottom left well's ROI.
# +x is going to the right, +y is going up.
# each ROI is defined by coordinates at the bottom left corner and the top right corner.
# each well is length 1 in chamber coordinates

roi00 = [[0,0], [1,1]]

def defwells(roi00, xpad, ypad):

    
r = 55
c = 310
rpad = 32
cpad = 30
nrows = 300
ncols = 300
scaling = 1.015

for x in [0, 1, 2, 3]:
    for y in [0, 1, 2]:
        r1 = r +(nrows+rpad)*y
        r2 = r1 + nrows*scaling
        c1 = c + (ncols+cpad)*x
        c2 = c1 + ncols*scaling
        plotrect([r1, r2, c1, c2])

plt.savefig('wells_chambcoord.png')

imfile = 'background.tif'
t1 = 140
t2 = 215
imgdim = (1080, 1920)
onesimage = np.ones(imgdim)
WINLEN = 50

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

