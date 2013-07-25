import glob
import os
import shutil
from mn.cmn.cmn import *

# Writes down last 900 frames rather than first 900.
names = glob.glob('*.jpg')
x = len(names)
writejpglist(x-900, x)

