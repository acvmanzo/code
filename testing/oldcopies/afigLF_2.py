#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the aggression data.

import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import libs.aglib as al
import libs.courtshiplib as cl
import cmn.cmn as cmn
from afigLFset import *

print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.

# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfolat(OFILELAT)
cl.createinfoprop(OFILEPROP)
cl.createstatfile(OFILEMULTIPROPTEST, 'Multi Prop Test')
#cl.createproptestfile(PTFILE)
cl.createstatfile(FISHTFILE, 'Fisher\'s Exact Test')

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates latency bar plots. 
ks1 = zip(KINDLIST, SUBPLOTNS1, SUBPLOTLS1)
for k in ks1:
    print(k[0])
    if k[0] == 'flare' or k[0] == 'escm':
        continue
    try:
        al.multiplot_1barmw('lat', k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
        YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], \
        keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    except cmn.EmptyValueError:
        continue
    
# Creates frequency bar plots.
ks2 = zip(KINDLIST, SUBPLOTNS2, SUBPLOTLS2)
for k in ks2:
    print('behavior', k)
    al.multiplot_1barf(k[0], FNAME, CTRLKEY, BARWIDTH, KEYFILE, conf=0.95, 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, ymin=YMIN2, ylim=YLIM2,
    subplotn=k[1], subplotl=k[2], fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    
    al.writeinfoaglatmean(FNAME, OFILELAT, k[0], CTRLKEY, KEYFILE, 'True')
    al.writeinfoagprop(FNAME, OFILEPROP, k[0], KEYFILE, 'True')

# Adjusts figure areas.
plt.tight_layout()
fig1.subplots_adjust(top=0.92)
plt.savefig(OUTPUTFIG) #Saves figure.

# Writes the results of the statistical tests.
for k in KINDLIST:
    pd = al.dictfreq(k, FNAME)
    ppd = cl.dictpptest(pd, ctrlkey=CTRLKEY)
    adjppd1 = cl.mcpval(ppd, 'fdr')
    fd = cl.dictfishtest(pd, ctrlkey=CTRLKEY)
    adjppd = cl.mcpval(fd, 'fdr')
    cl.writepptestfile(OFILEMULTIPROPTEST, adjppd1, k)
    #al.writeproptestfile(PTFILE, pd, k, KEYFILE, 'True')
    cl.writepptestfile(FISHTFILE, adjppd, k)
# Settings for afig.py.

# Input and output files.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
OUTPUTFIG = DIR+'agfig.png' # Name of figure.
OFILELAT = DIR+'aglat.txt' # Name of file with latency info.
OFILEPROP = DIR+'agprop.txt' # Name of file with frequency info.
OFILEMULTIPROPTEST= DIR+'multiproptest.txt' # Name of file with results of the R 
#function 'prop.test'
PTFILE = DIR+'aproptest.txt'
FISHTFILE = DIR+'agfishtest.txt'

# Info about figure content.
KINDLIST = ['flare', 'charge', 'escd', 'escm'] # Behaviors to be analyzed.

# Figure parameters.
SUBPLOTNS1 = [241, 242, 243, 244] # Subplots of the figure for latency.
SUBPLOTNS2 = [245, 246, 247, 248] # Subplots of the figure for frequency.
SUBPLOTLS1 = ['A', 'B', 'C', 'D'] # Labels for the subplots.
SUBPLOTLS2 = ['E', 'F', 'G', 'H'] # Labels for the subplots.

FIGDPI=1200 # Figure DPI.
FIGW=13 # Figure width.
FIGH=7 # Figure height.

FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Options for bar plots.
BARWIDTH=1
YMIN=-10

# Options for latency plots:
YLABEL1='Latency (s)'
YAXISTICKS1 = 5 # Number of y-axis ticks.

# Options for frequency plots:
YLABEL2 ='%'
YAXISTICKS2 = 7 # Number of y-axis ticks.
YMIN2 = 0
YLIM2 = 130
# Settings for afig.py.

# Input and output files.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
OUTPUTFIG = DIR+'agfig.png' # Name of figure.
OFILELAT = DIR+'aglat.txt' # Name of file with latency info.
OFILEPROP = DIR+'agprop.txt' # Name of file with frequency info.
OFILEMULTIPROPTEST= DIR+'multiproptest.txt' # Name of file with results of the R 
#function 'prop.test'
PTFILE = DIR+'aproptest.txt'
FISHTFILE = DIR+'agfishtest.txt'

# Info about figure content.
KINDLIST = ['flare', 'charge', 'escd', 'escm'] # Behaviors to be analyzed.

# Figure parameters.
SUBPLOTNS1 = [241, 242, 243, 244] # Subplots of the figure for latency.
SUBPLOTNS2 = [245, 246, 247, 248] # Subplots of the figure for frequency.
SUBPLOTLS1 = ['A', 'B', 'C', 'D'] # Labels for the subplots.
SUBPLOTLS2 = ['E', 'F', 'G', 'H'] # Labels for the subplots.

FIGDPI=1200 # Figure DPI.
FIGW=13 # Figure width.
FIGH=7 # Figure height.

FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Options for bar plots.
BARWIDTH=1
YMIN=-10

# Options for latency plots:
YLABEL1='Latency (s)'
YAXISTICKS1 = 5 # Number of y-axis ticks.

# Options for frequency plots:
YLABEL2 ='%'
YAXISTICKS2 = 7 # Number of y-axis ticks.
YMIN2 = 0
YLIM2 = 130
from libs.aglib import *

KINDLIST = ['wingthreat', 'charge', 'anyag', 'escd', 'escm']
#KIND = 'wingthreat'
FNAME = '20131119_agdata_wms_sorted.csv'
FREQDIR = 'freqfig'

cmn.makenewdir(FREQDIR)
for KIND in KINDLIST:
    print(KIND)
    d = dictagfreq2(KIND, FNAME)
    
    for k, v in d.iteritems():
        print(k, sum(v)/100, len(v))
    
    plotagfreq(KIND, d, 'true')
    plt.savefig('{0}/freq{1}.png'.format(FREQDIR, KIND))

from aglib import *
import courtshiplib as cl

KINDLIST = ['charge', 'escd']
#KINDLIST = ['flare', 'charge', 'escd', 'escm']
#KINDLIST = ['flare']
FNAME = 'allag.csv'
PROPFILE = 'freq_of_behavior.txt'
LATFILE = 'latency_to_behavior.txt'
PROPTESTFILE = 'proptest.txt'
SHAPFILE = 'shap_lat.txt'
KEYFILE = 'keylist'

cl.createinfolat(LATFILE)
cl.createinfoprop(PROPFILE)
cl.createshapfile(SHAPFILE)
    
for KIND in KINDLIST:
    print(KIND)
    #latd = dictaglat(KIND, FNAME)
    #print(KIND, 'lat', latd)
    #plotaglatbw(KIND, latd, iskeyfile='No')
    ##writeinfolat(FNAME, LATFILE, KIND, 'cs', KEYFILE, iskeyfile='False')
    #plt.savefig('lat' + KIND + '.png')
    d = dictaglat(KIND, FNAME)
    freqd = dictfreq(KIND, FNAME)
    #print(KIND, 'freq', freqd)
    #plotagfreq(KIND, freqd)
    #plt.savefig('freq' + KIND + '.png')

    writeinfoprop(FNAME, PROPFILE, KIND, KEYFILE, iskeyfile='False')
    writeproptestfile(PROPTESTFILE, freqd, KIND, KEYFILE, iskeyfile='false')
    cl.writeshapfile(SHAPFILE, d, KIND)



#! /usr/bin/env python

# Executable function for analyzing courtship data.

from courtshiplib import *

KINDLIST = ['wing', 'copsuc', 'copatt1'] # List of behaviors; wing = wing 
 #extension; copsuc = successful copulation; copatt1 = first attempted 
 #copulation.
FNAME = '2013-0718_courtship_data_for_nrsa.csv' # Name of file with the data 
#from manual scoring.
SHAPFILE = 'shap_lat.txt' # Name of file listing results of the Shapiro-Wilk 
#test.
MCPVALFILE = 'mcpvalue_lat_exact.txt' # Name of file listing results of the 
#Mann-Whitney U Test, with p-values adjusted for multiple comparisons.
MWTEST = 'exact' # Specifies whether to use the R function wilcox.exact 
#('exact') or wilcox.test ('std')
MCCORR = 'fdr' # Specifies how to adjust p-values to correct for multiple 
#comparisons using the R function p.adjust ('fdr' = false discovery rate')
PTFILE = 'proptest.txt' # Name of file listing the results of the proportion 
#test, where p-values give the probability of observing the results if the null
 #hypothesis that all the proportions are from the same distribution is true.
CTRLKEY = '+/+' # Name of the control strain that all other lines will be 
#compared to in the Mann-Whitney U Test.
DIR = 'summary/' # Name of the directory where plots and text files will be 
#saved.
QQDIR = DIR+'qqplots/' # Name of the directory where qqplots will be saved.

# Creates the directories where the plots will go.
cmn.makenewdir(DIR)
cmn.makenewdir(QQDIR)

# For each type of behavior, plots a latency graph, frequency graph, and qqplots for each genotype.
for KIND in KINDLIST:
    plotlatbw(KIND, FNAME, iskeyfile='No')
    plt.savefig(DIR+KIND+'lat')
    plotfreq(KIND, FNAME, iskeyfile='No')
    plt.savefig(DIR+KIND+'freq')
    plotqqplots(KIND, FNAME, QQDIR, CTRLKEY)

# Creates and writes files with the results of the Shapiro-Wilk test for normality, the Mann Whitney U Test (comparing each genotype to the control genotype, specified above) and the proportion test (for a group of proportions [#successes/total], determines if any of the proportions differ from each other).
createshapfile(DIR+SHAPFILE)
createmwfile(DIR+MCPVALFILE)
createproptestfile(DIR+PTFILE)

for k in KINDLIST:
    d = dictlat(k, FNAME)
    mwd = dictmw(d, ctrlkey=CTRLKEY, test=MWTEST)
    adjpd = mcpval(mwd, MCCORR)

    writeshapfile(DIR+SHAPFILE, d, k)
    writemwfile(DIR+MCPVALFILE, adjpd, k)

    pd = dictfreq(k, FNAME)
    writeproptestfile(DIR+PTFILE, pd, k)
#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the courtship data.

import courtshiplib as cl
import cmn.cmn as cmn
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

print('data filename, ctrlkey')
FNAME = sys.argv[1]
CTRLKEY = sys.argv[2]

# Input and output files.
#FNAME = '2013-0718_courtship_data_for_nrsa.csv' #File containing original data.
#FNAME = 'allcourtship.csv' #File containing original data.
#FNAME = 'alljcourtship.csv' #File containing original data.
#FNAME = 'allwillcourtship.csv' #File containing original data.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
OUTPUTFIG = DIR+'courtresexp.png' # Name of figure.
OFILELAT = DIR+'courtreslat.txt' # Name of file with latency info.
OFILEPROP = DIR+'courtresprop.txt' # Name of file with frequency info.
OFILEMULTIPROPTEST= DIR+'multiproptest.txt' # Name of file with results of the R 
#function 'prop.test'
FISHTFILE = DIR+'agfishtest.txt'

# Info about figure content.
KINDLIST = ['wing', 'copatt1', 'copsuc'] # Behaviors to be analyzed.
#CTRLKEY = '+/+' # Name of the control strain that all other lines will be 
#CTRLKEY = 'cs-Apr' # Name of the control strain that all other lines will be 
#CTRLKEY = 'cs-Jenee' # Name of the control strain that all other lines will be 
#CTRLKEY = 'cs-Jenee' # Name of the control strain that all other lines will be 
#compared to in the Mann-Whitney U Test.

# Figure parameters.
SUBPLOTNS1 = [231, 232, 233] # Subplots of the figure.
SUBPLOTNS2 = [234, 235, 236] # Subplots of the figure.
SUBPLOTLS1 = ['A', 'B', 'C'] # Labels for the subplots.
SUBPLOTLS2 = ['D', 'E', 'F'] # Labels for the subplots.
FIGW=8 # Figure width.
FIGH=6 # Figure height.
FIGDPI=1000 # Figure DPI.
FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Options for both types of plots:
#BARNUM=6 # Number of conditions to be plotted.
BARWIDTH=1
YMIN=-10

# Options for 1bar plot:
YLABEL1='Latency (s)'
YAXISTICKS1 = 5 # Number of y-axis ticks.

# Options for 1barf plot:
YLABEL2 ='%'
YAXISTICKS2 = 7 # Number of y-axis ticks.
YMIN2 = 0
YLIM2 = 130
LEGLABELS = ['we', 'attcop', 'cop']

# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfolat(OFILELAT)
cl.createinfoprop(OFILEPROP)
cl.createpptestfile(OFILEMULTIPROPTEST)
cl.createpptestfile(FISHTFILE)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates subplots where the bar graph has 1 bar for each genotype 
#(i.e., latency bar plots).
ks1 = zip(KINDLIST, SUBPLOTNS1, SUBPLOTLS1)
for k in ks1:
    cl.multiplot_1bar(k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
    YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], \
    keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    # Writes two files with the summary information for frequency and latency plots.
    #d =cl.dictfreq(k[0], FNAME)
    cl.writeinfolat(FNAME, OFILELAT, k[0], CTRLKEY, KEYFILE, 'True')
    
ks2 = zip(KINDLIST, SUBPLOTNS2, SUBPLOTLS2)
for k in ks2:
    print('behavior', k)
    cl.multiplot_1barf(k[0], FNAME, CTRLKEY, BARWIDTH, KEYFILE, conf=0.95, 
    ylabel=YLABEL2, yaxisticks=YAXISTICKS2, ymin=YMIN2, ylim=YLIM2, \
    subplotn=k[1], subplotl=k[2], 
    fontsz=FONTSZ, stitlesz=STITLESZ, leglabels=LEGLABELS, lw=LW)
    cl.writeinfoprop(FNAME, OFILEPROP, k[0], KEYFILE, 'True')

# Adjusts figure areas.
plt.tight_layout()
fig1.subplots_adjust(top=0.92)
plt.savefig(OUTPUTFIG) #Saves figure.

for k in KINDLIST:
    pd = cl.dictfreq(k, FNAME)
    ppd = cl.dictpptest(pd, ctrlkey=CTRLKEY)
    adjppd1 = cl.mcpval(ppd, 'fdr')
    fd = cl.dictfishtest(pd, ctrlkey=CTRLKEY)
    adjppd = cl.mcpval(fd, 'fdr')
    cl.writepptestfile(OFILEMULTIPROPTEST, adjppd1, k)
    #al.writeproptestfile(PTFILE, pd, k, KEYFILE, 'True')
    cl.writepptestfile(FISHTFILE, adjppd, k)
#! /usr/bin/env python

# Executable function for plotting a four-panel figure with the courtship data.

import courtshiplib as cl
import cmn.cmn as cmn
import matplotlib.pyplot as plt
import matplotlib as mpl

# Input and output files.
#FNAME = '2013-0718_courtship_data_for_nrsa.csv' #File containing original data.
FNAME = 'allcourtship.csv' #File containing original data.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
OUTPUTFIG = DIR+'courtres.png' # Name of figure.
OFILELAT = DIR+'courtreslat.txt' # Name of file with latency info.
OFILEPROP = DIR+'courtresprop.txt' # Name of file with frequency info.
OFILEPROPTEST= DIR+'proptest.txt' # Name of file with results of the R 
#function 'prop.test'

# Info about figure content.
KINDLIST = ['wing', 'copatt1', 'copsuc'] # Behaviors to be analyzed.
#CTRLKEY = '+/+' # Name of the control strain that all other lines will be 
CTRLKEY = 'cs-Apr' # Name of the control strain that all other lines will be 
#compared to in the Mann-Whitney U Test.

# Figure parameters.
SUBPLOTNS = [221, 222, 223, 224] # Subplots of the figure.
SUBPLOTLS = ['A', 'B', 'C', 'D'] # Labels for the subplots.
FIGW=8 # Figure width.
FIGH=6 # Figure height.
FIGDPI=1000 # Figure DPI.
FONTSZ=9 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=10 # Title font size.

# Options for both types of plots:
#BARNUM=6 # Number of conditions to be plotted.
BARWIDTH=1
YMIN=-10

# Options for 1bar plot:
YLABEL1='Latency (s)'
YAXISTICKS1 = 5 # Number of y-axis ticks.

# Options for 3bar plot:
COLORS=['#555659', '#d3d3d3', 'w']
YLABEL2 ='%'
YAXISTICKS2 = 7 # Number of y-axis ticks.
YMIN2 = 0
YLIM2 = 130
LEGLABELS = ['we', 'attcop', 'cop']



# Creates directory and output text files.
cmn.makenewdir(DIR)
cl.createinfolat(OFILELAT)
cl.createinfoprop(OFILEPROP)

# Creates a figure of the indicated size and dpi.
fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
edgecolor='k')

# Creates subplots where the bar graph has 1 bar for each genotype 
#(i.e., latency bar plots).
ks = zip(KINDLIST, SUBPLOTNS, SUBPLOTLS)
for k in ks:
    cl.multiplot_1bar(k[0], FNAME, CTRLKEY, BARWIDTH, YMIN, \
    YLABEL1, yaxisticks=YAXISTICKS1, subplotn=k[1], subplotl=k[2], \
    keyfile=KEYFILE, fontsz=FONTSZ, stitlesz=STITLESZ, lw=LW)
    # Writes two files with the summary information for frequency and latency plots.
    #d =cl.dictfreq(k[0], FNAME)
    #cl.writeinfolat(FNAME, OFILELAT, k[0], CTRLKEY)
    #cl.writeinfoprop(FNAME, OFILEPROP, k[0])

# Creates subplots where the bar graph has 3 bars for each genotype 
#(i.e., frequency bar plots).
cl.multiplot_3bars(KINDLIST, FNAME, CTRLKEY, KEYFILE, conf=0.05, ylabel=YLABEL2, \
yaxisticks=YAXISTICKS2, ymin=YMIN2, ylim=YLIM2, colors=COLORS, \
subplotn=SUBPLOTNS[-1], subplotl=SUBPLOTLS[-1], barwidth=BARWIDTH, \
fontsz=FONTSZ, stitlesz=STITLESZ, leglabels=LEGLABELS, lw=LW)
# Adjusts figure areas.
plt.tight_layout()
fig1.subplots_adjust(top=0.92)
plt.savefig(OUTPUTFIG) #Saves figure.



from courtshiplib import *

KINDLIST = ['wing', 'copsuc', 'copatt1']
FNAME = 'allcourtship.csv'
PROPFILE = 'freq_of_courtship.txt'
LATFILE = 'latency_to_courtship.txt'
KEYFILE = 'keylist'
CTRLKEY = 'cs-June'
SHAPFILE = 'shap_lat.txt' # Name of file listing results of the Shapiro-Wilk 
#test.
MCPVALFILE = 'mcpvalue_lat_exact.txt' # Name of file listing results of the 
#Mann-Whitney U Test, with p-values adjusted for multiple comparisons.
MWTEST = 'exact' # Specifies whether to use the R function wilcox.exact 
#('exact') or wilcox.test ('std')
MCCORR = 'fdr' # Specifies how to adjust p-values to correct for multiple 
#comparisons using the R function p.adjust ('fdr' = false discovery rate')
PTFILE = 'proptest.txt' # Name of file listing the results of the proportion 
#test, where p-values give the probability of observing the results if the null
 #hypothesis that all the proportions are from the same distribution is true.
PPTFILE = 'pairproptest.txt' # Name of file listing results of the pairwise
#proportion test.

createinfolatmean(LATFILE)
createinfoprop(PROPFILE)

createshapfile(SHAPFILE)
createmwfile(MCPVALFILE)
createproptestfile(PTFILE)
createpptestfile(PPTFILE)

for KIND in KINDLIST:
    print(KIND)
    plotlatbw(KIND, FNAME, 'true')
    plt.savefig(KIND+'lat')
    plotfreq(KIND, FNAME, 'true')
    plt.savefig(KIND+'freq')
    
    writeinfolatmean(FNAME, LATFILE, KIND, 'cs-Apr')
    writeinfoprop(FNAME, PROPFILE, KIND)

for k in KINDLIST:
    print(k)
    d = dictlat(k, FNAME)
    mwd = dictmw(d, ctrlkey=CTRLKEY, test=MWTEST)
    adjpd = mcpval(mwd, MCCORR)
       

    writeshapfile(SHAPFILE, d, k)
    writemwfile(MCPVALFILE, adjpd, k)

    pd = dictfreq(k, FNAME)
    print('ppd')
    ppd = dictpptest(pd, ctrlkey=CTRLKEY)
    print(ppd)
    print('adjppd')
    adjppd = mcpval(ppd, MCCORR)
    writepptestfile(PPTFILE, adjppd, k)



