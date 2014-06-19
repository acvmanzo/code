import numpy as np
import os
import glob

dirlist = sorted(glob.glob('*'))

avg_males = []
avg_females = []
for d in dirlist:
    os.chdir(d)
    with open('toptags_edgeR_fdr05_gene', 'r') as f:
        x = len(list(f))
        print(x)
    if '_M' in d:
        avg_males.append(x)
    if '_F' in d:
        avg_females.append(x)
    print(d)
    os.system('cat toptags_edgeR_fdr05_gene | wc -l')
    os.chdir('../')
print(np.mean(avg_males))
print(np.mean(avg_females))

