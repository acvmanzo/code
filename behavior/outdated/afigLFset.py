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
