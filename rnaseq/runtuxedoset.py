
#SEQ_DIR = '/home/andrea/Documents/lab/RNAseq/sequences'
#RESULTS_DIR = '/home/andrea/Documents/lab/RNAseq/results'
SEQ_DIR = '/home/andrea/rnaseqanalyze/sequences'
RESULTS_DIR = '/home/andrea/rnaseqanalyze/results'

SEQ_SUBDIR = 'sequences'
SEQBATCHGLOB = '2014-*/'
SAMPLESEQGLOB = 'Sample_*'

COMBINED_FASTQ_SUFFIX = 'combined.fastq.gz'
TOPHAT_DIR = 'tophat_out'
TOPHATCMD_FILE = 'tophatcmd.txt'
BAM_FILE = '{}/{}'.format(TOPHAT_DIR, 'accepted_hits.bam')
CUFFLINKS_DIR = 'cufflinks_out'
CUFFLINKSLOG_FILE = 'cufflinks.log'
CUFFLINKSCMD_FILE = 'cufflinkscmd.txt'

GFF_FILE = '/home/andrea/rnaseqanalyze/references/dmel-all-filtered-r5.57.gff'
MITOGFF_FILE = '/home/andrea/rnaseqanalyze/references/dmel-dmel_mitochondrion_genome-r5.57.gff'
BTINDEX = '/home/andrea/rnaseqanalyze/references/dmel-all-chromosome-r5.57'

DIR_INFO = {
'seq_dir': SEQ_DIR,
'seq_subdir': SEQ_SUBDIR,
'results_dir': RESULTS_DIR,
'seqbatchglob': SEQBATCHGLOB,
'sampleseqglob': SAMPLESEQGLOB
}

TOPHAT_CUFFLINKS_INFO = {
'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX,
'tophat_dir': TOPHAT_DIR,
'tophatcmd_file': TOPHATCMD_FILE,
'bam_file': BAM_FILE,
'cufflinks_dir': CUFFLINKS_DIR,
'cufflinkslog_file': CUFFLINKSLOG_FILE,
'cufflinkscmd_file': CUFFLINKSCMD_FILE,
'gff_file': GFF_FILE,
'mitogff_file': MITOGFF_FILE,
'btindex': BTINDEX
}
