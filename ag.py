from aglib import *
import courtshiplib as cl

KINDLIST = ['charge', 'escd']
#KINDLIST = ['flare', 'charge', 'escd', 'escm']
#KINDLIST = ['flare']
FNAME = 'allag.csv'
PROPFILE = 'freq_of_behavior.txt'
LATFILE = 'latency_to_behavior.txt'
PROPTESTFILE = 'proptest.txt'
SHAPFILE = 'shap_lat.txt'
KEYFILE = 'keylist'

cl.createinfolat(LATFILE)
cl.createinfoprop(PROPFILE)
cl.createshapfile(SHAPFILE)
    
for KIND in KINDLIST:
    print(KIND)
    #latd = dictaglat(KIND, FNAME)
    #print(KIND, 'lat', latd)
    #plotaglatbw(KIND, latd, iskeyfile='No')
    ##writeinfolat(FNAME, LATFILE, KIND, 'cs', KEYFILE, iskeyfile='False')
    #plt.savefig('lat' + KIND + '.png')
    d = dictaglat(KIND, FNAME)
    freqd = dictfreq(KIND, FNAME)
    #print(KIND, 'freq', freqd)
    #plotagfreq(KIND, freqd)
    #plt.savefig('freq' + KIND + '.png')

    writeinfoprop(FNAME, PROPFILE, KIND, KEYFILE, iskeyfile='False')
    writeproptestfile(PROPTESTFILE, freqd, KIND, KEYFILE, iskeyfile='false')
    cl.writeshapfile(SHAPFILE, d, KIND)



