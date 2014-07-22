# Settings for all_correlations.py

from rnaseq_settings import *
import os
import cmn.cmn as cmn
import datetime
import shutil

curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


#IMPORTANT PARAMETERS

#MAXFPKM = 5000 

#Specifies whether correlation analysis performed with only a subset of genes.
#If so, set equal to the name of the table in the database that contains this
#list. Else set to 'False'
#GENE_SUBSET_TABLE = False
#GENE_SUBSET_TABLE = 'prot_coding_genes'



# Directories used.
# Files generated.
PEARSON_CORRFILE = 'pearson_correlations.txt' 
SPEARMAN_CORRFILE = 'spearman_correlations.txt' 
CORRLOG = '{}_correlations.log'.format(curtime)
CORRLOGPATH = os.path.join(CORRELATION_DIR, CORRLOG)

#if ALLREPS_OR_BERKIDS == 'allreps':
COND_DIR = False
BERKIDLIST = False

# Adjust paths for condition subset analyses.
#if ALLREPS_OR_BERKIDS == 'berkids':
    #TESTED_BERKIDS = 'selected_berkids' # File with list of berkeley ids for analysis.
    #COND_DIR = 'NrxIV_M' # Name of folder where results will be saved.
    #COND_PATH = os.path.join(CORRELATION_DIR, COND_DIR)
    #cmn.makenewdir(COND_PATH)
    ##BERKIDLIST = cmn.load_keys(TESTED_BERKIDS)
    ##shutil.copy(TESTED_BERKIDS, os.path.join(COND_PATH, TESTED_BERKIDS))
    ##PEARSON_CORRFILE, SPEARMAN_CORRFILE = [os.path.join(COND_PATH, x) \
            ##for x in [PEARSON_CORRFILE, SPEARMAN_CORRFILE]]
    #CORRLOGPATH = os.path.join(COND_PATH, CORRLOG)
    #SAVED_CORRELATION_SETTINGS_PATH = os.path.join(COND_PATH,
            #'{}_settings.py'.format(curtime))



SCATTER_DPI = 1000
#SCATTER_FIGSIZE = (10, 5.5)
SCATTER_FIGSIZE = (5.5, 5.5)
#SCATTER_SUBPLOTS = [121, 122]
SCATTER_SUBPLOTS = [111]
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
if PC_LOG == True:
    HIST_YLIMS = [6000, 1000, 200, 100]
HIST_TITLES = ['All bins', 'Zoom in on bins with very low FPKM',
    'Zoom in on bins with low FPKM', 'Zoom in on bins with high FPKM']
HIST_MAXFPKM = 2000
if PC_LOG == True:
    HIST_MAXFPKM = 4
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

