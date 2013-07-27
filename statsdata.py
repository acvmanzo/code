import rstatslib as rsl
import plotdata as pd
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri as rpyn
import os

KINDLIST = ['wing', 'copsuc', 'copatt1']
DATAFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/2013-07_courtship_inprog.csv'
SHAPFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/shap.txt'
MCFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/mcpvalue.txt'
CTRL = 'cs'

def createshapfile(shapfile):

    r = robjects.r
    normsample = r['rnorm'](50)
    x = rsl.shapirowilk(normsample)
    with open(shapfile, 'w') as f:
        f.write('Shapiro-Wilk test results\n')
        f.write('Condition\tBehavior\tp-value\n')
        f.write('{0}\t{1}\t{2:.4g}\n'.format('normsample', 'normsample', x[1][0]))


def writeshapfile(shapfile, datafile, kind):

    r = robjects.r
    unlist = r['unlist']
    kname = kind + 'lat'

    d = pd.dictlat(kind, DATAFILE)
    for n, v in d.iteritems():
        v = unlist(v)
        x = rsl.shapirowilk(v)
        with open(SHAPFILE, 'a') as f:
            f.write('{0}\t{1}\t{2:.4g}\n'.format(n, kname, x[1][0]))



#createshapfile(SHAPFILE)
#for k in KINDLIST:
    #writeshapfile(SHAPFILE, DATAFILE, k)

r = robjects.r
unlist = r['unlist']
k = KINDLIST[0]
d = pd.dictlat(k, DATAFILE)
print(d)

mwlist = []
mwdict = {}

for n,v in d.iteritems():
    #print(n)
    v, ctrl = map(unlist, [v, d[CTRL]])
    #v = unlist(v)
    #ctrl = unlist(d[CTRL])

    r = robjects.r
    test = r['wilcox.test']
    z = test(v, ctrl, alternative="two.sided")
    #print(z)

    #print(z.rx('p.value'))
    #z = rsl.mannwhitney(v,ctrl)
    #z1 = r('z[['statistic']]')

    #print(n, z[0], z[1], z[2])
    mwlist.append((n, z.rx('p.value')[0][0]))
    mwdict[n] = {}
    mwdict[n]['sigtest'] = z.rx('method')[0][0]
    mwdict[n]['pval'] = z.rx('p.value')[0][0]

#print(mwlist)

a, b = zip(*mwlist)
#print(a)
#print(b)
adjustp = rsl.padjust(list(b), "fdr", len(b))
#print(adjustp)

c = zip(a, adjustp)
#print(c)
print(mwdict)
for item in c:
    print(mwdict[item[0]])
    mwdict[item[0]]['adjpval'] = item[1]

print(mwdict)

with open(MCFILE, 'w') as f:
    for i, v in mwdict.iteritems():
        f.write('{0}\t{1}\t{2}\n'.format(i, v['pval'], v['adjpval']))


#with open(MCFILE, 'w') as f:
    #f.write('{0}'.format(c[0]))
