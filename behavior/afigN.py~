
import os
import sys
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmn.cmn as cmn
import libs.aglib as al
import libs.courtshiplib as cl
import libs.rstatslib as rl
from afigFset import *


print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.



d = dictagnum(kind, FNAME)
md = cl.dictttest(d, ctrlkey='cs-Apr')
#md = cl.dictmw(d, ctrlkey='cs-Apr')
mtd = cl.mcpval(md)
cl.createmwfile(kind+'_num_ttest_results.txt')
cl.writemwfile(kind+'_num_ttest_results.txt', mtd, kind)
#cl.createmwfile(kind+'_num_mw_results.txt')
#cl.writemwfile(kind+'_num_mw_results.txt', mtd, kind)

cl.createshapfile('shapfile_num.txt')
cl.writeshapfile('shapfile_num.txt', d, kind)

fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
plotagnum(kind, d)
plt.savefig('{0}_num.png'.format(kind))

    
for kind in KINDLIST:
    print(kind)
    d = dictagdur(kind, FNAME)
    print(d)
    md = cl.dictmw(d, ctrlkey='cs-Apr')
    mtd = cl.mcpval(md)
    print('mtd', mtd)
    cl.createmwfile(kind+'_dur_mw_results.txt')
    cl.writemwfile(kind+'_dur_mw_results.txt', mtd, kind)
    fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    plotagdur(kind, d)
    plt.savefig('{0}_dur.png'.format(kind))
