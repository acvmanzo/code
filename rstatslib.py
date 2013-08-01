import numpy as np
import os
import cmn.cmn as cmn
import rpy2.robjects as robjects


def shapirowilk(values):

    r = robjects.r
    test = r['shapiro.test']
    return(test(values))

def mannwhitney(x, y):

    r = robjects.r
    test = r['wilcox.test']
    return(test(x, y, alternative="two.sided"))

def mannwhitneyexact(x, y):

    r = robjects.r
    addpath = r['.libPaths']
    addpath('/home/andrea/rlib')
    library = r['library']
    library('exactRankTests')
    test = r['wilcox.exact']
    return(test(x, y, alternative="two.sided"))

def padjust(p, method, n):

    r = robjects.r
    test = r['p.adjust']
    return(test(p, method, n))

def binomci_w(x, n, conflevel, methods='wilson'):
    # x = vector of number of successes in binomial experiment
    # n = vector of number of independent trials in binomial experiment

    r = robjects.r
    library = r['library']
    library('binom')
    ci = r['binom.confint']
    return(ci(x, n, conflevel, methods))

#rnorm = r['rnorm']
#datanorm = rnorm(50)
#winglat, copsuclat, copattlat = dictlat(FNAME)

#mwinglat, mcopsuclat, mcopattlat = map(means,[winglat, copsuclat, copattlat])
##print('python', winglat['cs'])

#rcs_wlat = robjects.FloatVector(winglat['cs'])
#rnrxi_wlat = robjects.FloatVector(winglat['NrxI'])
#rnrxiv_wlat = robjects.FloatVector(winglat['NrxIV'])

#rcs_copattlat = robjects.FloatVector(copattlat['cs'])
#rnrxi_copattlat = robjects.FloatVector(copattlat['NrxI'])

#rcs_copsuclat = robjects.FloatVector(copsuclat['cs'])
#rnrxi_copsuclat = robjects.FloatVector(copsuclat['NrxI'])

#rnorm = r['rnorm']
#datanorm = rnorm(50)
#print(datanorm)

#shaptest = r['shapiro.test']
#print('cs')
#print(shaptest(rcs_copattlat))
#print('norm')
#print(shaptest(datanorm))

#wilcoxtest = r['wilcox.test']
#x = wilcoxtest(rcs_copsuclat, rnrxi_copsuclat)

#isatomic = r['is.atomic']
