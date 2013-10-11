import numpy as np
import os
import glob
import time
import math
import shutil

### FUNCTIONS FOR FILE HANDLING ###

def makenewdir(newdir):
    """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""

    try:
        os.makedirs(newdir)
    except OSError as e:
        if e.errno == 17:
            pass
    return(newdir)


def listsortfs(fdir):
    os.chdir(fdir)
    fs = os.listdir(fdir)
    fs = [os.path.abspath(f) for f in fs]
    fs = sorted(fs)
    return(fs)


def batchfiles(fn_name, params, ftype, fdir='.'):
    """Carries out the function 'fn_name' recursively on files with 
    extension 'itype' (e.g., 'jpg' or '*') in directory 'fdir'.
    """
    os.chdir(fdir)
    names = glob.iglob('*{0}'.format(ftype))
    # Absolute path rather than relative path allows changing of directories 
    # in fn_name.
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    for name in names:
        print os.path.basename(name)
        fn_name(name, params)

def batchdirs(fn_name, ftype, fdir='.'):
    """Carries out the function 'fn_name' recursively on directories in directory 'fdir'.
    """
    dirs = listsortfs(fdir)
    for d in dirs:
        print os.path.basename(d)
        fn_name(d)

def batch_s(fdir):
    os.chdir(fdir)
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    return(names)


def defpardir(wdir='.'):
    """Returns the parent folder of the folder specified in wdir."""
    return(os.path.dirname(os.path.abspath(wdir)))


def defsibdir(sibbase, wdir='.'):
    '''Returns the pathname for a directory that is one branch up from wdir 
    and have the name sibbase.
    '''
    pardir = defpardir(wdir)
    sibdir = os.path.join(pardir, sibbase)
    return(sibdir)
    

def makepardir_data():
    """Returns the experiment/ folder path if you are in a data/movie folder."""
    return(os.path.dirname(os.path.abspath('../')))

def makepardir_subexpt():
    """Returns the experiment/ folder path if you are in a folder one level lower (ex., data or
    summary."""
    return(os.path.dirname(os.path.abspath('.')))


### FUNCTIONS FOR LOADING DATA ###

def load_keys(file):
    K = []
    with open(file) as f:
        for l in f:
            K = l.strip('\n').split(',')
    return(K)


def loadmeans(fname):
    dictmeans = {}

    with open(fname) as f:
        f.next()
        for l in f:
            condition, mean, stdev, stderror, n = l.strip('\n').split(',')[0:5]
            dictmeans[condition] = map(float, [mean, stdev, stderror, n])
    return(dictmeans)


### FUNCTIONS USED IN COMPUTATION ###

def window(winlen):
    
    wind = list(np.ones(winlen)/winlen)
    return(wind)

def myround(x, base=10):
    return int(base * round(float(x)/base))


### FUNCTIONS FOR MANIPULATING STRINGS ###

def var_str(name, value, delimiter):
    return name + delimiter + value + '\n'
    

### FUNCTIONS FOR CHECKING OVERWRITING ###

class FileError(Exception):
    def __init__(self, value):
       self.value = value
    def __str__(self):
       return repr(self.value)


def check(obj, overwrite):
    """Checks whether obj (file, directory) exists.
    Inputs:
    obj = file or directory
    overwrite = 'yes' or 'no'; 'yes' to ovewrite
    """
    if os.path.exists(obj) and overwrite == 'no':
        m = '{0} already exists'.format(obj)
        raise FileError(m)
    try:
        if os.path.exists(obj) and overwrite == 'yes':
            shutil.rmtree(obj)
    except OSError as e:
        if e.errno == 20:
            os.remove(obj)
