# Script for plotting standard curves for primers used in qRT-PCR.

from libs.qrtpcrlib import *

DATAFILES = sorted(glob.glob('*.csv'))
GROUPBYS = ['plate', 'pool']
USEAVGS = ['points', 'avg']

d = {}
for fname in DATAFILES:
    print fname
    loadscdata(d, fname)
    
for groupby in GROUPBYS:
    for useavg in USEAVGS:
        getsc(d, useavg, groupby)
