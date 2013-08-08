
import courtshiplib as cl
import cmn.cmn as cmn
import matplotlib.pyplot as plt
import matplotlib as mpl

# Options for the whole figure.
FNAME = '2013-0718_courtship_data _for_nrsa.csv'
DIR = 'presfig/'
OUTPUTFIG = DIR+'courtres.png'
OFILELAT = DIR+'courtreslat.txt'
OFILEPROP = DIR+'courtresprop.txt'
OFILEPROPTEST= DIR+'proptest.txt'

KINDLIST = ['wing', 'copatt1', 'copsuc']
SUBPLOTNS = [221, 222, 223, 224]
SUBPLOTLS = ['A', 'B', 'C', 'D']
CTRLKEY = '+/+'

FIGW=7
FIGH=5
FIGDPI=1000
FONTSZ=9
LW = 1
STITLESZ=10

# Options for both types of plots:
BARNUM=6
BARWIDTH=1
XLIM=BARNUM*BARWIDTH+2*BARWIDTH
YMIN=-10

# Options for 1bar plot:
YLABEL1='Latency (s)'
YAXISTICKS1 = 5

# Options for 3bar plot:
COLORS=['#555659', '#d3d3d3', 'w']
YLABEL2 ='%'
YAXISTICKS2 = 7
YMIN2 = 0
YLIM2 = 130
LEGLABELS = ['we', 'attcop', 'cop']

# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfolat(OFILELAT)
cl.createinfoprop(OFILEPROP)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')

# Creates subplots where the bar graph has 1 bar for each genotype (i.e., latency bar plots).
ks = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS)
for k in ks:
    cl.multiplot_1bar(k[0], FNAME, CTRLKEY, BARNUM, BARWIDTH, XLIM, YMIN, YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    # Writes two files with the summary information for frequency and latency plots.
    d =cl.dictfreq(k[0], FNAME)
    cl.writeinfolat(FNAME, OFILELAT, k[0], CTRLKEY)
    cl.writeinfoprop(FNAME, OFILEPROP, k[0])

# Creates subplots where the bar graph has 3 bars for each genotype (i.e., frequency bar plots).
cl.multiplot_3bars(KINDLIST, FNAME, 'keylist', conf=0.05, ylabel=YLABEL2, yaxisticks=YAXISTICKS2, ymin=YMIN2, ylim=YLIM2, colors=COLORS, subplotn=SUBPLOTNS[-1], subplotl=SUBPLOTLS[-1], barwidth=BARWIDTH, barnum=BARNUM, fontsz=FONTSZ, stitlesz=STITLESZ, leglabels=LEGLABELS, lw=LW)
# Adjusts figure areas.
plt.tight_layout()
fig1.subplots_adjust(top=0.92)
plt.savefig(OUTPUTFIG) #Saves figure.



