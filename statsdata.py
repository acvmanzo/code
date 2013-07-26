import statsdata as sd
import plotdata as pd
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri as rpyn
import os

KINDLIST = ['wing', 'copsuc', 'copatt1']
DATAFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/2013-07_courtship_inprog.csv'
SHAPFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/shapfile.txt'

r = robjects.r
#winglat, copsuclat, copattlat = dictlat(FNAME)

#mwinglat, mcopsuclat, mcopattlat = map(means,[winglat, copsuclat, copattlat])
##print('python', winglat['cs'])

#rcs_wlat = robjects.FloatVector(winglat['cs'])
#rnrxi_wlat = robjects.FloatVector(winglat['NrxI'])
#rnrxiv_wlat = robjects.FloatVector(winglat['NrxIV'])

#rcs_copattlat = robjects.FloatVector(copattlat['cs'])
#rnrxi_copattlat = robjects.FloatVector(copattlat['NrxI'])

#rcs_copsuclat = robjects.FloatVector(copsuclat['cs'])
#rnrxi_copsuclat = robjects.FloatVector(copsuclat['NrxI'])

#rnorm = r['rnorm']
#datanorm = rnorm(50)
#print(datanorm)

#shaptest = r['shapiro.test']
#print('cs')
#print(shaptest(rcs_copattlat))
#print('norm')
#print(shaptest(datanorm))

#wilcoxtest = r['wilcox.test']
#x = wilcoxtest(rcs_copsuclat, rnrxi_copsuclat)

#isatomic = r['is.atomic']


unlist = r['unlist']
with open(SHAPFILE, 'w') as e:
    e.write('Shapiro-Wilk test results\n')
    e.write('Condition,Behavior,p-value\n')

rnorm = r['rnorm']
ctrl = rnorm(50)
x = sd.shapirowilk(ctrl)
with open(SHAPFILE, 'a') as f:
    f.write('{0},{1},{2:.4g}\n'.format('ctrl', 'ctrl', x[1][0]))

for k in KINDLIST:

    #if os.path.exists(SHAPFILE) == False:
    kname = k + 'lat'
    d = pd.dictlat(k, DATAFILE)

    for n, v in d.iteritems():

        v = unlist(v)
        x = sd.shapirowilk(v)

        with open(SHAPFILE, 'a') as f:
            f.write('{0},{1},{2:.4g}\n'.format(n, kname, x[1][0]))



