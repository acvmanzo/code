from aglib import *

KINDLIST = ['flare', 'charge', 'escd', 'escm']
FNAME = '20131015data.csv'


for KIND in KINDLIST:
    plotlatbw(KIND, FNAME, iskeyfile='No')
    plt.savefig(KIND+'lat.png')
