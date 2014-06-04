# This library contains functions for analyzing qRT-PCR data.

import glob
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import cmn.cmn as cmn
import sys
import os
import psycopg2


REFERENCE = 'GAPDH'
MUTRESDIR = '/home/andrea/Documents/lab/qRT-PCR/2_results/mut/'

### ACCESSING DATABASE ###

conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

### FUNCTIONS FOR GENERATING STANDARD CURVES AND CALCULATING EFFICIENCIES ###

def primertogene():
    d = {}
    cur.execute("SELECT gene, primer FROM qpcr_primers WHERE primer is not Null ORDER BY gene;")
    allrows = cur.fetchall()
    for r in allrows:
        d[r[1]] = r[0]
    
    d['cg34127-gp1'] = 'CG34127'
    d['nrxi-gp1'] = 'NrxI'
    d['betaintnu3'] = 'Bintnu'
    d['bintnu-M'] = 'Bintnu'
    d['pten-R'] = 'pten'
    d['pten-Ryan'] = 'pten' 
    d['NrxI-Takeo'] = 'NrxI' 
    d['bintnu-gp1'] = 'Bintnu'
    d['Nhe3'] = 'Nhe3'
    d['NrXIV'] = 'NrxIV'
    d['en3'] = 'En'
    d['NrxIV-Ralph'] = 'NrxIV'
    d['en-Diana'] = 'En'
    d['Nhe3-Dhruv'] = 'Nhe3'
    
    #print d
    return d


def loadscdata(d, fname):
    '''Loads standard curve data from a csv file with the format described 
    below into a dictionary.
    The csv file should contain the following columns: blank,
    Well,Fluor,Label,Target,Content,Sample, Biological Set Name, Cq, Cq Mean,
    Starting Quantity (SQ), Log Starting Quantity,SQ Mean,SQ Std. Dev,Set Point,Well Note
    
    Input:
    d = dictionary to add data to
    fname = csv file containing data    
    
    Return:
    Dictionary in which the keywords are targets and the values are 
    subdictionaries of points. Keywords in this subdictionary are the 
    the log [starting quantity], and the values are lists of Cq values.
    '''
    
    date = os.path.basename(fname)[:11]
    
    #with open(fname, 'r') as f:
        #f.next()
        #l = f.next()
        #vals = l.strip('\n').split(',')
        #target = vals[3]
        
    with open(fname, 'r') as f:
        f.next()
        for l in f:
            #print(l)
            blank, well, fluor, target, content, sample, bset, cq, cqmean, cqsd, sq, logsq, sqmean, sqsd, setpoint, wellnote = l.strip('\n').split(',')
            if 'NTC' in content or 'NRT' in content:
                continue
            
            logsq = '{0:.3f}'.format(float(logsq))
            target = target + '_' + date
            
            if target not in d:
                d[target] = {}
            if logsq not in d[target] and (cqmean != '' or cqmean != '0'):
                d[target][logsq] = []
            if cq != '':
                d[target][logsq].append(np.float(cq))
                            

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
            if not ys:
                continue
            mean = np.mean(ys)
            stdev = np.std(ys)
            n = len(ys)
            sterr = stdev/np.sqrt(n)
            e[k][x] = [mean, stdev, n, sterr]
    #print 'avgd', e
    return(e)
            

def create_efile(efile):
    '''Creates a file listing the efficiencies calculated from the standard 
    curve.'''
    
    with open(efile, 'w') as g:
        g.write('Gene\tEfficiency\tr^2\tAvg\tPoints\tGroup by\n')
    
    
def write_efile(efile, params, gene, useavg, groupby):
    '''Writes into a file listing the efficiencies calculated from the standard 
    curve.'''
    
    e, r2 = params['e'], params['r2']
    with open(efile, 'a') as g:
        g.write('{0}\t{1:.3f}\t{2:.3f}\t{3}\t{4}\n'.format(gene, e, r2, useavg, groupby))


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


def plotstdcurve(params, target, resdir, useavg, groupby, primertogenedict,  meansterr=0):
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
    
    gene = primertogene()[target.split('_')[0]]
    
    if gene == 'Bintnu':
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
    
    plt.title(gene+'_'+target)
    plt.ylim(15, 40)
    
    plt.tight_layout()
    figname = resdir+gene+'_'+target+'_'+useavg+'_'+groupby
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
    id = output of avgpoints()
    Output:
    A dictionary in which each keyword is a genotype and the values are 
    comprised of three lists; the first list contains the log[starting 
    quantity] values; the second list contains the average Cq values, and the 
    third list contains the standard error of the average Cq values.
    '''       
    e = {}
    for k in d.iterkeys():
        #print(k)
        x = []
        y = []
        sterr = []
        for xlab, meanparams in d[k].iteritems():
            x.append(float(xlab))
            y.append(meanparams[0])
            sterr.append(meanparams[3])
        e[k] = (x, y, sterr)
    return(e)


def platetopool(d):
    
    e = {}
    for target, dvals in d.iteritems():
        newtarget = target.split('_')[0]
        if newtarget not in e:
            e[newtarget] = {}
        #print dvals
        for logsq, cqs in dvals.iteritems():
            if logsq not in e[newtarget]:
                e[newtarget][logsq] = []
            e[newtarget][logsq].extend(cqs)
            
    return(e)

def getsc(d, useavg, groupby):
    
    if groupby == 'pool':
        d = platetopool(d)
    
    if useavg == 'avg':
        avgd = avgpoints(d)
        plotdict = convertavg(avgd)
    
    if useavg == 'points':
        plotdict = convertpoints(d)

    scdir = os.path.basename(os.path.abspath('.'))
    resdir = '{0}{1}/{2}_{3}/'.format(MUTRESDIR, scdir, useavg, groupby)
    cmn.makenewdir(resdir)
    efile = resdir + 'efficiencies_'+useavg+'_'+groupby+'.txt'
    create_efile(efile)
    
    for k, v in plotdict.iteritems():
        print k
        logsq = v[0]
        cq = v[1]
        if useavg == 'avg':
            meansterr = v[2]
        if useavg == 'points':
            meansterr = 0
        params = fitline(logsq, cq)
  
        plotstdcurve(params, k, resdir, useavg, groupby, meansterr)
        write_efile(efile, params, k, useavg, groupby)

### FUNCTIONS FOR TESTING MUTANT VS CONTROL GENE EXPRESSION ###

def combinedata(gname, datadir='.'):
    '''Combines csv files in the datadir directory into one csv file with the following columns:
    DataID,Date,Well,Target,Content,Sample,Cq'''

    os.chdir(datadir)
    fnames = sorted(glob.glob('*.csv'))
    #gname = os.path.dirname(os.path.abspath('.')) + '/2014-0408_alldata_fmt.csv'

    dataid = 999
    with open(gname, 'w') as g:
        g.write('DataID,Date,Expt,Well,Target,Content,Sample,Cq\n')
        for fname in fnames:
            date = fname.split('_')[0][:7] + '-' + fname.split('_')[0][7:]
            exptid = fname.split('_mut_')[0]
            with open(fname, 'r') as f:
                    for l in f:
                        dataid = dataid + 1
                        blank, well, fluor, target, content, sample, biolset, cq, cqmean, cqstd = l.split(',')[:10]
                        if well == 'Well':
                            continue
                        newlist = [str(dataid), date, exptid, well, target, content, sample, cq]
                        newline = ','.join(newlist) + '\n'
                        g.write(newline)


def get_good_primers():
    '''Get list of primers I chose.'''
    dp2g = primertogene()
    cur.execute("select primer from qpcr_primers where used_primer is True;")
    primerlist = [p[0] for p in cur.fetchall()]
    return primerlist


def get_good_exptd():
    '''Get list of experiment dates with useful data.'''
    cur.execute("select exptd from qpcr_experiments where usedata is True;")
    exptlist = [e[0].isoformat() for e in cur.fetchall()] 
    return set(exptlist)


def get_targets(exptid):
    '''For the experiment in exptid, get a list of targets (i.e., primers).'''
    cur.execute("SELECT target FROM qpcr_mut WHERE exptid = '{0}';".format(exptid))
    targets = [t[0] for t in cur.fetchall()]
    uniquet = set(targets)
    return uniquet
    
def getcqdict(gensqlstring, targetlist, exptid):
    '''Generates a dictionary where the keys are the targets (primers) and the values are the Cq values. Cq values are 
    retrieved from a postgres database.
    Input:
    gensqlstring = sql command string specifying the search parameters; generated by the functions sqlsearch_t_ref_CS(),
    sqlsearch_t_mut(), and sqlsearch_ref_mut
    targetlist = list of primers/targets
    '''
    
    goodexpts = ', '.join(["'{0}'".format(x) for x in get_good_exptd()])
    #print 'goodexpts', goodexpts
    d = {}
    for t in targetlist:
        print t
        gene = primertogene()[t]
        cur.execute(gensqlstring(exptid, t, gene, goodexpts))
        d[t] = [cq[0] for cq in cur.fetchall()]
    return d


def sqlsearch_t_ref_CS(exptid, t, gene, goodexpts):
    '''Generates a sql search string to find the CQs of target and reference gene expression in CS flies.
    Input:
    exptid = exptid of the experiment
    t = target
    gene = gene (found from the target by the function primertogene())
    goodexpts = list of experiment dates that gave conclusive results
    Output:
    string
    '''

    sqlsearch = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* 'CS' AND exptd in ({2});".format(exptid, t, goodexpts)
    return sqlsearch


def sqlsearch_t_mut(exptid, t, gene, goodexpts):
    '''Generates a sql search string to find the CQs of target gene expression in mutant flies.
    Input:
    exptid = exptid of the experiment
    t = target
    gene = gene (found from the target by the function primertogene())
    goodexpts = list of experiment dates that gave conclusive results
    Output:
    string
    '''

    sqlsearch = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}' AND exptd in ({3});".format(exptid, t, gene, goodexpts)
    return sqlsearch


def sqlsearch_ref_mut(exptid, t, gene, goodexpts):
    '''Generates a sql search string to find the CQs of reference gene expression in mutant flies.
    Input:
    exptid = exptid of the experiment
    t = target
    gene = gene (found from the target by the function primertogene())
    goodexpts = list of experiment dates that gave conclusive results
    Output:
    string
    '''

    sqlsearch = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}' AND exptd in ({3});".format(exptid, REFERENCE, gene, goodexpts)
    return sqlsearch
    

def write_t_ref_CS(d_t_ref_CS, exptid):
    '''Writes the reference gene and target gene CQs in CS flies to a file.
    Input:
    d_t_ref_CS: dictionary generated by the getcqdict(sqlsearch_t_ref_CS) function
    '''
    
    ref_CS = d_t_ref_CS[REFERENCE]
    for t in d_t_ref_CS:
        if t == 'GAPDH':
            continue
        gname = MUTRESDIR + '{0}_{1}_{2}_cs.txt'.format(t, REFERENCE, exptid)
        with open(gname, 'w') as g:
            g.write('{0}_Ref_cq\t{1}_T_cq\n'.format(REFERENCE, t))
            mut_CS = d_t_ref_CS[t]
            ref_mut_CS = zip(ref_CS, mut_CS)
            for rcq, mcq in ref_mut_CS:
                g.write('{0}\t{1}\n'.format(rcq, mcq))

def write_t_ref_mut(d_t_mut, d_ref_mut, exptid):
    '''Writing the reference gene and target gene CQs in mutant flies to a file.
    Input:
    d_t_mut = dictionary generated by the getcqdict(sqlsearch_t_mut) function
    d_ref_mut = dictionary generated by the getcqdict(sqlsearch_ref_mut) function'''

    for t in d_t_mut.keys():
        if t == 'GAPDH':
            continue
        gname = MUTRESDIR + '{0}_{1}_{2}_mut.txt'.format(t, REFERENCE, exptid)
        with open(gname, 'w') as g:
            g.write('{0}_Ref_cq\t{1}_T_cq\n'.format(REFERENCE, t))
            gene = primertogene()[t]
            ref_mut = d_ref_mut[t]
            mut_mut = d_t_mut[t]
            ref_mut_mut = zip(ref_mut, mut_mut)
            for rcq, mcq in ref_mut_mut:                
                g.write('{0}\t{1}\n'.format(rcq, mcq))


def batch_write_cqs(csvdir):
    '''Function for writing files with the CQs of target and reference genes for both mutant and control samples
    (separate files)
    '''

    os.chdir(csvdir) 
    fnames = glob.glob('*.csv')
    for fname in fnames:
        exptid = fname.split('_mut_')[0]
        targets = get_targets(exptid)
        write_t_ref_CS(getcqdict(sqlsearch_t_ref_CS, targets, exptid), exptid)
        d_ref_mut = getcqdict(sqlsearch_ref_mut, targets, exptid)
        d_t_mut = getcqdict(sqlsearch_t_mut, targets, exptid)
        write_t_ref_mut(d_t_mut, d_ref_mut, exptid)

#batch_write_cqs('.')
#def getcqdict_t_ref_CS():
    #getcqdict(
#ss_cs_cq = "SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* 'CS' AND usedata = True;".format(exptid, t)
#d_cs_cq = getcqdict(ss_cs_cq, uniquet)
#print d_cs_cq


#d_mut_cq = {}
#for t in uniquet:
    #gene = dp2g[t]
    #if gene == 'GAPDH':
        #continue
    #cur.execute("SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptid, t, gene))
    #d_mut_cq[t] = [cq[0] for cq in cur.fetchall()]
#print 'Target genes, mutant flies', d_mut_cq

 #Getting CQs of reference gene expression in mutant flies.
#d_ref_mut_cq = {}
#for t in uniquet:
    #gene = dp2g[t]
    #if gene == 'GAPDH':
        #continue
    #cur.execute("SELECT cq FROM qpcr_mut WHERE exptid = '{0}' AND target = '{1}' AND sample ~* '{2}';".format(exptid, reference, gene))
    #d_ref_mut_cq[gene] = [cq[0] for cq in cur.fetchall()]

#print 'Ref gene, mutant flies', d_ref_mut_cq
