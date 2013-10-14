import cProfile
import re
from libs.winglib import *

exptfiles = exptfiles(os.path.abspath('.'))
exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
rotfigdir, wingfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles


#IMNUMS = [str(x) for x in np.arange(10, 20, 1)]
#IMAGES = ['mov000'+n+'.jpeg' for n in IMNUMS]
#os.chdir(movdir)
cProfile.run('re.compile("multimint|exptfiles, IMAGES, plotfiles=\'no\', savemc=\'no\'")')

#cProfile.run('re.compile("foo|bar")')
