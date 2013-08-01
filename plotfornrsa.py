import courtshiplib as cl
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmn.cmn as cmn
import numpy as np
import pylab
import rstatslib as rsl
import rpy2.robjects as robjects

def multiplot_1bar(kind, fname, barnum, barwidth, xlim, ymin, ylabel, subplotn, subplotl, keyfile='keylist', fontsz=9, lw=1, stitlesz=10):

    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)

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

    # Defines coordinates for each bar.
    lastbar = (1.5*barnum*barwidth)-barwidth # X-coordinate of last bar
    x_gen1 = np.linspace(0.5+0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 # Coordinates for the temperature labels.

    # Defines the axes.
    ax = plt.subplot(subplotn)

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
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))

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



def multiplot_3bars(kindlist, fname, keyfile, conf, ylabel, subplotn, subplotl, ymin, barwidth, barnum, fontsz, stitlesz, leglabels, lw=1):

    mpl.rc('axes', linewidth=lw)
    mpl.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)

    # Load data
    
    keylist = cmn.load_keys(keyfile)
    colors = ['#555659', '#d3d3d3', 'w']
    
    # Defines the axes.
    ax = plt.subplot(subplotn)
    
    lastbar = (barnum*len(kindlist)*barwidth)
    print(lastbar)
    x_gen1 = np.linspace(1.5*barwidth, lastbar+barnum*barwidth, barnum).tolist()
    
    for i, kind in enumerate(kindlist):
        d = cl.dictfreq(kind, fname)
        db = cl.dictbin(d, conf, label=kind)
        print(db)

        vals = []
        conds = []
        lowerci = []
        upperci = []
        nsuc = []
        n = []
        
        # Defines coordinates for each bar.
        x_list = [x + i for x in x_gen1]

        for k in keylist:
            vals.append(db[k]['prop'])
            conds.append(k)
            nsuc.append(db[k]['nsuc'])
            n.append(db[k]['n'])
            lowerci.append(db[k]['prop']-100*db[k]['lowerci'])
            upperci.append(100*db[k]['upperci']-db[k]['prop'])

        # Defines the colors for each bar.
        #cols = ['k', '#c9ced4', 'w']
        #colors = np.tile(cols, len(keylist).tolist())


        # Defines limit of x axis.
        #xlim = x_list[-1]+1.5*barwidth

        #Plots the bar plot.
        truebarw = barwidth-(0.05*barwidth)
        plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, color=colors[i], bottom=0, ecolor='k', capsize=0.5, linewidth=lw, label=leglabels[i])

        print(n)
        r = robjects.r
        unlist = r['unlist']
        print(rsl.proptest(unlist(nsuc), unlist(n)))

    #Coordinates where the xlabels will be listed.
    
    xlabel_list = [x  for x in x_list]
    plt.xticks(xlabel_list, conds, rotation=45, fontproperties=fontv)


    # Formats the yticks.
    plt.yticks(fontproperties=fontv)

    # Formats the xticks.
    #plt.xticks(multialignment = 'center', fontproperties=fontv)

    #Uncomment lines below to display without top and right borders.
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
            
    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Uncomment the line below to remove all of the plot axis lines.
    #plt.setp(ax, frame_on=False)

    #Uncomment the line below to remove all tick marks/labels.
    #ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())

    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(7))


    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax.get_xticklines():
        line.set_visible(False)

     #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
 
    # Sets the x- and y-axis limits.
    ylim = 130
    plt.ylim(ymin, ylim)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')

    plt.title('% Flies displaying behavior', fontsize=stitlesz)
   
    
    #Plots legend.
    a1 = plt.legend(ncol=len(kindlist), loc='upper center', labelspacing=0.1, columnspacing=0.7, markerscale=0.5, fontsize=fontsz, handletextpad=0.3, borderpad=0)
    
    #bbox_to_anchor=(0.1, 0.95, 0.8, 0.1)
    
    # Changes legend font to fontsz.
    #ltext  = a1.get_texts()
    #plt.setp(ltext, fontproperties=fontv)
     #Removes border around the legend.
    a1.draw_frame(False)
    
    plt.text(-0.1, 1.1, subplotl, transform=ax.transAxes)
    
