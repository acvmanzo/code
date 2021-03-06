
import os
import sys
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import libs.agcourtlib as acl
import libs.courtshiplib as cl
import libs.rstatslib as rl
from afigNset import *


print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

cmn.makenewdir(DIR)
#acl.createstatfile(NUMTFILE, 'T-test')
acl.createstatfile(NUMMWFILE, 'Mann-Whitney Test')
acl.createshapfile(SHAPNUMFILE)
acl.createinfonum(NUMFILE, 'median')


fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')
ks2 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS, YLIMS, STARPOS)
for k in ks2:
    print('behavior', k)
    acl.multiplot('agnummed', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2],
    binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    lw=LW, starpos=k[4])

# Adjusts figure areas.
plt.tight_layout()
# Saves figure
plt.savefig(OUTPUTFIG1)

#fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')
#for k in ks2:
    #print('behavior', k)
    #acl.multiplot('agnummean', k[0], FNAME, CTRLKEY, BARWIDTH, ymin=YMIN, ylim=k[3], 
    #ylabel=YLABEL2, yaxisticks=YAXISTICKS2, subplotn=k[1], subplotl=k[2],
    #binconf=0.95, keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ,
    #lw=LW, starpos=k[4])

## Adjusts figure areas.
#plt.tight_layout()
## Saves figure
#plt.savefig(OUTPUTFIG2)


for kind in KINDLIST:
    print 'kind', kind
    d = acl.dictagnum(kind, FNAME)
    print 'keys', d.keys()
    md = acl.dictttest(d, ctrlkey=CTRLKEY)
    mwd = acl.dictmw(d, ctrlkey=CTRLKEY)
    mtd = acl.mcpval(md)
    print mtd
    mcmwd = acl.mcpval(mwd)
    #acl.writestatfile(NUMTFILE, mtd, kind)
    acl.writeshapfile(SHAPNUMFILE, d, kind)
    acl.writestatfile(NUMMWFILE, mcmwd, kind)
    acl.writeinfonum(NUMFILE, d, kind, 'median')

    
#for kind in KINDLIST:
    #print(kind)
    #d = acl.dictagdur(kind, FNAME)
    #print(d)
    #md = cl.dictmw(d, ctrlkey='CS')
    #mtd = cl.mcpval(md)
    #print('mtd', mtd)
    #cl.createmwfile(kind+'_dur_mw_results.txt')
    #cl.writemwfile(kind+'_dur_mw_results.txt', mtd, kind)
    #fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    #plotagdur(kind, d)
    #plt.savefig('{0}_dur.png'.format(kind))
