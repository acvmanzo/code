from wingsettings import *
from libs.winglib import *
from s5 import *


def testframeint():
    
    exptfiles = getexptfiles(os.path.abspath('.'))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    
    #IMNUMS = [str(x) for x in np.arange(10, 11, 1)]
    #IMAGES = ['mov000'+n+'.jpeg' for n in IMNUMS]
    #os.chdir(movdir)
    #movsmc, movmmc, movroi = multimint(exptfiles1, IMAGES, plotfiles='no', 
    #savemc='no')
    
    
    bgarray = np.load(bgpickle)
    imfile = os.path.join(movdir, 'mov00734.jpeg')
    plotfiles = 'no'
    frameint(exptfiles, bgarray, imfile, plotfiles)
    
    


import cProfile
print(os.getcwd())
cProfile.run('testframeint()', 'prof_cv2_all')
#testframeint()


#To view and sort/analyze the statistics:
#import pstats
#p = pstats.Stats('profstatsmultimint')
 #p.strip_dirs().sort_stats(-1).print_stats()
 #p.sort_stats('cumulative').print_stats(10)
