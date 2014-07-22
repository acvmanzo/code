# Settings for all_correlations.py

from rnaseq_settings import *
import os
import cmn.cmn as cmn
import shutil


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
#HIST_YLIMS = [18000, 1000, 25, 5]
HIST_YLIMS = [6000, 1000, 200, 100]
HIST_TITLES = ['All bins', 'Zoom in on bins with very low FPKM',
    'Zoom in on bins with low FPKM', 'Zoom in on bins with high FPKM']
#HIST_MAXFPKM = 2000
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

