import numpy as np
import glob as glob
import os
import mn.cmn.cmn as cmn

def loadlengths(fname):
   
    ldata = np.loadtxt(fname, skiprows=1, usecols=(3,))
    
    return(ldata.tolist())


datad = os.path.abspath('.')
exptd = os.path.dirname(datad)
summd = os.path.join(exptd, 'summary')
cmn.makenewdir(summd)

l = []
names = glob.glob('*')
for name in names:
    os.chdir(name)
    lengths = loadlengths('results1.txt')
    l.append(lengths)
    os.chdir('../')

ml = np.mean(l)
outfile = os.path.join(summd, '5x_mean.txt')
with open(outfile, 'w') as f:
    f.write('actual length = 0.2 mm\n')
    f.write('mean pixel length = ' + str(ml) + '\n')
    
    
    
