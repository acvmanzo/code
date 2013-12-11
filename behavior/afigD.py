
import os
import sys
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import libs.aglib as al
import libs.courtshiplib as cl
import libs.rstatslib as rl
from afigDset import *


print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

# Creates output text files.
cmn.makenewdir(DIR)
cl.createshapfile(SHAPFILE)
cl.createstatfile(MWFILE, 'Mann Whitney U Test')
cl.createstatfile(TFILE, 'T Test')
cl.createinfodur(DURFILE, 'median')
cl.createinfodur(DURFILE2, 'mean')


# Loads data and writes output text files.
for kind in KINDLIST:
    d = al.dictagdur2(kind, FNAME)
    mwd = cl.dictmw(d, CTRLKEY)
    pmwd = cl.mcpval(mwd, 'fdr', 'True', KEYFILE)
    
    md = cl.dictttest(d, CTRLKEY)
    pmd = cl.mcpval(md, 'fdr', 'True', KEYFILE)
    
    cl.writeshapfile(SHAPFILE, d, kind)
    cl.writestatfile(MWFILE, pmwd, kind)
    cl.writestatfile(TFILE, pmd, kind)
    cl.writeinfodur(DURFILE, d, kind, CTRLKEY, 'median')
    cl.writeinfodur(DURFILE2, d, kind, CTRLKEY, 'mean')

# Creates figures.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates box and whisker duration plots.
ks1 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS)
for k in ks1:
    try:
        al.multiplot_1barmw('dur', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
        YLABEL, yaxisticks=YAXISTICKS, subplotn=k[1], subplotl=k[2], \
        keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    except cmn.EmptyValueError:
        continue
plt.tight_layout()
plt.savefig(OUTPUTFIG) #Saves figure.
plt.close()


# Creates bar duration plots.
fig2 = plt.figure(figsize=(FIGW2, FIGH2), dpi=FIGDPI2, facecolor='w', \
edgecolor='k')
ks2 = zip(KINDLIST2, SUBPLOTNS2, SUBPLOTLS2)
for k in ks2:
    try:
        al.multiplot_1barmean('dur', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN2, \
        YLABEL, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2], \
        keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    except cmn.EmptyValueError:
        continue
# Adjusts figure areas.
plt.tight_layout()
plt.savefig(OUTPUTFIG2) #Saves figure.
plt.close()
    
