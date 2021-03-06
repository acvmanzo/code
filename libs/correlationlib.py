# Library containing functions useful for finding correlation coefficients
# of samples based on gene expression.

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
import libs.rnaseqlib as rl

BERKIDLEN = 8

#### Removed to rnaseqlib.py
#def add_berkid(berkid, fpkm_path, berkid_fpkm_path):
    #'''adds the berkid to the last columns of an
    #fpkm file output by cufflinks.
    #'''
    #with open(berkid_fpkm_path, 'w') as g:
        #with open(fpkm_path, 'r') as f:
            #next(f)
            #for l in f:
                #newline = l.strip('\n') + '\t{0}\n'.format(berkid)
                #g.write(newline) 


#### Removed to rnaseqlib.py
#def madd_berkid(cufflink_fpkm_path_tuples):
    #'''Input is list of tuples of the following form:
    #(berkid, fpkm path, berkid_fpkm_path)
    #'''
    #for berkid, cf, bcf in cufflink_fpkm_path_tuples:
        #if not os.path.exists(cf):
            #logging.info('%s does not exist', cf)
            #continue
        #add_berkid(berkid, cf, bcf)



def gen_joincmd(selectlist, berkids, dbtable, maxfpkm, gene_subset_table,
        quant):
    '''returns a string with a command for joining tables.
    the joined table contains fpkm values for two samples, and
    includes all the genes reported in the gene fpkm file output
    by cufflinks.
    input:
    selectlist = list of columns that will be selected from the table
    berkids = list of sample berkeley ids that will be compared
    dbtable = database table that contains the fpkm data
    maxfpkm = maximum fpkm of genes that will be compared. set to false
    quant = 'cufflinks' or 'htseq'
    if all genes should be included, or to another number otherwise.
    '''
    if quant == 'cufflinks':
        joinfield = 'tracking_id'
    elif quant == 'htseq':
        joinfield = 'gene_short_name'

    selectstring = ", ".join(selectlist)
    if maxfpkm:
        mfstring = 'and t0.fpkm < {0} and t1.fpkm < {0}'.format(maxfpkm)
    else:
        mfstring = ''
    
    if gene_subset_table:
        gsstring = 'inner join {} as t2 using ({})'.format(gene_subset_table,
                joinfield)
    else:
        gsstring = ''

    if quant == 'cufflinks':
        joincmd = "select {0} from {1} as t0 full outer join {1} as t1 using ({6}) {5} where t0.berkid = '{2}' and t1.berkid = '{3}' and t0.{6} != '' and t0.fpkm_status = 'OK' and t1.fpkm_status = 'OK' {4} order by {6};".format(selectstring, dbtable, berkids[0], 
                berkids[1], mfstring, gsstring, joinfield)

    elif quant == 'htseq':
        joincmd = "select {0} from {1} as t0 full outer join {1} as t1 using ({6}) {5} where t0.berkid = '{2}' and t1.berkid = '{3}' and t0.{6} != '' {4} order by {6};".format(selectstring, 
                dbtable, berkids[0], berkids[1], mfstring, gsstring, 
                joinfield)

    logging.debug('%s', joincmd)
    return(joincmd)

def join_db_table(joincmd, cur):
    '''joins tables as specified in joincmd using the cur cursor and 
    returns a list of the rows in the joined table.
    '''
    cur.execute(joincmd)
    jointable = np.array(cur.fetchall())
    logging.debug('table length = %s', len(jointable))
    return(jointable)


def mjoin_db_table(berkidlist, selectlist, dbtable, maxfpkm, cur, 
        gene_subset_table, quant):
    '''applies join_db_table and gen_joincmd for each pairwise 
    combination of samples given in berkidlist; returns a list of lists
    '''
    comp_index = itertools.combinations(range(len(berkidlist)), 2) # list of indices for all 
    #pairwise comparisons of each sample.
    comparisons = []
    for i in comp_index:
        #cur = conn.cursor()
        berkids = [berkidlist[x] for x in i]
        joincmd = gen_joincmd(selectlist, berkids, dbtable, maxfpkm, 
                gene_subset_table, quant)
        jointable = join_db_table(joincmd, cur)
        comparisons.append(jointable)
    return(comparisons)   


def get_fpkmorcounts(jointable, colnames,quant):
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
    if quant == 'cufflinks':
        fpkm0, fpkm1 = [array[x][:].astype(np.float) for x in [colnames.index('t0.fpkm'),
            colnames.index('t1.fpkm')]]
    if quant == 'htseq':
        fpkm0, fpkm1 = [array[x][:].astype(np.float) for x in [colnames.index('t0.counts'),
            colnames.index('t1.counts')]]
    berkid0, berkid1, = [array[x][0] for x in [colnames.index('t0.berkid'), 
        colnames.index('t1.berkid')]]

    return([fpkm0, fpkm1], [berkid0, berkid1])


def get_pearson_correlation(fpkms):
    '''applies a linear regression to the list of lists fpkms. returns the
    correlation coefficient, slope, and intercept.
    '''
    slope, intercept, r, p, std_err = stats.linregress(fpkms[0], fpkms[1])
    return(r, slope, intercept)

def add_pseudocount(fpkms):
    return(np.array(fpkms)+1)

def log_transform(fpkms):
    return(np.log2(np.array(fpkms)))


def get_spearman_correlation(fpkms):
    return(stats.spearmanr(fpkms[0], fpkms[1]))

def create_corr_file(correlationfile):
    '''creates a file where the correlation data will be written.'''
    with open(correlationfile, 'w') as g:
        g.write('berkid0\tsample0\tberkid1\tsample1\tr\tr^2\t#genes\n')


def save_corr_file(r, berkid0, sample0, berkid1, sample1, num_genes,
        correlationfile):
    '''writes the correlation data into the file correlationfile'''
    with open(correlationfile, 'a') as g:
        g.write('{}\t{}\t{}\t{}\t{:.4f}\t{:.4f}\t{}\n'.format(berkid0, 
            sample0, berkid1, sample1, r, np.square(r), num_genes))


def axislim(num):
    '''returns the axis limit for a maximum value of num'''
    lim = int(math.ceil(max(num))*1.1)
    return(lim)

def format_plot(berkids, samples, fpkmlim, quant):
    '''formats a scatter plot comaring gene expression of two samples.'''
    if quant == 'cufflinks':
        xlabel = 'log2 RPKM {} {}'.format(berkids[0], samples[0])
        ylabel = 'log2 RPKM {} {}'.format(berkids[1], samples[1])
    elif quant == 'htseq':
        xlabel = 'log2 counts {} {}'.format(berkids[0], samples[0])
        ylabel = 'log2 counts {} {}'.format(berkids[1], samples[1])

    title = '{} vs. {}'.format(samples[0],samples[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(0, fpkmlim)    
    plt.ylim(0, fpkmlim)
  

def plot_scatter(fpkms, berkids, samples, r, slope, intercept, 
        num_genes, subplotnum, fpkmlim, quant): 
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
    plt.plot(xline, yline, c='b', ls = '--', label='Reg line')
    plt.plot(xline, xline, c='r', ls = '--', label='slope=1')
    plt.legend(loc='lower right')
    ax = plt.gca()
    #textstr = 'r = {:.3f}\n# genes = {}'.format(r, num_genes)
    textstr = 'r = {:.3f}'.format(r, num_genes)
    format_plot(berkids, samples, fpkmlim, quant)

    if subplotnum == 111:
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    ax.ticklabel_format(style='sci', scilimits=(-1,2))

def make_figname(berkids, samples, figtype):
    '''generates a figure name using the berkids and sample names of the
    samples being compared. figtype can be 'hist' or 'correlation'.'''
    figname_base = '{}-{}_vs_{}-{}_{}.png'.format(samples[0], berkids[0], samples[1], 
            berkids[1], figtype)
    return(figname_base)


def genfig_scatter_zoom(fpkms, berkids, samples, r, slope, intercept, 
        num_genes, fpkmlim, scatter_info, fig_dir, quant):
    '''generates a figure containing scatter plots that compare expression of two samples.
    inputs:
    fpkms = list of fpkm values for both samples (list of 2 lists)
    berkids = list of berkeley ids
    samples = list of samples
    r = correlation coefficient
    slope = slope of linear regression line
    intercept = intercept of linear regression line
    fpkmlim = limit of the fpkm values that will be plotted
    scatter_info = dictionary with the following values:
        scatter_figsize = size of figure
        scatter_subplots = list of subplots to be plotted
        scatter_maxfpkm = maximum fpkm value to be plotted
        scatter_figdir = main correlation directory
    quant = 'cufflinks' or 'htseq'
'''
    d = scatter_info
    limlist = [fpkmlim, d['scatter_maxfpkm']]
    fig1 = plt.figure(figsize=d['scatter_figsize'], dpi=d['scatter_dpi'])
    for s, l in zip(d['scatter_subplots'], limlist):
        plot_scatter(fpkms, berkids, samples, r, slope, intercept, num_genes,
            s, l, quant)
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
    '''generates a figure comprised of three histograms comparing the expression
    values of two samples.
    inputs:
    fpkms = list of fpkm values for both samples (list of 2 lists)
    berkids = list of berkeley ids
    samples = list of samples
    fpkmlim = limit of the fpkm values that will be plotted
    hist_info = dictionary with the following values:
        hist_figsize = size of figure
        hist_subplots = list of subplots to be plotted
        hist_ylim = list of ylimits
        hist_maxfpkm = maximum fpkm value to be plotted
        hist_maxfpkm_frac = fraction of max fpkm value to be plotted
    '''
    d = hist_info
    limlist = [fpkmlim, d['hist_maxfpkm']*d['hist_maxfpkm_frac'], 
            d['hist_maxfpkm'], fpkmlim]
    fig1 = plt.figure(figsize=d['hist_figsize'], dpi=d['hist_dpi'])
    for s, l, t, y in zip(d['hist_subplots'], limlist, d['hist_titles'], 
            d['hist_ylims']):
        compare_hist(fpkms, berkids, samples, l, s, y, t)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, make_figname(berkids, samples, 'hist')))
    plt.close()


def copy_data_to_table(cufflink_fpkm_paths, berkid_fpkm_file, cuff_table, 
        berkidlen):
    '''copies cufflinks data to database table.
    inputs:
    cufflink_fpkm_paths: paths to original genes.fpkm_tracking file output by
    cufflinks
    berkid_fpkm_file: new name for fpkm file with the berkid appended to each
    row
    cuff_table: database table with cufflinks data
    berkidlen: length of berkid names
    '''
    logging.info('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    berkid_cufflink_fpkm_paths = [rl.get_cufflink_berkid_fpkm_path(cf,
            berkid_fpkm_file, berkidlen) for cf in cufflink_fpkm_paths]
    berkids = [rl.get_berkid(cf, berkidlen) for cf in cufflink_fpkm_paths]
    print(berkids)
    rl.madd_berkid(zip(berkids, cufflink_fpkm_paths, 
        berkid_cufflink_fpkm_paths), removeblank='yes')
    rl.mcopy_to_dbtable(berkid_cufflink_fpkm_paths, cuff_table, cur)
    conn.commit()
    cur.close()
    logging.info('closing connection')
    conn.close()

def get_joined_arrays(cufflink_fpkm_paths, selectlist, cuff_table, maxfpkm,
        gene_subset_table, berkidlen, quant):

    logging.info('joining and querying tables')
    logging.info('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur1 = conn.cursor()
    berkidlist = rl.get_berkidlist(cufflink_fpkm_paths, berkidlen)
    logging.info(berkidlist)
    joined_arrays = mjoin_db_table(berkidlist, selectlist, cuff_table, maxfpkm, cur1, 
            gene_subset_table, quant)
    cur1.close()
    logging.info('closing connection')
    conn.close()
    return(joined_arrays)


def get_sample_correlations(joined_arrays, fig_dir, pearson_corrfile, 
        spearman_corrfile, selectlist, corrplotobj, pc_log, quant):
    ''' 
    Inputs:
    corrplotobj: object of class CorrPlotData from the rnaseq_settings module
    '''
    corrplotinfo = corrplotobj.__dict__
    logging.info('finding correlations')
    logging.info('opening connection') 
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    
    for joined_array in joined_arrays:
        num_genes = np.shape(joined_array)[0]
        fpkms, berkids = get_fpkmorcounts(joined_array, selectlist, quant)
        if pc_log == True:
            fpkms = log_transform(add_pseudocount(fpkms))
        cur2 = conn.cursor()
        samples = [rl.get_samplename(x, cur2) for x in berkids]
        cur2.close()
        fpkmlim = max([axislim(x) for x in fpkms])
        
        logging.info('Samples: %s', samples)
        r, slope, intercept = get_pearson_correlation(fpkms)
        save_corr_file(r, berkids[0], samples[0], berkids[1], samples[1],
                num_genes, pearson_corrfile)
        
        sr = get_spearman_correlation(fpkms)
        save_corr_file(sr[0], berkids[0], samples[0], berkids[1], samples[1],
                num_genes, spearman_corrfile)

        logging.info('plotting scatter plots')
        cmn.makenewdir(fig_dir)
        genfig_scatter_zoom(fpkms, berkids, samples, r, slope, intercept, 
                num_genes, fpkmlim, corrplotinfo, fig_dir, quant)

        logging.info('plotting histograms')
        genfig_compare_hist_zoom(fpkms, berkids, samples, fpkmlim,
               corrplotinfo, fig_dir)
    
    logging.info('closing connections') 
    conn.close()




