import courtshiplib as cl
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmn.cmn as cmn
import numpy as np
import pylab

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

    #pylab.setp(bp['medians'], color='gray')

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



def multiplot_3bars(type, fname, keyfile, errors, savefig, figname, ylim, border, ylabel, fontsz, figw, figh, figdpi, yaxisticks, ymin, barwidth, barnum, lw):

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

    matplotlib.rc('axes', linewidth=lw)
    matplotlib.rc('axes.formatter', limits = [-6, 6])

    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(fontsz)


    keylist = cmn.load_keys(keyfile)
    d = dictlat(kind, fname)


    # Defines coordinates for each bar.
    lastbar = (barnum*barwidth)-(0.5*barwidth) # X-coordinate of last bar
    x_gen1 = np.linspace(0.5*barwidth, lastbar, barnum).tolist()
    x_gen2 = [x + (lastbar + 2*barwidth) for x in x_gen1]
    x_gen2 = [x + (lastbar + 2*barwidth) for x in x_gen1]
    x_gen3 = [x + (lastbar + 2*barwidth) for x in x_gen2]
    x_list = x_gen1
    x_list.extend(x_gen2)
    x_list.extend(x_gen3)


    # Defines the colors for each bar.
    #color1 = np.tile('k', barnum-1).tolist()
    #redcol = '#B52634'
    #bluecol = '#2a77d5'
    graycol = '#c9ced4'
    #color1.append(redcol)
    colors = np.tile(graycol, 3).tolist()


    #Coordinates where the xlabels will be listed.
    truebarw = barwidth-(0.05*barwidth)
    xlabel_list = [x + truebarw/2 for x in x_list]

    # Defines limit of x axis.
    xlim = x_list[-1]+1.5*barwidth

    #Creates a figure of the indicated size and dpi.
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')


    #Plots the bar plot.
    plt.bar(x_list, means, width=truebarw, bottom=0, color=colors, ecolor='k', capsize=0.5, linewidth=lw)
    #Uncomment the line below and comment the line above to plot both positive and negative error bars.
    #plt.bar(x_list, means, width=0.9, bottom=0, color=colors, ecolor='k')

    # The following code plots only the negative error bars for negative data points and positive error bars for positive data poitns.
    ts = zip(means, stderrs)
    negerr = []
    poserr = []
    if type == 'cibdiffa':
        for t in ts:
            if t[0] < 0:
                negerr.append(t[1])
                poserr.append(0)
            if t[0] >= 0:
                negerr.append(0)
                poserr.append(t[1])

        if errors == 'stderr':
            plt.errorbar(xlabel_list, means, yerr=[negerr,poserr], fmt=None, ecolor='k', lw=lw, capsize=2)
            print(means)
            print(poserr)
        else:
            raise

    else:
    #Uncomment the lines below to plot only the positive error bars.

    #Values for negative error bars (all zeros).
        zeros = np.tile(0, len(x_list)).tolist()
        if errors == 'stderr':
            plt.errorbar(xlabel_list, means, yerr=[zeros,stderrs], fmt=None, ecolor='k', lw=lw, capsize=2)
        if errors == 'stdev':
            plt.errorbar(xlabel_list, means, yerr=[zeros,stdevs], fmt=None, ecolor='k' ,lw=lw, capsize=2)

    # Defines the axes.
    ax = plt.gca()


    if type == 'cibdiffa':
        conds2 = []
        for cond in conds:
            print(cond)
            cond = cond.replace('dtrpa1', 'dTRPA1')
            conds2.append(cond)
        conds = conds2


    # Adds labels to the x-axis at the x-coordinates specified in xlabel_list; labels are specified in the conds list.
    if type == 'gcpeakf' or type == 'gcarea' or type == 'gcdur' or type == 'dyearea':
        plt.xticks(xlabel_list, conds, fontproperties=fontv, rotation=90)

    if type == 'capdata' or type == 'freq' or type == 'volperpump' or type == 'cibdiffa' or type == '721_lof' or type == '721_gof':
        plt.xticks(xlabel_list, conds, rotation=90, fontproperties=fonti)

    if type == 'gcareapool' or type == 'gcpeakfpool' or type == 'gcdurpool' or type == 'dyeareapool':
        plt.xticks(xlabel_list, conds, fontproperties=fontv)



    # 'genlabely' and 'genline' sets the y coordinates for where the secondary genotype labels and the horizontal line above them appear.


    if type == 'cibarea':
        genlabely = -1250
        genline = -950

    if type == 'gcpeakfpool' or 'gcpeakf':
        genlabely = 100
        genline = 85

    if type == 'dyeareapool':
        #genlabely = -0.085
        genlabely = 0.3
        genline = 0.3

    if type == 'dyearea':
        #genlabely = -0.0378
        genlabely = 0.15
        genline = -0.0345

    if type == 'gcareapool' or type == 'gcarea':
        genlabely = -325
        genline = -275

    if type == 'gcdurpool':
        genlabely = 29
        genline = 29

    if type == 'gcdur':
        genlabely = 25
        genline = -5.5

    if type == 'pumps':
        genlabely = -14
        genline = -11.5



    if type == 'pumps' or type == 'cibarea':
        temps = []
        for cond in conds:
            if cond.endswith('24') == True:
                temps.append('24')
            if cond.endswith('32') == True:
                temps.append('32')
        print(conds)

        # Xlabels corresponding to the temperatures are added.
        plt.xticks(xlabel_list, temps, rotation=0, fontproperties=fontv)

        # List of genotypes are generated.
        genotypes = []
        for cond in conds:
            if '32' in cond:
                pass
            elif 'MN11+12' in cond:
                #cond = cond.replace('+12-GAL4', '\n+12-\nGAL4\n')
                cond = cond.replace('+12-GAL4', '+12-\nGAL4')
                #cond = cond.replace('+12 x', '\n+12 x\n')
                cond = cond.replace('+12 x', '+12 x\n')
                cond = cond.replace(' - 24', '')
                cond = cond.replace('-GAL4','GAL4')
                #cond = cond.replace('-','-\n')
                #cond = cond.replace('x ','x\n')
                cond = cond.replace('dtrpa1', 'dTRPA1')
                genotypes.append(cond)

            else:
                cond = cond.replace(' - 24', '')
                cond = cond.replace('-','-\n')
                cond = cond.replace('dtrpa1', 'dTRPA1')
                cond = cond.replace('x ','x\n')

                genotypes.append(cond)
        print('genotypes', genotypes)

        # Genotypes are plotted below the temperature labels.
        # Selects every even number from the x coordinate list.
        x_genotypes1 =  map(lambda i: x_list[i],filter(lambda i: i%2 == 0,range(len(x_list))))
        # Adds an extra barwidth for each x coordinate.
        x_genotypes = [x+barwidth for x in x_genotypes1]
        genotypes_x = zip(genotypes, x_genotypes)
        for item in genotypes_x:
            # Plots the genotypes at the specified coordinates (x coordinate, y coordinate, string)
            print('genlabely', genlabely)
            plt.text(item[1], genlabely, item[0], fontproperties=fonti, horizontalalignment='center', verticalalignment='top', multialignment='center',rotation=90)

        # Uncomment the lines below to draw vertical lines between the genotype names.
        #xlines1 = [x+ 2*barwidth for x in x_genotypes1]
        #xlines2 = [x_list[0], x_gen2[0], x_gen3[0]]
        #for q in [xlines1, xlines2]:
            #for x in q:
                #xv = np.tile(x, 2).tolist()
                #yv = [-16, ymin]
                 ##plt.axvline(x, 0, 1, lw=1, c='k', clip_on='False')
                #line = mpl.lines.Line2D(xv, yv, lw=1., color='k')
                #line.set_clip_on(False)
                #l = ax.add_line(line)

        # Uncomment the lines below to draw horizontal lines above the genotype names.
        for x in x_genotypes1:
            xv = [x+0.5, x + (2*barwidth-0.5)]
            yv = np.tile(genline, 2).tolist()
            #yv = [-16, ymin]
             #plt.axvline(x, 0, 1, lw=1, c='k', clip_on='False')
            line = mpl.lines.Line2D(xv, yv, lw=lw, color='k')
            line.set_clip_on(False)
            l = ax.add_line(line)

    if type == 'gcpeakfpool' or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool':
        x_genotypes1 =  map(lambda i: x_list[i],filter(lambda i: i%2 == 0,range(len(x_list))))
        # Adds an extra barwidth for each x coordinate.
        x_genotypes = [x+1.25*barwidth for x in x_genotypes1]
        genotypes_x = zip(genotypes, x_genotypes)
        for item in genotypes_x:
            # Plots the genotypes at the specified coordinates (x coordinate, y coordinate, string)
            plt.text(item[1], genlabely, item[0], fontproperties=fonti, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)

         # Uncomment the lines below to draw horizontal lines above the genotype names.
        for x in x_genotypes1:
            print(x)
            #xv = [x-0.6, x + (2.5*barwidth)+0.3]
            xv = [x, x + (2.25*barwidth)]
            yv = np.tile(genline, 2).tolist()
            #yv = [-16, ymin]
             #plt.axvline(x, 0, 1, lw=1, c='k', clip_on='False')
            line = mpl.lines.Line2D(xv, yv, lw=lw, color='k')
            line.set_clip_on(False)
            l = ax.add_line(line)

        # Writes xlabel.
        plt.xlabel('[Sucrose]', fontproperties=fontv, labelpad=4)

    if type == 'gcpeakf648' or type == 'gcdur648' or type == 'gcarea648' or type == 'dyearea648':
        plt.text(lastbar/2 + 0.75*barwidth, genlabely, 'MN11+12', fontproperties=fonti, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)

        #line = mpl.lines.Line2D([x_list[0], lastbar+barwidth], [genline, genline], lw=1., color='k')
        #line.set_clip_on(False)
        #l = ax.add_line(line)


    # Formats the yticks.
    plt.yticks(fontproperties=fontv)

    # Formats the xticks.
    if type == 'gcpeakf' or type == 'gcpeakfpool' or type == 'gcarea' or type == 'gcdur' or type == 'dyearea' or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool':
        plt.xticks(multialignment = 'center', fontproperties=fontv)

    #Uncomment lines below to display without top and right borders.
    if border == 'no':
        for loc, spine in ax.spines.iteritems():
            if loc in ['left','bottom']:
                pass
            elif loc in ['right','top']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)


    if border == 'no' and type == 'cibdiffa':
        for loc, spine in ax.spines.iteritems():
            if loc in ['left']:
                pass
            elif loc in ['right','top', 'bottom']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)


        plt.axhline(y=0, xmin=0, xmax=xlim, color='k', linewidth=1)


    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Uncomment the line below to remove all of the plot axis lines.
    #plt.setp(ax, frame_on=False)

    #Uncomment the line below to remove all tick marks/labels.
    #ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())

    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks))


    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax.get_xticklines():
        line.set_visible(False)

     #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    if type == 'freq' or type == 'volperpump' or type == 'capdata':
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(right=0.8)
        fig1.subplots_adjust(left=0.15)
        #fig1.subplots_adjust(top=0.8)

    if type == 'gcpeakf' or type == 'gcpeakfpool' or type == 'gcarea' or type == 'gcdur' or type == 'dyearea' or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool':
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(right=0.8)
        fig1.subplots_adjust(left=0.15)
        fig1.subplots_adjust(top=0.9)
        #fig1.subplots_adjust(top=0.75)


    if type == 'cibdiffa':
        fig1.subplots_adjust(left = 0.15)
        fig1.subplots_adjust(bottom=0.45)

    if type == 'pumps':
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(right=0.8)
        fig1.subplots_adjust(left=0.15)

     #Might be best to keep it all uniform.
    #fig1.subplots_adjust(left = 0.15)
    #fig1.subplots_adjust(bottom=0.4)
    #fig1.subplots_adjust(right=0.95)


    # Sets the x- and y-axis limits.
    plt.axis( [0, xlim, ymin, ylim])

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')

    #plt.title('# Pumps over 30 seconds', fontsize=20)

    # Saves the figure with the name 'figname'.
    if savefig == 'yes':
        plt.savefig(figname+'.svg', dpi=300)
        plt.savefig(figname+'.png', dpi=300)
