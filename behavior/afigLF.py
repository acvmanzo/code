#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the aggression data.

import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import libs.aglib as al
import libs.courtshiplib as cl
import cmn.cmn as cmn
from afigLFset import *

print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfolat(OFILELAT)
cl.createinfoprop(OFILEPROP)
cl.createpptestfile(OFILEMULTIPROPTEST)
#cl.createproptestfile(PTFILE)
cl.createpptestfile(FISHTFILE)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates latency bar plots. 
ks1 = zip(KINDLIST, SUBPLOTNS1, SUBPLOTLS1)
for k in ks1:
    print(k[0])
    if k[0] == 'flare' or k[0] == 'escm':
        continue
    try:
        al.multiplot_1barmw('lat', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
        YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], \
        keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    except cmn.EmptyValueError:
        continue
    
# Creates frequency bar plots.
ks2 = zip(KINDLIST, SUBPLOTNS2, SUBPLOTLS2)
for k in ks2:
    print('behavior', k)
    al.multiplot_1barf(k[0], FNAME, CTRLKEY, BARWIDTH, KEYFILE, conf=0.95, 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, ymin=YMIN2, ylim=YLIM2,
    subplotn=k[1], subplotl=k[2], fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    
    al.writeinfoaglatmean(FNAME, OFILELAT, k[0], CTRLKEY, KEYFILE, 'True')
    al.writeinfoagprop(FNAME, OFILEPROP, k[0], KEYFILE, 'True')

# Adjusts figure areas.
plt.tight_layout()
fig1.subplots_adjust(top=0.92)
plt.savefig(OUTPUTFIG) #Saves figure.

# Writes the results of the statistical tests.
for k in KINDLIST:
    pd = al.dictfreq(k, FNAME)
    ppd = cl.dictpptest(pd, ctrlkey=CTRLKEY)
    adjppd1 = cl.mcpval(ppd, 'fdr')
    fd = cl.dictfishtest(pd, ctrlkey=CTRLKEY)
    adjppd = cl.mcpval(fd, 'fdr')
    cl.writepptestfile(OFILEMULTIPROPTEST, adjppd1, k)
    #al.writeproptestfile(PTFILE, pd, k, KEYFILE, 'True')
    cl.writepptestfile(FISHTFILE, adjppd, k)
