from libs.aglib import *
import libs.courtshiplib as cl

#KINDLIST = ['wingthreat', 'charge', 'anyag', 'escd', 'escm']
KINDLIST = ['wingthreat']
FNAME = 'testdatash.csv'
CTRLKEY = 'cs'
KEYFILE = 'keylist'
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
#for KIND in KINDLIST:
    #print(KIND)
    #d = dictagdur2(KIND, FNAME)
    #print(d)
    
    #for k, v in d.iteritems():
        #print(k, sum(v))

for KIND in KINDLIST:
    d = dictagdur2(KIND, FNAME)
    md = cl.dictttest(d, CTRLKEY)
    adjpd = cl.mcpval(md, 'fdr', 'True', KEYFILE)
    print(md)
