#This script extracts data from the REST output files so that I can plot
#it using matplotlib.

import os
import libs.genplotlib as gpl
import numpy as np
import itertools
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl


def get_rest_dict(restdir='.'):
    os.chdir(restdir)
    fnames = glob.glob('*.mht')
    #fname = '/home/andrea/Documents/lab/qRT-PCR/3_analysis/rest/bintnu-GP1.mht'

    d = {}
    for fname in fnames:
        with open(fname, 'r') as f:
            
            #samples = list(itertools.dropwhile(lambda x: x !='Legend:<BR><i>P(H1) - Probability of alternate\n', \
            #itertools.takewhile(lambda x: x !='Result<th>\n', f)))
            #samples = list(itertools.takewhile(lambda x: x !='Legend:<BR><i>P(H1) - Probability of alternate\r\n', \
                #itertools.dropwhile(lambda x: x !='Result<th>\r\n', f)))

            data = list(itertools.dropwhile(lambda x: x !='Result</th>\r\n', itertools.takewhile(lambda x: x !=  
                'Legend:<BR><i>P(H1) - Probability of alternate \r\n', f)))
            #for s in samples:
                #print s
            #data = list(itertools.takewhile(lambda x: x == '<TD valign=3Dtop align=3D"left">', f))
            #print data

        newdata = []
        for da in data:
            #print 'old', da
            nd =  da.rstrip('</TD>\r\n').replace('<TD valign=3Dtop align=3D"left"> ', '').replace('<TD valign=3Dtop align=3D"right"> ', '')
            #print 'new', nd
            newdata.append(nd)    
        #print 'new', newdata
        #target, result = newdata[13], newdata[20]
        #targetexp, pval = [float(x) for x in [newdata[16],  newdata[19]]]
        #stderr = [float(x) for x in newdata[17].split(' - ')]
        #ci95 = [float(x) for x in newdata[18].split(' - ')]

        target, result = [newdata[13], newdata[20]]
        if result == '&nbsp;':
            result = 'UNCHANGED'
        #print target 
        d[target] = {}
        d[target]['result'] = result
        d[target]['exp'], d[target]['pval'] = [float(x) for x in [newdata[16],  newdata[19]]]
        d[target]['sterr'] = [float(x) for x in newdata[17].split(' - ')]
        d[target]['ci95'] = [float(x) for x in newdata[18].split(' - ')]

    #print d.keys()
#    for k in d.keys():
        #print k, d[k]

    return d

def plot_rest(d, figname, figw=6, figh=4, ylim=20):

    # Plot properties.
    figdpi = 1000
    fontsz = 12 
    lw = 1
    barcolor = '#3299CC'
    barwidth = 1
    yaxisticks = 5
    #hlinecolor = '#BB2A3C' 
    hlinecolor = 'k' 

    # Sets font to Arial and assigns font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/arial.ttf')
    fontv.set_size(fontsz)
    # Sets italicized font.
    fonti = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/ariali.ttf')
    fonti.set_size(fontsz)

    # Load plot data.
    xticks = sorted(d.keys(), key=lambda s: s.lower())
    xvals = range(1, len(xticks)*2, barwidth*2)
    xtickvals = [float(x) + float(barwidth)/2 for x in xvals]
    yvals = [d[k]['exp'] for k in xticks]
    sterrlim = [(d[k]['sterr']) for k in xticks]
    lsterrlim, usterrlim = zip(*sterrlim)
    lsterr = np.array(yvals)-np.array(lsterrlim)
    usterr = np.array(usterrlim) - np.array(yvals)
    #print lsterr, usterr
    pvals = [d[k]['pval'] for k in xticks]
    #print xticks
    #print 'xvals', xvals
    #print 'xtickvals', xtickvals
    #print yvals
    #print sterrlim

    # Plot bar plot.
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    plt.bar(xvals, yvals, width=1, color='w', edgecolor='w', log=True)
    ax = plt.gca()
    plt.errorbar(xtickvals, yvals, yerr=[lsterr, usterr], mfc='k', mec='k', ecolor='k', ms=7,
    elinewidth=1, barsabove='True', capsize=3, fmt='o')

    # Adds labels to the x-axis at the x-coordinates specified in xtickvals; labels are specified in the conds list
    plt.xticks(xtickvals, xticks, fontproperties=fonti, rotation=45)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel('Fold change', labelpad=2, fontproperties=fontv, multialignment='center')

    # Title
    #plt.title('Expression change in autism mutants')

    # Removes borders
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)

    # Sets the x- and y-axis limits.
    xlim = xvals[-1]+1.5*barwidth
    plt.axis([0, xlim, 0.3, ylim])


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
    #ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(yaxisticks))
    #ax.axis([1, 10000, 1, 100000])
    #ax.loglog())
    #ax.set_yscale('log')
    #ax.set_yticks([0.5, 1, 2])
    ax.set_yscale('log')
    ax.set_yticks([0.2, 0.5, 1, 2, 5, 10, 20]) 
    ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    
    # ========ADDS SIGNIFICANCE STARS============

    #print('pvals',pvals)

    p05i = [i for i, pval in enumerate(pvals) if pval <0.05 and pval >= 0.01]

    relpos = 0.9
    #print(p05i)
    for i in p05i:
        plt.text(xtickvals[i], relpos*ylim, '*', horizontalalignment='center', 
        fontsize=fontsz)

    p01i = [i for i, pval in enumerate(pvals) if pval <0.01 and pval >= 0.001]
    #print(p01i)
    for i in p01i:
        plt.text(xtickvals[i], relpos*ylim, '**', horizontalalignment='center', 
        fontsize=fontsz)

    p001i = [i for i, pval in enumerate(pvals) if pval <0.001]
    #print(p001i)
    for i in p001i:
        plt.text(xtickvals[i], relpos*ylim, '***', horizontalalignment='center', 
        fontsize=fontsz)

    # Draw a horizontal line at y = 1.
    plt.axhline(y=1, lw=1, color=hlinecolor, ls='--')
    #plt.show()

    # Saves figure.
    plt.tight_layout()
    plt.savefig('../'+figname)


def write_rest_info(d, outfile):
    '''Write the results of the REST analysis into one file
    Input:
    d = dictionary returned by get_rest_dict()
    outfile = name of output file
    '''
    with open(outfile, 'w') as f:
        f.write('Genotype,ExprRatio,pval,ci95lower,ci95upper,sterrlower,sterrupper\n')
    with open(outfile, 'a') as f:
        for gene, v in d.iteritems():
            f.write('{},{},{},{},{},{},{}\n'.format(gene, v['exp'], v['pval'], v['ci95'][0], v['ci95'][1], v['sterr'][0], v['sterr'][1]))



c = get_rest_dict()
print c
#d = {}
#e = {}
#for k, v in c.iteritems():
    #if v['exp'] > 2:
        #e[k]=v
    #else:
        #d[k] = v
#plot_rest(e, 'qpcr_rest_data_high.png', figw=3, figh=4, ylim=11)
#plot_rest(d, 'qpcr_rest_data_low.png', ylim=3)
plot_rest(c, 'qpcr_rest_data_all.png', ylim=20)
write_rest_info(c, '../qpcr_rest_data_all.txt')
