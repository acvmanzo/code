import numpy as np
import matplotlib.pyplot as plt
import genplotlib as gpl
import cmn.cmn as cmn
import rstatslib as rsl
import rpy2.robjects as robjects
import os

K = 'copsuc'
KINDLIST = ['wing', 'copsuc', 'copatt1']
DATAFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/2013-07_courtship_inprog.csv'
SHAPFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/shap_lat.txt'
MCPVALFILE = '/home/andrea/Documents/lab/behavior_ca/courtship/codprac/mcpvalue_lat.txt'
CTRL = 'cs'

def convtosec (minvalue, secvalue):
    return(60*minvalue + secvalue)


def courtshipline(line):

    """Generates dictionary with the values from line, with the parameters as keywords.

    fname is of the following format:
    Data, Offset (s), Well #, Genotype, Wing ext (m), Wing ext (s), Cop
    Suc (m),Cop Suc (s),Cop Att 1 (m),Cop Att 1 (s)
    """

    cvals = {}
    x = ['date', 'movie', 'offset', 'well', 'gen', 'wingm', 'wings', 'copsucm', 'copsucs', 'copatt1m', 'copatt1s']
    y = line.split(',')[0:11]
    z = zip(x, y)

    for item in z:
        cvals[item[0]] = item[1]

    return(cvals)


def dictlat(kind, fname):

    """
    Generates a dictionary from data in 'fname' where the keywords are genotypes and the values are the latencies to a behavior specified by 'kind'.

    kind = 'wing' (wing extension), 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    """

    d = {}
    f = open(fname)
    f.next()
    for l in f:
        cdict= courtshipline(l)

        gen = cdict['gen']
        if gen not in d:
            d[gen] = []

        km = kind + 'm'
        ks = kind + 's'

        if cdict[km] != 'x' and cdict[km] != '-':
            d[gen].append(convtosec(float(cdict[km]), float(cdict[ks]))-float(cdict['offset']))

    return(d)


def dictfreq(kind, fname):

    """Generates a dictionary from data in 'fname' where the keywords are genotypes and the values are the % of flies displaying a behavior specified by 'kind'.

    kind = 'wing' (wing extension), 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    """

    d = {}
    f = open(fname)
    f.next()
    for l in f:
        cdict= courtshipline(l)

        gen = cdict['gen']
        if gen not in d:
            d[gen] = []

        ks = kind + 's'

        if cdict[ks] == 'x':
            d[gen].append(0)

        try:
            if float(cdict[ks]) >= 0:
                d[gen].append(100)
        except(ValueError):
            pass

    return(d)



def dictmeans(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the values are lists of
    the mean frequency, standard deviation, standard error, and n for that condition.
    """

    mean_dict = {}

    for condition, value in dict.iteritems():
        meanval = np.mean(value)
        stdev = np.std(value)
        n = len(value)
        sterr = stdev/np.sqrt(n)

        if condition not in mean_dict:
            mean_dict[condition] = []

        mean_dict[condition].append(meanval)
        mean_dict[condition].append(stdev)
        mean_dict[condition].append(sterr)
        mean_dict[condition].append(n)
        mean_dict[condition].append('{0}'.format(label))

    return(mean_dict)



def plotlat(kind, fname, iskeyfile = 'true', keyfile='keylist', type='b'):

    d = dictlat(kind, fname)
    md = dictmeans(d)

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = 'Latency (s)'

    if kind == 'wing':
        ftitle = 'Latency to wing extension'

    if kind == 'copsuc':
        ftitle = 'Latency to copulation'

    if kind == 'copatt1':
        ftitle = 'Latency to first copulation attempt'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle)


def plotfreq(kind, fname, iskeyfile = 'true', keyfile='keylist', type='b'):

    d = dictfreq(kind, fname)
    md = dictmeans(d)

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = '%'

    if kind == 'wing':
        ftitle = 'Percentage of flies displaying wing extension'

    if kind == 'copsuc':
        ftitle = 'Percentage of flies copulating'

    if kind == 'copatt1':
        ftitle = 'Percentage of flies attempting copulation'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle)



def savegraph(fname = 'graph'):
    """Saves the bar graph plotted with 'plotbar'."""
    plt.savefig(fname)


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
    mwdict = {}

    for i,v in datadict.iteritems():

        v, ctrl = map(unlist, [v, d[CTRL]])
        mw = rsl.mannwhitney(v, ctrl)

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


def createmwfile(filename):

    with open(filename, 'w') as f:
        f.write('Condition\tBehavior\tSigtest\tMultCompar\tp-value\tAdj p-value\n')


def writemwfile(filename, pvaldict, kind):

    for k, v in pvaldict.iteritems():
        with open(filename, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, v['sigtest'][:8], v['adjpvaltest'], v['pval'], v['adjpval']))










