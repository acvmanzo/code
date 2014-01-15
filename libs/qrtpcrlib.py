import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import cmn.cmn as cmn
import sys


#graphtype = sys.argv[1]

GRAPHTYPES = ['allpoints', 'avgpoints', 'no_outliers', 'avg+no_outliers']
for graphtype in GRAPHTYPES:
    print('GRAPHTYPE', graphtype)

    if graphtype == 'allpoints':
        RESDIR = 'allpoints/'

    if graphtype == 'avgpoints':
        RESDIR = 'avgpoints/'

    if graphtype == 'no_outliers':
        RESDIR = 'no_outliers/'
        
    if graphtype == 'avg+no_outliers':
        RESDIR = 'avg+no_outliers/'

    FNAMES = ['sc_nhe3_en_rev.csv', 'sc_bintnu_cg34127.csv', 
    'sc_gapdh_pten_nrxiv_nrxi.csv', 'sc_gapdh.csv']
    #FNAMES = ['sc_nhe3_en_rev.csv']

    cmn.makenewdir(RESDIR)
    efile = RESDIR+'efficiencies.txt'
    with open(efile, 'w') as g:
            g.write('Gene\tEfficiency\tr^2\n')

    for fname in FNAMES:
        content = 'x'
        d = {}
        with open(fname, 'r') as f:
            f.next()
            for l in f:
                #print(l)
                vals = l.strip('\n').split(',')
                gene = vals[3]
                #print(gene)
                if gene == '':
                    continue
                if gene not in d:
                    d[gene] = []
                    #d[gene]['points'] = []
                
                if graphtype == 'allpoints':
                    try:
                        cq = np.float(vals[5])
                    except ValueError:
                        continue
                
                if graphtype == 'no_outliers':
                    try:
                        cq = np.float(vals[6])
                    except ValueError:
                        continue
                
                if graphtype == 'avgpoints':
                    #print(l)
                    #print(vals[4] != content)
                    if vals[4] != content:
                        try:
                            cq = np.float(vals[7])
                        except ValueError:
                            continue
                    else:
                        continue
                    content = vals[4]

                if graphtype == 'avg+no_outliers':
                    if vals[4] != content:
                        try:
                            cq = np.float(vals[8])
                        except ValueError:
                            continue
                    else:
                        continue
                    content = vals[4]
                
                try:
                    logsq = np.float(vals[13])
                except ValueError:
                    continue
                
                d[gene].append((cq, logsq))

        #print(d)

        for k, v in d.iteritems():
            print(k)
            cq = np.array(zip(*v)[0])
            logsq = np.array(zip(*v)[1])
            # Using np.linalg.lstsq
            #A = np.vstack([logsq, np.ones(len(logsq))]).T
            #reg = np.linalg.lstsq(A, cq)
            #m,c = reg[0]
            #r = reg[1]
            
            # Using scipy.stats.linregress
            m, c, r, pv, stderr = stats.linregress(logsq, cq)
            e = np.power(10, (-1/m)) - 1 # Definition used by REST
            r2 = r**2
            #print(k, m, c, e, r2) 
            
            
            fig = plt.figure(figsize=(5, 5), dpi=1000)
            ax = plt.gca()
            plt.scatter(logsq, cq)
            plt.plot(logsq, m*logsq+c, 'r')
            plt.ylabel('cq')
            plt.xlabel('log (starting quantity)')
            if k == 'Itgbetanu':
                plt.text(0.05, 0.2, 'y = {0:.3f}*x+ {1:.3f}'.format(m, c), transform=ax.transAxes)
                plt.text(0.05, 0.15, 'E = 10^(-1/slope) - 1 = {0:.3f}'.format(e), transform=ax.transAxes)
                plt.text(0.05, 0.1, 'r^2 = {0:.3f}'.format(r2), transform=ax.transAxes)
            else:
                plt.text(0.3, 0.9, 'y = {0:.3f}*x+ {1:.3f}'.format(m, c), transform=ax.transAxes)
                plt.text(0.3, 0.85, 'E = 10^(-1/slope) - 1 = {0:.3f}'.format(e), transform=ax.transAxes)
                plt.text(0.3, 0.8, 'r^2 = {0:.3f}'.format(r2), transform=ax.transAxes)
            
            plt.title(k)
            plt.ylim(15, 40)
            
            plt.tight_layout()
            plt.savefig(RESDIR+'stdcurve_'+k)
            plt.close()
            

            with open(efile, 'a') as g:
                g.write('{0}\t{1:.3f}\t{2:.3f}\n'.format(k, e, r2))
