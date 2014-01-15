# Settings for cfigLF6.py

import os
import sys

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
OUTPUTFIG2 = '{0}cfigLmean_{1}.png'.format(DIR, CDIR) # Name of figure with box 
#and whisker plots.

SHAPFILE = '{0}clatshap_{1}.txt'.format(DIR, CDIR) # Name of file with 
#results of Shapiro test for normality.
PROPFILE = '{0}cpropinfo_{1}.txt'.format(DIR, CDIR) # Name of file with 
#frequency info.
LATFILEMED = '{0}clatinfomed_{1}.txt'.format(DIR, CDIR) # Name of file with 
#latency info.
LATFILEMEAN = '{0}clatinfomean_{1}.txt'.format(DIR, CDIR) # Name of file with 
#latency info.
FISHTFILE = '{0}cfishtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Fisher's test.
LATMWFILE = '{0}clatmwtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Mann-Whitney test.
    

# Options for all plots.
BARWIDTH=1
YMIN=0

# Figure parameters for latency+frequency plot.
KINDLIST = ['we', 'copatt1', 'copsuc'] # Behaviors to be analyzed.
FIGW=12 # Figure width.
FIGH=7 # Figure height.
FIGDPI=1000 # Figure DPI.
FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Parameters for latency subplots.
SUBPLOTNS1 = [231, 232, 233] # Subplots of the figure for latency.
SUBPLOTLS1 = ['A', 'B', 'C'] # Labels for the subplots.
YLIMS1 = [100, 600, 600]
STARPOS1 = [0.75, 0.75, 0.75]

YLABEL1='Latency (s)'
YAXISTICKS1 = 5 # Number of y-axis ticks.

# Parameters for proportion subplots.
SUBPLOTNS2 = [234, 235, 236] # Subplots of the figure for frequency.
SUBPLOTLS2 = ['D', 'E', 'F'] # Labels for the subplots.
YLIMS2 = [110, 110, 110]
STARPOS2 = [0.75, 0.75, 0.75]
BINCONF = 0.95 # Confidence of binomial confidence intervals.

# Options for frequency plots:
YLABEL2 ='%'
YAXISTICKS2 = 5 # Number of y-axis ticks.

# Figure parameters for latency bar plot.
FIGW3=12 # Figure width.
FIGH3=4 # Figure height.
SUBPLOTNS3 = [131, 132, 133] # Subplots of the figure for latency.1
SUBPLOTLS3 = ['A', 'B', 'C'] # Labels for the subplots.
YLIMS3 = [150, 600, 600]
STARPOS3 = [0.75, 0.75, 0.75]
YAXISTICKS3 = 5

