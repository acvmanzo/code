import rpy2.robjects as robjects
from plotdata import *

FNAME ='/home/andrea/Documents/lab/behavior_ca/courtship/codprac/2013-07_courtship_inprog.csv'

r = robjects.r

winglat, copsuclat, copattlat = dictlat(FNAME)
mwinglat, mcopsuclat, mcopattlat = map(means,[winglat, copsuclat, copattlat])
#print('python', winglat['cs'])

rcs_wlat = robjects.FloatVector(winglat['cs'])
rnrxi_wlat = robjects.FloatVector(winglat['NrxI'])
rnrxiv_wlat = robjects.FloatVector(winglat['NrxIV'])

rcs_copattlat = robjects.FloatVector(copattlat['cs'])
rnrxi_copattlat = robjects.FloatVector(copattlat['NrxI'])

rcs_copsuclat = robjects.FloatVector(copsuclat['cs'])
rnrxi_copsuclat = robjects.FloatVector(copsuclat['NrxI'])

rnorm = r['rnorm']
datanorm = rnorm(50)
print(datanorm)

shaptest = r['shapiro.test']
print('cs')
print(shaptest(rcs_copattlat))
print('norm')
print(shaptest(datanorm))

wilcoxtest = r['wilcox.test']
print(wilcoxtest(rcs_copsuclat, rnrxi_copsuclat))
