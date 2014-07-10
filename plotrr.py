
import os
#import pylab
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
#import cmn.cmn as cmn
#import libs.genplotlib as gpl
#import libs.rstatslib as rsl
#import rpy2.robjects as robjects


def multiplot(barwidth, ymin, ylim, ylabel, yaxisticks, fontsz=9, stitlesz=10, lw=1, starpos=0.8):
    

    # ======== LOAD DATA =============


    vals = [1.0000000, 0.952381,0.1087963,0.5077160,0.7978395,0.3989198,0.9791667,1.333333]
    valsarr = np.array([1.0000000, 0.952381,0.1087963,0.5077160,0.7978395,0.3989198,0.9791667,1.333333])
    conds = ['wild type', 'Betaintnu', 'CG34127','en','Nhe3','NrxI','NrxIV','pten']
    pvals = [1, 1.0000000,float(3.435737e-10),float('6.822819e-04'),float('1.520537e-01'),float('4.357747e-05'),float('1.000000e+00'),0.2702228]
    lowercinum = np.array([0,0.5763321,0.03640119,0.32733873,0.58824737,0.23783224,0.76559003,0.8732456])
    uppercinum = ([0,1.573797,0.3251716,0.7874888,1.0821092,0.6691144,1.2523248,2.035828])

    upperci = list(uppercinum-valsarr)
    lowerci = list(valsarr-lowercinum)

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
    #ax = plt.subplot(subplotn)
    

    # =========== PLOT DATA =======================
   
    print(len(x_list), len(vals), len(lowerci), len(upperci))
    plt.bar(x_list, vals, yerr=[lowerci,upperci], width=truebarw, 
        color='#d3d3d3', bottom=0, ecolor='k', capsize=0.5, linewidth=lw)

    
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
    #t = plottitle(metric, kind)
    t = 'Relative fighting levels'

    plt.title(t, fontsize=stitlesz)
    
    # Labels the subplot
    #plt.text(-0.2, 1.0, subplotl, transform=ax.transAxes)
    
    
    # ========FORMATS THE PLOT==========

    # Removes borders
    ax = plt.gca()
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
            

FIGDPI=1200 # Figure DPI.
FIGW=4# Figure width.
#FIGW=6 # Figure width.
FIGH=2.25 #Figure height.

FONTSZ=10.5# Size of font.
LW = 1 # Width of lines in the figure.
STITLESZ=10 # Title font size.

BARWIDTH=1
YMIN=0
YLABEL =''
YAXISTICKS = 4 # Number of y-axis ticks.
YLIM = 2

fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')
multiplot(BARWIDTH, YMIN, YLIM, YLABEL, YAXISTICKS, fontsz=9, stitlesz=10, lw=1, starpos=0.8)
plt.tight_layout()
plt.savefig('rrplot.png')
