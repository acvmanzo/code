def agfreqcmd_old(kind, blist, genlist):
    '''Helper function used in dictagfreq2() that appends values to a list depending on whether a specific behavior has occurred.

    Input:
    kind = kind of behavior
    blist = list of behaviors
    genlist = list of occurrences of each behavior; if a behavior has occurred, genlist is extended
    '''
    
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
def agdurcmd_old(kind, blist, durlist, genlist):
    
    blist, durlist = map(np.array, [blist, durlist])
    durlist = durlist.astype(int)
    
    if len(durlist) > 0:
    
        
        if kind == 'charge':
            val = np.sum(durlist[blist=='c'])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)

        if kind == 'chase':
            ind = (blist=='ch')
            val = np.sum(durlist[ind])
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

def agnumcmd_old(kind, blist, genlist):
    
    blist = np.array(blist)
    
    if len(blist) > 0:    
        
        if kind == 'charge':
            ind = (blist=='c')+(blist=='o')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind == 'chargeonly':
            ind = (blist=='c')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind == 'chase':
            ind = (blist=='ch')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='escd':
            val = len(blist[blist=='d'])
            if val > 0:
                genlist.append(val)        
        if kind =='escm':
            val = len(blist[blist=='m'])
            if val > 0:
                genlist.append(val)   
                         

# Contains functions useful for analyzing aggression and courtship
# data from a csv file generated during manual scoring.

#General information:

#Behavior code as listed in data:
#'boxing': 'b',
#'charge': 'c',
#'chase': 'ch',
#'chasing': 'ch',
#'fencing': 'f',
#'grab': 'g',
#'lunge': 'l', 
#'lunging': 'l',
#'hold': 'h',
#'push': 'p',
#'singing': 'other',
#'tumble': 't',
#'wt': 'wt',
#'wing threat': 'wt',
#'wrestling': 'w'


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
    y = line.strip('\n').split(',')[:14]
    movieparse = y[0].strip('.MTS').split('_')
    if len(movieparse) == 5: 
        movieparse.insert(3, 'PF24')
    y.extend(movieparse)
    
    
    x = ['movie', 'moviecode', 'offset', 'well', 'agmin', 'agsec', 'agdur', 
    'agtype', 'agcomm', 'escmin', 'escsec', 'escdur', 'esctype', 'escbeh', 'gen', 'date', 'assay', 'fps', 'flyid', 'side', 'moviepart']
    
    z = zip(x, y)

    for item in z:
        vals[item[0]] = item[1]

    return(vals)


def agfreqcmd(kind, blist, genlist):
    '''Helper function used in dictagfreq2() that appends values to a list depending on whether a specific behavior has occurred.

    Input:
    kind = kind of behavior
    blist = list of behaviors
    genlist = list of occurrences of each behavior; if a behavior has occurred, genlist is extended
    '''
    
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
                
                     
            y = adict['well']
    
    agfreqcmd(kind, b, d[gen])
    
    return(d)



def agdurcmd(kind, blist, durlist, genlist):
    
    blist, durlist = map(np.array, [blist, durlist])
    durlist = durlist.astype(int)
    
    if len(durlist) > 0:
    
        
        if kind == 'charge':
            val = np.sum(durlist[blist=='c'])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)

        if kind == 'chase':
            ind = (blist=='ch')
            val = np.sum(durlist[ind])
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


def agnumcmd(kind, blist, genlist):
    
    blist = np.array(blist)
    
    if len(blist) > 0:    
        
        if kind == 'charge':
            ind = (blist=='c')+(blist=='o')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind == 'chargeonly':
            ind = (blist=='c')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind == 'chase':
            ind = (blist=='ch')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='escd':
            val = len(blist[blist=='d'])
            if val > 0:
                genlist.append(val)        
        if kind =='escm':
            val = len(blist[blist=='m'])
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
            if gen not in d:
                d[gen] = []
                
            y = adict['well']
    
    agdurcmd(kind, b, dur, d[gen])

    return(d)


def dictagnum(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    indicate the number of times each fly exhibits the behavior.

    kind = 'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data
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
            
            if adict['well'] != y:
                if len(b) > 0:
                    agnumcmd(kind, b, d[gen])
                b = []
            
            if adict['agtype'] != '-' and adict['agtype'] != 'x':
                b.append(adict['agtype'])
            
            if adict['esctype'] != '' and adict['escdur'] != '':
                b.append(adict['esctype'])

            gen = adict['gen']
            if gen not in d:
                d[gen] = []
                
            y = adict['well']
    
    agnumcmd(kind, b, d[gen])
    print d
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
            cd = cline2(l)
            gen = cd['gen']
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
            cd = cline2(l)
            gen = cd['gen']
            if gen not in d:
                d[gen] = []
                
            if cd['ctype'] == kind and cd['cmin'] != 'x' and cd['cmin'] != '-':
                d[gen].append(100)
            if cd['ctype'] == kind and cd['cmin'] == 'x':
                d[gen].append(0)
    return(d)
    

#### FUNCTIONS FOR CONSTRUCTING DICTIONARIES WITH RESULTS OF STATISTICAL 
#TESTS####


def dictbin(idict, conf, methods='wilson', label='data'):
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

    for condition, value in idict.iteritems():

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
        mean_dict[condition]['upperci'] = z.rx('upper')[0][0]*100
        mean_dict[condition]['conf'] = conf
    return(mean_dict)



def dictmw(d, ctrlkey, test='exact'):

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
            print 'No values for condition', i
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


def dictttest(d, ctrlkey):


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
        if len(v) < 2:
            continue
        if i == ctrlkey:
            continue
            
        v, ctrl = map(unlist, [v, d[ctrlkey]])

        try:
            mw = rsl.ttest(v, ctrl)
            mwdict[i]['pval'] = mw.rx('p.value')[0][0]
        except:
            mw = []

        mwdict[i] = {}
        mwdict[i]['sigtest'] = 'Welchs t-test'
        mwdict[i]['n'] = len(v)
        mwdict[i]['mean'] = np.mean(v).tolist()
        mwdict[i]['control'] = ctrlkey
        mwdict[i]['stdev'] = np.std(v).tolist()
        mwdict[i]['sterr'] = np.std(v).tolist()/np.sqrt(len(v))

        mw = rsl.ttest(v, ctrl)
        mwdict[i]['pval'] = mw.rx('p.value')[0][0]
    return(mwdict)    


def dictfishtest(d, ctrlkey):
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
        nfail = [len(x) - np.sum(x)/100 for x in [v, d[ctrlkey]]]
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
            print 'KeyError!', k
            continue
     
    #for k in keylist:
        #assert pvals[gens.index(k)] == pvaldict[k]['pval']
    if len(pvals) >= 2:
        try:
            pvals.pop(gens.index(ctrl[0]))
            gens.remove(ctrl[0])

            adjpvals = list(rsl.padjust(pvals, method))
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
        with open(fname, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(k, kind, \
            v['control'], v['sigtest'][:15], v['adjpvaltest'], v['pval'], \
            v['adjpval']))


def createinfolat(ofile):
    '''Creates a file with information on the latency graphs plotted in 
    multiplot.'''
    with open(ofile, 'w') as f:
        f.write('Genotype\tBehavior\tMedian latency (s)\tn\n')

def createinfolatmean(ofile):
    '''Creates a file with information on the latency graphs plotted in 
    multiplot.'''
    with open(ofile, 'w') as f:
        f.write('Genotype\tBehavior\tMean\tStdev\tSterr\tn\n')


def writeinfolat(ofile, d, kind, ctrlkey, measure, iskeyfile='True', 
keyfile='keylist'):
    """Writes into a file with information on the latency graphs plotted in 
    multiplot.
    
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



def createinfonum(fname, measure):
    '''Creates a file with information on the behavior number graph plotted in 
    multiplot.'''

    if measure == 'mean':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
            'Mean Duration (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

    if measure == 'median':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\n'.format('Genotype', 'Behavior', \
            'Median Number (s)', '# pairs exhibiting behavior'))

def createinfodur(fname, measure):
    '''Creates a file with information on the behavior duration graph plotted in 
    multiplot.'''

    if measure == 'mean':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
            'Mean Duration (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

    if measure == 'median':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\n'.format('Genotype', 'Behavior', \
            'Median Duration (s)', '# pairs exhibiting behavior'))


def writeinfonum(ofile, d, kind, ctrlkey, measure, iskeyfile='True', 
keyfile='keylist'):
    '''Writes into a file with information on the frequency graphs plotted in multiplot.

    Input:
    ofile = name of output file
    d = dictionary with behavior data
    kind = type of behavior
    ctrlkey = name of control group that other groups will be compared to (e.g., 'CS')
    measure = mean or median: writes down information pertaining to the mean or the median of the data
    iskeyfile = 'True' or 'False': whether or not a file with a keylist exists
    keyfile = name of keylist file
    '''
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()
    
    if measure == 'mean':
        md = dictttest(d, ctrlkey)
        for k in keylist:
            try:
                with open(ofile, 'a') as f:
                    f.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4}\n'.format(k, kind, 
                    md[k]['mean'], md[k]['sterr'], md[k]['n']))
            except KeyError:
                continue
                
    if measure == 'median':
        md = dictmw(d, ctrlkey)
        for k in keylist:
            try:
                with open(ofile, 'a') as f:
                    f.write('{0}\t{1}\t{2:.2f}\t{3}\n'.format(k, kind, 
                    md[k]['median'], md[k]['n']))  
            except KeyError:
                continue

def writeinfodur(ofile, d, kind, ctrlkey, measure, iskeyfile='True', 
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
        md = dictmw(d, ctrlkey)
        for k in keylist:
            try:
                with open(ofile, 'a') as f:
                    f.write('{0}\t{1}\t{2:.2f}\t{3}\n'.format(k, kind, 
                    md[k]['median'], md[k]['n']))  
            except KeyError:
                continue


def createinfoprop(ofile):
    '''Creates a file with information on the frequency graphs plotted with
    'multiplot'.
    '''
    with open(ofile, 'w') as f:
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format('Genotype', 'Behavior', \
        '# pairs exhibiting behavior', '# pairs tested', \
        '% exhibiting behavior', 'ci_lower', 'ci_upper' ))


def createinfopropmean(ofile):
    '''Creates a file with information on the frequency graphs plotted with
    'multiplot'.
    '''
    with open(ofile, 'w') as f:
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format('Genotype', 'Behavior', \
        'Mean', '# pairs tested', 'stdev', 'sterr' ))


def writeinfoprop(ofile, d, binconf, kind, iskeyfile='True', keyfile='keylist'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot.
    d = dictionary with proportion data
    binconf = confidence of binomial confidence interval
    kind = type of behavior
    iskeyfile = 'True' or 'False': whether or not a file with a keylist exists
    keyfile = name of keylist file
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


def writeinfopropmean(ofile, d, kind, iskeyfile='True', keyfile='keylist'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot.
    d = dictionary with proportion data
    '''
    md = dictttest(d)
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = md.iterkeys()

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
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, 
            md[k]['mean'], md[k]['n'], md[k]['stdev'], md[k]['sterr']))
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
            t = 'Latency to\nfirst copulation attempt'
    
    if metric == 'aglatmed' or metric == 'agdurmean' or metric == 'agdurmed':
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
        if kind == 'chase':
            t = 'Duration of\nchasing'
            
    if metric == 'agprop' or metric == 'cprop':
        if kind == 'wingthreat':
            t = '% pairs with\nwingthreat'
        if kind == 'charge':
            t = '% pairs charging'
        if kind == 'anyag':
            t = '% pairs fighting'
        if kind == 'escd':
            t = '% pairs with\ndominant esc'
        if kind == 'escm':
            t = '% pairs with\nmutual esc'
        if kind == 'we':
            t = '% flies displaying\nwing extension'
        if kind == 'copsuc':
            t = '% flies copulating'
        if kind == 'copatt1':
            t = '% flies attempting\ncopulation'

    if metric == 'agnummean' or metric=='agnummed':
        if kind == 'wingthreat':
            t = 'Number of\nwing threats'
        if kind == 'charge':
            t = 'Number of\ncharges'
        if kind == 'chargeonly':
            t = 'Number of\ncharges,\nno orientation'
        if kind == 'escd':
            t = 'Number of bouts\nof dominant escalation'
        if kind == 'escm':
            t = 'Number of bouts\nof mutual escalation'
        if kind == 'chase':
            t = 'Number of bouts\nof chasing'
            
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
    
    if metric == 'agdurmed':
        d = dictagdur2(kind, fname)
        md = dictmw(d, ctrlkey)
        adjpd = mcpval(md, 'fdr', 'True', keyfile)

    if metric == 'agnummean':
        fulld = dictagnum(kind, fname)
        d = {}
        for k in keylist:
            d[k] = fulld[k]    
        md = dictttest(d, ctrlkey)
        adjpd = mcpval(md, 'fdr', 'True', keyfile)
    
    if metric == 'agnummed':
        d = dictagnum(kind, fname)
        md = dictmw(d, ctrlkey)
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
    
    if metric == 'aglatmed' or metric == 'aglatmed' or metric == 'clatmed' or metric == 'agnummed' or metric == 'agdurmed':
        for k in keylist:
            if not d[k]:
                continue
            vals.append(d[k])
            #conds.append('{0}; n={1}'.format(k, mwd[k]['n']))
            conds.append('{0}'.format(k))
            try:
                pvals.append(adjpd[k]['adjpval'])
            except KeyError:
                continue
    
    if metric == 'agdurmean' or metric == 'clatmean' or metric == 'agnummean':
        for k in keylist:
            if not d[k]:
                continue
            try:
                vals.append(md[k]['mean'])
                #conds.append('{0}\nn={1}'.format(k, mwd[k]['n']))
                #conds.append('{0}; n={1}'.format(k, md[k]['n']))
                conds.append('{0}'.format(k))
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
            #conds.append('{0}; n={1}'.format(k, db[k]['n']))
            conds.append('{0}'.format(k))
            nsuc.append(db[k]['nsuc'])
            n.append(db[k]['n'])
            lowerci.append(db[k]['prop']-db[k]['lowerci'])
            upperci.append(db[k]['upperci']-db[k]['prop'])
            pvals.append(adjppd[k]['adjpval'])
    
    return(vals, conds, pvals, n, stdev, sterr, lowerci, upperci, nsuc)  


def plotbdata(metric, vals, x_list, sterr, truebarw, lw, lowerci, upperci):

    if metric == 'aglatmed' or metric == 'aglatmed' or metric == 'clatmed' or metric == 'agnummed' or metric == 'agdurmed':
    #Plots the box and whisker plot.
        bp = plt.boxplot(vals, positions=x_list, sym='')
        pylab.setp(bp['boxes'], color='black')
        pylab.setp(bp['whiskers'], color='black', ls='-')
        pylab.setp(bp['medians'], color='black')
    
    if metric == 'agdurmean' or metric == 'clatmean' or metric == 'agnummean':
    # Plots a bar plot displaying means.
        bp = plt.bar(x_list, vals, yerr=sterr, width=truebarw, color='#d3d3d3', \
        bottom=0, ecolor='k', capsize=0.5, linewidth=lw)    
    
    if metric == 'agprop' or metric == 'cprop':
    # Plots a bar plot displaying proportions.
        plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, 
        color='#d3d3d3', bottom=0, ecolor='k', capsize=0.5, linewidth=lw)



def multiplot(metric, kind, fname, ctrlkey, barwidth, ymin, ylim, ylabel, 

yaxisticks, subplotn, subplotl, binconf, keyfile='keylist', fontsz=9, 
stitlesz=10, lw=1, starpos=0.8):
    

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
    #plt.xticks(x_list, conds, rotation=45, fontproperties=fonti)
    
    x_list = [x + 0.5*truebarw for x in x_gen1]
    plt.xticks(x_list, conds, rotation=90, fontproperties=fonti)

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


    p05i = [i for i, pval in enumerate(pvals) if pval <0.05 and pval >= 0.01]
    
    for i in p05i:
        plt.text(x_list[i], starpos*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    for i in p01i:
        plt.text(x_list[i], starpos*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    for i in p001i:
        plt.text(x_list[i], starpos*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)
            
# Contains functions useful for analyzing aggression data from a csv file 
# generated during manual scoring.
# Some functions used for analysis are in the courtshiplib.py library.


import os
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import rpy2.robjects as robjects
import cmn.cmn as cmn
import libs.genplotlib as gpl
import libs.rstatslib as rsl
import courtshiplib as cl


#### FUNCTIONS FOR CONSTRUCTING DICTIONARIES ####

def agline(line):

    """Generates dictionary with the values from line, with the parameters as 
    keywords.
    line is of the following format:
    Date, Movie, Offset (s), Well #, Genotype, 
    flare or wing threat (m), (s), 
    wing threat + charge, orient, or lunge (m), (s),
    escalation - dominant (m), (s), (dur),
    escalation - mutual (m), (s), (dur)
    """

    vals = {}
    x = ['date', 'movie', 'offset', 'well', 'gen', 'flarem', 'flares', 
    'chargem', 'charges', 'charget', 'escdm', 'escds', 'escddur', 'escmm', 'escms', 
    'escmdur']
    y = line.strip('\n').split(',')[0:16]
    z = zip(x, y)

    for item in z:
        vals[item[0]] = item[1]

    return(vals)


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





def dictaglat(kind, fname):
    """
    Generates a dictionary from data in 'fname' where the keywords are 
    genotypes and the values are the latencies to a behavior specified by 'kind'.

    kind = 'flare' (flare or wing threat alone), 
    'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data

    """
    km = kind + 'm'
    ks = kind + 's'
    
    d = {}
    f = open(fname)
    f.next()
    f.next()
    y = 0

    for l in f:
        #print(l)
        adict = agline(l)
        #print(adict['charget'])

        if y == adict['well']:
            continue
        else:
            gen = adict['gen']
            if gen not in d:
                d[gen] = []            

        if adict[km] != 'x' and adict[km] != '-' and adict[km] != '':
            d[gen].append(cmn.convtosec(float(adict[km]), float(adict[ks]))
            - float(cmn.convtosec(float(adict['offset']), 0)))
        
        if kind == 'flare':
            if adict[km] == '':
                d[gen].append(cmn.convtosec(float(adict['chargem']), 
                float(adict['charges'])) -
                float(cmn.convtosec(float(adict['offset']), 0)))
        
        y = adict['well']
    return(d)


def dictagfreq(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    are a list in which an entry of "100" = success and an entry of "0" = failure.

    kind = 'flare' (flare or wing threat alone), 
    'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data
    """

    d = {}
    f = open(fname)
    f.next()
    f.next()
    y = '0'
    for l in f:
        adict = agline(l)
        if y == adict['well']:
            continue        
        gen = adict['gen']
        if gen not in d:
            d[gen] = []        
        km = kind + 'm'
        ks = kind + 's'
        
        if kind == 'escd' or kind == 'escm':
            if adict[ks] == '':
                d[gen].append(0)
            elif int(adict[ks]) >= 0:
                d[gen].append(100)
        else:
            if adict[ks] == 'x':
                d[gen].append(0)
            elif adict[ks] == '-':
                pass
            elif adict[ks] == '':
                d[gen].append(100)
            elif int(adict[ks]) >= 0:
                d[gen].append(100)
        y = adict['well']
        
    return(d)

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

def dictagnum(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    indicate the number of times each fly exhibits the behavior.

    kind = 'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data
    """

    with open(fname, 'r') as g:
        g.next()
        g.next()
        m = g.next()
    startdict = agline(m)
    genold = startdict['gen']

    f = open(fname)
    f.next()
    f.next()
    d = {}
    y = '1'
    nb = []
    for l in f:
        adict = agline(l)
        ks = kind + 's'
        gen = adict['gen']
        well = adict['well']

        if adict['gen'] not in d:
            d[gen] = []
        
        if gen != genold:
            d[genold].append(sum(nb))
            nb = []
        else: 
            if adict['well'] != y:
                d[gen].append(sum(nb))
                nb = []
        
        if kind == 'charge':
            if adict[ks] == 'x':
                nb.append(0)
            elif int(adict[ks]) >= 0 and (adict['charget'] == 'c' or 
            adict['charget'] == 'o'):
                nb.append(1)
            elif adict[ks] == '-':
                pass
            #print('nb', nb)

        if kind == 'escd' or kind == 'escm':
            if adict[ks] == '':
                nb.append(0)
            elif int(adict[ks]) >= 0:
                nb.append(1)
            elif adict[ks] == '-':
                pass

        y = adict['well']
        genold = adict['gen']
        
    d[gen].append(sum(nb))
        
    return(d)

    
def dictagdur(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    indicate the duration over which each fly exhibits the behavior.

    kind = 'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data
    """

    with open(fname, 'r') as g:
        g.next()
        g.next()
        m = g.next()
    startdict = agline(m)
    genold = startdict['gen']

    f = open(fname)
    f.next()
    f.next()
    d = {}
    y = '1'
    nb = []
    for l in f:
        adict = agline(l)
        kdur = kind + 'dur'
        gen = adict['gen']
        well = adict['well']

        if adict['gen'] not in d:
            d[gen] = []
        
        if gen != genold:
            d[genold].append(sum(nb))
            nb = []
        else: 
            if adict['well'] != y:
                #print(sum(nb))
                d[gen].append(sum(nb))
                nb = []
        
        if adict[kdur] == '':
            nb.append(0)
        elif int(adict[kdur]) >= 0:
            nb.append(int(adict[kdur]))
        elif adict[ks] == '-':
            pass
    

        y = adict['well']
        genold = adict['gen']
        
    d[gen].append(sum(nb))

    return(d)



def dictagdurb(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values 
    indicate the duration over which each fly exhibits the behavior.

    kind = 'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data
    """

    with open(fname, 'r') as g:
        g.next()
        g.next()
        m = g.next()
    startdict = agline(m)
    genold = startdict['gen']

    f = open(fname)
    f.next()
    f.next()
    d = {}
    y = '1'
    nb = []
    for l in f:
        adict = agline(l)
        kdur = kind + 'dur'
        gen = adict['gen']
        well = adict['well']

        if adict['gen'] not in d:
            d[gen] = []
               
        if gen != genold:
            if sum(nb) != 0:
                d[genold].append(sum(nb))
                nb = []
            elif sum(nb) == 0:
                nb = []
        else: 
            if adict['well'] != y:
                if sum(nb) != 0:
                    d[gen].append(sum(nb))
                    nb = []
                elif sum(nb) == 0:
                    nb = []
        
        #if adict[kdur] == '':
            #nb.append(0)
        #elif int(adict[kdur]) >= 0:
            #nb.append(int(adict[kdur]))
        #elif adict[ks] == '-':
            #pass
        
        if adict[kdur] == '':
            continue
        elif int(adict[kdur]) > 0:
            nb.append(int(adict[kdur]))
        elif adict[ks] == '-':
            pass

        y = adict['well']
        genold = adict['gen']
    
    if sum(nb) != 0:
        d[gen].append(sum(nb))

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


#### FUNCTIONS FOR WRITING RESULTS OF DATA ANALYSIS TO TEXT FILES ####

def writeinfoaglatmean(ifile, ofile, kind, ctrlkey, keyfile, iskeyfile='False'):
    '''Writes into a file with information on the latency graphs plotted in 
    multiplot_1bar.'''

    d = dictaglat(kind, ifile)
    mwd = cl.dictmeans(d)
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()

    for k in keylist:

        if kind == 'flare':
            nk = 'flare or >'
        if kind == 'charge':
            nk = 'any aggression'
        if kind == 'escd':
            nk = 'dominant escalation'
        if kind == 'escm':
            nk = 'mutual escalation'

        #print(mwd[k][0])
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4}\n'.format(k, nk, mwd[k][0], 
            mwd[k][2], mwd[k][3]))


def writeinfomean(d, ofile, kind, ctrlkey, keyfile, iskeyfile='False'):

    mwd = cl.dictmeans(d)
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


def writeinfoagprop(d, ofile, kind, keyfile, iskeyfile='False'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot_1bar.
    d = dictionary with proportion data
    '''

    bd = cl.dictbin(d)
    
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
        
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4:.2%}\t{5}\t{6}\n'.format(k, kind, 
            bd[k]['nsuc'], bd[k]['n'], float(bd[k]['nsuc'])/float(bd[k]['n']),  
            bd[k]['lowerci'], bd[k]['upperci']))
            #mx.append(np.max(v['n']))
            #mi.append(np.min(v['n']))
    #with open(ofile, 'a') as f:
        #f.write('Max n = {0}\n'.format(np.max(mx)))
        #f.write('Min n = {0}\n'.format(np.min(mi)))


def writeproptestfile(ofile, d, kind, keyfile, iskeyfile='false'):
    """Input is a dictionary in which the keywords are genotypes or conditions 
    and the values are a list in which an entry of "100" = success and an 
    entry of "0" = failure (output of dictagfreq)"""
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())
    
    newd = {}
    for k in keylist:
        newd[k] = d[k]

    pt = cl.dictproptest(newd)
    with open(ofile, 'a') as f:
        f.write('{0}\t{1}\n'.format(kind, pt))



### FUNCTIONS FOR PLOTTING FIGURES ###

def plotaglatbw(kind, d, iskeyfile = 'true', type='bw'):
    '''Plots a box and whisker plot of the latency data.'''

    md = cl.dictmeans(d)

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = 'Latency (s)'
    ftitle = 'Latency'

    if kind == 'flare':
        ftitle = 'Latency to first flare or wing threat'

    if kind == 'charge':
        ftitle = 'Latency to aggression'

    if kind == 'escd':
        ftitle = 'Latency to dominant escalation'
        
    if kind == 'escm':
        ftitle = 'Latency to mutual escalation'
    
    
    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large')
    if kind == 'wing':
        plt.ylim(0, 150)


def plotagfreq(kind, d, iskeyfile = 'true', keyfile='keylist', type='b'):
    """Generates a bar plot of the frequency of each type of behavior for 
    each genotype.

    kind = 'wingthreat' (wing threat), 
    'charge' (wing threat + charge or orientation),
    'anyag' (wing threat + charge, orientation, pushing, lunge, chase, grab, 
    hold, dominant or mutual escalation)
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
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

    if kind == 'flare':
        ftitle = 'Percent with flared wings\nor aggression'
        
    if kind == 'wingthreat':
        ftitle = 'Percent exhibiting wing threat'
        
    if kind == 'charge':
        ftitle = 'Percent exhibiting charges'

    if kind == 'anyag':
        ftitle = 'Percent exhibiting aggression'

    if kind == 'escd':
        ftitle = 'Percent exhibiting dominant escalation'
    
    if kind == 'escm':
        ftitle = 'Percent exhibiting mutual escalation'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large', err='none', figw=6, figh=4)
    if kind == 'escd' or kind == 'escm':
        plt.ylim(0, 30)
    else:
        plt.ylim(0, 110)


def plotagnum(kind, d, iskeyfile='True', keyfile='keylist', type='b'):
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
    

def plotagdur(kind, d, iskeyfile='True', keyfile='keylist', type='b'):
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
    
    ftitle = 'Mean duration of behavior'

    if kind == 'escd':
        ftitle = 'Mean duration of dominant escalation'
    
    if kind == 'escm':
        ftitle = 'Mean duration of mutual escalation'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large', err='none', figw=10, figh=8)
    
    plt.ylim(0)


#### FUNCTIONS FOR PLOTTING A PUBLICATION-QUALITY FIGURE ####

def plotlattitle(kind):
    
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
    return(t)

def plotdurtitle(kind):
    
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
    return(t)
    
    
    
def multiplot_1barmw(metric, kind, fname, ctrlkey, barwidth, ymin, ylabel, 
yaxisticks, subplotn, subplotl, keyfile='keylist', fontsz=9, stitlesz=10, lw=1):

    # ======== LOAD DATA =============
    if keyfile == 'no':
        keylist = sorted(d.keys())
    else:
        keylist = cmn.load_keys(keyfile)
    
    if metric == 'lat':
        d = dictaglat(kind, fname)
    
    if metric == 'dur':
        d = dictagdur2(kind, fname)
    
    mwd = cl.dictmw(d, ctrlkey)
    adjpd = cl.mcpval(mwd, 'fdr', 'True', keyfile)
   
    vals = []
    conds = []
    pvals = []
    for k in keylist:
        #print(not d[k])
        if not d[k]:
            continue
        vals.append(d[k])
        #conds.append('{0}\nn={1}'.format(k, mwd[k]['n']))
        conds.append('{0}; n={1}'.format(k, mwd[k]['n']))
        try:
            pvals.append(adjpd[k]['adjpval'])
        except KeyError:
            continue
    
    if not vals:
        m = 'No values'
        raise cmn.EmptyValueError(m)
    
    
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
    
    if metric == 'dur':
        if kind == 'wingthreat':
            ylim = 300
        if kind == 'charge':
            ylim = 30
        if kind == 'anyag':
            ylim = 50
        if kind == 'escd':
            ylim = 150
        if kind == 'escm':
            ylim = 20
    else:
        maxvals = [max(x) for x in vals]
        maxval = max(maxvals)
        ylim = cmn.myround(1*maxval)

    plt.axis( [0, xlim, ymin, ylim])


    # ========ADDS TICKS, LABELS and TITLES==========

    # Adds labels to the x-axis at the x-coordinates specified in x_list; 
    #labels are specified in the conds list.
    plt.xticks(x_list, conds, fontproperties=fonti, rotation=45)

    # Labels the yaxis; labelpad is the space between the ticklabels and 
    #y-axis label.
    plt.ylabel(ylabel, labelpad=2, fontproperties=fontv, multialignment='center')

    # Add title
    if metric == 'lat':
        t = plotlattitle(kind)
    if metric == 'dur':
        t = plotdurtitle(kind)
    plt.title(t, fontsize=stitlesz)

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




def multiplot_1barf(kind, fname, ctrlkey, barwidth, keyfile, conf, ylabel, 
yaxisticks, ymin, ylim, subplotn, subplotl, fontsz, stitlesz, lw=1):

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
    d = dictagfreq2(kind, fname)
    db = cl.dictbin(d, conf, label=kind)
    #ppd = cl.dictpptest(d, ctrlkey)
    #adjppd = cl.mcpval(ppd, 'fdr')
    fd = cl.dictfishtest(d, ctrlkey=ctrlkey)
    adjppd = cl.mcpval(fd, 'fdr')

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
        #conds.append('{0}\nn={1}'.format(k, db[k]['n']))
        conds.append('{0}; n={1}'.format(k, db[k]['n']))
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
    #print(x_list)
                
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
    if kind == 'escd':
        ylim = 0.5*ylim
    if kind == 'escm':
        ylim = 0.25*ylim
    plt.ylim(ymin, ylim)

    # Plots and formats xlabels.
    xlabel_list = [x for x in x_list]
    plt.xticks(xlabel_list, conds, rotation=45, fontproperties=fonti)

    # Formats the yticks.
    plt.yticks(fontproperties=fontv)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')

    # Add title
    if kind == 'flare':
        plt.title('% pairs with\nflared wings', fontsize=stitlesz)
    
    if kind == 'wingthreat':
        plt.title('% pairs with\nwingthreat', fontsize=stitlesz)
    
    if kind == 'charge':
        plt.title('% pairs charging', fontsize=stitlesz)

    if kind == 'anyag':
        plt.title('% pairs fighting', fontsize=stitlesz)

    if kind == 'escd':
        plt.title('% pairs with\ndominant escalation', fontsize=stitlesz)
    
    if kind == 'escm':
        plt.title('% pairs with\nmutual escalation', fontsize=stitlesz)


    # Labels the subplot
    plt.text(-0.1, 1.0, subplotl, transform=ax.transAxes)


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
        plt.text((x_list[i]+truebarw/2.), 0.7*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    #print(p01i)
    for i in p01i:
        print(x_list[i])
        plt.text((x_list[i]+truebarw/2.), 0.7*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    #print(p001i)
    for i in p001i:
        plt.text((x_list[i]+truebarw/2.), 0.7*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)




def multiplot_1barmean(metric, kind, fname, ctrlkey, barwidth, ymin, ylabel, 
yaxisticks, subplotn, subplotl, keyfile='keylist', fontsz=9, stitlesz=10, lw=1):

    # ======== LOAD DATA =============
    if keyfile == 'no':
        keylist = sorted(d.keys())
    else:
        keylist = cmn.load_keys(keyfile)
    
    if metric == 'dur':
        d = dictagdur2(kind, fname)
        
    md = cl.dictttest(d, ctrlkey)
    adjpd = cl.mcpval(md, 'fdr', 'True', keyfile)
   
    vals = []
    conds = []
    n = []
    stdev = []
    sterr = []
    pvals = []
    
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
    
    if not vals:
        m = 'No values'
        raise cmn.EmptyValueError(m)
    
    
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

    # Defines the axes.
    ax = plt.subplot(subplotn)

    # =========== PLOT DATA =======================

    #Plots the box plot.
    truebarw = 0.35*barwidth
    bp = plt.bar(x_list, vals, yerr=sterr, width=truebarw, color='#d3d3d3', \
    bottom=0, ecolor='k', capsize=0.5, linewidth=lw)    
    

    # Sets the x- and y-axis limits.
    xlim = x_list[-1]+1.5*barwidth
    
    if metric == 'dur':
        if kind == 'wingthreat':
            ylim = 300
        if kind == 'charge':
            ylim = 30
        if kind == 'anyag':
            ylim = 50
        if kind == 'escd':
            ylim = 150
        if kind == 'escm':
            ylim = 20
    else:
        maxvals = [max(x) for x in vals]
        maxval = max(maxvals)
        ylim = cmn.myround(1*maxval)

    plt.axis( [0, xlim, ymin, ylim])


    # ========ADDS TICKS, LABELS and TITLES==========

    # Adds labels to the x-axis at the x-coordinates specified in x_list; 
    #labels are specified in the conds list.
    plt.xticks(x_list, conds, fontproperties=fonti, rotation=45)

    # Labels the yaxis; labelpad is the space between the ticklabels and 
    #y-axis label.
    plt.ylabel(ylabel, labelpad=2, fontproperties=fontv, multialignment='center')

    # Add title
    if metric == 'lat':
        t = plotlattitle(kind)
    if metric == 'dur':
        t = plotdurtitle(kind)
    plt.title(t, fontsize=stitlesz)

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
# Contains functions useful for analyzing courtship and aggression 
# data from a csv file generated during manual scoring.

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

#### FUNCTIONS FOR CONSTRUCTING DICTIONARIES ####

def courtshipline(line):

    """Generates dictionary with the values from line, with the parameters as 
    keywords.

    fname is of the following format:
    Data, Offset (s), Well #, Genotype, Wing ext (m), Wing ext (s), Cop
    Suc (m),Cop Suc (s),Cop Att 1 (m),Cop Att 1 (s)
    """

    cvals = {}
    x = ['date', 'movie', 'offset', 'well', 'gen', 'wingm', 'wings', 'copsucm',
    'copsucs', 'copatt1m', 'copatt1s']
    y = line.strip('\n').split(',')[0:11]
    z = zip(x, y)

    for item in z:
        cvals[item[0]] = item[1]

    return(cvals)


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
    
    

def dictlat(kind, fname):
    """
    Generates a dictionary from data in 'fname' where the keywords are 
    genotypes and the values are the latencies to a behavior specified by 
    'kind'.

    kind = 'wing' (wing extension), 'copatt1' (first copulation attempt), 
    'copsuc' (successful copulation)
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
    """Generates a dictionary where the keywords are genotypes and the values 
    are a list in which an entry of "100" = success and an entry of "0" = failure.

    kind: 'wing' (wing extension) 'copatt1' (first copulation attempt), 
    'copsuc' (successful copulation)
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


def dictmeans(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the
    values are lists of the mean, standard deviation, standard error, and n for
    that condition.

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


def dictbin(dict, conf=0.95, methods='wilson', label='data'):
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


def dictpptest(d, ctrlkey='cs'):
    """Returns a dictionary with p-values resulting from a proportion test
    to determine whether each experimental condition differs from the control
    condition. The proportion test used is R's prop.test.
       
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
        mwdict[i]['sigtest'] = 'Proportion test'

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


def dictgroupproptest(d):
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
        f.write('Genotype\tBehavior\tMedian latency (s)\tn\tAdj p-value\tCtrl\n')


def writeinfolat(ifile, ofile, kind, ctrlkey, keyfile, iskeyfile='False'):
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


def createinfolatmean(fname):
    with open(fname, 'w') as g:
        g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
        'Mean latency (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

def writeinfolatmean(ifile, ofile, kind, ctrlkey):
    """Similar to writeinfolat(), but reports the mean rather than the 
    median."""
    
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
    


def createinfodur(fname, measure):
    
    if measure == 'mean':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
            'Mean Duration (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

    if measure == 'median':
        with open(fname, 'w') as g:
            g.write('{0}\t{1}\t{2}\t{3}\n'.format('Genotype', 'Behavior', \
            'Median Duration (s)', '# pairs exhibiting behavior'))


def writeinfodur(ofile, d, kind, ctrlkey, measure, iskeyfile='True', 
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


def writeinfoprop(ifile, ofile, kind, keyfile, iskeyfile='false'):
    '''Writes into a file with information on the frequency graphs plotted in 
    multiplot_1barf.'''

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




#### FUNCTIONS FOR MAKING PLOTS ####

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

    
    gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle)
    plt.ylim(0, 120)



#### FUNCTIONS FOR PLOTTING A PUBLICATION-QUALITY FIGURE ####

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


