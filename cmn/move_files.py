import os
import shutil
import glob

#htseqfile = 'htseqcount'
#print(als.plot_htseqcount_dist(htseqfile))

th_resdirpath = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat_2str'
htseq_dir = 'htseq_out'
newhtseq_dir = 'htseq_out_trash'

os.chdir(th_resdirpath)
resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
for resdir in resdirs:
    os.chdir(resdir)
    print(resdir)
    print(os.path.exists(htseq_dir))
    print(newhtseq_dir)
    shutil.move(htseq_dir, newhtseq_dir)
