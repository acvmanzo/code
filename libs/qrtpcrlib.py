import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import cmn.cmn as cmn
import sys


#graphtype = sys.argv[1]

#GRAPHTYPES = ['allpoints', 'avgpoints', 'no_outliers', 'avg+no_outliers']
GRAPHTYPES = ['avg+no_outliers']
#GRAPHTYPES = ['avgpoints']
FNAMES = ['sc_nhe3_en_rev.csv', 'sc_bintnu_cg34127.csv', \
'sc_gapdh_pten_nrxiv_nrxi.csv', 'sc_gapdh.csv']
FNAMES = ['sc_bintnu_cg34127.csv']



def defresdir(graphtype):
    if graphtype == 'allpoints':
        resdir = 'allpoints/'

    if graphtype == 'avgpoints':
        resdir = 'avgpoints/'

    if graphtype == 'no_outliers':
        resdir = 'no_outliers/'
        
    if graphtype == 'avg+no_outliers':
        resdir = 'avg+no_outliers/'
        
    cmn.makenewdir(resdir)
    return(resdir)

def usepoints(datalist, vals, cqindex, logsqindex):
    
    if vals[cqindex] != '':
        cq = np.float(vals[cqindex])
        logsq = np.float(vals[logsqindex])
        datalist.append((cq, logsq))

def loaddata(fname, graphtype):
    d = {}
    cqs = []
    logsqs = []
    with open(fname, 'r') as f:
        f.next()
        l = f.next()
        vals = l.strip('\n').split(',')
        content = vals[4]
        gene = vals[3]
    with open(fname, 'r') as f:
        f.next()
        for l in f:
            print(l)
            vals = l.strip('\n').split(',')
            gene = vals[3]
            
            if gene not in d:
                d[gene] = []
                    
            if graphtype == 'allpoints':
                usepoints(d[gene], vals, 5, 13)
                            
            if graphtype == 'no_outliers':
                usepoints(d[gene], vals, 6, 13)
            
            if graphtype == 'avgpoints':
                if vals[4] == content:
                    if vals[5] != '':
                        cqs.append(np.float(vals[5]))
                        logsqs.append(np.float(vals[13]))
                    if vals[5] == '':
                        continue
                elif vals[4] != content:
                    if cqs:
                        cq = np.mean(cqs)
                        logsq = np.mean(logsqs)
                        d[oldgene].append((cq, logsq))
                        cqs = []
                        logsqs = []
                    if vals[5] != '':
                        cqs.append(np.float(vals[5]))
                        logsqs.append(np.float(vals[13]))
                content = vals[4]
                oldgene = vals[3]

            if graphtype == 'avg+no_outliers':
                print('cqs', cqs)
                print('logsqs', logsqs)
                print(vals[4], content)
                if vals[4] == content:
                    if vals[6] != '':
                        cqs.append(np.float(vals[6]))
                        logsqs.append(np.float(vals[13]))
                    if vals[6] == '':
                        continue
                elif vals[4] != content:
                    if cqs:
                        cq = np.mean(cqs)
                        logsq = np.mean(logsqs)
                        d[oldgene].append((cq, logsq))
                        cqs = []
                        logsqs = []
                    if vals[6] != '':
                        cqs.append(np.float(vals[6]))
                        logsqs.append(np.float(vals[13]))
                content = vals[4]
                oldgene = vals[3]
    
    
    if graphtype == 'avgpoints' or graphtype == 'avg+no_outliers':
        cq = np.mean(cqs)
        logsq = np.mean(logsqs)
        d[gene].append((cq, logsq))
    return(d)


def create_efile(efile):
    with open(efile, 'w') as g:
        g.write('Gene\tEfficiency\tr^2\n')
    
    
def write_efile(efile, params, gene):
    e, r2 = params['e'], params['r2']
    with open(efile, 'a') as g:
        g.write('{0}\t{1:.3f}\t{2:.3f}\n'.format(gene, e, r2))


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
    params['logsq'] = logsq
    params['cq'] = cq
    params['m'] = m
    params['c'] = c
    params['e'] = e
    params['r2'] = r2
    
    return(params)


def plotstdcurve(params, gene, resdir, graphtype):
    
    logsq, cq, m, c, e, r2 = params['logsq'], params['cq'], params['m'], \
    params['c'], params['e'], params['r2']
    
    fig = plt.figure(figsize=(5, 5), dpi=1000)
    ax = plt.gca()
    plt.scatter(logsq, cq)
    plt.plot(logsq, m*logsq+c, 'r')
    plt.ylabel('cq')
    plt.xlabel('log (starting quantity)')
    if k == 'Itgbetanu':
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
    plt.savefig(resdir+'stdcurve_'+gene+'_'+graphtype)
    plt.close()
    

for graphtype in GRAPHTYPES:
    print('GRAPHTYPE', graphtype)
    efile = defresdir(graphtype)+'efficiencies_'+graphtype+'.txt'
    create_efile(efile)
    for fname in FNAMES:
        print(fname)
        d = loaddata(fname, graphtype)
        print(d)
        for k, v in d.iteritems():
            print(k)
            cq = np.array(zip(*v)[0])
            logsq = np.array(zip(*v)[1])
            params = fitline(logsq, cq)
            plotstdcurve(params, k, defresdir(graphtype), graphtype)
            write_efile(efile, params, k)





