from courtshiplib import *


KINDLIST = ['wing', 'copsuc', 'copatt1']
FNAME = '2013-0718_courtship_data _for_nrsa.csv'
K = 'copsuc'
KINDLIST = ['wing', 'copsuc', 'copatt1']
SHAPFILE = 'shap_lat.txt'
MCPVALFILE = 'mcpvalue_lat_exact.txt'
CTRL = 'cs'


print(os.path.abspath('.'))
for KIND in KINDLIST:
    plotlat(KIND, FNAME)
    plt.savefig(KIND+'lat')
    plotfreq(KIND, FNAME)
    plt.savefig(KIND+'freq')

createshapfile(SHAPFILE)
createmwfile(MCPVALFILE)


for k in KINDLIST:
    d = dictlat(k, FNAME)
    mwd = dictmw(d)
    adjpd = mcpval(mwd, 'fdr')

    writeshapfile(SHAPFILE, d, k)
    writemwfile(MCPVALFILE, adjpd, k)

