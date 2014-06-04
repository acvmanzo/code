# Uses timeit to time a function.

from wingsettings import *
from libs.winglib import *


def testframeint():
    exptfiles = getexptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    bgarray = np.load(bgpickle)
    imfile = os.path.join(movdir, 'mov00734.jpeg')
    plotfiles = 'no'
    
    frameint(exptfiles, bgarray, imfile, plotfiles)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("testframeint()", setup="from __main__ import testframeint", 
    number=10))


