import numpy as np
import math
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
import psycopg2
from scipy import stats
import itertools
import logging


def add_berkid(sample, fpkm_path, sample_fpkm_path):
    with open(sample_fpkm_path, 'w') as g:
        with open(fpkm_path, 'r') as f:
            next(f)
            for l in f:
                newline = l.strip('\n') + '\t{0}\n'.format(sample)
                g.write(newline) 

def copy_to_dbtable(sample_fpkm_path, tablename, cur):
    cur.copy_from(open(sample_fpkm_path), tablename)

def gen_joincmd(selectlist, berkids, datatable, maxfpkm):

    selectstring = ", ".join(selectlist)
    if maxfpkm:
        mfstring = ' AND t1.fpkm < {0} AND t2.fpkm < {0}'.format(maxfpkm)
    else:
        mfstring = ''
    joincmd = "SELECT {0} FROM {1} as t0 FULL OUTER JOIN {1} as t1 USING (tracking_id) WHERE t0.berkid = '{2}' AND t1.berkid = '{3}' AND t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK'{4} ORDER BY tracking_id;".format(selectstring, datatable, berkids[0], berkids[1], mfstring)
    logging.info('%s', joincmd)
    return(joincmd)


def join_db_table(joincmd, cur):

    cur.execute(joincmd)
    jointable = np.array(cur.fetchall())
    logging.info('table length = %s', len(jointable))
    return(jointable)


def mjoin_db_table(berkidlist, selectlist, datatable, maxfpkm, cur):
    '''Input:
    samples = list of berkids to compare 
    '''
    comp_index = itertools.combinations(range(len(berkidlist)), 2) # List of indices for all pairwise comparisons of each sample.
    comparisons = []
    for i in comp_index:
        #cur = conn.cursor()
        berkids = [berkidlist[x] for x in i]
        joincmd = gen_joincmd(selectlist, berkids, datatable, maxfpkm)
        jointable = join_db_table(joincmd, cur)
        comparisons.append(jointable)
    return(comparisons)   


def get_samplename(berkid, cur):
    samplecmd = "SELECT sample FROM autin WHERE berkid = '{}'".format(berkid)
    cur.execute(samplecmd)
    sample = cur.fetchone()[0]
    return(sample)


def get_fpkm(joinedarray, selectlist):
    ''' 
    Input:
    joinedarray = an array containing the FPKM for genes in two samples; returned by join_db_table()
    '''
    array = np.transpose(joinedarray)
    colnames = selectlist
    fpkm0, fpkm1 = [array[x][:].astype(np.float) for x in [colnames.index('t0.fpkm'),colnames.index('t1.fpkm')]]
    berkid0, berkid1, = [array[x][0] for x in [colnames.index('t0.berkid'), colnames.index('t1.berkid')]]

    return([fpkm0, fpkm1], [berkid0, berkid1])

def get_correlation(fpkms):
    '''
    Input:
    '''
    slope, intercept, r, p, std_err = stats.linregress(fpkms[0], fpkms[1])
    return(r, slope, intercept)

def create_corr_file(correlationfile):
    with open(correlationfile, 'w') as g:
        g.write('berkid0\tsample0\tberkid1\tsample1\tr\tr^2\n')

def save_corr_file(r, berkid0, sample0, berkid1, sample1, correlationfile):
    with open(correlationfile, 'a') as g:
        g.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(berkid0, sample0, berkid1, sample1, r, np.square(r)))

def mcopy_to_dbtable(cuffpaths, tablename, cur, conn):

    logging.info('making tables')
    for cuffpath in cuffpaths:
        copy_to_dbtable(cuffpath, tablename, cur)
    conn.commit()

def axislim(num):
    lim = int(math.ceil(max(num))*1.1)
    return(lim)

def format_plot(berkids, samples, lim):

    xlabel = '{} {}'.format(berkids[0], samples[0])
    ylabel = '{} {}'.format(berkids[1], samples[1])
    title = 'FPKM of {} vs. {}'.format(samples[0],samples[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(0, lim)    
    plt.ylim(0, lim)
  


def plot_scatter(fpkms, berkids, samples, r, slope, intercept, subplotnum, lim): 
    
    plt.subplot(subplotnum)
    plt.scatter(fpkms[0], fpkms[1], c='k', marker='o', s=3)
    xline = range(lim)
    yline = [slope*x + intercept for x in xline] 
    plt.plot(xline, yline, c='r', ls = '--')
    textstr = 'r = {:.3f}'.format(r) 
    format_plot(berkids, samples, lim)

    ax = plt.gca()
    if subplotnum == 121:
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    ax.ticklabel_format(style='sci', scilimits=(-1,2))

def make_figname(berkids, samples, figtype):

    figname_base = '{}-{}_vs_{}-{}_{}.png'.format(samples[0], berkids[0], samples[1], berkids[1], figtype)
    return(figname_base)


def plot_hist(fpkms, berkids, samples, lim, subplotnum):

    plt.subplot(subplotnum)
    plt.hist(fpkms[0][fpkms[0]<lim], bins=50, color='r', alpha=0.5, label='{}'.format(samples[0]))
    plt.hist(fpkms[1][fpkms[1]<lim], bins=50, color='b', alpha=0.5, label='{}'.format(samples[1]))
    plt.legend()
    if subplotnum == 311:
        plt.ylim(0, 25)
    elif subplotnum == 312:
        plt.ylim(0, 200)
    elif subplotnum == 313:
        ax = plt.gca()
        ax.ticklabel_format(style='sci', scilimits=(-1,2))

    plt.ylabel('Gene number')
    plt.xlabel('FPKM')

def get_sample_correlations(cufflink_fpkm_files, cuff_table, selectlist, maxfpkm):

    logging.info('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    mcopy_to_dbtable(cufflink_fpkm_files, cuff_table, cur, conn)
    cur.close()
    
    logging.info('joining and querying tables')
    cur1 = conn.cursor()
    data = mjoin_db_table(berkidlist, selectlist, cuff_table, maxfpkm, cur1)

    logging.info('finding correlations')
    create_corr_file(corrfile)
    for array in data:
        fpkms, berkids = get_fpkm(array, SELECTLIST)
        r, slope, intercept = get_correlation(fpkms)
        samples = [get_samplename(x, cur1) for x in berkids]
        logging.info('%s', samples)
        save_corr_file(r, berkids[0], samples[0], berkids[1], samples[1], corrfile)

        logging.info('plotting scatter plots')
        fpkmlim = max([axislim(x) for x in fpkms])
        fig1 = plt.figure(figsize=(10, 5))
        plot_scatter(fpkms, berkids, samples, r, slope, intercept, 121, fpkmlim)
        plot_scatter(fpkms, berkids, samples, r, slope, intercept, 122, MAXFPKMPLOT)
        plt.tight_layout()
        plt.savefig(os.path.join(savefigdir, make_figname(berkids, samples, 'correlation')))
        plt.close()
        logging.info('plotting histograms')
        fig1 = plt.figure(figsize=(10, 10))
        plot_hist(fpkms, berkids, samples, fpkmlim, 311)
        plot_hist(fpkms, berkids, samples, MAXFPKMHIST, 312)
        plot_hist(fpkms, berkids, samples, 0.008*MAXFPKMHIST, 313)
        plt.savefig(os.path.join(savefigdir, make_figname(berkids, samples, 'hist')))
        plt.tight_layout()
        plt.close()
   
    #cur1.close()
    #conn.close()


