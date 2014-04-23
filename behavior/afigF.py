#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the aggression data.

import os
import sys
import shutil
import matplotlib.pyplot as plt
import libs.agcourtlib as acl
import cmn.cmn as cmn
from afigFset import *

print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

# Creates directory and output text files.
cmn.makenewdir(DIR)
acl.createinfoprop(PROPFILE)
acl.createstatfile(FISHTFILE, 'Fisher\'s test')

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates frequency bar plots.
ks2 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS, YLIMS, STARPOS)
for k in ks2:
    print('behavior', k)
    acl.multiplot('agprop', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2],
    binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])

# Adjusts figure areas.
plt.tight_layout()
# Saves figure
plt.savefig(OUTPUTFIG)


# Writes the results of the statistical tests and graph info.
for k in KINDLIST:
    pd = acl.dictagfreq2(k, FNAME)
    fd = acl.dictfishtest(pd, ctrlkey=CTRLKEY)
    adjfd = acl.mcpval(fd, 'fdr')
    acl.writestatfile(FISHTFILE, adjfd, k)
    acl.writeinfoprop(PROPFILE, pd, 0.95, k, 'True', KEYFILE)

# Copies the figure settings into the results directory.
shutil.copy('/home/andrea/Documents/lab/code/behavior/afigFset.py', FIGSETFILE)
