from libs.aglib import *

KINDLIST = ['wingthreat', 'charge', 'anyag', 'escd', 'escm']
#KIND = 'wingthreat'
FNAME = '20131119_agdata_wms_sorted.csv'
FREQDIR = 'freqfig'

cmn.makenewdir(FREQDIR)
for KIND in KINDLIST:
    print(KIND)
    d = dictagfreq2(KIND, FNAME)
    
    for k, v in d.iteritems():
        print(k, sum(v)/100, len(v))
    
    plotagfreq(KIND, d, 'true')
    plt.savefig('{0}/freq{1}.png'.format(FREQDIR, KIND))

