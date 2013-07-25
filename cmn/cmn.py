import numpy as np
import os
import glob
import time
import math

def hmsub(trace):
    """Mean-subtracts and then multiplies a trace (a numpy array) with a Hamming function of the same size as the 
    trace."""
    
    return(np.hamming(np.size(trace))*(trace - np.mean(trace)))


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


def pd_avg(phasediffs):
   
    """ Finds the 'average' phase differences of a list of phase differences (phasediffs). 
    Because phases wrap, you can't just take the mean. To find the phase difference for each fly, 
    find the cos(phase) and sin(phase) values for each bin. Average those, and then take the 
    arctangent to find the 'average' phase. The length of the vector to [avg_pd_cos(x), 
    avg_pd_sin(x)] gives a measure of the spread of the data. (The closer to 1, the tighter the 
    data).
    """
    

    pd_cosx = [np.cos(pd) for pd in phasediffs]
    pd_sinx = [np.sin(pd) for pd in phasediffs]
    
    avg_pd_cosx = np.mean(pd_cosx)
    avg_pd_sinx = np.mean(pd_sinx)
    
    # atan2 finds the angle and chooses the correct quadrant.
    avgphasediff = math.atan2(avg_pd_sinx, avg_pd_cosx)
    avglength = np.sqrt( (avg_pd_sinx)**2 + (avg_pd_cosx)**2 )
    
    return(avgphasediff, avglength)


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



def writejpglist(frame1, frame2):
    if os.path.exists('list.txt') == True:
        os.remove('list.txt')
    jpegs = glob.glob('*.jpg')
    jpegs.sort()
    
    for jpeg in jpegs[frame1:frame2]:
        with open('list.txt', 'a') as f:
            f.write(jpeg + '\n')


def batch_s(fdir):
    os.chdir(fdir)
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    return(names)
