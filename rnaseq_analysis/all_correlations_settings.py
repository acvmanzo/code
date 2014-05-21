from runtuxedoset import *
import os
import cmn.cmn as cmn
import datetime

curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

SAMPLEINFO_TABLE = 'autin'
CUFF_TABLE = 'cufflinks_data'
#SELECTLIST = ['t0.tracking_id', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 't1.berkid', 't1.fpkm', 't1.fpkm_status']
SELECTLIST = ['t0.gene_short_name', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 't1.berkid', 't1.fpkm', 't1.fpkm_status']
MAXFPKM = 5000 

# Directories used.
#CORRELATION_DIR = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations'
CORRELATION_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/correlations_tophat'
if MAXFPKM != False:
    CORRELATION_DIR = CORRELATION_DIR + '_maxfpkm{}'.format(MAXFPKM)
cmn.makenewdir(CORRELATION_DIR)
CORRELATION_SETTINGS_PATH = '/home/andrea/Documents/lab/code/rnaseq_analysis/all_correlations_settings.py'
SAVED_CORRELATION_SETTINGS_PATH = os.path.join(CORRELATION_DIR, 'settings.py') 

PEARSON_CORRFILE = 'pearson_correlations.txt' 
SPEARMAN_CORRFILE = 'spearman_correlations.txt' 
CORRLOG = '{}_correlations.log'.format(curtime)
CORRLOGPATH = os.path.join(CORRELATION_DIR, CORRLOG)


FPKM_FILE = 'genes.fpkm_tracking'
BERKID_FPKM_FILE = 'genes_berkid.fpkm_tracking'

SCATTER_FIGSIZE = (10, 5.5)
SCATTER_DPI = 1000
SCATTER_SUBPLOTS = [121, 122]
SCATTER_MAXFPKM = 2000

SCATTER_INFO = {
        'scatter_figsize': SCATTER_FIGSIZE,
        'scatter_dpi': SCATTER_DPI,
        'scatter_subplots': SCATTER_SUBPLOTS,
        'scatter_maxfpkm': SCATTER_MAXFPKM,
        }

HIST_FIGSIZE = (10, 14)
HIST_DPI = 1250
HIST_SUBPLOTS = [411, 412, 413, 414]
HIST_YLIMS = [18000, 1000, 25, 5] 
HIST_TITLES = ['All bins', 'Zoom in on bins with very low FPKM',
    'Zoom in on bins with low FPKM', 'Zoom in on bins with high FPKM']
HIST_MAXFPKM = 2000
HIST_MAXFPKM_FRAC = 0.01

HIST_INFO = {
        'hist_figsize': HIST_FIGSIZE,
        'hist_dpi': HIST_DPI,
        'hist_subplots': HIST_SUBPLOTS,
        'hist_ylims': HIST_YLIMS,
        'hist_titles': HIST_TITLES,
        'hist_maxfpkm': HIST_MAXFPKM,
        'hist_maxfpkm_frac': HIST_MAXFPKM_FRAC
}

