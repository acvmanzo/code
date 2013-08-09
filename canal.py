#! /usr/bin/env python

# Executable function for analyzing courtship data.

from courtshiplib import *

KINDLIST = ['wing', 'copsuc', 'copatt1'] # List of behaviors; wing = wing extension; copsuc = successful copulation; copatt1 = first attempted copulation.
FNAME = '2013-0718_courtship_data _for_nrsa.csv' # Name of file with the data from manual scoring.
SHAPFILE = 'shap_lat.txt' # Name of file listing results of the Shapiro-Wilk test.
MCPVALFILE = 'mcpvalue_lat_exact.txt' # Name of file listing results of the Mann-Whitney U Test, with p-values adjusted for multiple comparisons.
MWTEST = 'exact' # Specifies whether to use the R function wilcox.exact ('exact') or wilcox.test ('std')
MCCORR = 'fdr' # Specifies how to adjust p-values to correct for multiple comparisons using the R function p.adjust ('fdr' = false discovery rate')
PTFILE = 'proptest.txt' # Name of file listing the results of the proportion test, where p-values give the probability of observing the results if the null hypothesis that all the proportions are from the same distribution is true.
CTRLKEY = '+/+' # Name of the control strain that all other lines will be compared to in the Mann-Whitney U Test.
DIR = 'summary/' # Name of the directory where plots and text files will be saved.
QQDIR = DIR+'qqplots/' # Name of the directory where qqplots will be saved.

# Creates the directories where the plots will go.
cmn.makenewdir(DIR)
cmn.makenewdir(QQDIR)

# For each type of behavior, plots a latency graph, frequency graph, and qqplots for each genotype.
for KIND in KINDLIST:
    plotlat(KIND, FNAME)
    plt.savefig(DIR+KIND+'lat')
    plotfreq(KIND, FNAME)
    plt.savefig(DIR+KIND+'freq')
    plotqqplots(KIND, FNAME, QQDIR, CTRLKEY)

# Creates and writes files with the results of the Shapiro-Wilk test for normality, the Mann Whitney U Test (comparing each genotype to the control genotype, specified above) and the proportion test (for a group of proportions [#successes/total], determines if any of the proportions differ from each other).
createshapfile(DIR+SHAPFILE)
createmwfile(DIR+MCPVALFILE)
createproptestfile(DIR+PTFILE)

for k in KINDLIST:
    d = dictlat(k, FNAME)
    mwd = dictmw(d, ctrlkey=CTRLKEY, test=MWTEST)
    adjpd = mcpval(mwd, MCCORR)

    writeshapfile(DIR+SHAPFILE, d, k)
    writemwfile(DIR+MCPVALFILE, adjpd, k)

    pd = dictfreq(k, FNAME)
    writeproptestfile(DIR+PTFILE, pd, k)
