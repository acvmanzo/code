from wingsettings import *
from libs.winglib import *


def testframeint():
    exptfiles1 = exptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles1
    bgarray = np.load(bgpickle)
    imfile = os.path.join(movdir, 'mov00734.jpeg')
    plotfiles = 'no'
    
    frameint(exptfiles1, bgarray, imfile, plotfiles)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("testframeint()", setup="from __main__ import testframeint", 
    number=10))


