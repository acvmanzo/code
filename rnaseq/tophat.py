import sys
import os
import glob

#cat NA10831_ATCACG_L002_R1_001.fastq.gz NA10831_ATCACG_L002_R1_002.fastq.gz > NA10831_ATCACG_L002_R1_combined.fastq.gz


def get_dirs(folder, globstring):
    os.chdir(folder)
    dirs = [os.path.abspath(x) for x in sorted(glob.glob('{0}').format(globstring))]
    return(dirs)

def get_exptdirs(seqbase):
    os.chdir(seqbase)
    exptdirs = [

def get_sampledirs(exptdir):
    os.chdir(exptdir)
    sampledirs = 
    return(sampledirs)

def gen_combined_gzfile(sampledir):
    '''
    Input:
    sampledir = contains sequence files and has the name 'Sample_RGxx0xxx'
    '''
    samplename = os.path.basename(sampledir).split('_')[1]
    gzfiles = ' '.join(glob.glob('*.fastq.gz'))
    #gzfilestring = ' '.join(gzfiles)
    combined_gzfile = '{}_combined.fastq.gz'.format(samplename)
    if not os.path.exists(combined_gzfile):
        catcmd = 'cat {} > {}'.format(gzfiles, combined_gzfile)
        print('Generating {}'.format(combined_gzfile))
        os.system(catcmd)
    else:
        print('{} exists'.format(combined_gzfile))


def mgen_combined_gzfile(sampledirs):
    for sd in sampledirs:
        os.chdir(sd)
        gen_combined_gzfile(sd)


seqbase = '/home/andrea/rnaseqanalyze/sequences/'
exptdir = 
