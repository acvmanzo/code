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
    'chargem', 'charges', 'charget', 'escdm', 'escds', 'escddur', 'escmm', 'escms', 
    'escmdur']
    y = line.strip('\n').split(',')[0:16]
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


def dictmw(d, ctrlkey='cs', test='exact'):

    """Returns a dictionary in which the keys are the genotypes and the 
    values are the results of the Mann-Whitney test as implemented in R.

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
            elif adict[ks] == '-':
                pass
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

def createinfolatmean(fname):
    with open(fname, 'w') as g:
        g.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
        'Mean latency (s)', 'Std Error (s)', '# pairs exhibiting behavior'))

def createinfoprop(fname):
    with open(fname, 'w') as f:
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format('Genotype', 'Behavior', \
        '# pairs exhibiting behavior', '# pairs tested', '% exhibiting behavior'))

def writeinfolat(ifile, ofile, kind, ctrlkey, keyfile, iskeyfile='False'):
    '''Writes into a file with information on the latency graphs plotted in multiplot_1bar.'''

    d = dictaglat(kind, ifile)
    mwd = dictmw(d, ctrlkey)
    mcwd = cl.mcpval(mwd)
    mx = []
    mi = []
    
    if iskeyfile == 'True':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = d.iterkeys()

    for k in keylist:
        try:
            with open(ofile, 'a') as f:
                f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, \
                mwd[k]['median'], mwd[k]['n'], mcwd[k]['adjpval'], mcwd[k]['control']))
                mx.append(np.max(mwd[k]['n']))
                mi.append(np.min(mwd[k]['n']))
        except KeyError:
            continue

    #with open(ofile, 'a') as f:
        #f.write('Max n = {0}\n'.format(np.max(mx)))
        #f.write('Min n = {0}\n'.format(np.min(mi)))


def writeinfolatmean(ifile, ofile, kind, ctrlkey, keyfile, iskeyfile='False'):
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


def writeinfoprop(ifile, ofile, kind, keyfile, iskeyfile='False'):
    '''Writes into a file with information on the 
    frequency graphs plotted in multiplot_1bar.'''

    d = dictfreq(kind, ifile)
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


def multiplot_1bar(kind, fname, ctrlkey, barwidth, ymin, ylabel, yaxisticks, 
subplotn, subplotl, keyfile='keylist', fontsz=9, stitlesz=10, lw=1):

    # ======== LOAD DATA =============
    if keyfile == 'no':
        keylist = sorted(d.keys())
    else:
        keylist = cmn.load_keys(keyfile)
        
    d = dictaglat(kind, fname)
    #print('d', d)
    mwd = dictmw(d, ctrlkey)
    #print('mwd', mwd)
    adjpd = cl.mcpval(mwd, 'fdr', 'True', keyfile)
    #print('adjpd', adjpd)
        
    
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

    #print(kind)
    maxvals = [max(x) for x in vals]
    maxval = max(maxvals)
    #print('maxval', maxval)
    if kind == 'copsuc':
        ylim = 1.3*maxval
    elif kind == 'wing':
        ylim = 1.6*maxval
    else:
        ylim = 1.2*maxval
    ylim = cmn.myround(ylim)

    #xlim=barnum*barwidth+1.5*barwidth
    #xlim=barnum*barwidth+4*barwidth
    #print('xlim', xlim)
    plt.axis( [0, xlim, ymin, ylim])


    # ========ADDS TICKS, LABELS and TITLES==========

    # Adds labels to the x-axis at the x-coordinates specified in x_list; labels are specified in the conds list.
    plt.xticks(x_list, conds, fontproperties=fonti, rotation=45)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=2, fontproperties=fontv, multialignment='center')

    # Add title
    if kind == 'flare':
        plt.title('Latency to\nflared wings', fontsize=stitlesz)
    if kind == 'charge':
        plt.title('Latency to\nfighting', fontsize=stitlesz)
    if kind == 'escd':
        plt.title('Latency to\ndominant escalation', fontsize=stitlesz)
    if kind == 'escm':
        plt.title('Latency to\nmutual escalation', fontsize=stitlesz)

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
    d = dictfreq(kind, fname)
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

    if kind == 'charge':
        plt.title('% pairs fighting', fontsize=stitlesz)

    if kind == 'escd':
        plt.title('% pairs with\ndominant escalation', fontsize=stitlesz)
    
    if kind == 'escm':
        plt.title('% pairs with\nmutual escalation', fontsize=stitlesz)


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


def writeproptestfile(ofile, d, kind, keyfile, iskeyfile='false'):
    """Input is a dictionary in which the keywords are genotypes or conditions and the values are a list in which an entry of "100" = success and an entry of "0" = failure (output of dictfreq)"""
    
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


