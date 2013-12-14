
import os
import sys
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import libs.agcourtlib as acl
import libs.rstatslib as rl
from afigDset import *


print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

# Creates output text files.
cmn.makenewdir(DIR)
acl.createshapfile(SHAPFILE)
acl.createstatfile(MWFILE, 'Mann Whitney U Test')
acl.createstatfile(TFILE, 'T Test')
acl.createinfodur(DURFILE, 'median')
acl.createinfodur(DURFILE2, 'mean')


# Creates figures.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates box and whisker duration plots.
ks1 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS, YLIMS, STARPOS)
for k in ks1:
    try:
        acl.multiplot('agdurmed', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
        ylim = k[3], ylabel=YLABEL, yaxisticks=YAXISTICKS, subplotn=k[1], \
        subplotl=k[2], binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, \
        stitlesz=STITLESZ, lw=LW, starpos=k[4])
    except cmn.EmptyValueError:
        continue
plt.tight_layout()
plt.savefig(OUTPUTFIG) #Saves figure.
plt.close()


# Creates bar duration plots.
fig2 = plt.figure(figsize=(FIGW2, FIGH2), dpi=FIGDPI2, facecolor='w', \
edgecolor='k')
ks2 = zip(KINDLIST2, SUBPLOTNS2, SUBPLOTLS2, YLIMS2, STARPOS2)
for k in ks2:
    try:
        acl.multiplot('agdurmean', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN2, k[3], \
        YLABEL, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2], \
        binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW,\
        starpos=k[4])
    except cmn.EmptyValueError:
        continue
# Adjusts figure areas.
plt.tight_layout()
plt.savefig(OUTPUTFIG2) #Saves figure.
plt.close()
    

# Writes output text files.
for kind in KINDLIST:
    d = acl.dictagdur2(kind, FNAME)
    mwd = acl.dictmw(d, CTRLKEY)
    pmwd = acl.mcpval(mwd, 'fdr', 'True', KEYFILE)
    
    md = acl.dictttest(d, CTRLKEY)
    pmd = acl.mcpval(md, 'fdr', 'True', KEYFILE)
    
    acl.writeshapfile(SHAPFILE, d, kind)
    acl.writestatfile(MWFILE, pmwd, kind)
    acl.writestatfile(TFILE, pmd, kind)
    acl.writeinfodur(DURFILE, d, kind, 'median')
    acl.writeinfodur(DURFILE2, d, kind, 'mean')
