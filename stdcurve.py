from libs.qrtpcrlib2 import *

DATADIR = 'data'
FNAMES = ['20130919a_sc_gapdh_pten_nrxiv_nrxi.csv', '20130919b_sc_gapdh.csv']
POINTS = 'nooutliers'
GROUPBY = 'plate'
USEAVG = 'points'


datafiles = [os.path.join(DATADIR, f) for f in FNAMES]
d = {}
for fname in datafiles:
    loadscdata(d, fname, POINTS, GROUPBY)

getsc(d, USEAVG, POINTS, GROUPBY)



#for graphtype in ['no_outliers']:
    #print('GRAPHTYPE', graphtype)
    #efile = ql.defresdir(graphtype)+'efficiencies_'+graphtype+'.txt'
    #ql.create_efile(efile)
    #d = {}
    #for fname in FNAMES:
        #print(fname)
        #d = ql.loaddata(d, fname, graphtype)
    #print(d)
    #for k, v in d.iteritems():
        #print(k)
        #cq = np.array(zip(*v)[0])
        #logsq = np.array(zip(*v)[1])
        #params = ql.fitline(logsq, cq)
        #ql.plotstdcurve(params, k, ql.defresdir(graphtype), graphtype)
        #ql.write_efile(efile, params, k, graphtype)
