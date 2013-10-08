from piltest2 import *

# Code for dividing image into wells.

imfile = 'background.tif'
orig_im = np.array(Image.open(imfile)).astype(float)

# Coordinates in chamber coordinates, with (0,0) at the bottom left corner of the bottom left well's ROI.
# +x is going to the right, +y is going up.
# each ROI is defined by coordinates at the bottom left corner and the top right corner.
# each well is length 1 in chamber coordinates

roi00 = [[0,0], [1,1]]
def defwells(roi00, xpad, ypad):

    
    for x in [0, 1, 2, 3]:
        for y in [0, 1, 2]:
            
    



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
