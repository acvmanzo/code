import numpy as np
import os
import glob
import time
import math


def makenewdir(newdir):
    """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""

    try:
        os.makedirs(newdir)
    except OSError as e:
        if e.errno == 17:
            pass
    return(newdir)

def var_str(name, value):
    return name + ',' + value + '\n'


def batch(fn_name, ftype, params, fdir='.'):
    """Carries out the function 'fn_name' recursively on files with extension 'itype' (e.g., 'jpg' or '*') in directory 'fdir'.
    """


    os.chdir(fdir)
    names = glob.iglob('*{0}'.format(ftype))
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    for name in names:
        if ftype != params.itype:
            t = time.strftime('%H:%M:%S')
            print os.path.basename(name), t

        fn_name(name, params)


def makepardir():
    """Returns the experiment/ folder path if you are in a phase_analysis/ folder."""
    return(os.path.dirname(os.path.abspath('.')))

def makepardir_data():
    """Returns the experiment/ folder path if you are in a data/movie folder."""
    return(os.path.dirname(os.path.abspath('../')))

def makepardir_subexpt():
    """Returns the experiment/ folder path if you are in a folder one level lower (ex., data or
    summary."""
    return(os.path.dirname(os.path.abspath('.')))


def load_keys(file):
    K = []
    with open(file) as f:
        for l in f:
            K = l.strip('\n').split(',')
    return(K)



def batch_s(fdir):
    os.chdir(fdir)
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    return(names)


def myround(x, base=10):
    return int(base * round(float(x)/base))


def loadmeans(fname):
    dictmeans = {}

    with open(fname) as f:
        f.next()
        for l in f:
            condition, mean, stdev, stderror, n = l.strip('\n').split(',')[0:5]
            dictmeans[condition] = map(float, [mean, stdev, stderror, n])
    return(dictmeans)
