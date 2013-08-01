import numpy as np
import matplotlib.pyplot as plt
import genplotlib as gpl
import cmn.cmn as cmn
import rstatslib as rsl
import rpy2.robjects as robjects
import os


r = robjects.r

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
    fname = dictionary with raw data

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

    """Generates a dictionary where the keywords are genotypes and the values are a list in which an entry of "100" = success and an entry of "0" = failure.

    kind: 'wing' (wing extension) 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    fname: file containing raw data
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


def dictproptest(d, conf=0.05):
    """Returns a p-value for whether a set of proportions are from the same distribution. Input is a dictionary in which the keywords are genotypes or conditions and the values are a list in which an entry of "100" = success and an entry of "0" = failure (output of dictfreq).

    """

    ks = []
    nsuc = []
    n=[]

    for k, v in d.iteritems():
        ks.append(k)
        nsuc.append(np.sum(v)/100)
        n.append(len(v))

    dpt = zip(ks, nsuc, n)

    unlist = r['unlist']
    pt = rsl.proptest(unlist(nsuc), unlist(n))
    return(pt.rx('p.value')[0][0])


def createproptestfile(fname):

    """Creates a file (specified in 'fname') that will list the results of the proportion test as implemented in R.
    """

    with open(fname, 'w') as f:
        f.write('Proportion test results\n')
        f.write('Kind\tp-value\n')


def writeproptestfile(ofile, d, kind):
    """Input is a dictionary in which the keywords are genotypes or conditions and the values are a list in which an entry of "100" = success and an entry of "0" = failure (output of dictfreq)"""

    pt = dictproptest(d)
    with open(ofile, 'a') as f:
        f.write('{0}\t{1}\n'.format(kind, pt))



def dictmeans(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the values are lists of the mean frequency, standard deviation, standard error, and n for that condition.

    dict: dictionary where keys are genotypes and values are raw data
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


def dictbin(dict, conf=0.05, methods='wilson', label='data'):
    """Generates a new dictionary from frequency data.
    Input:
    dict = output of function dictfreq
    conf = confidence level for confidence intervals
    methods = method for constructing conf. interval
    label = parameter being measured

    Output:
    A dictionary where the keywords are conditions or genotypes and the values are as follows:
    nsuc = number of successes
    n = number of trials
    prop = nsuc/n
    method = method for constructing binomical confidence intervals (see documentation for rstatslib.binomici_w
    lowerci = min value of confidence interval
    upperci = max value of confidence interval
    """

    mean_dict = {}

    for condition, value in dict.iteritems():

        meanval = np.mean(value)
        stdev = np.std(value)

        xsuc = np.sum(value)/100
        n = len(value)

        z = rsl.binomci_w(xsuc, n, conf, methods)

        if condition not in mean_dict:
            mean_dict[condition] = {}

        mean_dict[condition]['nsuc'] = xsuc
        mean_dict[condition]['n'] = n
        mean_dict[condition]['method'] = methods
        mean_dict[condition]['label'] = label
        mean_dict[condition]['prop'] = z.rx('mean')[0][0]*100
        mean_dict[condition]['lowerci'] = z.rx('lower')[0][0]
        mean_dict[condition]['upperci'] = z.rx('upper')[0][0]


    return(mean_dict)



def plotlat(kind, fname, iskeyfile = 'true', keyfile='keylist', type='b'):

    """Generates a bar plot of the latencies for each type of behavior for each genotype.

    kind: type of behavior - 'wing' (wing extension) 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    fname: file containing raw data
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be plotted; default name is 'keylist'
    type: type of plot; default is 'b' which is a bar plot
    """

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

    """Generates a bar plot of the frequency of each type of behavior for each genotype.

    kind: type of behavior - 'wing' (wing extension) 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    fname: file containing raw data
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be plotted; default name is 'keylist'
    type: type of plot; default is 'b' which is a bar plot
    """


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



def createshapfile(fname):

    """Creates a file (specified in 'fname') that will list the results of the Shapiro-Wilk test of normality as implemented in R. One line is written with the results from a set of values drawn from a normal distribution.
    """

    r = robjects.r
    normsample = r['rnorm'](50)
    x = rsl.shapirowilk(normsample)
    with open(fname, 'w') as f:
        f.write('Shapiro-Wilk test results\n')
        f.write('Condition\tBehavior\tp-value\n')
        f.write('{0}\t{1}\t{2:.4g}\n'.format('normsample', 'normsample', x[1][0]))


def writeshapfile(fname, datadict, kind):

    """Writes a file that lists the results of the Shapiro-Wilk test of normality as implemented in R.

    fname: name of the output file
    datadict: a dictionary with the keys as genotypes and the values as the raw data,
    kind: type of behavior - 'wing' (wing extension), 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    """

    r = robjects.r
    unlist = r['unlist']

    for n, v in datadict.iteritems():
        v = unlist(v)
        x = rsl.shapirowilk(v)
        with open(fname, 'a') as f:
            f.write('{0}\t{1}\t{2:.4g}\n'.format(n, kind, x[1][0]))


def dictmw(d, ctrlkey='cs', test='exact'):

    """Returns a dictionary in which the keys are the genotypes and the values are the results of the Mann-Whitney test as implemented in R.

    datadict: a dictionary with the keys as the genotypes and the values as the raw data
    ctrlkey: the name of the key for the dictionary entry that will serve as the control genotype; default is 'cs'
    """

    r = robjects.r
    unlist = r['unlist']
    mwdict = {}

    for i,v in d.iteritems():

        v, ctrl = map(unlist, [v, d[ctrlkey]])

        if test == 'exact':
            mw = rsl.mannwhitneyexact(v, ctrl)

        if test == 'std':
            mw = rsl.mannwhitney(v, ctrl)

        mwdict[i] = {}
        mwdict[i]['sigtest'] = mw.rx('method')[0][0]
        mwdict[i]['pval'] = mw.rx('p.value')[0][0]
        mwdict[i]['n'] = len(v)
        mwdict[i]['median'] = np.median(v).tolist()
        mwdict[i]['control'] = ctrlkey

    return(mwdict)


def mcpval(pvaldict, method='fdr', iskeyfile = 'true', keyfile='keylist'):

    """Returns a dictionary where the keys are genotypes and the values include p-values that are corrected for multiple comparisons using the p.adjust function in R.

    pvaldict = dictionary where the keys are genotypes and the values include p-values derived from a statistical test; should be the output of a function like dictmw()
    method = method chosen for multiple correction using the p.adjust function ('holm', 'hochberg', 'hommel', 'bonferroni', 'BH', 'BY', 'fdr', 'none')
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be used; default name is 'keylist'

    """

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(pvaldict.keys())

    gens = []
    pvals = []
    ctrl = []
    newdict = {}

    for k in keylist:
        gens.append(k)
        pvals.append(pvaldict[k]['pval'])
        ctrl.append(pvaldict[k]['control'])
        newdict[k] = pvaldict[k]

    for k in keylist:
        assert pvals[gens.index(k)] == pvaldict[k]['pval']

    pvals.pop(gens.index(ctrl[0]))
    gens.remove(ctrl[0])

    adjpvals = list(rsl.padjust(pvals, method, len(pvals)))
    newptuple = zip(gens, adjpvals)

    for t in newptuple:
        newdict[t[0]]['adjpval'] = t[1]
        newdict[t[0]]['adjpvaltest'] = method

    newdict[ctrl[0]]['adjpval'] = 'n/a'
    newdict[ctrl[0]]['adjpvaltest'] = 'n/a'

    return(newdict)


def createmwfile(fname):

    """Creates a file (specified in 'fname') that will list the results of the Mann-Whitney significance test as implemented in R.
    """

    with open(fname, 'w') as f:
        f.write('Condition\tBehavior\tControl\tSigtest\tMultCompar\tp-value\tAdj p-value\n')


def writemwfile(fname, pvaldict, kind):

    """Writes a file (specified in 'fname') listing the results of the Mann-Whitney significance test as implemented in R.

    pvaldict = dictionary where the keys are genotypes and the values include p-values derived from a statistical test; output of the mcpval function.
    kind = type of behavior - 'wing' (wing extension), 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    """

    for k, v in pvaldict.iteritems():
        with open(fname, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(k, kind, v['control'], v['sigtest'][:15], v['adjpvaltest'], v['pval'], v['adjpval']))


def plotqqplots(kind, fname, ctrl='cs'):

    d = dictlat(kind, fname)

    qqplot = r['qqplot']
    qqnorm = r['qqnorm']
    unlist = r['unlist']
    png = r['png']
    devoff = r['dev.off']

    for k in d.keys():
        name1 = 'qqplot'+k+'.png'
        png(file=name1)
        pl=qqplot(unlist(d[ctrl]), unlist(d[k]), xlab=ctrl, ylab=k, main="Q-Q Plot")
        devoff()

        name2 = 'qqnorm'+k+'.png'
        png(file=name2)
        pl=qqnorm(unlist(d[k]), ylab=k, main="Q-Q Norm")
        devoff()



