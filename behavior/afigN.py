#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the aggression 
# data showing number of different aggressive behaviors.

import os
import sys
import shutil
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import libs.agcourtlib as acl
import libs.courtshiplib as cl
import libs.rstatslib as rl
sys.path.append(os.path.abspath('.'))
from afigNset import *

print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.


cmn.makenewdir(DIR)
acl.createstatfile(NUMMWFILE_ALL, 'Mann-Whitney Test')
acl.createstatfile(NUMMWFILE_EX, 'Mann-Whitney Test')
acl.createshapfile(SHAPNUMFILE_ALL)
acl.createshapfile(SHAPNUMFILE_EX)
acl.createinfonum(NUMFILE_ALL, 'median')
acl.createinfonum(NUMFILE_EX, 'median')

print('Plotting figure - all flies')
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')
ks2 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS, YLIMSALL, STARPOS)
for k in ks2:
    print('BEHAVIOR', k)
    acl.multiplot('agnummedall', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2],
    binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])

# Adjusts figure areas.
plt.tight_layout()
# Saves figure
plt.savefig(OUTPUTFIG_ALL)

print('Plotting figure - with excluding flies')
fig2 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')
ks2 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS, YLIMSEX, STARPOS)
for k in ks2:
    print('BEHAVIOR', k)
    acl.multiplot('agnummedex', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2],
    binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])

# Adjusts figure areas.
plt.tight_layout()
# Saves figure
plt.savefig(OUTPUTFIG_EX)

print 'Writing output files - all flies'
for kind in KINDLIST:
    d = acl.dictagnum(kind, FNAME, 'all')
    mwd = acl.dictmw(d, ctrlkey=CTRLKEY)
    mcmwd = acl.mcpval(mwd)
    acl.writeshapfile(SHAPNUMFILE_ALL, d, kind)
    acl.writestatfile(NUMMWFILE_ALL, mcmwd, kind)
    acl.writeinfonum(NUMFILE_ALL, d, kind, CTRLKEY, 'median')

print 'Writing output files - with excluding flies'
for kind in KINDLIST:
    d = acl.dictagnum(kind, FNAME, 'ex')
    mwd = acl.dictmw(d, ctrlkey=CTRLKEY)
    mcmwd = acl.mcpval(mwd)
    acl.writeshapfile(SHAPNUMFILE_EX, d, kind)
    acl.writestatfile(NUMMWFILE_EX, mcmwd, kind)
    acl.writeinfonum(NUMFILE_EX, d, kind, CTRLKEY, 'median')


    
