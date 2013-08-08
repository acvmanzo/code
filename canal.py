from courtshiplib import *

KINDLIST = ['wing', 'copsuc', 'copatt1']
FNAME = '2013-0718_courtship_data _for_nrsa.csv'
K = 'copsuc'
KINDLIST = ['wing', 'copsuc', 'copatt1']
SHAPFILE = 'shap_lat.txt'
MCPVALFILE = 'mcpvalue_lat_exact.txt'
PTFILE = 'proptest.txt'
CTRL = '+/+'
DIR = 'summary/'

cmn.makenewdir(DIR)

print(os.path.abspath('.'))
for KIND in KINDLIST:
    plotlat(KIND, FNAME)
    plt.savefig(DIR+KIND+'lat')
    plotfreq(KIND, FNAME)
    plt.savefig(DIR+KIND+'freq')

createshapfile(DIR+SHAPFILE)
createmwfile(DIR+MCPVALFILE)
createproptestfile(DIR+PTFILE)

for k in KINDLIST:
    d = dictlat(k, FNAME)
    mwd = dictmw(d, ctrlkey='+/+')
    adjpd = mcpval(mwd, 'fdr')

    writeshapfile(DIR+SHAPFILE, d, k)
    writemwfile(DIR+MCPVALFILE, adjpd, k)

    pd = dictfreq(k, FNAME)
    writeproptestfile(DIR+PTFILE, pd, k)
