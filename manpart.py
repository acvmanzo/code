#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the parameters in the expt/text/wellparams.txt file. 

# Run from the expts/movie##/ folder.

# Adjust the parameter file to tweak the ROI positions.
# Explanations of the parameters are below:
#   config = 2-element list: [# wells in vertical direction, # wells in 
#       horizontal direction]; for aggression [3, 4]; for courtship [4,10]
#   r = Top row of the ROI surrounding the top left well.
#   c = Left column of the ROI surrounding the top left well.
#   rpad = # rows in between the wells (vertical direction)
#   cpad = # columns in between the wells (horizontal direction)
#   nrows = # rows in each ROI
#   ncols = # cols in each ROI
#   rshift = # rows to shift the ROI during each iteration in the horizontal 
#       direction; used if image is rotated
#   cshift = # columns to shift the ROI during each iteration in the vertical 
#       direction; used if image is rotated
#   scaling = scalar multiple of each value; used if the zoom is altered

# DO NOT EDIT THE 'wellparams.txt' FILE IN GEANY; IT WILL BREAK THE TABS

from libs.partimlib import *
from wingsettings import *

PTEXTFILE = os.path.join(TEXTBASE, WELLPARAMSN+'.txt')

findwellstext(BGFILE, PTEXTFILE, WELLPARAMSN, WELLCOORDSN, PICKLEBASE)
