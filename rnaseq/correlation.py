import numpy as np
import math
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
import psycopg2
from scipy import stats
import itertools
import cProfile
import pstats


#CUFF_TABLE_PREFIX = 'cuff_genes_fpkm'
CUFF_TABLE = 'cufflinks_data'
SELECTLIST = ['t0.tracking_id', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 't1.berkid', 't1.fpkm', 't1.fpkm_status']
MAXFPKM = False
MAXFPKMPLOT = 2000
MAXFPKMHIST= 2000


def get_cuff_info(cuffpath):
    cuffpath = os.path.abspath(cuffpath)
    sample = cuffpath.split('/')[6].split('_')[1]
    cufffile = os.path.join(cuffpath, 'genes.fpkm_tracking')
    newcufffile = os.path.join(cuffpath, 'genes_sample.fpkm_tracking')
    return(sample, cufffile, newcufffile)

def add_berkid(cuffpath):
    sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    with open(newcufffile, 'w') as g:
        with open(cufffile, 'r') as f:
            next(f)
            for l in f:
                newline = l.strip('\n') + '\t{0}\n'.format(sample)
                g.write(newline) 

#for cuffpath in cuffpaths:
    #add_id(cuffpath) 

#def make_db_table(cuffpath, cur):
    #os.chdir(cuffpath)
    #sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    #table_name = '{0}_{1}'.format(CUFF_TABLE_PREFIX, sample) 
    #tablecmd_create = 'DROP TABLE IF EXISTS {0} CASCADE; CREATE TABLE {0} (tracking_id character varying(20), class_code character varying(2), nearest_ref_id character varying(2), gene_id character varying(20), gene_short_name character varying(100), tss_id character varying(2), locus character varying(100), length character varying(2), coverage character varying(2), FPKM double precision , FPKM_conf_lo double precision, FPKM_conf_hi double precision, FPKM_status character varying(5), berkid character varying(20));'.format(table_name)
    ##print(tablecmd_create)
    #cur.execute("{0}".format(tablecmd_create))
    #cur.copy_from(open(newcufffile), table_name)

def copy_to_dbtable(cuffpath, tablename, cur):
    os.chdir(cuffpath)
    sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    cur.copy_from(open(newcufffile), tablename)

def gen_joincmd(selectlist, berkids, datatable, maxfpkm):
    #selectlist = ['t0.tracking_id', 't0.berkid', 'a0.sample', 't0.fpkm', 't0.fpkm_status', 't1.berkid', 'a1.sample', 't1.fpkm', 't1.fpkm_status']

    selectstring = ", ".join(selectlist)
    if maxfpkm:
        mfstring = ' AND t1.fpkm < {0} AND t2.fpkm < {0}'.format(maxfpkm)
    else:
        mfstring = ''
    joincmd = "SELECT {0} FROM {1} as t0 FULL OUTER JOIN {1} as t1 USING (tracking_id) WHERE t0.berkid = '{2}' AND t1.berkid = '{3}' AND t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK'{4} ORDER BY tracking_id;".format(selectstring, datatable, berkids[0], berkids[1], mfstring)
    print(joincmd)
    #joincmd.withautin = "SELECT {2} FROM {0} as t0 INNER JOIN autin as a0 using (berkid) FULL OUTER JOIN {1} as t1 INNER JOIN autin as a1 using (berkid) USING (tracking_id) WHERE t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK'{3} ORDER BY tracking_id;".format(table0, table1, selectstring, mfstring)
  
    return(joincmd)


def join_db_table(joincmd, cur):

    #print(joincmd)
    cur.execute(joincmd)
    jointable = np.array(cur.fetchall())
    print('table length = ', len(jointable))
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

    print('making tables')
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

def testmain():

    cuffpaths = ['/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out']
    corrfile = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations/correlations.txt'
    savefigdir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations'
    berkidlist = ('RGAM009B', 'RGAM010F', 'RGSJ006G')

    print('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")

    cur = conn.cursor()
    mcopy_to_dbtable(cuffpaths, CUFF_TABLE, cur, conn)
    cur.close()
    
    create_corr_file(corrfile)
    
    print('joining and querying tables')
    cur1 = conn.cursor()
    data = mjoin_db_table(berkidlist, SELECTLIST, CUFF_TABLE, MAXFPKM, cur1)

    print('finding correlations')
    for array in data:
        fpkms, berkids = get_fpkm(array, SELECTLIST)
        r, slope, intercept = get_correlation(fpkms)
        samples = [get_samplename(x, cur1) for x in berkids]
        print(samples)
        save_corr_file(r, berkids[0], samples[0], berkids[1], samples[1], corrfile)

        print('plotting scatter plots')
        fpkmlim = max([axislim(x) for x in fpkms])
        fig1 = plt.figure(figsize=(10, 5))
        plot_scatter(fpkms, berkids, samples, r, slope, intercept, 121, fpkmlim)
        plot_scatter(fpkms, berkids, samples, r, slope, intercept, 122, MAXFPKMPLOT)
        plt.tight_layout()
        plt.savefig(os.path.join(savefigdir, make_figname(berkids, samples, 'correlation')))
        plt.close()
        print('plotting histograms')
        fig1 = plt.figure(figsize=(10, 10))
        plot_hist(fpkms, berkids, samples, fpkmlim, 311)
        plot_hist(fpkms, berkids, samples, MAXFPKMHIST, 312)
        plot_hist(fpkms, berkids, samples, 0.008*MAXFPKMHIST, 313)
        plt.savefig(os.path.join(savefigdir, make_figname(berkids, samples, 'hist')))
        plt.tight_layout()
        plt.close()
   
    #cur1.close()
    #conn.close()

if __name__ == '__main__':
    testmain()
#cProfile.run('testmain()')
#cProfile.run('testmain()')
#p=pstats.Stats('conntest')
#p.strip_dirs().sort_stats(-1).print_stats()
#p.sort_stats('cumulative').print_stats(10)

