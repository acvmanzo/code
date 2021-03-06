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
