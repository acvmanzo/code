import os

#Structure of directories containing raw sequence files
#/home/andrea/Documents/lab/RNAseq/sequences/
    #2014-0401/
        #sequences/
            #Sample_RGAM009A/
                #RGAM009A_GTTTCG_L001_R1_001.fastq.gz
        #Basecall_Stats_Cxxxxxxxx.zip
    #2014-0412/
        #sequences/
            #Sample_RGAM009B/
                #RGAM009B_GGTAGC_L003_R1_001.fastq.gz

#Structure of directories that will contain analysis results 
#/home/andrea/lab/RNAseq/analysis/
    #correlations/
        #correl_tophat_pclog2/
            #Betaintnu_F/
                #Betaintnu_FA-RGAM011D_vs_Betaintnu_FB-RGAM012F_correlation.png
            #Betaintnu_M/
        #correl_tophat_protein_coding_genes_pclog2/
            #Betaintnu_F/
                #Betaintnu_FA-RGAM011D_vs_Betaintnu_FB-RGAM012F_correlation.png
            #Betaintnu_M/
    #results_tophat/
        #RGAM009A/
            #cufflinks_out/
                #genes.fpkm_tracking
                #isoforms.fpkm_tracking
                #skipped.gtf
                #transcripts.gtf
            #htseq_out/
                #htseqcount
                #htseqcount_berkid
                #htseqcount.info
                #htseqcount_prot_coding_genes
            #tophat_out/
                #logs/
                #accepted_hits.bam
                #align_summary.txt
                #deletions.bed
                #insertions.bed
                #junctions.bed
                #prep_reads.info
                #unmapped.bam
            #cufflinks.info
            #tophat.info
        #RGAM009B/
        #tophat_all_align_summary.txt
        #tuxedo_settings.py

REFSEQ_PATH = '/home/andrea/rnaseqanalyze/references/dmel-r5.57' 
GFF_PATH = os.path.join(REFSEQ_PATH, 'dmel-all-filtered-r5.57.gff')
GFF_PATH_NOFA = os.path.join(REFSEQ_PATH, 'dmel-all-filtered-r5.57-nofa.gff')
MITOGFF_PATH = os.path.join(REFSEQ_PATH, 'dmel-dmel_mitochondrion_genome-r5.57.gff')
BTINDEX = os.path.join(REFSEQ_PATH, 'dmel-all-chromosome-r5.57')

REFSEQDICT =    {'refseq_path': REFSEQ_PATH,
                 'gff_path': GFF_PATH,
                 'mitogff_path': MITOGFF_PATH,
                 'btindex': BTINDEX}


SEQ_PATH = '/home/andrea/Documents/lab/RNAseq/sequences'
SEQ_SUBDIR = 'sequences'
SEQBATCHGLOB = '2014-*/'
SAMPLESEQGLOB = 'Sample_*'
COMBINED_FASTQ_SUFFIX = 'combined.fastq.gz'

ANALYSIS_PATH = '/home/andrea/Documents/lab/RNAseq/analysis'

TH_RESDIR = 'results_tophat_secondstrand'
TH_RESDIRPATH = os.path.join(ANALYSIS_PATH, TH_RESDIR)
TH_DIR = 'tophat_out'
THCMD_FILE = 'tophatcmd.txt'
BAM_FILE = 'accepted_hits.bam'
TH_LOG_FILE = 'tophat.log'
TH_LOG_PATH = os.path.join(TH_RESDIRPATH, TH_LOG_FILE)
TH_SET_DIR_ORIG = '/home/andrea/Documents/lab/code/rnaseq_analysis'
TH_SET_FILE = 'tuxedo_settings.py'
TH_SET_PATH_ORIG = os.path.join(TH_SET_DIR_ORIG, TH_SET_FILE)
TH_SET_PATH_COPY = os.path.join(TH_RESDIRPATH, TH_SET_FILE)

CUFF_DIR = 'cufflinks_out'
CUFFLOG_FILE = 'cufflinks.log'
CUFFCMD_FILE = 'cufflinkscmd.txt'
CUFF_GFPKM = 'genes.fpkm_tracking'

HTSEQ_DIR = 'htseq_out'
HTSEQ_CMD_FILE = 'htseq.info'
HTSEQ_FILE = 'htseqcount'
RES_SAMPLE_GLOB = 'RG*'

EDGER_DIR = 'edgeR'

SAMPLEINFO_TABLE = 'autin'
HTSEQ_TABLE = 'htseq'

BERKIDLEN = 8

RNASEQDICT =    {'seq_dir': SEQ_PATH,
                'seq_subdir': SEQ_SUBDIR,
                'seqbatchglob': SEQBATCHGLOB,
                'sampleseqglob': SAMPLESEQGLOB,
                'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX,
                'analysis_path': ANALYSIS_PATH,
                'th_resdirpath': TH_RESDIRPATH,
                'th_log_path': TH_LOG_PATH,
                'th_dir': TH_DIR,
                'th_cmd_file': THCMD_FILE,
                'bam_file': BAM_FILE,
                'th_set_path_orig': TH_SET_PATH_ORIG,
                'th_set_path_copy': TH_SET_PATH_COPY, 
                'cuff_dir': CUFF_DIR,
                'cufflog_file': CUFFLOG_FILE,
                'cuffcmd_file': CUFFCMD_FILE,
                'htseq_dir': HTSEQ_DIR,
                'htseq_cmd_file': HTSEQ_CMD_FILE,
                'htseq_file': HTSEQ_FILE,
                'edger_dirpath': os.path.join(ANALYSIS_PATH, EDGER_DIR),
                }

def get_results_files(berkid):

    sample_dir = os.path.join(TH_RESDIRPATH, berkid)
    sample_th_dir = os.path.join(sample_dir, TH_DIR)
    sample_cuff_dir = os.path.join(sample_dir, CUFF_DIR)
    sample_htseq_dir = os.path.join(sample_dir, HTSEQ_DIR)

    d =     {'sample_dir': sample_dir,
             'sample_th_dir': sample_th_dir,
             'bam_path': os.path.join(sample_th_dir, BAM_FILE),
             'sample_cuff_dir': sample_cuff_dir,
             'cuff_gfpkm_path': os.path.join(sample_cuff_dir,
                 CUFF_GFPKM),
             'sample_htseq_dir': sample_htseq_dir,
             'htseq_count_path': os.path.join(sample_htseq_dir, HTSEQ_FILE)
             }
    return(d)


