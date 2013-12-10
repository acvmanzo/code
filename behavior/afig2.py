#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the aggression data.

import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import libs.aglib as al
import libs.courtshiplib as cl
import cmn.cmn as cmn
from afigset2 import *

print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfoprop(OFILEPROP)
cl.createpptestfile(FISHTFILE)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

  
# Creates frequency bar plots.
ks2 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS)
for k in ks2:
    print('behavior', k)
    al.multiplot_1barf(k[0], FNAME, CTRLKEY, BARWIDTH, KEYFILE, conf=0.95, 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, ymin=YMIN2, ylim=YLIM2,
    subplotn=k[1], subplotl=k[2], fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    
    al.writeinfoagprop(FNAME, OFILEPROP, k[0], KEYFILE, 'True')

# Adjusts figure areas.
plt.tight_layout()

# Saves figure
plt.savefig(OUTPUTFIG)


# Writes the results of the statistical tests.
for k in KINDLIST:
    pd = al.dictagfreq2(k, FNAME)
    fd = cl.dictfishtest(pd, ctrlkey=CTRLKEY)
    adjfd = cl.mcpval(fd, 'fdr')
    cl.writepptestfile(FISHTFILE, adjfd, k)
