# Settings for afig.py.
import os

# Input and output files.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
CDIR = os.path.basename(os.path.abspath('.'))
OUTPUTFIG1 = '{0}agnummedfig_{1}.png'.format(DIR, CDIR) # Name of figure.
OUTPUTFIG2 = '{0}agnummeanfig_{1}.png'.format(DIR, CDIR) # Name of figure.
NUMFILE = '{0}agnummedinfo_{1}.txt'.format(DIR, CDIR) # Name of file with 
#info.
NUMTFILE = '{0}agnumttest_{1}.txt'.format(DIR, CDIR) # Name of file with results.
NUMMWFILE = '{0}agnummwtest_{1}.txt'.format(DIR, CDIR)
SHAPNUMFILE = '{0}agnumshap_{1}.txt'.format(DIR, CDIR)

# Info about figure content.
KINDLIST = ['escd'] # Behaviors to be analyzed.

# Figure parameters.
SUBPLOTNS = [111, 132, 133] # Subplots of the figure for frequency.
SUBPLOTLS = ['', 'B', 'C'] # Labels for the subplots.
YLIMS = [20, 10, 10]
#STARPOS = [0.85, 0.85, 0.85] # Coordinate to position significance stars; % of 
STARPOS = [0.8, 0.8, 0.8] # Coordinate to position significance stars; % of 
#ylim

FIGDPI=1200 # Figure DPI.
FIGW=3 # Figure width.
FIGH=2.75 #Figure height.

FONTSZ=11# Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=11 # Title font size.

BARWIDTH=1
YMIN=0
YLABEL2 ='# instances of behavior'
YAXISTICKS2 = 7 # Number of y-axis ticks.
