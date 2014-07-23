# Script with functions to that extract alignment statistics for each sample 
# and saves them to a file. Have functions to extract statistics for clc and
# tophat alignments, and htseq-count results.

import csv
import libs.htseqlib as hl
import libs.rnaseqlib as rl
import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import os
import glob

TH_ALIGN_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat'
CLC_ALIGN_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/CLC_results'
TOPHAT_DIR = 'tophat_out'
HTSEQ_DIR = 'htseq_out'
SUMM_FILE = 'align_summary.txt'
CLC_ALL_SUMM_FILE = 'clc_all_align_summary.txt'
HTSEQ_FILE = 'htseqcount'
TH_ALL_SUMM_FILE = 'tophat_all_align_summary.txt'
HTSEQ_ALL_SUMM_FILE = 'htseq_all_unique_summary.txt'


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
    #print(d) 
    return(d)

def add_htseq_counts(htseqfile):
    '''Adds up the counts found in the htseq-count file.
    '''
    counts = 0 
    with open(htseqfile, 'r') as f:
        for l in f:
            gene, count = l.split('\t')
            if '__' in gene:
                continue
            counts += int(count)
    logging.info(counts)
    return(counts)

def add_clc_counts(clcfile):
    '''Adds up the counts in the CLC file: Unique gene reads'''
    counts = 0
    with open(clcfile, 'r') as f:
        print(next(f).split('\t')[5])
        for l in f:
            count = l.split('\t')[5]
            counts += int(count)
    logging.info(counts)
    return(counts)


def create_summ_file(all_summ_file):
    with open (all_summ_file, 'w') as g:
        g.write('Berkid\tSample\tInput\tMapped\t% of Input\tMulti-alignment\t% Multi\n')

def write_summ_file(all_summ_file, d, berkid, sample):
    '''Writes the summary file.
    Inputs:
    all_summ_file: output file
    d: dictionary output by get_align_info_clc or get_align_info_tophat
    berkid: berkeley id
    sample: sample name matching berkid
    '''

    d['pmulti'] = d['multireads']/d['mapped']*100
    d['pmapped'] = d['mapped']/d['input_reads']*100

    print(d)
    print(all_summ_file)
    #print(os.getcwd())
    with open(all_summ_file, 'a') as g:
        g.write('{}\t{}\t{:}\t{:}\t{:.1f}\t{:}\t{:.1f}\n'.format(berkid,
            sample, d['input_reads'], d['mapped'], d['pmapped'], 
            d['multireads'], d['pmulti']))


def batch_align_summ_tophat(th_align_dir, all_summ_file, tophat_dir, summ_file):
    '''Extracts alignment information from each sample folder and combines
    them into one file.
    Inputs:
    th_align_dir: tophat results directory containing all the sample folders
    all_summ_file: name of output file
    tophat_dir: name of the directory within each sample folder that contains
        the alignment files
    summ_file: name of the alignment summary file output by tophat
    '''
    conn = psycopg2.connect("dbname=rnaseq user=andrea")

    all_summ_path = os.path.join(th_align_dir, all_summ_file) 
    create_summ_file(all_summ_path)

    os.chdir(th_align_dir)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        cur = conn.cursor()
        os.chdir(os.path.join(resdir, tophat_dir))
        berkid = os.path.basename(resdir)
        print(berkid)
        try:
            sample = rl.get_samplename(berkid, cur)
            cur.close()
            print(sample)
        except TypeError:
            continue
        d = get_align_info_tophat(summ_file)
        write_summ_file(all_summ_path, d, berkid, sample)
    conn.close()
        
def batch_align_summ_clc(clc_align_dir, all_summ_file):
    '''Extracts alignment information from each CLC summary file and combines
    them into one file.
    Inputs:
    clc_align_dir: CLC results directory containing all the exported CLC 
        output files
    all_summ_file: name of output file
    '''

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
        sample = rl.get_samplename(berkid, cur)
        cur.close()
        write_summ_file(all_summ_path, d, berkid, sample)
    conn.close()


def add_aligner_col(all_summ_file, aligner):

    new_all_summ_file = all_summ_file.rstrip('.txt') + 'withal.txt'

    with open(new_all_summ_file, 'w') as g:
        with open(all_summ_file, 'r') as f:
            #g.write(next(f).strip('\n') + '\tAligner\n')
            next(f)
            for l in f:
                g.write(l.replace(',', '').rstrip('\n') + '\t{}\n'.format(aligner))


def batch_align_summ_htseqcount(th_align_dir, all_summ_file, htseq_dir, 
        htseqfile):
    '''Extracts alignment information from each sample folder and combines
    them into one file.
    Inputs:
    th_align_dir: tophat results directory containing all the sample folders
    all_summ_file: name of output file
    tophat_dir: name of the directory within each sample folder that contains
        the alignment files
    summ_file: name of the alignment summary file output by tophat
    '''
    conn = psycopg2.connect("dbname=rnaseq user=andrea")

    all_summ_path = os.path.join(th_align_dir, all_summ_file) 
    create_summ_file(all_summ_path)

    os.chdir(th_align_dir)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        try:
            os.chdir(os.path.join(resdir, htseq_dir))
            berkid = os.path.basename(resdir)
            print(berkid)
            try:
                cur = conn.cursor()
                sample = rl.get_samplename(berkid, cur)
                cur.close()
                print(sample)
            except TypeError:
                continue
            count = add_htseq_counts(htseqfile)
            print(count)
            with open(all_summ_path, 'a') as g:
                g.write('{}\t{}\t{:}\n'.format(berkid,
                    sample, count))
        except FileNotFoundError:
            continue
    conn.close()

def list_htseq_counts(htseqfile):
    '''Adds up the counts found in the htseq-count file.
    '''
    counts = []
    with open(htseqfile, 'r') as f:
        for l in f:
            gene, count = l.split('\t')
            if '__' in gene:
                continue
            counts.append(int(count))
    return(counts)

def plot_htseqcount_dist(htseqfile):
    '''Run from htseq_out folder'''
    counts = list_htseq_counts(htseqfile)
    logcounts = [np.log2(c+1) for c in counts]
    #plt.hist(logcounts, bins=1000, color='b')
    #plt.ylim(0, 500)
    #plt.savefig('loghist.png')
    #plt.close()
    #plt.hist(counts, bins=10000, color='b')
    #plt.xlim(0, 100000)
    #plt.ylim(0, 4000)
    #plt.savefig('hist.png')
    #plt.close()
    #plt.boxplot(counts)
    #plt.ylim(0, 10000)
    #plt.savefig('boxplot.png')
    d = {}
    d['med'] = np.median(counts)
    d['logmed'] = np.median(logcounts)
    d['max'] = np.max(counts)
    d['logmax'] = np.max(logcounts)
    d['min'] = np.min(counts)
    d['logmin'] = np.min(logcounts)
    return(d)


if __name__ == '__main__':
    #batch_align_summ_tophat(TH_ALIGN_DIR, TH_ALL_SUMM_FILE, TOPHAT_DIR, 
            #SUMM_FILE)

    #add_aligner_col(CLC_ALL_SUMM_FILE, 'clc')
    add_aligner_col(TH_ALL_SUMM_FILE, 'tophat_2str')
    batch_align_summ_htseqcount(TH_ALIGN_DIR, HTSEQ_ALL_SUMM_FILE, HTSEQ_DIR,
        HTSEQ_FILE)
