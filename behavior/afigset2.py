# Settings for afig.py.
import os

# Input and output files.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
CDIR = os.path.basename(os.path.abspath('.'))
OUTPUTFIG = '{0}agfig_{1}.png'.format(DIR, CDIR) # Name of figure.
OFILEPROP = '{0}agpropinfo_{1}.txt'.format(DIR, CDIR) # Name of file with 
#frequency info.
#OFILEMULTIPROPTEST= DIR+'multiproptest.txt' # Name of file with results of the R 
#function 'prop.test'
FISHTFILE = '{0}agfishtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Fisher's test.

# Info about figure content.
KINDLIST = ['anyag', 'escd', 'escm'] # Behaviors to be analyzed.

# Figure parameters.
SUBPLOTNS = [131, 132, 133] # Subplots of the figure for frequency.
SUBPLOTLS = ['A', 'B', 'C'] # Labels for the subplots.

FIGDPI=1200 # Figure DPI.
FIGW=12 # Figure width.
FIGH=4 # Figure height.

FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Options for bar plots.
BARWIDTH=1
YMIN=-10

# Options for frequency plots:
YLABEL2 ='%'
YAXISTICKS2 = 7 # Number of y-axis ticks.
YMIN2 = 0
YLIM2 = 110
