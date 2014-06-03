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



