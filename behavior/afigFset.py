# Settings for afig.py.
import os

# Input and output files.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
CDIR = os.path.basename(os.path.abspath('.'))
OUTPUTFIG = '{0}agpropfig_{1}.png'.format(DIR, CDIR) # Name of figure.
PROPFILE = '{0}agpropinfo_{1}.txt'.format(DIR, CDIR) # Name of file with 
#frequency info.
#OFILEMULTIPROPTEST= DIR+'multiproptest.txt' # Name of file with results of the R 
#function 'prop.test'
FISHTFILE = '{0}agfishtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Fisher's test.
NUMTFILE = '{0}agnumttest_{1}.txt'.format(DIR, CDIR) # Name of file with results.
SHAPNUMFILE = '{0}agnumshap_{1}.txt'.format(DIR, CDIR)
FIGSETFILE = '{0}figset_{1}.txt'.format(DIR, CDIR)

# Info about figure content.
#KINDLIST = ['charge'] # Behaviors to be analyzed.
KINDLIST = ['charge', 'escd', 'escm'] # Behaviors to be analyzed.

# Figure parameters.
SUBPLOTNS = [131, 132, 133] # Subplots of the figure for frequency.
SUBPLOTLS = ['A', 'B', 'C'] # Labels for the subplots.
SUBPLOTLS = ['', '', ''] # Labels for the subplots.
YLIMS = [110, 30, 30]
#STARPOS = [0.85, 0.85, 0.85] # Coordinate to position significance stars; % of 
STARPOS = [0.8, 0.8, 0.8] # Coordinate to position significance stars; % of 
#ylim
BINCONF = 0.95 # Confidence of binomial confidence intervals.

#SUBPLOTNS = [111] # Subplots of the figure for frequency.
#SUBPLOTLS = [''] # Labels for the subplots.
#YLIMS = [110]
#STARPOS = [0.8] # Coordinate to position significance stars; % of 
##ylim
#BINCONF = 0.95 # Confidence of binomial confidence intervals.

FIGDPI=1200 # Figure DPI.
FIGW=8.5# Figure width.
#FIGW=6 # Figure width.
FIGH=2.5 #Figure height.

FONTSZ=10.5# Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=10 # Title font size.

BARWIDTH=1
YMIN=0
YLABEL2 ='%'
YAXISTICKS2 = 7 # Number of y-axis ticks.
