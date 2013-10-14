from libs.winglib import *
from wingsettings import *


def testmovie(exptdir, secint):
    '''Takes several frames throughout movie and plots thresholded plots.
    Inputs:
    exptdir = expts/exptxx directory
    secint = interval between each analyzed frame, in seconds
    '''
    exptfiles = exptfiles(os.path.abspath(exptdir))
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle = exptfiles
    
    frames = cmn.listsortfs(movdir)
    fps = getfps
    slices = len(frames)/(fps*secint)
    multimint(exptfiles=exptfiles, 
    images=frames[::slices], plotfiles='yes', savemc='no')

testmovie('.', SECINTTEST)

