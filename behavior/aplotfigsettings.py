

# Input and output files.
#FNAME = '2013-0718_courtship_data_for_nrsa.csv' #File containing original data.
#FNAME = 'allcourtship.csv' #File containing original data.
#FNAME = 'alljcourtship.csv' #File containing original data.
#FNAME = 'allwillcourtship.csv' #File containing original data.
KEYFILE = 'keylist'
DIR = 'presfig/' # Directory that figure will be saved in.
OUTPUTFIG = DIR+'agresexp.png' # Name of figure.
OFILELAT = DIR+'agreslat.txt' # Name of file with latency info.
OFILEPROP = DIR+'agresprop.txt' # Name of file with frequency info.
OFILEMULTIPROPTEST= DIR+'multiproptest.txt' # Name of file with results of the R 
#function 'prop.test'
PTFILE = DIR+'aproptest.txt'
FISHTFILE = DIR+'agfishtest.txt'

# Info about figure content.
KINDLIST = ['flare', 'charge', 'escd', 'escm'] # Behaviors to be analyzed.
#CTRLKEY = '+/+' # Name of the control strain that all other lines will be 
#CTRLKEY = 'cs-Apr' # Name of the control strain that all other lines will be 
#CTRLKEY = 'cs-Jenee' # Name of the control strain that all other lines will be 
#CTRLKEY = 'cs-Jenee' # Name of the control strain that all other lines will be 
#compared to in the Mann-Whitney U Test.

# Figure parameters.
#SUBPLOTNS1 = [421, 423, 425, 427] # Subplots of the figure.
#SUBPLOTNS2 = [422, 424, 426, 428] # Subplots of the figure.
SUBPLOTLS1 = ['A', 'B', 'C', 'D'] # Labels for the subplots.
SUBPLOTLS2 = ['E', 'F', 'G', 'H'] # Labels for the subplots.
#FIGW=6 # Figure width.
#FIGH=10 # Figure height.
FIGDPI=1200 # Figure DPI.

SUBPLOTNS1 = [241, 242, 243, 244]
SUBPLOTNS2 = [245, 246, 247, 248]
FIGW=13
FIGH=7

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
