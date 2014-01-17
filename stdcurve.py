from libs.qrtpcrlib import *

DATADIR = 'data'
FNAMES = ['20130919a_sc_gapdh_pten_nrxiv_nrxi.csv', '20130919b_sc_gapdh.csv', 
'20130920_sc_bintnu_cg34127.csv', '20131001_sc_nhe3_en_rev.csv']

POINTSS = ['nooutliers', 'allpoints']
GROUPBYS = ['plate', 'pool']
USEAVGS = ['points', 'avg']


datafiles = [os.path.join(DATADIR, f) for f in FNAMES]

for points in POINTSS:
    for groupby in GROUPBYS:
        d = {}
        for fname in datafiles:
            loadscdata(d, fname, points, groupby)
            for useavg in USEAVGS:
                getsc(d, useavg, points, groupby)

