import os
import shutil
import glob

#htseqfile = 'htseqcount'
#print(als.plot_htseqcount_dist(htseqfile))

def move_htseq_files():
    th_resdirpath = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat_2str'
    htseq_dir = 'htseq_out_un'
    newhtseq_dir = 'htseq_out'

    os.chdir(th_resdirpath)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        os.chdir(resdir)
        print(resdir)
        print(os.path.exists(htseq_dir))
        print(newhtseq_dir)
        shutil.move(htseq_dir, newhtseq_dir)

def change_david_file():
    resdirpath = '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes'
    fncluster = 'toptags_edgeR_0.10fbgn_fncluster.txt'
    fnchart = 'toptags_edgeR_0.10fbgn_fnchart.txt'
    fntable = 'toptags_edgeR_0.10fbgn_fntable.txt'
    geneclass = 'toptags_edgeR_0.10fbgn_geneclass.txt'

    os.chdir(resdirpath)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('*/')])
    for resdir in resdirs:
        os.chdir(resdir)
        print(resdir)
        if os.path.exists('DAVID'):
            os.chdir('DAVID')
            for x in [fncluster, fnchart, fntable, geneclass]:
                if os.path.exists(x):
                    newx = x.replace('.txt', '')
                    print(newx)
                    shutil.move(x, newx)

#change_david_file()
