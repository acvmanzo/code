#! /usr/bin/env python

# Executable function for plotting a six-panel figure with courtship data.

import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import libs.agcourtlib as acl
from cfigLF6set import *


# Creates directory and output text files.
cmn.makenewdir(DIR)
acl.createshapfile(SHAPFILE)
acl.createinfolat(LATFILEMED)
acl.createinfolatmean(LATFILEMEAN)
acl.createinfoprop(PROPFILE)
acl.createinfopropmean(PROPMEANFILE)
acl.createstatfile(LATMWFILE, 'Mann-Whitney Test')
acl.createstatfile(FISHTFILE, 'Fisher\'s Exact Test')

# Creates a 6-panel latency (top) and frequency (bottom) figure.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates latency bar subplots.
ks1 = zip(KINDLIST, SUBPLOTNS1, SUBPLOTLS1, YLIMS1, STARPOS1, YMINS1)
for k in ks1:
    acl.multiplot('clatmed', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=k[5], ylim=k[3], 
    ylabel=YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2],
    binconf=BINCONF, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])

# Creates frequency bar subplots.
ks2 = zip(KINDLIST, SUBPLOTNS2, SUBPLOTLS2, YLIMS2, STARPOS2)
for k in ks2:
    acl.multiplot('cprop', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2],
    binconf=BINCONF, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])

# Saves figure.
plt.tight_layout()
plt.savefig(OUTPUTFIG) #Saves figure.
plt.close()


# Creates a 3-panel latency figure, with means and bar plots instead of a box 
#and whisker plot.
fig2 = plt.figure(figsize=(FIGW3, FIGH3), dpi=FIGDPI, facecolor='w', \
edgecolor='k')
# Creates latency bar plots.
ks3 = zip(KINDLIST, SUBPLOTNS3, SUBPLOTLS3, YLIMS3, STARPOS3)
for k in ks1:
    acl.multiplot('clatmean', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    ylabel=YLABEL1, yaxisticks=YAXISTICKS3, subplotn=k[1], subplotl=k[2],
    binconf=BINCONF, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])
    
# Saves figure.
plt.tight_layout()
plt.savefig(OUTPUTFIG2) #Saves figure.
plt.close()


# Writes output text files.
for kind in KINDLIST:
    
    ld = acl.dictclat(kind, FNAME)
    mwd = acl.dictmw(ld, CTRLKEY)
    ldadjpd = acl.mcpval(mwd, 'fdr', 'True', KEYFILE)
    
    pd = acl.dictcprop(kind, FNAME)
    fd = acl.dictfishtest(pd, CTRLKEY)
    fdadjpd = acl.mcpval(fd, 'fdr')
    
    acl.writeshapfile(SHAPFILE, ld, kind)
    acl.writestatfile(LATMWFILE, ldadjpd, kind)
    acl.writestatfile(FISHTFILE, fdadjpd, kind)
    acl.writeinfolat(LATFILEMED, ld, kind, CTRLKEY, 'median', 'True', KEYFILE)
    acl.writeinfolat(LATFILEMEAN, ld, kind, CTRLKEY, 'mean', 'True', KEYFILE)
    acl.writeinfoprop(PROPFILE, pd, BINCONF, kind, 'True', KEYFILE)
    acl.writeinfopropmean(PROPMEANFILE, pd, kind, 'True', KEYFILE)
