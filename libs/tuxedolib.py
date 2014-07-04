# Library containing functions useful for running tophat and cufflinks on 
# multiple samples.

import sys
import os
import glob
import cmn.cmn as cmn
import logging
import datetime
import psycopg2


def get_berkid_info(conn, berkidlist, infotable, colquery):
    '''Queries a postgresql database table (infotable) and extracts the 
    information specified in colquery for the berkids specified in berkidlist.
    Returns a dictionary where the keys are the berkeley ids and the
    values are a tuple of the database values.
    Inputs:
    conn = open psycopg2 connection to the database
    berkidlist = list of berkids
    infotable = database table to be queried
    colquery = list of columns that will be returned; input to a SELECT 
    statement
    '''
    cur = conn.cursor()
    berkid_dict = {}
    for bid in berkidlist:
        query = "SELECT {} FROM {} WHERE berkid = '{}'".format(', '.join(colquery), 
                infotable, bid)
        cur.execute(query)
        berkid_dict[bid] = cur.fetchall()[0]
    cur.close()
    return(colquery, berkid_dict)

def gen_seq_paths(colquery, berkid_dict, seq_dir, seq_subdir):
    '''From the berkid_dict generated in get_berkid_info(), generates a list of
    sequence directory paths.'''
    seqdir_paths = []
    seqd_col = colquery.index('seqd')
    for berkid, info in berkid_dict.items():
        seqd = info[seqd_col].strftime("%Y-%m%d")
        seqdir_path = os.path.join(seq_dir, seqd, seq_subdir, \
            'Sample_{}'.format(berkid))
        seqdir_paths.append(seqdir_path)
    return(seqdir_paths)

def get_berkid_seq_res_paths(berkidlist, infotable, colquery, seq_dir,\
        seq_subdir, results_dir):
    '''For a list of berkids (berkidlist), generates the paths to the 
    sequence directories and the directories containing the results of tophat
    and cufflinks analyses.
    '''
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    colquery, berkid_dict = get_berkid_info(conn, berkidlist, \
        infotable, colquery)
    conn.close()
    seqpaths = gen_seq_paths(colquery, berkid_dict, seq_dir, seq_subdir)
    respaths = [os.path.join(results_dir, berkid) for berkid in berkidlist]
    return(seqpaths, respaths)

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
    '''Combines multiple gzipped sequence files into one combined file.
    Input:
    sampledir = contains sequence files and has the name 'Sample_RGxx0xxx'
    results_dir = main results directory
    combined_gzpath = path of combined_gzpath
    '''
    os.chdir(sample_seqdir)
    gzfiles = ' '.join(sorted(glob.glob('*[0-9].fastq.gz')))
    #logging.info(os.path.exists(combined_gzpath))
    if not os.path.exists(combined_gzpath):
        catcmd = 'cat {} > {}'.format(gzfiles, combined_gzpath)
        logging.info('Generating %s', os.path.basename(combined_gzpath))
        os.system(catcmd)
    else:
        logging.info('%s exists', os.path.basename(combined_gzpath))


def get_combined_gzpath(sample_resdir, sample, combined_fastq_suffix):
    '''Generates the name of the combined sequence file used for the function gen_combined_gzfile().
    Inputs:
    sample_resdir = results directory for the sample
    sample = name of samplek
    combined_fastq_suffix = suffix to append to end of combined file
    Output:
    String specifying the path to the combined gzipped sequence file
    '''
    return(os.path.join(sample_resdir, '{}_{}'.format(sample, combined_fastq_suffix)))


def unzip_gzfile(gzfile):
    '''Gunzips the gzfile'''
    uzfile = gzfile.strip('.gz')
    if not os.path.exists(uzfile):
        logging.info('Unzipping %s', os.path.basename(gzfile))
        os.system('gunzip {}'.format(gzfile))
    else:
        logging.info('Unzipped %s exists', os.path.basename(gzfile))


def mgen_combined_gzfile(sampledirs, results_base_dir):
    '''Generates a combined sequence file for the directories in sampledirs and 
    saves them in the appropriate folder in the results_base_dir.'''
    for sd in sampledirs:
        os.chdir(sd)
        combined_gzpath = gen_combined_gzfile(sd, results_base_dir)

def run_tophat(tophatdir, gff_file, btindex, fastafile, tophatcmd_file):
    '''Runs tophat from the command line with the indicated options and writes the command
    used into a file.
    Inputs:
    tophatdir = name of the directory where tophat saves its results
    gff_file = name of the gff file used when tophat aligns using a reference genome
    btindex = root name of the bowtie index files need by tophat
    fastafile = name of the combined, unzipped fasta file containing reads
    tophatcmd_file = name of the file where the tophat command is written
    '''
    tophatcmd = 'tophat -o {} -p 8 --no-coverage-search -G {} {} {}'.format(tophatdir, gff_file, 
            btindex, fastafile)
    logging.info('%s', tophatcmd)
    os.system(tophatcmd)
    with open(tophatcmd_file, 'w') as f:
        f.write(tophatcmd)


def run_cufflinks(mitogff_file, gff_file, bam_file, cufflinkslog_file, cufflinkscmd_file):
    '''Runs cufflinks from the command line with the indicated options and writes the command
    used into a file.
    Inputs:
    mitogff_file: gff file containing mitochondrial genome annotations for use with masking in 
    cufflinks
    gff_file: gff file used when cufflinks quanitifies transcript expression using a reference 
    genome
    bam_file: bam file with the alignment information; output by tophat
    cufflinkslog_file: file into which the stdout of the cufflinks command will be written
    cufflinkscmd_file: file into which the cufflinks command is written
    '''

    cufflinkscmd = 'cufflinks -o cufflinks_out -p 8 -M {} -G {} -u {} >& {}'.format(mitogff_file, 
            gff_file, bam_file, cufflinkslog_file)
    logging.info('%s', cufflinkscmd)
    with open(cufflinkscmd_file, 'w') as f:
        f.write(cufflinkscmd)
    os.system(cufflinkscmd)

def run_tophat_cufflinks(sample, sample_seqdir, sample_resdir, tophat_cufflinks_info):
    '''
    Runs tophat and cufflinks on one sample.
    Inputs:
    sample = berkid for the sample
    sample_seqdir = directory containing the sequence files for each sample
    results_dir = main results directory
    tophat_cufflinks_info: dictionary containing the following keys/values:
        combined_fastq_suffix = suffix for the combined fastq file
        tophat_dir = directory for tophat results
        tophatcmd_file = file containing the tophat command used
        bam_file = name of bamfile output by the tophat program
        cufflinks_dir = directory for cufflinks results
        cufflinkslog_file = file containing info about cufflinks program (writes stdout to this 
        file)
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
    logging.info('%s', fastafile)    

    if os.path.exists(d['tophat_dir']):
        logging.warning('%s', 'tophat directory exists')
    else:
        run_tophat(d['tophat_dir'], d['gff_file'], d['btindex'], fastafile, d['tophatcmd_file'])
        os.remove(fastafile)
   
    # Run cufflinks.
    if os.path.exists(d['cufflinks_dir']):
        logging.warning('cufflinks directory exists')
    else:
        run_cufflinks(d['mitogff_file'], d['gff_file'], d['bam_file'], d['cufflinkslog_file'], 
                d['cufflinkscmd_file']) 
    

def seqdir_run_tophat_cufflinks(dir_info, tophat_cufflinks_info):
    '''Runs tophat and cufflinks on multiple samples organized in the following manner:
    main seqdir > sequence batch folder (date) > sequence subdirectory (sequences/) > sample 
    folder
    Inputs:
    dir_info: List containing the following variables:
        seqdir = directory that contains all the sequence files; I have divided the 
        sequence files into 'sequence batch' folders based on the date that they were sent to be 
        sequenced. Each 'sequence batch' folder contains multiple 'sample folders' that contains 
        the sequences for that sample.
        seq_subdir = directory that contains the compressed sequence files in each sample folder
        results_dir = directory that will contain all the aligning and expression results for 
        each sample
        seqbatchglob = string that is unique to names of sequence batch folders
        sampleglob = string that is unique to names of sample folders
    tophat_cufflinks_info: List containing the variables needed for the run_tophat_cufflinks()
    '''
    d = dir_info
    seqbatchdirs = get_dirs(d['seq_dir'], d['seqbatchglob']) # Finds all the sequence batch 
    # folders.
    logging.info('Sequence batch directories %s', seqbatchdirs)
    for sbd in seqbatchdirs:
        try:
            sample_seqdirs = get_dirs(os.path.join(sbd, d['seq_subdir']), d['sampleseqglob'])
            logging.info('Sample directories %s', [os.path.basename(x) for x in sample_seqdirs])
        except FileNotFoundError:
            logging.warning('Sequence folder does not exist')
            continue
        
        for sample_seqdir in sample_seqdirs:
            sample = os.path.basename(sample_seqdir).split('_')[1]
            logging.info('%s', sample)
            sample_resdir = os.path.join(d['results_dir'], sample) 
            if not os.path.exists(os.path.join(sample_resdir, tophat_cufflinks_info['tophat_dir'])):
                cmn.makenewdir(sample_resdir)
                logging.info('Running tophat and cufflinks')
                run_tophat_cufflinks(sample, sample_seqdir, sample_resdir , tophat_cufflinks_info)
            else:
                logging.warning('Tophat and cufflinks output exists')


