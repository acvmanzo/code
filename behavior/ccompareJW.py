# Script to compare courtship behavior of CS flies from Jenee's experiments
# and my experiments.

import matplotlib as mpl
import numpy as np
import os
import matplotlib.pyplot as plt

fname = 'courtship_JW.csv'
gname = 'courtship_JW_propinfomean.csv'
hname = 'courtship_JW_latinfomean.csv'

def reformatJW():
    with open(fname, 'r') as f:
        with open(gname, 'w') as g:
            with open(hname, 'w') as h:
                g.write('Genotype\tBehavior\tMean\tStdev\tSterr\tn\n')
                h.write('Genotype\tBehavior\tMean\tStdev\tSterr\tn\n')
                f.next()
                f.next()
                for l in f:
                    print repr(l)
                    genotype, f_copsuc_mean, f_copsuc_sem, f_we_mean, f_we_sem, f_copatt1_mean, 
                    f_copatt1_sem, l_copsuc_mean, l_copsuc_sem, l_we_mean, l_we_sem, 
                    l_copatt1_mean, l_copatt1_sem = l.strip('\r\n').split(',')

                    genotype = genotype + '-JW'

                    g.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(genotype, 'we', 
                        100*float(f_we_mean), 'x', 'x', 100*float(f_we_sem)))
                    g.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(genotype, 'copatt1', 
                        100*float(f_copatt1_mean), 'x', 'x', 100*float(f_copatt1_sem)))
                    g.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(genotype, 'copsuc', 
                        100*float(f_copsuc_mean), 'x', 'x', 100*float(f_copsuc_sem)))

                    h.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(genotype, 'we', l_we_mean, 
                        'x', l_we_sem, 'x'))
                    h.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(genotype, 'copatt1', 
                        l_copatt1_mean, 'x', l_copatt1_sem, 'x'))
                    h.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(genotype, 'copsuc', 
                        l_copsuc_mean, 'x', l_copsuc_sem, 'x'))
             


def loadlatdata(hname):
    with open(hname, 'r') as h:
        h.next()

        dbeh = {}
        for l in h:
            #print l
            genotype, beh, mean, stdev, sterr, n = l.strip('\n').split('\t')
            
            if beh not in dbeh:
                dbeh[beh] = {} 
                
            #if gen not in dbeh[beh]:
                #dbeh[beh][gen] = []

            dbeh[beh][genotype] = [float(mean), float(sterr)]

    return dbeh

def loadpropdata(hname):
    with open(hname, 'r') as h:
        h.next()

        dbeh = {}
        for l in h:
            #print l
            genotype, beh, mean, n, stdev, sterr = l.strip('\n').split('\t')
            
            if beh not in dbeh:
                dbeh[beh] = {} 
                
            #if gen not in dbeh[beh]:
                #dbeh[beh][gen] = []

            dbeh[beh][genotype] = [float(mean), float(sterr)]

    return dbeh


def plotdata(dlat, dprop):


    FIGW = 14 
    FIGH = 7 
    FIGDPI = 1000
    BARW = 1

    SUBPLOTNS1 = [[231, 232, 233], [234, 235, 236]]
    YLIMS1 = [[100, 400, 400], [150, 150, 150]]
    TITLES1 = [['Latency to\nwing extension', 'Latency to\nfirst copulation attempt', 
        'Latency to\ncopulation'], ['% flies displaying\nwing extension', 
        '% flies\nattempting copulation', '% flies copulating']]
    YLABEL = ['Latency (s)', '%']
    #FIGNAME = 'courtship_comparison_JW_AM_latency.png'


    fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', \
    edgecolor='k')

    keylist = ['cs-JW', 'cs', 'cg30116-JW', 'cg30116', 'fz-JW', 'fz', 'syx-JW', 'syx', 'tou-JW',
            'tou']
    behlist = ['we', 'copatt1', 'copsuc']

    fontsz = 12
    # Sets font to Arial and assigns font properties.
    fontv = mpl.font_manager.FontProperties()
    fontv = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/arial.ttf')
    fontv.set_size(fontsz)
    # Sets italicized font.
    fonti = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/ariali.ttf')
    fonti.set_size(fontsz)

    for j, d in enumerate([dlat, dprop]):
        for i, beh in enumerate(behlist):
            means = []
            sterrs = []
            for gen in keylist:
                means.append(d[beh][gen][0])
                sterrs.append(d[beh][gen][1])

            ax = plt.subplot(SUBPLOTNS1[j][i])

            print j,  beh
            print means
            print sterrs

            xvals = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14]
            xvals = [x*1.5 for x in xvals]
            xtickvals = [x + 0.5*BARW for x in xvals] 
            plt.bar(xvals, means, yerr=sterrs, width=1, color='#606060', ecolor='#606060')
            plt.xticks(xvals, keylist, rotation=90)
            
            plt.title(TITLES1[j][i])
            plt.ylabel(YLABEL[j])
            plt.ylim((0, YLIMS1[j][i]))

            # Removes borders
            for loc, spine in ax.spines.iteritems():
                if loc in ['left','bottom']:
                    pass
                elif loc in ['right','top']:
                    spine.set_color('none') # don't draw spine
                else:
                    raise ValueError('unknown spine location: %s'%loc)

            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')



    plt.tight_layout()
    plt.savefig('courtship_JW_AM_compare.png')



#reformatJW()
dlat = loadlatdata('courtship_JW_AM_latinfomean.csv')
dprop = loadpropdata('courtship_JW_AM_propinfomean.csv')
plotdata(dlat, dprop)
    
