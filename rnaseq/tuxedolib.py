import sys
import os
import glob
import cmn.cmn as cmn


def get_dirs(folder, globstring):
    '''Returns all the directories in a folder that match the string 'globstring'
    '''
    os.chdir(folder)
    dirs = [os.path.abspath(x) for x in sorted(glob.glob('{0}'.format(globstring)))]
    return(dirs)

#def get_exptdirs(seqbase):
    #'''Returns all the directories in the seq basefolder that match the globstring'''
    #return(get_dirs(seqbase, '2014-*/'))

#def get_sampledirs(exptdir):
    #seqdir = os.path.join(exptdir, 'sequences')
    #return(get_dirs(seqdir, 'Sample_*'))

def gen_combined_gzfile(sample_seqdir, combined_gzpath):
    '''
    Input:
    sampledir = contains sequence files and has the name 'Sample_RGxx0xxx'
    results_dir = main results directory
    combined_gzpath = path of combined_gzpath
    '''
    os.chdir(sample_seqdir)
    gzfiles = ' '.join(sorted(glob.glob('*[0-9].fastq.gz')))
    #print(os.path.exists(combined_gzpath))
    if not os.path.exists(combined_gzpath):
        catcmd = 'cat {} > {}'.format(gzfiles, combined_gzpath)
        print('Generating {}'.format(os.path.basename(combined_gzpath)))
        os.system(catcmd)
    else:
        print('{} exists'.format(combined_gzpath))


def get_combined_gzpath(sample_resdir, sample, combined_fastq_suffix):
    '''Inputs:
    sample_resdir = results directory for the sample
    sample = name of samplek
    combined_fastq_suffix = suffix to append to end of combined file
    '''
    return(os.path.join(sample_resdir, '{}_{}'.format(sample, combined_fastq_suffix)))


def unzip_gzfile(gzfile):
    uzfile = gzfile.strip('.gz')
    if not os.path.exists(uzfile):
        print('Unzipping {0}'.format(os.path.basename(gzfile)))
        os.system('gunzip {}'.format(gzfile))
    else:
        print('Unzipped {0} exists'.format(os.path.basename(gzfile)))


def mgen_combined_gzfile(sampledirs, results_base_dir):
    for sd in sampledirs:
        os.chdir(sd)
        combined_gzpath = gen_combined_gzfile(sd, results_base_dir)

def run_tophat(tophatdir, gff_file, btindex, fastafile, tophatcmd_file):
    tophatcmd = 'tophat -o {} -p 8 --no-coverage-search -G {} {} {}'.format(tophatdir, gff_file, btindex, fastafile)
    print(tophatcmd)
    #os.system(tophatcmd)
    with open(tophatcmd_file, 'w') as f:
        f.write(tophatcmd)


def run_cufflinks(mitogff_file, gff_file, bam_file, cufflinkslog_file, cufflinkscmd_file):
    cufflinkscmd = 'cufflinks -o cufflinks_out -p 8 -M {} -G {} -u {} >& {}'.format(mitogff_file, gff_file, bam_file, cufflinkslog_file)
    print(cufflinkscmd)
    with open(cufflinkscmd_file, 'w') as f:
        f.write(cufflinkscmd)
    #os.system(cufflinkscmd)

def run_tophat_cufflinks(sample, sample_seqdir, sample_resdir, tophat_cufflinks_info):
    '''
    Runs tophat and cufflinks on one sample.
    Inputs:
    sample_seqdir = directory containing the sequence files for each sample
    results_dir = main results directory
    tophat_cufflinks_info: dictionary containing the following keys/values:
        combined_fastq_suffix = suffix for the combined fastq file
        tophat_dir = directory for tophat results
        tophatcmd_file = file containing the tophat command used
        bam_file = name of bamfile output by the tophat program
        cufflinks_dir = directory for cufflinks results
        cufflinkslog_file = file containing info about cufflinks program (writes stdout to this file)
        cufflinkscmd_file = file containing the cufflinks command used
        gff_file = name of genome gff file for use wtih tophat and cufflinks 
        mitogff_file = name of mitochondriol gff file for use in masking during cufflinks
        btindex = name of bowtie index files used for tophat
    '''
    d = tophat_cufflinks_info 
    os.chdir(sample_seqdir)
    # Concatenate the sequence files into one file.
    combined_gzpath = get_combined_gzpath(sample_resdir, sample, d['combined_fastq_suffix'])

    gen_combined_gzfile(sample_seqdir, combined_gzpath) 
    # Unzip the combined sequence file.
    unzip_gzfile(combined_gzpath)
    
    # Run tophat.
    os.chdir(sample_resdir)
    fastafile = os.path.basename(combined_gzpath).strip('.gz')
    print(fastafile)    

    if os.path.exists(d['tophat_dir']):
        print('tophat directory exists')
    else:
        run_tophat(d['tophat_dir'], d['gff_file'], d['btindex'], fastafile, d['tophatcmd_file'])
        os.remove(fastafile)
   
    # Run cufflinks.
    if os.path.exists(d['cufflinks_dir']):
        print('cufflinks directory exists')
    else:
        run_cufflinks(d['mitogff_file'], d['gff_file'], d['bam_file'], d['cufflinkslog_file'], d['cufflinkscmd_file']) 
    

def mrun_tophat_cufflinks(dir_info, tophat_cufflinks_info):
    '''Runs tophat and cufflinks on multiple samples.
    Inputs:
    dir_info: List containing the following variables:
        seqdir = directory that contains all the sequence files; I have divided the 
        sequence files into 'sequence batch' folders based on the date that they were sent to be 
        sequenced. Each 'sequence batch' folder contains multiple 'sample folders' that contains the
        sequences for that sample.
        seq_subdir = directory that contains the compressed sequence files in each sample folder
        results_dir = directory that will contain all the aligning and expression results for each sample
        seqbatchglob = string that is unique to names of sequence batch folders
        sampleglob = string that is unique to names of sample folders
    tophat_cufflinks_info: List containing the variables needed for the run_tophat_cufflinks()
    '''
    d = dir_info
    seqbatchdirs = get_dirs(d['seq_dir'], d['seqbatchglob']) # Finds all the sequence batch folders.
    print('Sequence batch directories', seqbatchdirs)
    for sbd in seqbatchdirs:
        try:
            sample_seqdirs = get_dirs(os.path.join(sbd, d['seq_subdir']), d['sampleseqglob'])
            print('Sample directories')
            print([os.path.basename(x) for x in sample_seqdirs])
        except FileNotFoundError:
            print('Sequence folder does not exist')
            continue
        
        for sample_seqdir in sample_seqdirs:
            sample = os.path.basename(sample_seqdir).split('_')[1]
            print(sample)
            sample_resdir = os.path.join(d['results_dir'], sample) 
            cmn.makenewdir(sample_resdir)
            print('Running tophat and cufflinks')
            run_tophat_cufflinks(sample, sample_seqdir, sample_resdir , tophat_cufflinks_info)

