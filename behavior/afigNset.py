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
#KINDLIST = ['wingthreat', 'charge', 'chase', 'escd', 'escm'] # Behaviors to be analyzed.
KINDLIST = ['charge', 'escd', 'escm'] # Behaviors to be analyzed.

# Figure parameters.
#SUBPLOTNS = [151, 152, 153, 154, 155] # Subplots of the figure for frequency.
#SUBPLOTLS = ['', '', '', '', ''] # Labels for the subplots.
#YLIMS = [30, 25, 10, 10, 10]
##STARPOS = [0.85, 0.85, 0.85] # Coordinate to position significance stars; % of 
#STARPOS = [0.8, 0.8, 0.8, 0.8, 0.8] # Coordinate to position significance stars; % of 
##ylim

SUBPLOTNS = [131, 132, 133] # Subplots of the figure for frequency.
SUBPLOTLS = ['', '', ''] # Labels for the subplots.
YLIMS = [30, 10, 10]
#STARPOS = [0.85, 0.85, 0.85] # Coordinate to position significance stars; % of 
STARPOS = [0.8, 0.8] # Coordinate to position significance stars; % of 

FIGDPI=1500 # Figure DPI.
#FIGW=11.5 # Figure width.
#FIGH=3 #Figure height.

FIGW=9 # Figure width.
FIGH=3 #Figure height.

FONTSZ=11# Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=11 # Title font size.

BARWIDTH=1
YMIN=0
YLABEL2 ='# instances of behavior'
YAXISTICKS2 = 7 # Number of y-axis ticks.
