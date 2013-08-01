import courtshiplib as cl
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmn.cmn as cmn
import numpy as np
import pylab
import rstatslib as rsl
import rpy2.robjects as robjects


def multiplot_1bar(kind, fname, barnum, barwidth, xlim, ymin, ylabel, yaxisticks, subplotn, subplotl, keyfile='keylist', fontsz=9, stitlesz=10, lw=1):

    # ======== SET INITIAL FIGURE PROPERTIES =============
    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)

    # Defines coordinates for each bar.
    lastbar = (1.5*barnum*barwidth)-barwidth # X-coordinate of last bar
    x_gen1 = np.linspace(0.5+0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 # Coordinates for the temperature labels.

    # Defines the axes.
    ax = plt.subplot(subplotn)

    # =========== PLOT DATA =======================

    # Load data
    keylist = cmn.load_keys(keyfile)
    d = cl.dictlat(kind, fname)
    mwd = cl.dictmw(d)
    adjpd = cl.mcpval(mwd, 'fdr')

    vals = []
    conds = []
    pvals = []

    for k in keylist:
        vals.append(d[k])
        conds.append(k)
        pvals.append(adjpd[k]['adjpval'])

    #Plots the box plot.
    bp = plt.boxplot(vals, positions=x_list, sym='')
    pylab.setp(bp['boxes'], color='black')
    pylab.setp(bp['whiskers'], color='black', ls='-')
    pylab.setp(bp['medians'], color='black')

    # Sets the x- and y-axis limits.
    xlim = x_list[-1]+1.5*barwidth

    maxval = np.max(np.max(vals))
    if kind == 'copsuc':
        ylim = 1.3*maxval
    else:
        ylim = maxval
    ylim = cmn.myround(ylim)

    plt.axis( [0, xlim, ymin, ylim])


    # ========ADDS TICKS, LABELS and TITLES==========

    # Adds labels to the x-axis at the x-coordinates specified in x_list; labels are specified in the conds list.
    plt.xticks(x_list, conds, fontproperties=fontv, rotation=45)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=2, fontproperties=fontv, multialignment='center')

    # Add title
    if kind == 'wing':
        plt.title('Latency to wing extension', fontsize=stitlesz)

    if kind == 'copsuc':
        plt.title('Latency to copulation', fontsize=stitlesz)

    if kind == 'copatt1':
        plt.title('Latency to first copulation attempt', fontsize=stitlesz)

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

    p05i = [i for i, pval in enumerate(pvals) if pval <0.05]
    for i in p05i:
        plt.text(x_list[i], 0.75*ylim, '*', horizontalalignment='center', fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01]
    for i in p01i:
        plt.text(x_list[i], 0.75*ylim, '**', horizontalalignment='center', fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    for i in p001i:
        plt.text(x_list[i], 0.75*ylim, '***', horizontalalignment='center', fontsize=fontsz)



def multiplot_3bars(kindlist, fname, keyfile, conf, ylabel, yaxisticks, ymin, ylim, colors, subplotn, subplotl, barwidth, barnum, fontsz, stitlesz, leglabels, lw=1):

    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)

    # Defines the axes.
    ax = plt.subplot(subplotn)

    # Defines variables used in finding coordinates for each bar.
    lastbar = (barnum*len(kindlist)*barwidth)
    x_gen1 = np.linspace(1.5*barwidth, lastbar+barnum*barwidth, barnum).tolist()

    # Load data.
    keylist = cmn.load_keys(keyfile)

    for i, kind in enumerate(kindlist):
        d = cl.dictfreq(kind, fname)
        db = cl.dictbin(d, conf, label=kind)
        vals = []
        conds = []
        lowerci = []
        upperci = []
        nsuc = []
        n = []

        # Defines coordinates for each bar.
        x_list = [x + i for x in x_gen1]

        # Appends data for the bar plot to appropriate lists.
        for k in keylist:
            vals.append(db[k]['prop'])
            conds.append(k)
            nsuc.append(db[k]['nsuc'])
            n.append(db[k]['n'])
            lowerci.append(db[k]['prop']-100*db[k]['lowerci'])
            upperci.append(100*db[k]['upperci']-db[k]['prop'])


        # Plots the bar plot for each kind of data.
        truebarw = barwidth-(0.05*barwidth)
        plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, color=colors[i], bottom=0, ecolor='k', capsize=0.5, linewidth=lw, label=leglabels[i])


    # ======== ADDS TICKS, LABELS and TITLES==========

    # Sets the x- and y-axis limits.
    plt.ylim(ymin, ylim)

    # Plots and formats xlabels.
    xlabel_list = [x for x in x_list]
    plt.xticks(xlabel_list, conds, rotation=45, fontproperties=fontv)

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
    a1 = plt.legend(ncol=len(kindlist), loc='upper center', labelspacing=0.1, columnspacing=0.7, markerscale=0.5, fontsize=fontsz, handletextpad=0.3, borderpad=0)
    #Removes border around the legend.
    a1.draw_frame(False)


def createinfolat(ofile):
    with open(ofile, 'w') as f:
        f.write('Genotype\tBehavior\tmedian\tn\tAdj p-value\tCtrl\n')

def writeinfolat(ifile, ofile, kind):

    d = cl.dictlat(kind, ifile)
    mwd = cl.dictmw(d)
    mcwd = cl.mcpval(mwd)

    mx = []
    mi = []

    for k in d.keys():
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(k, kind, mwd[k]['median'], mwd[k]['n'], mcwd[k]['adjpval'], mcwd[k]['control']))
            mx.append(np.max(mwd[k]['n']))
            mi.append(np.min(mwd[k]['n']))

    with open(ofile, 'a') as f:
        f.write('Max n = {0}\n'.format(np.max(mx)))
        f.write('Min n = {0}\n'.format(np.min(mi)))


def createinfoprop(ofile):
    with open(ofile, 'w') as f:
        f.write('Genotype\tBehavior\tnsuc\tn\n')


def writeinfoprop(ifile, ofile, kind):
    d = cl.dictfreq(kind, ifile)
    bd = cl.dictbin(d)

    mx = []
    mi = []
    for k, v in bd.iteritems():
        with open(ofile, 'a') as f:
            f.write('{0}\t{1}\t{2}\t{3}\n'.format(k, kind, v['nsuc'], v['n']))
            mx.append(np.max(v['n']))
            mi.append(np.min(v['n']))
    with open(ofile, 'a') as f:
        f.write('Max n = {0}\n'.format(np.max(mx)))
        f.write('Min n = {0}\n'.format(np.min(mi)))
