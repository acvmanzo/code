
# Contains functions useful for analyzing aggression and courtship
# data from a csv file generated during manual scoring.


import os
import pylab
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import rpy2.robjects as robjects
import cmn.cmn as cmn
import libs.genplotlib as gpl
import libs.rstatslib as rsl
import rpy2.robjects as robjects

r = robjects.r

#### FUNCTIONS FOR CONSTRUCTING DATA DICTIONARIES FROM CSV FILES ####

### AGGRESSION ###

def agline2(line):
    """Generates dictionary with the values from line, with the parameters as 
    keywords.
    line is of the following format:
    Movie, Movie (Ryan's code), Offset (s), Well #, Aggressive Behavior 
    (min), (sec), (dur), (type), (comments), Escalation (min), (sec), (dur), 
    (type), (behaviors), (comments) 
    """
    
    vals = {}
    y = line.strip('\n').split(',')
    y.extend(y[0].strip('.MTS').split('_'))
    
    #print(y)
    
    x = ['movie', 'moviecode', 'offset', 'well', 'agmin', 'agsec', 'agdur', 
    'agtype', 'agcomm', 'escmin', 'escsec', 'escdur', 'esctype', 'escbeh', 
    'esccomm', 'gen', 'date', 'assay', 'fps', 'flyid', 'side', 'moviepart']
    
    z = zip(x, y)

    for item in z:
        vals[item[0]] = item[1]

    return(vals)


def agfreqcmd(kind, blist, genlist):
    
    #print('blistcount', blist.count('wt'))
    
    if kind == 'wingthreat':
        if blist.count('wt') > 0 or blist.count('xwt') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
    
    if kind == 'charge':
        if blist.count('c') > 0 or blist.count('o') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
    
    if kind == 'anyag':
        if blist.count('c') > 0 or \
        blist.count('o') > 0 or \
        blist.count('p') > 0 or \
        blist.count('l') > 0 or \
        blist.count('ch') > 0 or \
        blist.count('g') > 0 or \
        blist.count('h') > 0 or \
        blist.count('d') > 0 or \
        blist.count('m') > 0 or \
        blist.count('wr') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
        
    
    if kind == 'escd':
        if blist.count('d') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
    
    if kind == 'escm':
        if blist.count('m') > 0:
            genlist.append(100)
        else:
            genlist.append(0)


def dictagfreq2(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    are a list in which an entry of "100" = success and an entry of "0" = failure.

    kind = 'wingthreat' (wing threat), 
    'charge' (wing threat + charge or orientation),
    'anyag' (wing threat + charge, orientation, pushing, lunge, chase, grab, 
    hold, dominant or mutual escalation)
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with sorted data
    """
    
    #x = ['movie', 'moviecode', 'offset', 'well', 'agmin', 'agsec', 'agdur', 
    #'agtype', 'agcomm', 'escmin', 'escsec', 'escdur', 'esctype', 'escbeh', 
    #'esccomm', 'gen', 'date', 'assay', 'fps', 'flyid', 'side', 'moviepart']

    d = {}
    y = '1'
    b = []
    
    with open(fname) as f:
        for l in f:
            adict = agline2(l)
            #print(l)
            
            if adict['well'] != y:
                agfreqcmd(kind, b, d[gen])
                b = []
            
            if adict['agtype'] != '-':
                b.append(adict['agtype'])

            if adict['esctype'] != '':
                b.append(adict['esctype'])
            
            gen = adict['gen']   
            if gen not in d:
                d[gen] = [] 
                
            #print('b', b)
            #print('well', adict['well'])
            #print('gen', gen, 'd', d)
                     
            y = adict['well']
    
    agfreqcmd(kind, b, d[gen])
    
    return(d)


def agdurcmd(kind, blist, durlist, genlist):
    
    #print('blistcount', blist.count('wt'))
    blist, durlist = map(np.array, [blist, durlist])
    #print('new')
    #print('durlist', durlist)
    #print('blist', blist)
    durlist = durlist.astype(int)
    
    if len(durlist) > 0:
    
        #print('durlist', len(durlist), durlist)
        
        if kind == 'charge':
            val = np.sum(durlist[blist=='c'])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = np.sum(durlist[ind])
            #print(val)
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = np.sum(durlist[ind])
            #print(val)
            if val > 0:
                genlist.append(val)

        if kind =='escd':
            val = np.sum(durlist[blist=='d'])
            if val > 0:
                genlist.append(val)        
        if kind =='escm':
            val = np.sum(durlist[blist=='m'])
            if val > 0:
                genlist.append(val)   
                         

def dictagdur2(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    indicate the duration over which each fly exhibits the behavior.

    kind = 'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data
    """

    #x = ['movie', 'moviecode', 'offset', 'well', 'agmin', 'agsec', 'agdur', 
    #'agtype', 'agcomm', 'escmin', 'escsec', 'escdur', 'esctype', 'escbeh', 
    #'esccomm', 'gen', 'date', 'assay', 'fps', 'flyid', 'side', 'moviepart']

    d = {}
    y = '1'
    b = []
    dur = []
    
    with open(fname) as f:
        for l in f:
            #print(l)
            adict = agline2(l)
            
            if adict['well'] != y:
                if len(dur) > 0:
                    agdurcmd(kind, b, dur, d[gen])
                b = []
                dur = []
            
            if adict['agtype'] != '-' and adict['agtype'] != 'x' and \
            adict['agdur'] != '':
                b.append(adict['agtype'])
                dur.append(adict['agdur'])
            
            if adict['esctype'] != '' and adict['escdur'] != '':
                b.append(adict['esctype'])
                dur.append(adict['escdur'])

            gen = adict['gen']
            #print(gen)
            if gen not in d:
                d[gen] = []
                
            y = adict['well']
    
    agdurcmd(kind, b, dur, d[gen])

    return(d)


### COURTSHIP ###

def cline2(line):
    """Generates dictionary with the values from line, with the parameters as 
    keywords.

    fname is of the following format:
    Movie, Movie (Ryan's code),  Genotype, Offset (s), Well #, Courtship 
    Behavior (min), (sec), (dur), (type), (comments)
    """

    cvals = {}
    x = ['movie', 'moviecode', 'gen', 'offset', 'well', 'cmin', 'csec', 
    'cdur', 'ctype', 'ccomm', 'gens', 'date', 'assay', 'fps', 'flyid', 'side']
    y = line.strip('\n').split(',')
    y.extend(y[0].strip('.MTS').split('_'))
    
    z = zip(x, y)

    for item in z:
        cvals[item[0]] = item[1]

    return(cvals)


def dictclat(kind, fname):
      
    if kind == 'copatt1':
        kind = 'ca'
    if kind == 'copsuc':
        kind = 'cs'
    
    d = {}
    
    with open(fname) as f:
        f.next()
        f.next()
        for l in f:
            #print(l)
            cd = cline2(l)
            gen = cd['gen']
            #print(gen)
            if gen not in d:
                d[gen] = []
                
            if cd['ctype'] == kind and cd['cmin'] != 'x' and cd['cmin'] != '-':
                offset, cmin, csec = map(int, [cd['offset'], cd['cmin'], \
                cd['csec']])
                d[gen].append(cmn.convtosec(cmin, csec)-offset)
    return(d)


def dictcprop(kind, fname):

    if kind == 'copatt1':
        kind = 'ca'
    if kind == 'copsuc':
        kind = 'cs'

    d = {}
    
    with open(fname) as f:
        f.next()
        f.next()
        for l in f:
            #print(l)
            cd = cline2(l)
            gen = cd['gen']
            #print(gen)
            if gen not in d:
                d[gen] = []
                
            if cd['ctype'] == kind and cd['cmin'] != 'x' and cd['cmin'] != '-':
                d[gen].append(100)
            if cd['ctype'] == kind and cd['cmin'] == 'x':
                d[gen].append(0)
    return(d)
    

#### FUNCTIONS FOR CONSTRUCTING DICTIONARIES WITH RESULTS OF STATISTICAL 
#TESTS####


def dictbin(dict, conf, methods='wilson', label='data'):
    """Generates a new dictionary with binomical confidence intervals from 
    frequency data.
    Input:
    dict = output of function dictfreq
    conf = confidence level for confidence intervals
    methods = method for constructing conf. interval
    label = parameter being measured

    Output:
    A dictionary where the keywords are conditions or genotypes and the values 
    are as follows:
    nsuc = number of successes
    n = number of trials
    prop = nsuc/n
    method = method for constructing binomical confidence intervals 
    (see documentation for rstatslib.binomici_w)
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



def dictmw(d, ctrlkey='cs', test='exact'):

    """Returns a dictionary in which the keys are the genotypes and the values 
    are the results of the Mann-Whitney test as implemented in R.

    datadict: a dictionary with the keys as the genotypes and the values as 
    the raw data
    ctrlkey: the name of the key for the dictionary entry that will serve as 
    the control genotype; default is 'cs'
    """

    r = robjects.r
    unlist = r['unlist']
    mwdict = {}

    for i,v in d.iteritems():
        if not v:
            #mwdict[i] = []
            continue
            
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


def dictttest(d, ctrlkey='cs'):

    """Returns a dictionary in which the keys are the genotypes and the values 
    are the results of the Welch Two Sample t-test as implemented in R.

    datadict: a dictionary with the keys as the genotypes and the values as 
    the raw data
    ctrlkey: the name of the key for the dictionary entry that will serve as 
    the control genotype; default is 'cs'
    """

    r = robjects.r
    unlist = r['unlist']
    mwdict = {}

    for i,v in d.iteritems():
        #print(v)
        if len(v) < 2:
            continue
            
        v, ctrl = map(unlist, [v, d[ctrlkey]])

        mw = rsl.ttest(v, ctrl)

        mwdict[i] = {}
        mwdict[i]['pval'] = mw.rx('p.value')[0][0]
        mwdict[i]['sigtest'] = 'Welchs t-test'
        mwdict[i]['n'] = len(v)
        mwdict[i]['mean'] = np.mean(v).tolist()
        mwdict[i]['control'] = ctrlkey
        mwdict[i]['stdev'] = np.std(v).tolist()
        mwdict[i]['sterr'] = np.std(v).tolist()/np.sqrt(len(v))
    
    return(mwdict)    


def dictfishtest(d, ctrlkey='cs'):
    """Returns a dictionary with p-values of resulting from a proportion test
    to determine whether each experimental condition differs from the control
    condition. The proportion test used is Fisher's Exact Test implemented as
    R's fisher.test.
       
    datadict: a dictionary in which the keywords are genotypes 
    or conditions and the values are a list in which an entry of 
    "100" = success and an entry of "0" = failure (output of dictfreq)
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
        mwdict[i]['sigtest'] = 'Fisher\'s exact test'

    return(mwdict)


def mcpval(pvaldict, method='fdr', iskeyfile = 'True', keyfile='keylist'):

    """Returns a dictionary where the keys are genotypes and the values 
    are p-values that are corrected for multiple comparisons using the 
    p.adjust function in R.

    pvaldict = dictionary where the keys are genotypes and the values include 
    p-values derived from a statistical test; should be the output of a 
    function like dictmw(), dictpptest() or dictfishtest()
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
            #print('pvals-noctrl', pvals)
            gens.remove(ctrl[0])

            adjpvals = list(rsl.padjust(pvals, method))
            #print('adjpvals', adjpvals)
            newptuple = zip(gens, adjpvals)

            for t in newptuple:
                newdict[t[0]]['adjpval'] = t[1]
                newdict[t[0]]['adjpvaltest'] = method

            newdict[ctrl[0]]['adjpval'] = 'n/a'
            newdict[ctrl[0]]['adjpvaltest'] = 'n/a'
        except ValueError:
            pass

    return(newdict)




#### FUNCTIONS FOR WRITING RESULTS OF DATA ANALYSIS TO TEXT FILES ####


def createshapfile(fname):

    """Creates a file (specified in 'fname') that will list the results of the
    Shapiro-Wilk test of normality as implemented in R. One line is written 
    with the results from a set of values drawn from a normal distribution.
    """

    r = robjects.r
    normsample = r['rnorm'](50)
    x = rsl.shapirowilk(normsample)
    with open(fname, 'w') as f:
        f.write('Shapiro-Wilk test results\n')
        f.write('Condition\tBehavior\tp-value\n')
        f.write('{0}\t{1}\t{2:.4g}\n'.format('normsample', 'normsample', x[1][0]))


def writeshapfile(fname, datadict, kind):

    """Writes a file that lists the results of the Shapiro-Wilk test of 
    normality as implemented in R.

    fname: name of the output file
    datadict: a dictionary with the keys as genotypes and the values as the 
    raw data,
    kind: type of behavior - 'wing' (wing extension), 'copatt1' (first 
    copulation attempt), 'copsuc' (successful copulation)
    """

    r = robjects.r
    unlist = r['unlist']

    for n, v in datadict.iteritems():
        #print('n', n)
        #print('v', v)
        if len(v) < 3:
            continue
        if v == np.tile(v[0], len(v)).tolist():
            continue
        v = unlist(v)
        x = rsl.shapirowilk(v)
        with open(fname, 'a') as f:
            f.write('{0}\t{1}\t{2:.4g}\n'.format(n, kind, x[1][0]))


def createstatfile(fname, test):

    """Creates a file (specified in 'fname') that will list the results of 
    the selected significance test as implemented in R.
    """

    with open(fname, 'w') as f:
        f.write('{0} corrected for Multiple Comparisons\n'.format(test))
        f.write('Condition\tBehavior\tControl\tSigtest\tMultCompar\tp-value\t\
        Adj p-value\n')


def writestatfile(fname, pvaldict, kind):

    """Writes a file (specified in 'fname') listing the results of the 
    selected significance test as implemented in R.

    fname = file to write to
    pvaldict = dictionary where the keys are genotypes and the values include 
    p-values derived from a statistical test; output of the mcpval function.
    kind = type of behavior
    """

    for k, v in pvaldict.iteritems():
        #print(k)
        with open(fname, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(k, kind, \
            v['control'], v['sigtest'][:15], v['adjpvaltest'], v['pval'], \
            v['adjpval']))


def createinfolat(ofile):
    '''Creates a file with information on the latency graphs plotted in 
    multiplot_1bar.'''
    with open(ofile, 'w') as f:
        f.write('Genotype\tBehavior\tMedian latency (s)\tn\n')


def writeinfolat(ofile, d, kind, ctrlkey, measure, iskeyfile='True', 
keyfile='keylist'):
    """Writes into a file with information on the latency graphs plotted in 
    multiplot_1bar.
    
    ifile = file with data to be analyzed
    ofile = file to write to
    kind = type of behavior being analyzed
    ctrlkey = the dictionary key that will serve as the control genotype
    keyfile = file listing the genotypes (or keys) to be compared
    iskeyfile = "True" or "False"; whether the keyfile exists; default is 
    "False"
    """

   
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()

    if measure == 'median':
        mwd = dictmw(d, ctrlkey)
        for k in keylist:
            with open(ofile, 'a') as f:
                f.write('{0}\t{1}\t{2}\t{3}\n'.format(k, kind, mwd[k]['median'],\
                mwd[k]['n']))

    if measure == 'mean':
        md = dictttest(d, ctrlkey)
        for k in keylist:
            with open(ofile, 'a') as f:
                f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, \
                md[k]['mean'], md[k]['stdev'], md[k]['sterr'], md[k]['n']))


def createinfodur(fname, measure):
    
    if measure == 'mean':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
            'Mean Duration (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

    if measure == 'median':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\n'.format('Genotype', 'Behavior', \
            'Median Duration (s)', '# pairs exhibiting behavior'))


def writeinfodur(ofile, d, kind, measure, iskeyfile='True', 
keyfile='keylist'):
    '''measure = mean or median'''
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()
    
    if measure == 'mean':
        md = dictttest(d)
        for k in keylist:
            try:
                with open(ofile, 'a') as f:
                    f.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4}\n'.format(k, kind, 
                    md[k]['mean'], md[k]['sterr'], md[k]['n']))
            except KeyError:
                continue
                
    if measure == 'median':
        md = dictmw(d)
        for k in keylist:
            try:
                with open(ofile, 'a') as f:
                    f.write('{0}\t{1}\t{2:.2f}\t{3}\n'.format(k, kind, 
                    md[k]['median'], md[k]['n']))  
            except KeyError:
                continue


def createinfoprop(ofile):
    '''Creates a file with information on the frequency graphs plotted with
    'multiplot_1barf'.
    '''
    with open(ofile, 'w') as f:
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format('Genotype', 'Behavior', \
        '# pairs exhibiting behavior', '# pairs tested', \
        '% exhibiting behavior', 'ci_lower', 'ci_upper' ))


def writeinfoprop(ofile, d, binconf, kind, iskeyfile='True', keyfile='keylist'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot_1bar.
    d = dictionary with proportion data
    '''

    bd = dictbin(d, binconf)
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = bd.iterkeys()

    mx = []
    mi = []
    for k in keylist:
        if kind == 'flare':
            nk = 'flare or >'
        if kind == 'charge':
            nk = 'any aggression'
        if kind == 'escd':
            nk = 'dominant escalation'
        if kind == 'escm':
            nk = 'mutual escalation'
        if kind == 'we':
            nk = 'wing extension'
        if kind == 'copsuc':
            nk = 'successful copulation'
        if kind == 'copatt1':
            nk = 'first attempted copulation'
        
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4:.2%}\t{5}\t{6}\n'.format(k, kind, 
            bd[k]['nsuc'], bd[k]['n'], float(bd[k]['nsuc'])/float(bd[k]['n']),  
            bd[k]['lowerci'], bd[k]['upperci']))
            #mx.append(np.max(v['n']))
            #mi.append(np.min(v['n']))
    #with open(ofile, 'a') as f:
        #f.write('Max n = {0}\n'.format(np.max(mx)))
        #f.write('Min n = {0}\n'.format(np.min(mi)))



#### FUNCTIONS FOR PLOTTING FIGURES ###$

def plotlatbw(kind, d, iskeyfile = 'true', type='bw'):
    '''Plots a box and whisker plot of the latency data.'''

    md = cl.dictmeans(d)

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = 'Latency (s)'
    ftitle = plottitlelat(kind)
    
    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large')
    if kind == 'we':
        plt.ylim(0, 150)


def plotfreq(kind, d, iskeyfile = 'true', keyfile='keylist', type='b'):
    """Generates a bar plot of the frequency of each type of behavior for 
    each genotype.

    kind = type of behavior
    d: dictionary of frequencies, generated from dictagfreq2()
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be plotted; default name is 'keylist'
    type: type of plot; default is 'b' which is a bar plot
    """

    md = cl.dictmeans(d)

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = '%'

    ftitle = plottitleprop(kind)

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large', err='none', figw=6, figh=4)
    if kind == 'escd' or kind == 'escm':
        plt.ylim(0, 30)
    else:
        plt.ylim(0, 110)


def plotnum(kind, d, iskeyfile='True', keyfile='keylist', type='b'):
    """Generates a bar plot of the mean number of times each behavior occurs 
    for each genotype.
    
    kind = 'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be plotted; default name is 'keylist'
    type: type of plot; default is 'b' which is a bar plot
    """
    md = cl.dictmeans(d)

    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = 'Avg num'
    
    ftitle = 'Mean number of instances observed'

    if kind == 'charge':
        ftitle = 'Mean number of charges observed'

    if kind == 'escd':
        ftitle = 'Mean number of bouts of dominant escalation'
    
    if kind == 'escm':
        ftitle = 'Mean number of bouts of mutual escalation'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large', err='none', figw=10, figh=8)
    
    plt.ylim(0)
    

def plotdur(kind, d, iskeyfile='True', keyfile='keylist', type='b'):
    """Generates a bar plot of the mean number of times each behavior occurs 
    for each genotype.
    
    kind = 'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    iskeyfile: specifies whether a keylist file exists; default is 'true'
    keyfile: file with a list of the genotypes to be plotted; default name is 'keylist'
    type: type of plot; default is 'b' which is a bar plot
    """
    md = cl.dictmeans(d)

    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = 'Seconds'
    ftitle = plottitledur(kind)

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large', err='none', figw=10, figh=8)
    
    plt.ylim(0)


#### FUNCTIONS FOR PLOTTING A PUBLICATION-QUALITY FIGURE ####

def plottitle(metric, kind):
    
    if metric == 'aglatmed' or metric == 'clatmed' or metric == 'clatmean':
        if kind == 'flare':
            t = 'Latency to\nflared wings'
        if kind == 'charge':
            t = 'Latency to\ncharging'
        if kind == 'anyag':
            t = 'Latency to\naggression'
        if kind == 'escd':
            t = 'Latency to\ndominant escalation'
        if kind == 'escm':
            t = 'Latency to\nmutual escalation'
        if kind == 'we':
            t = 'Latency to\nwing extension'
        if kind == 'copsuc':
            t = 'Latency to\ncopulation'
        if kind == 'copatt1':
            t = 'Latency to\n1st copulation attempt'
    
    if metric == 'aglatmed' or metric == 'agdurmean':
        if kind == 'wingthreat':
            t = 'Wing threat duration'
        if kind == 'charge':
            t = 'Charge duration'
        if kind == 'anyag':
            t = 'Fighting index'
        if kind == 'escd':
            t = 'Duration of\ndominant escalation'
        if kind == 'escm':
            t = 'Duration of\nmutual escalation'
            
    if metric == 'agprop' or metric == 'cprop':
        if kind == 'wingthreat':
            t = '% pairs with\nwingthreat'
        if kind == 'charge':
            t = '% pairs charging'
        if kind == 'anyag':
            t = '% pairs fighting'
        if kind == 'escd':
            t = '% pairs with\ndominant escalation'
        if kind == 'escm':
            t = '% pairs with\nmutual escalation'
        if kind == 'we':
            t = '% flies displaying\nwing extension'
        if kind == 'copsuc':
            t = '% flies copulating'
        if kind == 'copatt1':
            t = '% flies attempting\ncopulation'
            
    return(t)



def loadplotdata(metric, kind, fname, ctrlkey, binconf, keyfile):
    # Load data for use in fancy multiplots.
    
    # For all plots.
    vals = []
    conds = []
    pvals = []
    
    # For mean plots.
    n = []
    stdev = []
    sterr = []
    
    # For frequency plots.
    lowerci = []
    upperci = []
    nsuc = []
    
    if keyfile == 'no':
        keylist = sorted(d.keys())
    else:
        keylist = cmn.load_keys(keyfile)
    
    # Define dictionaries.
    if metric == 'aglatmed':
        d = dictaglat(kind, fname)
        mwd = dictmw(d, ctrlkey)
        adjpd = mcpval(mwd, 'fdr', 'True', keyfile)
    
    if metric == 'aglatmed':
        d = dictagdur2(kind, fname)
        mwd = dictmw(d, ctrlkey)
        adjpd = mcpval(mwd, 'fdr', 'True', keyfile)
    
    if metric == 'agdurmean':
        d = dictagdur2(kind, fname)
        md = dictttest(d, ctrlkey)
        adjpd = mcpval(md, 'fdr', 'True', keyfile)
    
    if metric == 'agprop':
        d = dictagfreq2(kind, fname)
        db = dictbin(d, binconf, label=kind)
        fd = dictfishtest(d, ctrlkey=ctrlkey)
        adjppd = mcpval(fd, 'fdr', 'True', keyfile)

    if metric == 'clatmed':
        d = dictclat(kind, fname)
        mwd = dictmw(d, ctrlkey)
        adjpd = mcpval(mwd, 'fdr', 'True', keyfile)
    
    if metric == 'clatmean':
        d = dictclat(kind, fname)
        md = dictttest(d, ctrlkey)
        adjpd = mcpval(md, 'fdr', 'True', keyfile)
        
    if metric == 'cprop':
        d = dictcprop(kind, fname)
        db = dictbin(d, binconf, label=kind)
        fd = dictfishtest(d, ctrlkey=ctrlkey)
        adjppd = mcpval(fd, 'fdr')
        
        
    # Generate coordinate and pvalue lists.
    
    if metric == 'aglatmed' or metric == 'aglatmed' or metric == 'clatmed':
        for k in keylist:
            if not d[k]:
                continue
            vals.append(d[k])
            conds.append('{0}; n={1}'.format(k, mwd[k]['n']))
            try:
                pvals.append(adjpd[k]['adjpval'])
            except KeyError:
                continue
    
    if metric == 'agdurmean' or metric == 'clatmean':
        for k in keylist:
            if not d[k]:
                continue
            try:
                vals.append(md[k]['mean'])
                #conds.append('{0}\nn={1}'.format(k, mwd[k]['n']))
                conds.append('{0}; n={1}'.format(k, md[k]['n']))
                n.append(md[k]['n'])
                stdev.append(md[k]['stdev'])
                sterr.append(md[k]['sterr'])
                pvals.append(adjpd[k]['adjpval'])
            except KeyError:
                continue

    if metric == 'agprop' or metric == 'cprop':
        for k in keylist:
            vals.append(db[k]['prop'])
            #conds.append('{0}\nn={1}'.format(k, db[k]['n']))
            conds.append('{0}; n={1}'.format(k, db[k]['n']))
            nsuc.append(db[k]['nsuc'])
            n.append(db[k]['n'])
            lowerci.append(db[k]['prop']-db[k]['lowerci'])
            upperci.append(db[k]['upperci']-db[k]['prop'])
            pvals.append(adjppd[k]['adjpval'])
    
    return(vals, conds, pvals, n, stdev, sterr, lowerci, upperci, nsuc)  


def plotbdata(metric, vals, x_list, sterr, truebarw, lw, lowerci, upperci):

    if metric == 'aglatmed' or metric == 'aglatmed' or metric == 'clatmed':
    #Plots the box and whisker plot.
        bp = plt.boxplot(vals, positions=x_list, sym='')
        pylab.setp(bp['boxes'], color='black')
        pylab.setp(bp['whiskers'], color='black', ls='-')
        pylab.setp(bp['medians'], color='black')
    
    if metric == 'agdurmean' or metric == 'clatmean':
    # Plots a bar plot displaying means.
        bp = plt.bar(x_list, vals, yerr=sterr, width=truebarw, color='#d3d3d3', \
        bottom=0, ecolor='k', capsize=0.5, linewidth=lw)    
    
    if metric == 'agprop' or metric == 'cprop':
    # Plots a bar plot displaying proportions.
        plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, 
        color='#d3d3d3', bottom=0, ecolor='k', capsize=0.5, linewidth=lw)



def multiplot(metric, kind, fname, ctrlkey, barwidth, ymin, ylim, ylabel, 
yaxisticks, subplotn, subplotl, binconf, keyfile='keylist', fontsz=9, 
stitlesz=10, lw=1, starpos=0.75):
    

    # ======== LOAD DATA =============

    vals, conds, pvals, n, stdev, sterr, lowerci, upperci, nsuc = \
    loadplotdata(metric, kind, fname, ctrlkey, binconf, keyfile)

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
    barnum = len(vals)
    lastbar = (1.5*barnum*barwidth)-barwidth # X-coordinate of last bar
    x_gen1 = np.linspace(0.5+0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 

    # Set width of bars.
    truebarw = 0.35*barwidth

    # Defines the axes.
    ax = plt.subplot(subplotn)
    

    # =========== PLOT DATA =======================
    
    plotbdata(metric, vals, x_list, sterr, truebarw, lw, lowerci, upperci)
    
    
    # ======== ADDS TICKS, LABELS and TITLES==========
    # Sets the x- and y-axis limits.
    
    xlim = x_list[-1]+1.5*barwidth
    plt.axis( [0, xlim, ymin, ylim])
    
    # Plots and formats xlabels.
    plt.xticks(x_list, conds, rotation=45, fontproperties=fonti)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')
    

    # Add title
    t = plottitle(metric, kind)
    plt.title(t, fontsize=stitlesz)
    
    # Labels the subplot
    plt.text(-0.2, 1.0, subplotl, transform=ax.transAxes)
    
    
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
        plt.text(x_list[i], starpos*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    #print(p01i)
    for i in p01i:
        plt.text(x_list[i], starpos*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    #print(p001i)
    for i in p001i:
        plt.text(x_list[i], starpos*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)
            
