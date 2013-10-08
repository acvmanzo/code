from partimlib import *

d = {}
d['config'] = [3, 4]
d['r'] = 35
d['c'] = 345
d['rpad'] = 25
d['cpad'] = 23
d['nrows'] = 300
d['ncols'] = d['nrows'] # For a square ROI.
d['scaling'] = 0.98
d['rshift'] = 20
d['cshift'] = -20

bgfile = 'background.tif'

pickledir = 'pickled'
#cmn.makenewdir(pickledir)


#wp = WellParams(d)
#wells = wp.defwells()
##checkwells(wells, bgfile)
#wp.savewells(pickledir)
#wp.saveparams(pickledir)

picklefile = os.path.join(pickledir, 'wellparams')
findwells(picklefile, bgfile, pickledir)
