
from plotfornrsa import *



KIND = 'wing'
KINDLIST = ['wing', 'copatt1', 'copsuc']
LEGLABELS = ['we', 'attcop', 'cop']
SUBPLOTNS = [221, 222, 223, 224]
SUBPLOTLS = ['A', 'B', 'C', 'D']
FNAME = '2013-0718_courtship_data _for_nrsa.csv'
BARNUM=6
BARWIDTH=1
XLIM=BARNUM*BARWIDTH+2*BARWIDTH
YMIN=-10
FIGW=7
FIGH=5
FIGDPI=1000
FONTSZ=9

LW = 1
YLABEL='Latency (s)'


#Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')

ks = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS)

for k in ks:
    multiplot_1bar(k[0], FNAME, BARNUM, BARWIDTH, XLIM, YMIN, YLABEL, subplotn=k[1], subplotl = k[2], fontsz=FONTSZ)

multiplot_3bars(KINDLIST, FNAME, 'keylist', 0.05, ylabel='%', subplotn=SUBPLOTNS[-1], subplotl=SUBPLOTLS[-1], ymin=-1, barwidth=BARWIDTH, barnum=6, fontsz=FONTSZ, stitlesz=10, leglabels=LEGLABELS, lw=1)
    
plt.tight_layout()
fig1.subplots_adjust(top=0.92)
plt.savefig('test.png')
