#! /usr/bin/env python

# Executable function for plotting a six-panel figure with courtship data.

import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import libs.aglib as al
import libs.courtshiplib as cl
import cmn.cmn as cmn
from cfigLF6set import *


# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfolat(LATFILE)
cl.createinfoprop(PROPFILE)
cl.createstatfile(LATMWFILE)
cl.createstatfile(FISHTFILE)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates latency bar plots.
ks1 = zip(KINDLIST, SUBPLOTNS1, SUBPLOTLS1)
for k in ks1:
    cl.multiplot_1bar(k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
    YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], \
    keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)

# Creates frequency bar plots.
ks2 = zip(KINDLIST, SUBPLOTNS2, SUBPLOTLS2)
for k in ks2:
    cl.multiplot_1bar(k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
    YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], \
    keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)


