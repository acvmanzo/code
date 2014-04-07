from libs.qrtpcrlib import *
import glob



DATAFILES = sorted(glob.glob('*.csv'))
#DATAFILES = ['2013-0919_2_sc_sarah.csv']
#DATAFILES = ['2013-1001_1_sc_sarah.csv']
GROUPBYS = ['plate', 'pool']
USEAVGS = ['points', 'avg']

#print primertogene()


d = {}
for fname in DATAFILES:
    print fname
    loadscdata(d, fname)
    #print d
    
for groupby in GROUPBYS:
    for useavg in USEAVGS:
        getsc(d, useavg, groupby)
                
#d = {}
#fnames = ['2013-0919_1_sc_sarah.csv', '2013-0919_2_sc_sarah.csv']
#for fname in fnames:
#    loadscdata(d, fname)
#print 'original dictionary', d['GAPDH_2013-0919_1'], d['GAPDH_2013-0919_2']
##print 'pooled dictionary', platetopool(d)['GAPDH']

