import os

KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
CDIR = os.path.basename(os.path.abspath('.'))
OUTPUTFIG = '{0}agdurfig_{1}.png'.format(DIR, CDIR) # Name of figure.
SHAPFILE = '{0}agdurshap_{1}.txt'.format(DIR, CDIR) # Name of file with 
#results of Shapiro test for normality.
MWFILE = '{0}agdurmwtest_{1}.txt'.format(DIR, CDIR) # Name of file with results 
#of Mann-Whitney test.



# Info about figure content.
KINDLIST = ['wingthreat', 'charge', 'anyag', 'escd', 'escm'] # Behaviors to be analyzed.
#KINDLIST = ['wingthreat'] # Behaviors to be analyzed.
#KINDLIST = ['charge'] # Behaviors to be analyzed.


# Figure parameters.
SUBPLOTNS = [231, 232, 233, 234, 235] # Subplots of the figure for frequency.
SUBPLOTLS = ['A', 'B', 'C', 'D', 'E'] # Labels for the subplots.

FIGDPI=1200 # Figure DPI.
FIGW=12 # Figure width.
FIGH=8 # Figure height.

FONTSZ=11 # Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=12 # Title font size.

# Options for bar plots.
BARWIDTH=1
YMIN=-10
YLABEL = 'sec'
YAXISTICKS = 5
