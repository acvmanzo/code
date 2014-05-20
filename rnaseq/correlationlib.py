import numpy as np
import math
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import os
import psycopg2
from scipy import stats
import itertools
import logging
import cmn.cmn as cmn

BERKIDLEN = 8

    

def get_replicate_berkid_dict(cur, sampleinfo_table):
    cur.execute("SELECT DISTINCT genotype, sex FROM {} ORDER BY genotype, sex;".format(sampleinfo_table))
    conditions = cur.fetchall()
    all_berkid_dict = {}
    for condition in conditions:
        selcmd = "SELECT berkid FROM {} WHERE genotype = '{}' and sex = '{}' and seq_received = True ORDER BY berkid;".format(sampleinfo_table, condition[0], condition[1])
        logging.info('%s', selcmd)
        cur.execute(selcmd)
        berkids = [x[0] for x in cur.fetchall()]
        all_berkid_dict['_'.join(condition)] = berkids
    logging.info('berkids by condition: %s', all_berkid_dict)
    return(all_berkid_dict)
        

def get_cufflink_paths(berkid, cuff_results_dir):
    return(os.path.join(cuff_results_dir, berkid))


def get_replicate_cufflink_paths(cur, sampleinfo_table, cuff_results_dir, cuff_dir, berkid_fpkm_file):
    replicate_berkid_dict = get_replicate_berkid_dict(cur, sampleinfo_table)
    replicate_path_dict = {}
    for condition, berkids in replicate_berkid_dict.items():
        replicate_path_dict[condition] = [os.path.join(get_cufflink_paths(b, cuff_results_dir), cuff_dir, berkid_fpkm_file) for b in berkids]
    return(replicate_path_dict)


def add_berkid(berkid, fpkm_path, berkid_fpkm_path):
    '''adds the berkid to the last columns of an
    fpkm file output by cufflinks.
    '''
    with open(berkid_fpkm_path, 'w') as g:
        with open(fpkm_path, 'r') as f:
            next(f)
            for l in f:
                newline = l.strip('\n') + '\t{0}\n'.format(berkid)
                g.write(newline) 

def madd_berkid(cufflink_fpkm_paths, berkid_fpkm_file):
    berkid_fpkm_paths = []
    for cf in cufflink_fpkm_paths:
        if not os.path.exists(cf):
            logging.info('%s does not exist', cf)
            continue
        berkid = get_berkid(cf)
        berkid_fpkm_path = os.path.join(os.path.dirname(cf), berkid_fpkm_file) 
        print(berkid_fpkm_path)
        add_berkid(berkid, cf, berkid_fpkm_path)
        berkid_fpkm_paths.append(berkid_fpkm_path)
    return(berkid_fpkm_paths)

def find_num_genes(dbtable, berkid, cur):
    checkrowscmd = "select count (*) from (select * from {} where berkid = '{}') as foo;".format(dbtable, berkid)
    cur.execute(checkrowscmd)
    return(cur.fetchone()[0])


def copy_to_dbtable(berkid_fpkm_path, dbtable, cur):
    '''copies data from the modfied gene fpkm tracking file output
    by add_berkid() into the sql table dbtable using the cursor

    cur.
    '''
    #print(berkid_fpkm_p_ath)
    berkid = get_berkid(berkid_fpkm_path)
    print(berkid)
    checkrows = int(find_num_genes(dbtable, berkid, cur))
    if checkrows != 0:
        delcmd = "DELETE FROM {} WHERE berkid = '{}';".format(dbtable, berkid)
        cur.execute(delcmd)
    cur.copy_from(open(berkid_fpkm_path), dbtable)


def mcopy_to_dbtable(sample_fpkm_paths, dbtable, cur):
    '''applies copy_to_dbtable() to multiple fpkm files.
    '''
    logging.info('Copying data to table')
    for sample_fpkm_path in sample_fpkm_paths:
        copy_to_dbtable(sample_fpkm_path, dbtable, cur)

def gen_joincmd(selectlist, berkids, dbtable, maxfpkm):
    '''returns a string with a command for joining tables.
    the joined table contains fpkm values for two samples, and
    includes all the genes reported in the gene fpkm file output
    by cufflinks.
    input:
    selectlist = list of columns that will be selected from the table
    berkids = list of sample berkeley ids that will be compared
    dbtable = database table that contains the fpkm data
    maxfpkm = maximum fpkm of genes that will be compared. set to false
    if all genes should be included, or to another number otherwise.
    '''
    selectstring = ", ".join(selectlist)
    if maxfpkm:
        mfstring = ' and t0.fpkm < {0} and t1.fpkm < {0}'.format(maxfpkm)
    else:
        mfstring = ''
    joincmd = "select {0} from {1} as t0 full outer join {1} as t1 using (tracking_id) where t0.berkid = '{2}' and t1.berkid = '{3}' and t0.tracking_id != '' and t0.fpkm_status = 'OK' and t1.fpkm_status = 'OK'{4} order by tracking_id;".format(selectstring, dbtable, berkids[0], berkids[1], mfstring)
    logging.info('%s', joincmd)
    return(joincmd)


def join_db_table(joincmd, cur):
    '''joins tables as specified in joincmd using the cur cursor and 
    returns a list of the rows in the joined table.
    '''
    cur.execute(joincmd)
    jointable = np.array(cur.fetchall())
    logging.info('table length = %s', len(jointable))
    return(jointable)


def mjoin_db_table(berkidlist, selectlist, dbtable, maxfpkm, cur):
    '''applies join_db_table and gen_joincmd for each pairwise 
    combination of samples given in berkidlist; returns a list of lists
    '''
    comp_index = itertools.combinations(range(len(berkidlist)), 2) # list of indices for all pairwise comparisons of each sample.
    comparisons = []
    for i in comp_index:
        #cur = conn.cursor()
        berkids = [berkidlist[x] for x in i]
        joincmd = gen_joincmd(selectlist, berkids, dbtable, maxfpkm)
        jointable = join_db_table(joincmd, cur)
        comparisons.append(jointable)
    return(comparisons)   


def get_samplename(berkid, cur):
    '''given a berkid, returns the sample by querying a sql database
    using the cursor cur.'''
    samplecmd = "select sample from autin where berkid = '{}'".format(berkid)
    cur.execute(samplecmd)
    sample = cur.fetchone()[0]
    return(sample)

def get_fpkm(jointable, colnames):
    '''from the jointable returned by the function join_db_table(), returns
    the fpkm values and the berkids as a list of lists.
    input:
    jointable = an array containing the fpkm for genes in two samples; 
    returned by join_db_table()
    colnames = list of columns selected from the table; convenient to use
    the selectlist that was the input to the gen_joincmd() function 
    used in join_db_table().
    '''
    array = np.transpose(jointable)
    fpkm0, fpkm1 = [array[x][:].astype(np.float) for x in [colnames.index('t0.fpkm'),colnames.index('t1.fpkm')]]
    berkid0, berkid1, = [array[x][0] for x in [colnames.index('t0.berkid'), colnames.index('t1.berkid')]]
    return([fpkm0, fpkm1], [berkid0, berkid1])


def get_pearson_correlation(fpkms):
    '''applies a linear regression to the list of lists fpkms. returns the
    correlation coefficient, slope, and intercept.
    '''
    slope, intercept, r, p, std_err = stats.linregress(fpkms[0], fpkms[1])
    return(r, slope, intercept)

def get_spearman_correlation(fpkms):
    return(stats.spearmanr(fpkms[0], fpkms[1]))

def create_corr_file(correlationfile):
    '''creates a file where the correlation data will be written.'''
    with open(correlationfile, 'w') as g:
        g.write('berkid0\tsample0\tberkid1\tsample1\tr\tr^2\n')


def save_corr_file(r, berkid0, sample0, berkid1, sample1, correlationfile):
    '''writes the correlation data into the file correlationfile'''
    with open(correlationfile, 'a') as g:
        g.write('{}\t{}\t{}\t{}\t{:.4f}\t{:.4f}\n'.format(berkid0, sample0, berkid1, sample1, r, np.square(r)))


def axislim(num):
    '''returns the axis limit for a maximum value of num'''
    lim = int(math.ceil(max(num))*1.1)
    return(lim)

def format_plot(berkids, samples, fpkmlim):
    '''formats a scatter plot comaring gene expression of two samples.'''
    xlabel = '{} {}'.format(berkids[0], samples[0])
    ylabel = '{} {}'.format(berkids[1], samples[1])
    title = 'FPKM of {} vs. {}'.format(samples[0],samples[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(0, fpkmlim)    
    plt.ylim(0, fpkmlim)
  

def plot_scatter(fpkms, berkids, samples, r, slope, intercept, subplotnum, fpkmlim): 
    '''plots a scatter plot comparing gene expression of two samples.
    inputs:
    fpkms = a list of lists containing the fpkm values of two samples 
    berkids = berkids of the samples being compared (of the format rgam009b)
    samples = sample names of the samples being compared (of the format cs_ma)
    r = correlation coefficient of a linear regression of the gene 
    expression between two samples
    slope = slope of a linear regression of the gene expression between
    two samples
    intercept = slope of a linearegression line of the gene expression
    between two samples
    subplotnum = subplot number
    fpkmlim = limit of the fpkm values that will be plotted
    '''
    plt.subplot(subplotnum)
    plt.scatter(fpkms[0], fpkms[1], c='k', marker='o', s=3)
    xline = range(fpkmlim)
    yline = [slope*x + intercept for x in xline] 
    plt.plot(xline, yline, c='b', ls = '--')
    plt.plot(xline, xline, c='r', ls = '--')
    ax = plt.gca()
    textstr = 'r = {:.3f}'.format(r) 
    format_plot(berkids, samples, fpkmlim)

    if subplotnum == 121:
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    ax.ticklabel_format(style='sci', scilimits=(-1,2))

def make_figname(berkids, samples, figtype):
    '''generates a figure name using the berkids and sample names of the
    samples being compared. figtype can be 'hist' or 'correlation'.'''
    figname_base = '{}-{}_vs_{}-{}_{}.png'.format(samples[0], berkids[0], samples[1], berkids[1], figtype)
    return(figname_base)


def genfig_scatter_zoom(fpkms, berkids, samples, r, slope, intercept, fpkmlim, scatter_info, fig_dir):
    '''Generates a figure containing scatter plots that compare expression of two samples.
    Inputs:
    fpkms = List of fpkm values for both samples (list of 2 lists)
    berkids = List of berkeley ids
    samples = List of samples
    r = correlation coefficient
    slope = slope of linear regression line
    intercept = intercept of linear regression line
    fpkmlim = limit of the fpkm values that will be plotted
    scatter_info = Dictionary with the following values:
        scatter_figsize = size of figure
        scatter_subplots = list of subplots to be plotted
        scatter_maxfpkm = maximum fpkm value to be plotted
        scatter_figdir = main correlation directory
'''
    d = scatter_info
    limlist = [fpkmlim, d['scatter_maxfpkm']]
    fig1 = plt.figure(figsize=d['scatter_figsize'], dpi=d['scatter_dpi'])
    for s, l in zip(d['scatter_subplots'], limlist):
        plot_scatter(fpkms, berkids, samples, r, slope, intercept, s, l)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, make_figname(berkids, samples, 'correlation')))
    plt.close()

def plot_hist(fpkm, fpkmlim, sample, color):
    '''plots a histogram of list fpkm with fpkm values < list for sample'''
    plt.hist(fpkm, range=(0, fpkmlim), bins=50, color=color, alpha=0.5, label='{}'.format(sample))


def compare_hist(fpkms, berkids, samples, fpkmlim, subplotnum, ylim, title):
    '''plots two histograms showing the distribution of gene expression values
    in two samples.
    '''
    plt.subplot(subplotnum)
    for x, c in zip([0, 1], ['r', 'b']):
        plot_hist(fpkms[x], fpkmlim, samples[x], color=c)
    plt.legend()
    plt.ylim(0, ylim)
    ax = plt.gca()
    ax.ticklabel_format(style='sci', scilimits=(-1,2))
    plt.ylabel('gene number')
    plt.xlabel('FPKM')
    plt.title(title)

def genfig_compare_hist_zoom(fpkms, berkids, samples, fpkmlim, hist_info, fig_dir):
    '''Generates a figure comprised of three histograms comparing the expression
    values of two samples.
    Inputs:
    fpkms = List of fpkm values for both samples (list of 2 lists)
    berkids = List of berkeley ids
    samples = List of samples
    fpkmlim = limit of the fpkm values that will be plotted
    hist_info = Dictionary with the following values:
        hist_figsize = size of figure
        hist_subplots = list of subplots to be plotted
        hist_ylim = list of ylimits
        hist_maxfpkm = maximum fpkm value to be plotted
        hist_maxfpkm_frac = fraction of max fpkm value to be plotted
    '''
    d = hist_info
    limlist = [fpkmlim, d['hist_maxfpkm'], d['hist_maxfpkm']*d['hist_maxfpkm_frac']]
    fig1 = plt.figure(figsize=d['hist_figsize'], dpi=d['hist_dpi'])
    for s, l, t, y in zip(d['hist_subplots'], limlist, d['hist_titles'], d['hist_ylims']):
        compare_hist(fpkms, berkids, samples, l, s, y, t)
    plt.savefig(os.path.join(fig_dir, make_figname(berkids, samples, 'hist')))
    plt.tight_layout()
    plt.close()

def get_berkid(cufflink_fpkm_path, berkidlen=BERKIDLEN):
    '''Return a berkid extracted from a cufflink_fpkm_path'''
    cf = cufflink_fpkm_path
    return(cf[cf.find('RG'):cf.find('RG')+berkidlen])

def get_berkidlist(cufflink_fpkm_paths):
    '''Returns a list of berkids extracted from a list of cufflink output paths'''
    return([get_berkid(cf) for cf in cufflink_fpkm_paths])



def copy_data_to_table(cufflink_fpkm_paths, berkid_fpkm_file, cuff_table):

    logging.info('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    berkid_cufflink_fpkm_paths = madd_berkid(cufflink_fpkm_paths, berkid_fpkm_file)
    mcopy_to_dbtable(berkid_cufflink_fpkm_paths, cuff_table, cur)
    conn.commit()
    cur.close()
    conn.close()

def get_joined_arrays(cufflink_fpkm_paths, selectlist, cuff_table, maxfpkm):

    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    logging.info('joining and querying tables')
    cur1 = conn.cursor()
    berkidlist = get_berkidlist(cufflink_fpkm_paths)
    joined_arrays = mjoin_db_table(berkidlist, selectlist, cuff_table, maxfpkm, cur1)
    cur1.close()
    return(joined_arrays)


def get_sample_correlations(joined_arrays, fig_dir, pearson_corrfile, spearman_corrfile, selectlist, scatter_info, hist_info):
    
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    
    for joined_array in joined_arrays:
        fpkms, berkids = get_fpkm(joined_array, selectlist)
        cur2 = conn.cursor()
        samples = [get_samplename(x, cur2) for x in berkids]
        cur2.close()
        fpkmlim = max([axislim(x) for x in fpkms])
        
        logging.info('Samples: %s', samples)
        logging.info('finding correlations')
        r, slope, intercept = get_pearson_correlation(fpkms)
        save_corr_file(r, berkids[0], samples[0], berkids[1], samples[1], pearson_corrfile)
        
        sr = get_spearman_correlation(fpkms)
        save_corr_file(sr[0], berkids[0], samples[0], berkids[1], samples[1], spearman_corrfile)

        logging.info('plotting scatter plots')
        cmn.makenewdir(fig_dir)
        genfig_scatter_zoom(fpkms, berkids, samples, r, slope, intercept, fpkmlim, scatter_info, fig_dir)

        #logging.info('plotting histograms')
        #genfig_compare_hist_zoom(fpkms, berkids, samples, fpkmlim, hist_info, fig_dir)
   
    conn.close()




