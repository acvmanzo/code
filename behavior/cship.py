from courtshiplib import *

KINDLIST = ['wing', 'copsuc', 'copatt1']
#FNAME = 'courtship_data.csv'
FNAME = 'allcourtship.csv'
PROPFILE = 'freq_of_courtship.txt'
LATFILE = 'latency_to_courtship.txt'
KEYFILE = 'keylist'
CTRLKEY = 'cs-June'
SHAPFILE = 'shap_lat.txt' # Name of file listing results of the Shapiro-Wilk 
#test.
MCPVALFILE = 'mcpvalue_lat_exact.txt' # Name of file listing results of the 
#Mann-Whitney U Test, with p-values adjusted for multiple comparisons.
MWTEST = 'exact' # Specifies whether to use the R function wilcox.exact 
#('exact') or wilcox.test ('std')
MCCORR = 'fdr' # Specifies how to adjust p-values to correct for multiple 
#comparisons using the R function p.adjust ('fdr' = false discovery rate')
PTFILE = 'proptest.txt' # Name of file listing the results of the proportion 
#test, where p-values give the probability of observing the results if the null
 #hypothesis that all the proportions are from the same distribution is true.
PPTFILE = 'pairproptest.txt' # Name of file listing results of the pairwise
#proportion test.

createinfolatmean(LATFILE)
createinfoprop(PROPFILE)

createshapfile(SHAPFILE)
createmwfile(MCPVALFILE)
createproptestfile(PTFILE)
createpptestfile(PPTFILE)

for KIND in KINDLIST:
    print(KIND)
    plotlatbw(KIND, FNAME, 'true')
    plt.savefig(KIND+'lat')
    plotfreq(KIND, FNAME, 'true')
    plt.savefig(KIND+'freq')
    
    writeinfolatmean(FNAME, LATFILE, KIND, 'cs-Apr')
    writeinfoprop(FNAME, PROPFILE, KIND)

for k in KINDLIST:
    print(k)
    d = dictlat(k, FNAME)
    mwd = dictmw(d, ctrlkey=CTRLKEY, test=MWTEST)
    adjpd = mcpval(mwd, MCCORR)
       

    writeshapfile(SHAPFILE, d, k)
    writemwfile(MCPVALFILE, adjpd, k)

    pd = dictfreq(k, FNAME)
    print('ppd')
    ppd = dictpptest(pd, ctrlkey=CTRLKEY)
    print(ppd)
    print('adjppd')
    adjppd = mcpval(ppd, MCCORR)
    writepptestfile(PPTFILE, adjppd, k)



