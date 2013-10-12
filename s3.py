from libs.bglib import *
from wingsettings import *

exptdir = os.path.abspath('.')
os.chdir(MOVBASE)
genbgimexpt(exptdir, MOVBASE, PICKLEBASE, BGFILE, 20, 'median', 'jpeg')

