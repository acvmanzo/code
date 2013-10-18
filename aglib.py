import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import genplotlib as gpl
import cmn.cmn as cmn
import rstatslib as rsl
import rpy2.robjects as robjects
import os
import pylab
import courtshiplib as cl

def agline(line):

    """Generates dictionary with the values from line, with the parameters as 
    keywords.
    fname is of the following format:
    Date, Movie, Offset (s), Well #, Genotype, 
    flare or wing threat (m), (s), 
    wing threat + charge, orient, or lunge (m), (s),
    escalation - dominant (m), (s), (dur),
    escalation - mutual (m), (s), (dur)
    """

    vals = {}
    x = ['date', 'movie', 'offset', 'well', 'gen', 'flarem', 'flares', 
    'chargem', 'charges', 'escdm', 'escds', 'escddur', 'escmm', 'escms', 
    'escmdur']
    y = line.strip('\n').split(',')[0:15]
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


def dictfreq(kind, fname):
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
    y = 0
    for l in f:
        adict = agline(l)
        #print(adict)
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
            elif adict[ks] == '':
                d[gen].append(100)
            elif int(adict[ks]) >= 0:
                d[gen].append(100)
        y = adict['well']
        
    return(d)


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

    kind = 'flare' (flare or wing threat alone), 
    'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
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
    
    ftitle = 'Percent displaying behavior'

    if kind == 'flare':
        ftitle = 'Percent with flared wings\nor aggression'

    if kind == 'charge':
        ftitle = 'Percent exhibiting aggression'

    if kind == 'escd':
        ftitle = 'Percent exhibiting dominant escalation'
    
    if kind == 'escm':
        ftitle = 'Percent exhibiting mutual escalation'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle, 
    titlesize='large', err='none')
    plt.ylim(0, 110)


def writeinfolat(ifile, ofile, kind, ctrlkey):
    '''Writes into a file with information on the latency graphs plotted in multiplot_1bar.'''

    d = dictaglat(kind, ifile)
    mwd = cl.dictmeans(d)

    for k in d.keys():

        if kind == 'flare':
            nk = 'flare or >'
        if kind == 'charge':
            nk = 'any aggression'
        if kind == 'escd':
            nk = 'dominant escalation'
        if kind == 'escm':
            nk = 'mutual escalation'

        print(mwd[k][0])
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4}\n'.format(k, nk, mwd[k][0], 
            mwd[k][2], mwd[k][3]))

def writeproptestfile(ofile, d, kind):
    """Input is a dictionary in which the keywords are genotypes or conditions and the values are a list in which an entry of "100" = success and an entry of "0" = failure (output of dictfreq)"""

    pt = cl.dictproptest(d)
    with open(ofile, 'a') as f:
        f.write('{0}\t{1}\n'.format(kind, pt))

def writeinfoprop(ifile, ofile, kind):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot_1bar.'''

    d = dictfreq(kind, ifile)
    bd = cl.dictbin(d)

    mx = []
    mi = []
    for k, v in bd.iteritems():
        if kind == 'flare':
            nk = 'flare or >'
        if kind == 'charge':
            nk = 'any aggression'
        if kind == 'escd':
            nk = 'dominant escalation'
        if kind == 'escm':
            nk = 'mutual escalation'
        
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4:.2%}\n'.format(k, nk, v['nsuc'], \
            v['n'], float(v['nsuc'])/float(v['n'])))
            #mx.append(np.max(v['n']))
            #mi.append(np.min(v['n']))
    #with open(ofile, 'a') as f:
        #f.write('Max n = {0}\n'.format(np.max(mx)))
        #f.write('Min n = {0}\n'.format(np.min(mi)))

