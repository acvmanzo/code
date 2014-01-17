import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import cmn.cmn as cmn
import sys
import os


### FUNCTIONS FOR GENERATING STANDARD CURVES AND CALCULATING EFFICIENCIES ###
def loadscdata(d, fname, selected, groupby):
    '''Loads standard curve data from a csv file with the format described 
    below into a dictionary.
    The csv file should contain the following columns:
    Well,Fluor,Label,Target,Content,Cq,Cq-no_outliers,Cq Mean,
    Cq Mean-no_outliers,Cq Std. Dev,CV,>0.17?,Starting Quantity (SQ),
    Log Starting Quantity,SQ Mean,SQ Std. Dev,Set Point,Well Note
    
    Input:
    d = dictionary to add data to
    fname = csv file containing data    
    points = 'allpoints' or 'nooutliers'
    groupby = 'plate' or 'pool'
    
    Return:
    Dictionary in which the keywords are genes and the values are 
    subdictionaries of points. Keywords in this subdictionary are the 
    the log [starting quantity], and the values are lists of Cq values.
    '''
    
    with open(fname, 'r') as f:
        f.next()
        l = f.next()
        vals = l.strip('\n').split(',')
        gene = vals[3]
    with open(fname, 'r') as f:
        f.next()
        for l in f:
            #print(l)
            vals = l.strip('\n').split(',')
            if 'NTC' in vals[4] or 'NRT' in vals[4]:
                continue
            
            logsq = '{0:.3f}'.format(float(vals[13]))
            
            # Removes the '-#' from the genotype if results are to be pooled.
            if groupby == 'pool':
                gene = vals[3].split('-')[0]
            elif groupby == 'plate':
                gene = vals[3]
            
            if gene not in d:
                d[gene] = {}
            
            if selected == 'allpoints':
                if logsq not in d[gene] and vals[5] != '':
                    d[gene][logsq] = []
                if vals[5] != '':
                    d[gene][logsq].append(np.float(vals[5]))
                            
            if selected == 'nooutliers':
                if logsq not in d[gene] and vals[6] != '':
                    d[gene][logsq] = []
                if vals[6] != '':
                    d[gene][logsq].append(np.float(vals[6]))
                #print(d[gene][xval])
    return(d)


def avgpoints(d):
    '''Averages the points in a dictionary output by loadscdata() and returns 
    a new dictionary.
    Input:
    d = dictionary, returned by the function loadscdata()
    Output:
    A dictionary in which the keywords are genes and the values are  
    subdictionaries of points. Keywords in the subdictionary are the 
    log[starting quantity] and the values are lists with the values 
    [mean, stdev, n, sterr].
        mean = mean cq
        stdev = stdev of cq
        n = number of points averaged
        sterr = standard error of the mean
    '''
    e = {}
    for k in d.iterkeys():
        e[k] = {}
        #print('firstkey', d[k])
        for x, ys in d[k].iteritems():
            mean = np.mean(ys)
            stdev = np.std(ys)
            n = len(ys)
            sterr = stdev/np.sqrt(n)
            e[k][x] = [mean, stdev, n, sterr]
    return(e)
            

def create_efile(efile):
    '''Creates a file listing the efficiencies calculated from the standard 
    curve.'''
    
    with open(efile, 'w') as g:
        g.write('Gene\tEfficiency\tr^2\tAvg\tPoints\tGroup by\n')
    
    
def write_efile(efile, params, gene, useavg, selected, groupby):
    '''Writes into a file listing the efficiencies calculated from the standard 
    curve.'''
    
    e, r2 = params['e'], params['r2']
    with open(efile, 'a') as g:
        g.write('{0}\t{1:.3f}\t{2:.3f}\t{3}\t{4}\t{5}\n'.format(gene, e, r2, useavg, 
        selected, groupby))


def fitline(logsq, cq):

    # Using np.linalg.lstsq
    #A = np.vstack([logsq, np.ones(len(logsq))]).T
    #reg = np.linalg.lstsq(A, cq)
    #m,c = reg[0]
    #r = reg[1]
    
    # Using scipy.stats.linregress    
    m, c, r, pv, stderr = stats.linregress(logsq, cq)
    e = np.power(10, (-1/m)) - 1 # Definition used by REST
    r2 = r**2
    
    params = {}
    params['logsq'] = np.array(logsq)
    params['cq'] = np.array(cq)
    params['m'] = m
    params['c'] = c
    params['e'] = e
    params['r2'] = r2
    
    return(params)


def plotstdcurve(params, gene, resdir, useavg, selected, groupby, meansterr=0):
    '''
    useavg = 'avg' or 'points'
    '''
    
    logsq, cq, m, c, e, r2 = params['logsq'], params['cq'], params['m'], \
    params['c'], params['e'], params['r2']
    
    fig = plt.figure(figsize=(5, 5), dpi=1000)
    ax = plt.gca()
    if useavg=='points':
        plt.scatter(logsq, cq, c='b')        
    if useavg=='avg':
        plt.errorbar(logsq, cq, meansterr, mfc='b', mec='b', ecolor='k', ms=7,
        elinewidth=2, barsabove='True', capsize=5, fmt='o')

    plt.plot(logsq, m*logsq+c, 'r')
    plt.ylabel('cq')
    plt.xlabel('log (starting quantity)')
    if gene == 'Itgbetanu':
        plt.text(0.05, 0.2, 'y = {0:.3f}*x+ {1:.3f}'.format(m, c), \
        transform=ax.transAxes)
        plt.text(0.05, 0.15, 'E = 10^(-1/slope) - 1 = {0:.3f}'.format(e), \
        transform=ax.transAxes)
        plt.text(0.05, 0.1, 'r^2 = {0:.3f}'.format(r2), transform=ax.transAxes)
    else:
        plt.text(0.3, 0.9, 'y = {0:.3f}*x+ {1:.3f}'.format(m, c), \
        transform=ax.transAxes)
        plt.text(0.3, 0.85, 'E = 10^(-1/slope) - 1 = {0:.3f}'.format(e), \
        transform=ax.transAxes)
        plt.text(0.3, 0.8, 'r^2 = {0:.3f}'.format(r2), transform=ax.transAxes)
    
    plt.title(gene)
    plt.ylim(15, 40)
    
    plt.tight_layout()
    figname = resdir+'sc_'+gene+'_'+useavg+'_'+selected+'_'+groupby
    plt.savefig(figname)
    plt.close()

def convertpoints(d):
    '''Convert the dictionary output of loadscdata() to another dictionary 
    used as input to plotstdcurve().
    Input: 
    d = output of loadscdata()
    Output:
    A dictionary in which each keyword is a genotype and the values are 
    comprised of two lists; the first list contains the log[starting 
    quantity] values and the second list contains the Cq values.    
    '''    
    e = {}
    for k in d.iterkeys():
        a = []
        b = []
        for x, ys in d[k].iteritems():
            a.extend(np.tile(float(x), len(ys)))
            b.extend(ys)
        e[k] = (a, b)
    return(e)

def convertavg(d):
    '''Convert the dictionary output of avgpoints() to another dictionary 
    used as input to plotstdcurve().
    Input: 
    d = output of avgpoints()
    Output:
    A dictionary in which each keyword is a genotype and the values are 
    comprised of three lists; the first list contains the log[starting 
    quantity] values; the second list contains the average Cq values, and the 
    third list contains the standard error of the average Cq values.
    '''       
    e = {}
    for k in d.iterkeys():
        print(k)
        x = []
        y = []
        sterr = []
        for xlab, meanparams in d[k].iteritems():
            x.append(float(xlab))
            y.append(meanparams[0])
            sterr.append(meanparams[3])
        e[k] = (x, y, sterr)
    return(e)


def getsc(d, useavg, selected, groupby):
    if useavg == 'avg':
        avgd = avgpoints(d)
        plotdict = convertavg(avgd)
    
    if useavg == 'points':
        plotdict = convertpoints(d)

    resdir = 'results/'+useavg+'_'+selected+'_'+groupby+'/'
    cmn.makenewdir(resdir)
    efile = resdir + 'efficiencies_'+useavg+'_'+selected+'_'+groupby+'.txt'
    create_efile(efile)
    
    for k, v in plotdict.iteritems():
        logsq = v[0]
        cq = v[1]
        if useavg == 'avg':
            meansterr = v[2]
        if useavg == 'points':
            meansterr = 0
        params = fitline(logsq, cq)        
        plotstdcurve(params, k, resdir, useavg, selected, 
        groupby, meansterr)
        write_efile(efile, params, k, useavg, selected, groupby)

