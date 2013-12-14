#! /usr/bin/env python

# Settings for cfigLF6.py

import courtshiplib as cl
import cmn.cmn as cmn
import matplotlib.pyplot as plt
import matplotlib as mpl


print('data filename, ctrlkey')
FNAME = sys.argv[1] # File with data to be analyzed.
CTRLKEY = sys.argv[2] # Name of the control strain that all other lines will be 
#compared to.


# Input and output files.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
CDIR = os.path.basename(os.path.abspath('.'))
OUTPUTFIG = '{0}cfigLF_{1}.png'.format(DIR, CDIR) # Name of figure with box 
#and whisker plots.

PROPFILE = '{0}cpropinfo_{1}.txt'.format(DIR, CDIR) # Name of file with 
#frequency info.
LATFILE = '{0}clatinfo_{1}.txt'.format(DIR, CDIR) # Name of file with 
#latency info.
FISHTFILE = '{0}cfishtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Fisher's test.
LATMWFILE = '{0}clatmwtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Mann-Whitney test.
    

# Info about figure content.
KINDLIST = ['wing', 'copatt1', 'copsuc'] # Behaviors to be analyzed.

# Figure parameters.
SUBPLOTNS1 = [231, 232, 233] # Subplots of the figure for latency.
SUBPLOTNS2 = [234, 235, 236] # Subplots of the figure for frequency.
SUBPLOTLS1 = ['A', 'B', 'C'] # Labels for the subplots.
SUBPLOTLS2 = ['D', 'E', 'F'] # Labels for the subplots.

FIGW=9 # Figure width.
FIGH=6 # Figure height.
FIGDPI=1000 # Figure DPI.

FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Options for bar plots.
BARWIDTH=1
YMIN=0

# Options for latency plots:
YLABEL1='Latency (s)'
YAXISTICKS1 = 5 # Number of y-axis ticks.
YLIM1 = 300

# Options for frequency plots:
YLABEL2 ='%'
YAXISTICKS2 = 5 # Number of y-axis ticks.
YLIM2 = 110

