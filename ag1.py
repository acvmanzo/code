from libs.aglib import *

#KINDLIST = ['wingthreat', 'charge', 'anyag', 'escd', 'escm']
KINDLIST = ['wingthreat']
FNAME = 'testdatash.csv'
#FREQDIR = 'freqfig'

# Plots frequency figures
#cmn.makenewdir(FREQDIR)
#for KIND in KINDLIST:
    #print(KIND)
    #d = dictagfreq2(KIND, FNAME)
    
    #for k, v in d.iteritems():
        #print(k, sum(v)/100, len(v))
    
    #plotagfreq(KIND, d, 'true')
    #plt.savefig('{0}/freq{1}.png'.format(FREQDIR, KIND))


# Plots duration figure.
for KIND in KINDLIST:
    print(KIND)
    d = dictagdur2(KIND, FNAME)
    print(d)
    
    for k, v in d.iteritems():
        print(k, sum(v))
