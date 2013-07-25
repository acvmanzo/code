#! /usr/bin/env python

import glob
import os
from mn.cmn.cmn import *

# Writes a list of jpeg files. Used to generate the file 'list.txt' which is a list of jpegs that mplayer will play (here, first 900 jpeg files).
# Start from the '_wbr' folder.


folders = glob.glob('*')
for folder in folders:
    os.chdir(folder)
    writejpglist(0, 900)
    os.chdir('../')
