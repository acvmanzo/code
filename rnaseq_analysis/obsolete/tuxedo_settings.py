# Settings for running tuxedo scripts.

import os

#SEQ_DIR = '/home/andrea/Documents/lab/RNAseq/sequences'
#ANALYSIS_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/'
#RESULTS_DIR = os.path.join(ANALYSIS_DIR, 'results_tophat')
#LOG_FILE = os.path.join(RESULTS_DIR, 'mrun.log')
#SETTINGS_FILE = '/home/andrea/Documents/lab/code/rnaseq_analysis/tuxedo_settings.py'
#NEW_SETTINGS_FILE = os.path.join(RESULTS_DIR, 'tuxedo_settings.py')

#SEQ_SUBDIR = 'sequences'
#SEQBATCHGLOB = '2014-*/'
#SAMPLESEQGLOB = 'Sample_*'

#COMBINED_FASTQ_SUFFIX = 'combined.fastq.gz'
#TOPHAT_DIR = 'tophat_out'
#TOPHATCMD_FILE = 'tophatcmd.txt'
#BAM_FILE = '{}/{}'.format(TOPHAT_DIR, 'accepted_hits.bam')
#CUFFLINKS_DIR = 'cufflinks_out'
#CUFFLINKSLOG_FILE = 'cufflinks.log'
#CUFFLINKSCMD_FILE = 'cufflinkscmd.txt'

#GFF_FILE = '/home/andrea/rnaseqanalyze/references/dmel-r5.57/dmel-all-filtered-r5.57.gff'
#MITOGFF_FILE = '/home/andrea/rnaseqanalyze/references/dmel-r5.57/dmel-dmel_mitochondrion_genome-r5.57.gff'
#BTINDEX = '/home/andrea/rnaseqanalyze/references/dmel-r5.57/dmel-all-chromosome-r5.57'

#DIR_INFO = {
#'seq_dir': SEQ_DIR,
#'seq_subdir': SEQ_SUBDIR,
#'results_dir': RESULTS_DIR,
#'seqbatchglob': SEQBATCHGLOB,
#'sampleseqglob': SAMPLESEQGLOB
#}

#TOPHAT_CUFFLINKS_INFO = {
#'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX,
#'tophat_dir': TOPHAT_DIR,
#'tophatcmd_file': TOPHATCMD_FILE,
#'bam_file': BAM_FILE,
#'cufflinks_dir': CUFFLINKS_DIR,
#'cufflinkslog_file': CUFFLINKSLOG_FILE,
#'cufflinkscmd_file': CUFFLINKSCMD_FILE,
#'gff_file': GFF_FILE,
#'mitogff_file': MITOGFF_FILE,
#'btindex': BTINDEX
#}

REFSEQ_PATH = '/home/andrea/rnaseqanalyze/references/dmel-r5.57' 
GFF_PATH = os.path.join(REFSEQ_PATH, 'dmel-all-filtered-r5.57.gff')
MITOGFF_PATH = os.path.join(REFSEQ_PATH, 'dmel-dmel_mitochondrion_genome-r5.57.gff')
BTINDEX = os.path.join(REFSEQ_PATH, 'dmel-all-chromosome-r5.57')

REFSEQDICT =    {'refseq_path': REFSEQ_PATH,
                 'gff_path': GFF_PATH,
                 'mitogff_path': MITOGFF_PATH,
                 'btindex': BTINDEX}


