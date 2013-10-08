from partimlib import *

config = [3, 4]
r = 35
c = 345
rpad = 25
cpad = 23
nrows = 300
ncols = nrows # For a square ROI.
scaling = 0.98
rshift = 20
cshift = -20
bgfile = 'background.tif'

wp = WellParams(config, r, c, rpad, cpad, nrows, ncols, scaling, rshift, 
    cshift)

wells = wp.defwells()
checkwells(wells, bgfile)
