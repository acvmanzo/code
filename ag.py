from aglib import *

KINDLIST = ['flare', 'charge', 'escd', 'escm']
#KINDLIST = ['flare']
FNAME = '20131017_aganalyze.csv'
PROPFILE = 'freq_of_behavior.txt'
LATFILE = 'latency_to_behavior.txt'
PROPTESTFILE = 'proptest.txt'

createinfolat(LATFILE)
createinfoprop(PROPFILE)   
    
for KIND in KINDLIST:
    print(KIND)
    latd = dictaglat(KIND, FNAME)
    #print(KIND, 'lat', latd)
    plotaglatbw(KIND, latd, iskeyfile='No')
    writeinfolat(FNAME, LATFILE, KIND, 'cs')
    plt.savefig('lat' + KIND + '.png')
    freqd = dictfreq(KIND, FNAME)
    #print(KIND, 'freq', freqd)
    plotagfreq(KIND, freqd)
    plt.savefig('freq' + KIND + '.png')

    writeinfoprop(FNAME, PROPFILE, KIND)
    writeproptestfile(PROPTESTFILE, freqd, KIND)
