
# Contains functions useful for analyzing courtship data from a csv file generated during manual scoring.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import genplotlib as gpl
import cmn.cmn as cmn
import rstatslib as rsl
import rpy2.robjects as robjects
import os
import pylab
import math
import rpy2

r = robjects.r

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
            d[gen].append(cmn.convtosec(float(cdict[km]), float(cdict[ks])) -
            float(cdict['offset']))
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


def dictproptest(d):
    """Returns a p-value for whether a set of proportions are from the same 
    distribution. Input is a dictionary in which the keywords are genotypes 
    or conditions and the values are a list in which an entry of 
    "100" = success and an entry of "0" = failure (output of dictfreq).
    """

    ks = []
    nsuc = []
    n=[]

    for k, v in d.iteritems():
        ks.append(k)
        nsuc.append(np.sum(v)/100)
        n.append(len(v))

    dpt = zip(ks, nsuc, n)
    #print(dpt)
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
    """Generates a new dictionary in which the keywords are conditions and the values are lists of the mean, standard deviation, standard error, and n for that condition.

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


def dictbin(dict, conf=0.95, methods='wilson', label='data'):
    """Generates a new dictionary with binomical confidence intervals from frequency data.
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
        mean_dict[condition]['lowerci'] = z.rx('lower')[0][0]*100
        #print(condition, 'dictbinlowerci', z.rx('lower')[0][0]*100)
        mean_dict[condition]['upperci'] = z.rx('upper')[0][0]*100
        mean_dict[condition]['conf'] = conf


    return(mean_dict)


def plotlatbw(kind, fname, iskeyfile = 'true', keyfile='keylist', type='bw'):
    '''Plots a box and whisker plot of the latency data.'''

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
    if kind == 'wing':
        plt.ylim(0, 150)


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

    """Generates a bar plot of the frequency of each type of behavior for 
    each genotype.

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
    plt.ylim(0, 120)



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
        print('n', n)
        print('v', v)
        if len(v) < 3:
            continue
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
    
    
def dictpptest(d, ctrlkey='cs'):

    """Returns a dictionary in which the keys are the genotypes and the values are the results of the Mann-Whitney test as implemented in R.

    datadict: a dictionary with the keys as the genotypes and the values as the raw data
    ctrlkey: the name of the key for the dictionary entry that will serve as the control genotype; default is 'cs'
    """

    unlist = r['unlist']
    mwdict = {}

    for i,v in d.iteritems():

        nsuc = [np.sum(x)/100 for x in [v, d[ctrlkey]]]
        #print('nsuc', nsuc)
        n = [len(x) for x in [v, d[ctrlkey]]]
        #print('n', n)
        
        pt = rsl.proptest(unlist(nsuc), unlist(n))

        mwdict[i] = {}
        if math.isnan(pt.rx('p.value')[0][0]):
            mwdict[i]['pval'] = 1
        else:
            mwdict[i]['pval'] = pt.rx('p.value')[0][0]
        mwdict[i]['n'] = len(v)
        mwdict[i]['control'] = ctrlkey

    return(mwdict)

def dictfishtest(d, ctrlkey='cs'):

    """Returns a dictionary in which the keys are the genotypes and the values are the results of the Mann-Whitney test as implemented in R.

    datadict: a dictionary with the keys as the genotypes and the values as the
    raw data
    ctrlkey: the name of the key for the dictionary entry that will serve as 
    the control genotype; default is 'cs'
    """

    unlist = r['unlist']
    mwdict = {}

    for i,v in d.iteritems():

        nsuc = [np.sum(x)/100 for x in [v, d[ctrlkey]]]
        #print('nsuc', nsuc)
        nfail = [len(x) - np.sum(x)/100 for x in [v, d[ctrlkey]]]
        #print('nfail', nfail)
        nsuc = unlist(nsuc)
        nfail = unlist(nfail)
        
        ft = rsl.fishertest(nsuc[0], nfail[0], nsuc[1], nfail[1])

        mwdict[i] = {}
        if math.isnan(ft.rx('p.value')[0][0]):
            mwdict[i]['pval'] = 1
        else:
            mwdict[i]['pval'] = ft.rx('p.value')[0][0]
        mwdict[i]['n'] = len(v)
        mwdict[i]['control'] = ctrlkey

    return(mwdict)


def mcpval(pvaldict, method='fdr', iskeyfile = 'True', keyfile='keylist'):

    """Returns a dictionary where the keys are genotypes and the values 
    include p-values that are corrected for multiple comparisons using the 
    p.adjust function in R.

    pvaldict = dictionary where the keys are genotypes and the values include 
    p-values derived from a statistical test; should be the output of a function like dictmw()
    method = method chosen for multiple correction using the p.adjust function 
    ('holm', 'hochberg', 'hommel', 'bonferroni', 'BH', 'BY', 'fdr', 'none')
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be used; default name is 
    'keylist'

    """

    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(pvaldict.keys())

    gens = []
    pvals = []
    ctrl = []
    newdict = {}

    for k in keylist:
        try:
            pvals.append(pvaldict[k]['pval'])
            gens.append(k)
            ctrl.append(pvaldict[k]['control'])
            newdict[k] = pvaldict[k]
        except KeyError:
            continue
     
    #for k in keylist:
        #assert pvals[gens.index(k)] == pvaldict[k]['pval']
    #print('pvals', pvals)
    #print('gens', gens)
    #print('ctrl', ctrl)
    if len(pvals) >= 2:
        try:
            pvals.pop(gens.index(ctrl[0]))
            print('pvals-noctrl', pvals)
            gens.remove(ctrl[0])

            adjpvals = list(rsl.padjust(pvals, method))
            print('adjpvals', adjpvals)
            newptuple = zip(gens, adjpvals)

            for t in newptuple:
                newdict[t[0]]['adjpval'] = t[1]
                newdict[t[0]]['adjpvaltest'] = method

            newdict[ctrl[0]]['adjpval'] = 'n/a'
            newdict[ctrl[0]]['adjpvaltest'] = 'n/a'
        except ValueError:
            pass

    return(newdict)


def createmwfile(fname):

    """Creates a file (specified in 'fname') that will list the results of the Mann-Whitney significance test as implemented in R.
    """

    with open(fname, 'w') as f:
        f.write('Mann-Whitney U Test corrected for Multiple Comparisons\n')

        f.write('Condition\tBehavior\tControl\tSigtest\tMultCompar\tp-value\t\
        Adj p-value\n')


def writemwfile(fname, pvaldict, kind):

    """Writes a file (specified in 'fname') listing the results of the Mann-Whitney significance test as implemented in R.

    pvaldict = dictionary where the keys are genotypes and the values include p-values derived from a statistical test; output of the mcpval function.
    kind = type of behavior - 'wing' (wing extension), 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    """

    for k, v in pvaldict.iteritems():
        with open(fname, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(k, kind, \
            v['control'], v['sigtest'][:15], v['adjpvaltest'], v['pval'], \
            v['adjpval']))


def createpptestfile(fname):

    """Creates a file (specified in 'fname') that will list the results of the Mann-Whitney significance test as implemented in R.
    """

    with open(fname, 'w') as f:
        f.write('Proportion test corrected for Multiple Comparisons\n')

        f.write('Condition\tBehavior\tControl\tMultCompar\tp-value\t\
        Adj p-value\n')


def writepptestfile(ofile, pvaldict, kind):
    """Input is a dictionary in which the keywords are genotypes or conditions and the values are a list in which an entry of "100" = success and an entry of "0" = failure (output of dictfreq)"""

    for k, v in pvaldict.iteritems():
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, \
            v['control'], v['adjpvaltest'], v['pval'], v['adjpval']))    
    


def plotqqplots(kind, fname, outputdir, ctrl='cs'):

    curdir = os.path.abspath('.')
    d = dictlat(kind, fname)

    qqplot = r['qqplot']
    qqnorm = r['qqnorm']
    unlist = r['unlist']
    png = r['png']
    devoff = r['dev.off']

    os.chdir(outputdir)
    for k in d.keys():
        kname = k.replace('/', '_')
        name1 = 'qqplot'+kname+'.png'
        png(file=name1)
        pl=qqplot(unlist(d[ctrl]), unlist(d[k]), xlab=ctrl, ylab=k, main="Q-Q Plot")
        devoff()

        name2 = 'qqnorm'+kname+'.png'
        png(file=name2)
        pl=qqnorm(unlist(d[k]), ylab=k, main="Q-Q Norm")
        devoff()
    os.chdir(curdir)


#### BELOW ARE FUNCTIONS FOR PLOTTING A 4-PANEL PUBLICATION-QUALITY FIGURE ####

def multiplot_1bar(kind, fname, ctrlkey, barwidth, ymin, ylabel, yaxisticks, 
subplotn, subplotl, keyfile='keylist', fontsz=9, stitlesz=10, lw=1):

    # ======== LOAD DATA =============
    if keyfile == 'no':
        keylist = sorted(d.keys())
    else:
        keylist = cmn.load_keys(keyfile)
    d = dictlat(kind, fname)
    mwd = dictmw(d, ctrlkey)
    adjpd = mcpval(mwd, 'fdr')

    vals = []
    conds = []
    pvals = []

    for k in keylist:
        vals.append(d[k])
        conds.append('{0}\nn={1}'.format(k, mwd[k]['n']))
        pvals.append(adjpd[k]['adjpval'])

    # ======== SET INITIAL FIGURE PROPERTIES =============
    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font to Arial and assigns font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/arial.ttf')
    fontv.set_size(fontsz)
    # Sets italicized font.
    fonti = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/ariali.ttf')
    fonti.set_size(fontsz)

    # Defines coordinates for each bar.
    barnum = len(keylist)
    lastbar = (1.5*barnum*barwidth)-barwidth # X-coordinate of last bar
    x_gen1 = np.linspace(0.5+0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 

    # Defines the axes.
    ax = plt.subplot(subplotn)

    # =========== PLOT DATA =======================

    #Plots the box plot.

    bp = plt.boxplot(vals, positions=x_list, sym='')
    pylab.setp(bp['boxes'], color='black')
    pylab.setp(bp['whiskers'], color='black', ls='-')
    pylab.setp(bp['medians'], color='black')

    # Sets the x- and y-axis limits.
    xlim = x_list[-1]+1.5*barwidth

    #print(kind)
    maxvals = [max(x) for x in vals]
    maxval = max(maxvals)
    #print('maxval', maxval)
    if kind == 'copsuc':
        ylim = 1.3*maxval
    elif kind == 'wing':
        ylim = 1.3*maxval
    else:
        ylim = 1.3*maxval
    ylim = cmn.myround(ylim)

    #xlim=barnum*barwidth+1.5*barwidth
    #xlim=barnum*barwidth+4*barwidth
    print('xlim', xlim)
    plt.axis( [0, xlim, ymin, ylim])


    # ========ADDS TICKS, LABELS and TITLES==========

    # Adds labels to the x-axis at the x-coordinates specified in x_list; labels are specified in the conds list.
    plt.xticks(x_list, conds, fontproperties=fonti, rotation=45)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=2, fontproperties=fontv, multialignment='center')

    # Add title
    if kind == 'wing':
        plt.title('Latency to\nwing extension', fontsize=stitlesz)

    if kind == 'copsuc':
        plt.title('Latency to\ncopulation', fontsize=stitlesz)

    if kind == 'copatt1':
        plt.title('Latency to first\ncopulation attempt', fontsize=stitlesz)

    # Add subplot label
    plt.text(-0.1, 1.1, subplotl, transform=ax.transAxes)



    # ========FORMATS THE PLOT==========

    # Removes borders
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)


    # ========FORMATS THE TICKS=========

    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax.get_xticklines():
        line.set_visible(False)

    # Formats the y ticks.
    plt.yticks(fontproperties=fontv)

    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(yaxisticks))


    # ========ADDS SIGNIFICANCE STARS============

    #print('pvals',pvals)

    p05i = [i for i, pval in enumerate(pvals) if pval <0.05 and pval >= 0.01]
    
    
    #print(p05i)
    for i in p05i:
        plt.text(x_list[i], 0.85*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    #print(p01i)
    for i in p01i:
        plt.text(x_list[i], 0.85*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    #print(p001i)
    for i in p001i:
        plt.text(x_list[i], 0.85*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)


def multiplot_1barf(kind, fname, ctrlkey, barwidth, keyfile, conf, ylabel, yaxisticks, ymin, 
ylim, subplotn, subplotl, fontsz, stitlesz, leglabels, lw=1):

    # ======== SET INITIAL FIGURE PROPERTIES =============
    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)
    # Sets italicized font.
    fonti = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/ariali.ttf')
    fonti.set_size(fontsz)

    # Defines the axes.
    ax = plt.subplot(subplotn)

    # ======== LOAD DATA =============
    keylist = cmn.load_keys(keyfile)
    d = dictfreq(kind, fname)
    db = dictbin(d, conf, label=kind)
    #ppd = dictpptest(d, ctrlkey)
    #adjppd = mcpval(ppd, 'fdr')
    fd = dictfishtest(d, ctrlkey=ctrlkey)
    adjppd = mcpval(fd, 'fdr')

    vals = []
    conds = []
    lowerci = []
    upperci = []
    nsuc = []
    n = []
    pvals = []

    # Appends data for the bar plot to appropriate lists.
    for k in keylist:
        vals.append(db[k]['prop'])
        conds.append('{0}\nn={1}'.format(k, db[k]['n']))
        nsuc.append(db[k]['nsuc'])
        n.append(db[k]['n'])
        lowerci.append(db[k]['prop']-db[k]['lowerci'])
        upperci.append(db[k]['upperci']-db[k]['prop'])
        pvals.append(adjppd[k]['adjpval'])
        #print(k)
        #print('graph prop', db[k]['prop'])
        #print('graph lowerci-calc', lowerci)
        #print('graph lowerci-raw', db[k]['lowerci'])
        


    # Defines coordinates for each bar.
    barnum = len(keylist)
    lastbar = (1.5*barnum*barwidth)-barwidth
    x_gen1 = np.linspace(0.5+0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 
                
    # =========== PLOT DATA =======================
    
    # Plots the bar plot for each kind of data.
    truebarw = 0.35*barwidth
    plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, 
    color='#d3d3d3', bottom=0, ecolor='k', capsize=0.5, linewidth=lw)
    #plt.bar(x_list, vals, width=truebarw, color='k', bottom=0, 
    #ecolor='k', capsize=0.5, linewidth=lw)


    # ======== ADDS TICKS, LABELS and TITLES==========

    # Sets the x- and y-axis limits.
    xlim = x_list[-1]+1.5*barwidth
    plt.xlim(0, xlim)
    plt.ylim(ymin, ylim)

    # Plots and formats xlabels.
    xlabel_list = [x for x in x_list]
    plt.xticks(xlabel_list, conds, rotation=45, fontproperties=fonti)

    # Formats the yticks.
    plt.yticks(fontproperties=fontv)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')

    # Add title
    if kind == 'wing':
        plt.title('% flies courting', fontsize=stitlesz)

    if kind == 'copsuc':
        plt.title('% flies copulating', fontsize=stitlesz)

    if kind == 'copatt1':
        plt.title('% flies attempting\ncopulation', fontsize=stitlesz)


    # Labels the subplot
    plt.text(-0.1, 1.1, subplotl, transform=ax.transAxes)


    # ======== FORMATS THE PLOT==========
    #Uncomment lines below to display without top and right borders.
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)

    # ======== FORMATS THE TICKS ==========
    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(yaxisticks))

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax.get_xticklines():
        line.set_visible(False)


    # ======== PLOT AND FORMAT LEGEND ==========
    ##Plots legend.
    #a1 = plt.legend(ncol=len(kindlist), loc='upper center', labelspacing=0.1, 
    #columnspacing=0.7, markerscale=0.5, fontsize=fontsz, handletextpad=0.3, borderpad=0)
    ##Removes border around the legend.
    #a1.draw_frame(False)
    
    
    # ========ADDS SIGNIFICANCE STARS============

    #print('pvals',pvals)

    p05i = [i for i, pval in enumerate(pvals) if pval <0.05 and pval >= 0.01]
    
    #print(p05i)
    for i in p05i:
        plt.text((x_list[i]+truebarw/2.), 0.9*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    #print(p01i)
    for i in p01i:
        plt.text((x_list[i]+truebarw/2.), 0.9*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    #print(p001i)
    for i in p001i:
        plt.text((x_list[i]+truebarw/2.), 0.9*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)


def multiplot_3bars(kindlist, fname, ctrlkey, keyfile, conf, ylabel, yaxisticks, ymin, 
ylim, colors, subplotn, subplotl, barwidth, fontsz, stitlesz, leglabels, lw=1):

    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)
    # Sets italicized font.
    fonti = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/ariali.ttf')
    fonti.set_size(fontsz)

    # Defines the axes.
    ax = plt.subplot(subplotn)

    # Load data.
    keylist = cmn.load_keys(keyfile)
    barnum = len(keylist)

    # Defines variables used in finding coordinates for each bar.
    lastbar = (barnum*len(kindlist)*barwidth)
    x_gen1 = np.linspace(1.5*barwidth, lastbar+barnum*barwidth, barnum).tolist()


    for i, kind in enumerate(kindlist):
        d = dictfreq(kind, fname)
        db = dictbin(d, conf, label=kind)
        #print('db', db)
        ppd = dictpptest(d, ctrlkey)
        adjppd = mcpval(ppd, 'fdr')

        
        vals = []
        conds = []
        lowerci = []
        upperci = []
        nsuc = []
        n = []
        pvals = []

        # Defines coordinates for each bar.
        x_list = [x + i for x in x_gen1]

        # Appends data for the bar plot to appropriate lists.
        for k in keylist:
            vals.append(db[k]['prop'])
            conds.append(k)
            nsuc.append(db[k]['nsuc'])
            n.append(db[k]['n'])
            lowerci.append(db[k]['prop']-db[k]['lowerci'])
            upperci.append(db[k]['upperci']-db[k]['prop'])
            pvals.append(adjppd[k]['adjpval'])

                

        # Plots the bar plot for each kind of data.
        truebarw = barwidth-(0.05*barwidth)
        #plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, 
        #color=colors[i], bottom=0, ecolor='k', capsize=0.5, linewidth=lw, 
        #label=leglabels[i])
        plt.bar(x_list, vals, width=truebarw, color=colors[i], bottom=0, 
        ecolor='k', capsize=0.5, linewidth=lw, label=leglabels[i])


    # ======== ADDS TICKS, LABELS and TITLES==========

    # Sets the x- and y-axis limits.
    plt.ylim(ymin, ylim)

    # Plots and formats xlabels.
    xlabel_list = [x for x in x_list]
    plt.xticks(xlabel_list, conds, rotation=45, fontproperties=fonti)

    # Formats the yticks.
    plt.yticks(fontproperties=fontv)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')

    # Adds the title.
    plt.title('% Flies displaying behavior', fontsize=stitlesz)

    # Labels the subplot
    plt.text(-0.1, 1.1, subplotl, transform=ax.transAxes)


    # ======== FORMATS THE PLOT==========
    #Uncomment lines below to display without top and right borders.
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)

    # ======== FORMATS THE TICKS ==========
    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(yaxisticks))

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax.get_xticklines():
        line.set_visible(False)


    # ======== PLOT AND FORMAT LEGEND ==========
    #Plots legend.
    a1 = plt.legend(ncol=len(kindlist), loc='upper center', labelspacing=0.1, 
    columnspacing=0.7, markerscale=0.5, fontsize=fontsz, handletextpad=0.3, borderpad=0)
    #Removes border around the legend.
    a1.draw_frame(False)
    
    
    # ========ADDS SIGNIFICANCE STARS============

    print('pvals',pvals)

    p05i = [i for i, pval in enumerate(pvals) if pval <0.05 and pval >= 0.01]
    
    print(p05i)
    for i in p05i:
        plt.text(x_list[i], 0.9*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    print(p01i)
    for i in p01i:
        plt.text(x_list[i], 0.9*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    print(p001i)
    for i in p001i:
        plt.text(x_list[i], 0.9*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)


def createinfolat(ofile):
    '''Creates a file with information on the latency graphs plotted in multiplot_1bar.'''
    with open(ofile, 'w') as f:
        f.write('Genotype\tBehavior\tmedian\tn\tAdj p-value\tCtrl\n')


def writeinfolat(ifile, ofile, kind, ctrlkey, keyfile, iskeyfile='False'):
    '''Writes into a file with information on the latency graphs plotted in multiplot_1bar.'''

    d = dictlat(kind, ifile)
    mwd = dictmw(d, ctrlkey)
    mcwd = mcpval(mwd)
    mx = []
    mi = []
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()

    for k in keylist:
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, \
            mwd[k]['median'], mwd[k]['n'], mcwd[k]['adjpval'], mcwd[k]['control']))
            mx.append(np.max(mwd[k]['n']))
            mi.append(np.min(mwd[k]['n']))

    with open(ofile, 'a') as f:
        f.write('Max n = {0}\n'.format(np.max(mx)))
        f.write('Min n = {0}\n'.format(np.min(mi)))


def createinfolatmean(ofile):
    
    with open(ofile, 'w') as f:
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
    'Mean latency (s)', 'Std Error (s)', '# pairs exhibiting behavior'))
    

def writeinfolatmean(ifile, ofile, kind, ctrlkey):
    
    d = dictlat(kind, ifile)
    mwd = dictmeans(d)
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()

    for k in keylist:

        if kind == 'wing':
            nk = 'wing extension'
        if kind == 'copsuc':
            nk = 'successful copulation'
        if kind == 'copatt1':
            nk = 'first attempted copulation'

        #print(mwd[k][0])
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4}\n'.format(k, nk, mwd[k][0], 
            mwd[k][2], mwd[k][3]))
    
   


def createinfoprop(ofile):
    '''Creates a file with information on the frequency graphs plotted in multiplot_1bar.'''
    with open(ofile, 'w') as f:
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format('Genotype', 'Behavior', \
        '# pairs exhibiting behavior', '# pairs tested', \
        '% exhibiting behavior', 'ci_lower', 'ci_upper' ))


def writeinfoprop(ifile, ofile, kind, keyfile, iskeyfile='false'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot_1bar.'''

    d = dictfreq(kind, ifile)
    bd = dictbin(d)
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = dictbin.iterkeys()

    mx = []
    mi = []
    for k in keylist:
        
        if kind == 'wing':
            nk = 'wing extension'
        if kind == 'copsuc':
            nk = 'successful copulation'
        if kind == 'copatt1':
            nk = 'first attempted copulation'
        
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4:.2%}\t{5}\t{6}\n'.format(k, kind, 
            bd[k]['nsuc'], bd[k]['n'], float(bd[k]['nsuc'])/float(bd[k]['n']),  
            bd[k]['lowerci'], bd[k]['upperci']))
            mx.append(np.max(bd[k]['n']))
            mi.append(np.min(bd[k]['n']))
            
        #print('text', 'kind', k)
        #print('text', 'lowerci', bd[k]['lowerci'])
        
        
    #with open(ofile, 'a') as f:
        #f.write('Max n = {0}\n'.format(np.max(mx)))
        #f.write('Min n = {0}\n'.format(np.min(mi)))

