#! /usr/bin/env python

# This executable file determines the locations of an ROI surrounding each 
# well using the default ROI parameters. This should be run 

import os
import matplotlib.pyplot as plt
import numpy as np
import cmn.cmn as cmn
import libs.partimlib as pl
import libs.mtslib as ml
import libs.bglib as bl
#import libs.winglib as wl
from libs.winglib import *
import numpy as np
from wingsettings import *
from PIL import Image


IMNUMS = [str(x) for x in np.arange(10, 12, 1)]
IMAGES = ['mov000'+n+'.bmp' for n in IMNUMS]

exptdir = os.path.abspath('.')
os.chdir(movies)
[movsmc, movmmc, movroi] = multimint('../', IMAGES, 'yes')
os.chdir(exptdir)
plotintd([movsmc, movmmc, movroi])
    
            





        
