import csv
import rnaseqdirlib as rdl
import psycopg2
import os
import glob

TH_ALIGN_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat'
CLC_ALIGN_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/CLC_results'
TOPHAT_DIR = 'tophat_out'
SUMM_FILE = 'align_summary.txt'
ALL_SUMM_FILE = 'all_align_summary.txt'



def get_align_info_tophat(summ_file):
    '''Extract alignment information from the summary file'''
    d = {}
    with open (summ_file, 'r') as f:
        next(f)
        d['input_reads'] = int(next(f).split(':')[1].rstrip('\n').lstrip(' '))
        d['mapped'] = int(next(f).split(':')[1].split(' ')[2])
        m = next(f)
        multireads = m.split(':')[1].split(' ')[4]
        if multireads == '(':
            multireads = m.split(':')[1].split(' ')[3]
        d['multireads'] = int(multireads)
    return(d)



def batch_align_summ_tophat(th_align_dir, all_summ_file, tophat_dir, summ_file):
    conn = psycopg2.connect("dbname=rnaseq user=andrea")

    all_summ_path = os.path.join(clc_align_dir, all_summ_file) 
    create_summ_file(all_summ_path)

    os.chdir(th_align_dir)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        cur = conn.cursor()
        os.chdir(os.path.join(resdir, tophat_dir))
        berkid = os.path.basename(resdir)
        print(berkid)
        try:
            sample = rdl.get_samplename(berkid, cur)
            cur.close()
            print(sample)
        except TypeError:
            continue
        d = get_align_info_tophat(summ_file)
        write_summ_file(all_summ_file, d, berkid, sample)
        
def batch_align_summ_clc(clc_align_dir, all_summ_file):

    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    all_summ_path = os.path.join(clc_align_dir, all_summ_file) 
    create_summ_file(all_summ_path)

    os.chdir(clc_align_dir)
    xlsfiles = sorted([os.path.abspath(x) for x in glob.glob('*RNA-Seq.xls')])
    print(xlsfiles)
    for xf in xlsfiles:
        d = get_align_info_clc(xf)
        berkid = xf.split('_')[4]
        print('berkid', berkid)
        cur = conn.cursor()
        sample = rdl.get_samplename(berkid, cur)
        cur.close()
        write_summ_file(all_summ_path, d, berkid, sample)



def get_align_info_clc(xlsfile):

    csvfile = xlsfile.rstrip('.xls') + ('_mapinfo.csv')
    cmd = 'xls2csv {} > {}'.format(xlsfile, csvfile)
    os.system(cmd)
    d = {}
    with open(csvfile, 'r') as f:
        fr = csv.reader(f, delimiter=',')
        for l in fr:
            if l.count('Total fragments') > 0: 
                d['input_reads'] = int(l[l.index('Total fragments')+1])
            if l.count('Counted fragments') > 0:
                d['mapped'] = int(l[l.index('Counted fragments')+1])
            if l.count(' - uniquely') > 0:
                unique = int(l[l.index(' - uniquely')+1])
            if l.count(' - non-specifically') > 0:
                d['multireads'] = int(l[l.index(' - non-specifically')+1])

    print(d) 
    return(d)

def create_summ_file(all_summ_file):
    with open (all_summ_file, 'w') as g:
        g.write('Berkid\tSample\tInput\tMapped\t% of Input\tMulti-alignment\t% Multi\n')


def write_summ_file(all_summ_file, d, berkid, sample):

        d['pmulti'] = d['multireads']/d['mapped']*100
        d['pmapped'] = d['mapped']/d['input_reads']*100

        with open (all_summ_file, 'a') as g:
            g.write('{}\t{}\t{:,}\t{:,}\t{:.1f}\t{:,}\t{:.1f}\n'.format(berkid,
                sample, d['input_reads'], d['mapped'], d['pmapped'], 
                d['multireads'], d['pmulti']))
    
if __name__ == '__main__':
    batch_align_summ_clc(CLC_ALIGN_DIR, ALL_SUMM_FILE)
