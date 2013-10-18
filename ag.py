from aglib import *

KINDLIST = ['flare', 'charge', 'escd', 'escm']
#KINDLIST = ['flare']
FNAME = '20131017_aganalyze.csv'
PROPFILE = 'freq_of_behavior.txt'
LATFILE = 'latency_to_behavior.txt'
PROPTESTFILE = 'proptest.txt'

with open(LATFILE, 'w') as g:
    g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
    'Mean latency (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

with open(PROPFILE, 'w') as f:
    f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
    '# pairs exhibiting behavior', '# pairs tested', '% exhibiting behavior'))
    
    
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
