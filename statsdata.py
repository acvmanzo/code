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


