import rstatslib as rsl
import plotdata as pd
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri as rpyn
import os
import cmn.cmn as cmn

K = 'copsuc'
KINDLIST = ['wing', 'copsuc', 'copatt1']
DATAFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/2013-07_courtship_inprog.csv'
SHAPFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/shap_lat.txt'
MCPVALFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/mcpvalue_lat.txt'
CTRL = 'cs'

def createshapfile(shapfile):

    r = robjects.r
    normsample = r['rnorm'](50)
    x = rsl.shapirowilk(normsample)
    with open(shapfile, 'w') as f:
        f.write('Shapiro-Wilk test results\n')
        f.write('Condition\tBehavior\tp-value\n')
        f.write('{0}\t{1}\t{2:.4g}\n'.format('normsample', 'normsample', x[1][0]))


def writeshapfile(shapfile, datadict, kind):

    r = robjects.r
    unlist = r['unlist']

    for n, v in datadict.iteritems():
        v = unlist(v)
        x = rsl.shapirowilk(v)
        with open(SHAPFILE, 'a') as f:
            f.write('{0}\t{1}\t{2:.4g}\n'.format(n, kind, x[1][0]))



def dictmw(datadict):

    r = robjects.r
    unlist = r['unlist']
    #k = KINDLIST[0]
    #d = pd.dictlat(k, DATAFILE)

    #mwlist = []
    mwdict = {}

    for i,v in datadict.iteritems():

        v, ctrl = map(unlist, [v, d[CTRL]])
        mw = rsl.mannwhitney(v, ctrl)

        #mwlist.append((i, mw.rx('p.value')[0][0]))
        mwdict[i] = {}
        mwdict[i]['sigtest'] = mw.rx('method')[0][0]
        mwdict[i]['pval'] = mw.rx('p.value')[0][0]

    return(mwdict)


def mcpval(pvaldict, test, iskeyfile = 'true', keyfile='keylist'):

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(pvaldict.keys())

    gens = []
    pvals = []
    newdict = {}

    for k in keylist:
        gens.append(k)
        pvals.append(pvaldict[k]['pval'])
        newdict[k] = pvaldict[k]

    for k in keylist:
        assert pvals[gens.index(k)] == pvaldict[k]['pval']

    adjpvals = list(rsl.padjust(pvals, test, len(pvals)))
    newptuple = zip(gens, adjpvals)

    for t in newptuple:
        newdict[t[0]]['adjpval'] = t[1]
        newdict[t[0]]['adjpvaltest'] = test

    return(newdict)


#def createmwfile(pvaldict, filename):

    #testlist = []
    #adjplist = []

    #for i, v in pvaldict.iteritems():
        #testlist.append(v['sigtest'])
        #adjplist.append(v['adjpvaltest'])

    #with open(filename, 'w') as f:
        #f.write('Significance test: {}\n'.format(testlist[0]))
        #f.write('P-values adjusted using {}\n'.format(adjplist[0]))


def createmwfile(filename):

    with open(filename, 'w') as f:
        f.write('Condition\tBehavior\tSigtest\tMultCompar\tp-value\tAdj p-value\n')


def writemwfile(filename, pvaldict, kind):

    for k, v in pvaldict.iteritems():
        with open(filename, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, v['sigtest'][:8], v['adjpvaltest'], v['pval'], v['adjpval']))


def sample():
    a, b = zip(*mwlist)
    #print(a)
    #print(b)
    adjustp = rsl.padjust(list(b), "fdr", len(b))
    #print(adjustp)

    c = zip(a, adjustp)
    #print(c)
    #print(mwdict)
    for item in c:
        #print(mwdict[item[0]])
        mwdict[item[0]]['adjpval'] = item[1]

    print(mwdict)

    with open(MCFILE, 'w') as f:
        for i, v in mwdict.iteritems():
            f.write('{0}\t{1}\t{2}\n'.format(i, v['pval'], v['adjpval']))


    #with open(MCFILE, 'w') as f:
        #f.write('{0}'.format(c[0]))

createshapfile(SHAPFILE)
createmwfile(MCPVALFILE)

for k in KINDLIST:
    d = pd.dictlat(k, DATAFILE)

    mwd = dictmw(d)
    adjpd = mcpval(mwd, 'fdr')

    writeshapfile(SHAPFILE, d, k)
    writemwfile(MCPVALFILE, adjpd, k)
