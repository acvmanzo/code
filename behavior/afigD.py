
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

cmn.makenewdir(DIR)
cl.createshapfile(SHAPFILE)
cl.createmwfile(MWFILE)

for kind in KINDLIST:
    d = al.dictagdur2(kind, FNAME)
    mwd = cl.dictmw(d, CTRLKEY)
    adjpd = cl.mcpval(mwd, 'fdr', 'True', KEYFILE)
    print(d)
    cl.writeshapfile(SHAPFILE, d, kind)
    cl.writemwfile(MWFILE, adjpd, kind)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates duration plots. 
ks1 = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS)
for k in ks1:
    try:
        al.multiplot_1barmw('dur', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
        YLABEL, yaxisticks=YAXISTICKS, subplotn=k[1], subplotl=k[2], \
        keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    except cmn.EmptyValueError:
        continue
        
# Adjusts figure areas.
plt.tight_layout()
plt.savefig(OUTPUTFIG) #Saves figure.

for kind in KINDLIST:
    print(kind)
    d = al.dictagdur2(kind, FNAME)
    md = cl.dictmeans(d)
    print(md)


#d = dictagdur2(kind, FNAME)


#md = cl.dictttest(d, ctrlkey='cs-Apr')
##md = cl.dictmw(d, ctrlkey='cs-Apr')
#mtd = cl.mcpval(md)
#cl.createmwfile(kind+'_num_ttest_results.txt')
#cl.writemwfile(kind+'_num_ttest_results.txt', mtd, kind)
##cl.createmwfile(kind+'_num_mw_results.txt')
##cl.writemwfile(kind+'_num_mw_results.txt', mtd, kind)

#cl.createshapfile('shapfile_num.txt')
#cl.writeshapfile('shapfile_num.txt', d, kind)

#fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
#plotagnum(kind, d)
#plt.savefig('{0}_num.png'.format(kind))

    
#for kind in KINDLIST:
    #print(kind)
    #d = dictagdur(kind, FNAME)
    #print(d)
    #md = cl.dictmw(d, ctrlkey='cs-Apr')
    #mtd = cl.mcpval(md)
    #print('mtd', mtd)
    #cl.createmwfile(kind+'_dur_mw_results.txt')
    #cl.writemwfile(kind+'_dur_mw_results.txt', mtd, kind)
    #fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    #plotagdur(kind, d)
    #plt.savefig('{0}_dur.png'.format(kind))
