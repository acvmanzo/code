from wingsettings import *
from libs.winglib import *


def testframeint():
    
    exptfiles1 = exptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles1
    
    IMNUMS = [str(x) for x in np.arange(10, 11, 1)]
    IMAGES = ['mov000'+n+'.jpeg' for n in IMNUMS]
    os.chdir(movdir)
    movsmc, movmmc, movroi = multimint(exptfiles1, IMAGES, plotfiles='no', 
    savemc='no')
    
    
    #bgarray = np.load(bgpickle)
    #imfile = os.path.join(movdir, 'mov00734.jpeg')
    #plotfiles = 'no'
    #frameint(exptfiles1, bgarray, imfile, plotfiles)
    
    


import cProfile
print(os.getcwd())
cProfile.run('testframeint()', 'profstatsmultimint')
#testframeint()
