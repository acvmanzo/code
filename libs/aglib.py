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
                print(sum(nb))
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

        print(mwd[k][0])
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


def writeinfoagprop(ifile, ofile, kind, keyfile, iskeyfile='False'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot_1bar.'''

    d = dictagfreq2(kind, ifile)
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
        t = 'Courtship index'
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
        mwd = cl.dictmw(d, ctrlkey)
        adjpd = cl.mcpval(mwd, 'fdr', 'True', keyfile)
    
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
    print(x_list)
                
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



