import glob
import os

fdir = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat'
os.chdir(fdir)
sample_dirs = sorted([os.path.abspath(x) for x in glob.glob('*/')])
print(sample_dirs)

for sd in sample_dirs:
    os.chdir(sd)
    fastqfile = glob.glob('*.fastq')
    print(fastqfile)
    if fastqfile:
        os.remove(fastqfile[0])
