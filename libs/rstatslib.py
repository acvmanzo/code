# Wrappers for R functions. See R documentation for each function. Note that 
#the data is often returned as a string or float vector and needs to be 
#subscripted for use in python code.

import numpy as np
import os
import cmn.cmn as cmn
import rpy2.robjects as robjects

r = robjects.r
addpath = r['.libPaths']
addpath('/home/andrea/R/x86_64-unknown-linux-gnu-library/3.1')
def shapirowilk(values):
    # Tests whether values are normally distributed.

    test = r['shapiro.test']
    return(test(values))

def mannwhitney(x, y):
    # Nonparametric test to determine whether two populations are the same or not.

    test = r['wilcox.test']
    return(test(x, y, alternative="two.sided"))

def mannwhitneyexact(x, y):
    # Nonparametric test to determine whether two populations are the same or not; 
    #this function calculates exact p-values in the presence of ties.

    library = r['library']
    library('exactRankTests')
    test = r['wilcox.exact']
    return(test(x, y, alternative="two.sided"))

def padjust(p, method):
    # Adjusts p-values according to the method specified; method often used is
    #"fdr".

    test = r['p.adjust']
    return(test(p, method))
    

def binomci_w(x, n, conflevel, methods='wilson'):
    # Generates binomnial confidence intervals with the Wilson method as the default.
    # x = vector of number of successes in binomial experiment
    # n = vector of number of independent trials in binomial experiment

    library = r['library']
    library('binom')
    ci = r['binom.confint']
    return(ci(x, n, conflevel, methods))


def proptest(x, n, confleveln=0.95):
    # Tests whether a set of proportions are all the same or all different (like an ANOVA).
    # x = vector of number of successes in binomial experiment
    # n = vector of number of independent trials in binomial experiment

    proptest = r['prop.test']
    conflevel = robjects.StrVector("conf.level")
    return(proptest(x, n, **{'conf.level': confleveln}))


def pairwiseproptest(x, n, method, confleveln=0.95):
    # Applies prop.test to each pair in a group with adjustments for multiple
    #comparisons .
    # x = vector of number of successes in binomial experiment
    # n = vector of number of independent trials in binomial experiment
    pptest = r['pairwise.prop.test']
    conflevel = robjects.StrVector("conf.level")
    return(pptest(x, n, method, **{'conf.level': confleveln}))

def fishertest(nsuc1, nfail1, nsuc2, nfail2):
    
    fishertest = r['fisher.test']
    matrix = r['matrix']
    rlist = r['list']
    c = r['c']
    x = matrix(c(nsuc1, nfail1, nsuc2, nfail2), nrow=2, 
    dimnames=rlist(c("Gen1", "Gen2"), c("Success", "Failure")))
    return(fishertest(x))

def ttest(x, y):
    # With these options, uses the Welch t test for unequal variances.

    test = r['t.test']
    unlist = r['unlist']
    x = unlist(x)
    y = unlist(y)
    return(test(x, y))

#nsuc1 = 1
#nfail1 = 12
#nsuc2 = 14
#nfail2 = 17
#res = fishertest(nsuc1, nfail1, nsuc2, nfail2)
#print(res)
#print(res.rx('p.value')[0][0])
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
