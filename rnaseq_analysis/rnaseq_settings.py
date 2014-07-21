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
    #edger/
        #date_time_edger.log
        #prot_coding_genes/
            #Betaintnu_F/
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
        #date_time_rnaseq_settings.py


if args.option == 'unstranded':
    TH_RESDIR = 'results_tophat'
    CUFF_TABLE = 'cufflinks_data'
    HTSEQ_TABLE = 'htseq'
    DEGENE_TABLE = 'degenes'

if args.option == '2str':
    TH_RESDIR = 'results_tophat_2str'
    CUFF_TABLE = 'cufflinks_data_2str'
    HTSEQ_TABLE = 'htseq_2str'
    DEGENE_TABLE = 'degenes_2str'

SAMPLEINFO_TABLE = 'autin'

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

SET_DIR_ORIG = '/home/andrea/Documents/lab/code/rnaseq_analysis'
SET_FILE = 'rnaseq_settings.py'
SET_PATH_ORIG = os.path.join(SET_DIR_ORIG, SET_FILE)

TH_RESDIRPATH = os.path.join(ANALYSIS_PATH, TH_RESDIR)
TH_DIR = 'tophat_out'
THCMD_FILE = 'tophatcmd.txt'
BAM_FILE = 'accepted_hits.bam'
TH_LOG_FILE = 'tophat.log'
TH_SET_PATH_COPY = os.path.join(TH_RESDIRPATH, os.path.splitext(SET_FILE)[0])

CUFF_DIR = 'cufflinks_out'
CUFFLOG_FILE = 'cufflinks.log'
CUFFCMD_FILE = 'cufflinkscmd.txt'
CUFF_GFPKM = 'genes.fpkm_tracking'
BERKID_CUFF_GFPKM = 'genes_berkid.fpkm_tracking'

CORR_DIR = 'correlations'
CORR_DIRPATH = os.path.join(ANALYSIS_PATH, CORR_DIR, TH_RESDIR)
CORR_SET_PATH_COPY = os.path.join(CORR_DIRPATH, os.path.splitext(SET_FILE)[0])
CORR_FIGSET_FILE = 'corrfig_settings.py'
CORR_FIGSET_PATH_ORIG = os.path.join(SET_DIR_ORIG, CORR_FIGSET_FILE)
CORR_FIGSET_PATH_COPY = os.path.join(CORR_DIRPATH, os.path.splitext(CORR_FIGSET_FILE)[0])
PEARSON_CORRFILE = 'pearson_correlations.txt' 
SPEARMAN_CORRFILE = 'spearman_correlations.txt' 
CORRLOG_FILE = 'correlations.log'
#SELECTLIST = ['t0.tracking_id', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 
    #'t1.berkid', 't1.fpkm', 't1.fpkm_status']
SELECTLIST = ['t0.gene_short_name', 't0.berkid', 't0.fpkm', 't0.fpkm_status',
    't1.berkid', 't1.fpkm', 't1.fpkm_status']
MAXFPKM = False # Only genes with FPKMs below this value will be used to 
# calculate correlations; if no limit is desired, set to False.
PC_LOG = True # If set to 'True', adds 1 to each value in the list of 
# FPKMS for each sample and then log transforms the data (log base 2).

HTSEQ_DIR = 'htseq_out'
HTSEQ_CMD_FILE = 'htseq.info'
HTSEQ_LOG_FILE = 'htseq.log'
HTSEQ_FILE = 'htseqcount'
RES_SAMPLE_GLOB = 'RG*'

EDGER_DIR = 'edger'
EDGER_DIRPATH = os.path.join(ANALYSIS_PATH, EDGER_DIR, TH_RESDIR)
EDGER_LOG_FILE = 'edger.log'
EDGER_METADATA_FILE = 'metadata.txt'
EDGER_GROUP_FILE = 'groups'
EDGER_MDSPLOT_FILE = 'mds_plot.png'
EDGER_MVPLOT_FILE = 'mean_var_plot.png'
EDGER_BCVPLOT_FILE = 'biol_cv_plot.png'
EDGER_MAPLOT_FILE = 'masmear_plot_'
EDGER_TOPTAGS_FILE = 'toptags_edgeR.csv'
EDGER_DBTOPTAGS_FILE = 'db_toptags_edgeR.csv'
EDGER_TOPTAGS_FDR_FILE = 'toptags_edgeR_'
DE_HH_FILE = 'human_hom_'

DESEQ_DIR = 'deseq'
DESEQ_DIRPATH = os.path.join(ANALYSIS_PATH, DESEQ_DIR, TH_RESDIR)
DESEQ_LOG_FILE = 'deseq.log'


BERKIDLEN = 8

RNASEQDICT =    {'seq_dir': SEQ_PATH,
                'seq_subdir': SEQ_SUBDIR,
                'seqbatchglob': SEQBATCHGLOB,
                'sampleseqglob': SAMPLESEQGLOB,
                'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX,
                'sampleinfo_table': SAMPLEINFO_TABLE,
                'set_path_orig': SET_PATH_ORIG,
                'analysis_path': ANALYSIS_PATH,
                'th_resdirpath': TH_RESDIRPATH,
                'th_log_file': TH_LOG_FILE,
                'th_dir': TH_DIR,
                'th_cmd_file': THCMD_FILE,
                'bam_file': BAM_FILE,
                'th_set_path_copy': TH_SET_PATH_COPY, 
                'cuff_dir': CUFF_DIR,
                'cufflog_file': CUFFLOG_FILE,
                'cuffcmd_file': CUFFCMD_FILE,
                'corr_dir': CORR_DIR,
                'corr_dirpath': CORR_DIRPATH,
                'corr_set_path_copy': CORR_SET_PATH_COPY,
                'corr_figset_file': CORR_FIGSET_FILE,
                'corr_figset_path_orig': CORR_FIGSET_PATH_ORIG,
                'corr_figset_path_copy': CORR_FIGSET_PATH_COPY,
                'pearson_corrfile': PEARSON_CORRFILE,
                'spearman_corrfile': SPEARMAN_CORRFILE,
                'corrlog_file': CORRLOG_FILE,
                'htseq_dir': HTSEQ_DIR,
                'htseq_cmd_file': HTSEQ_CMD_FILE,
                'htseq_log_file': HTSEQ_LOG_FILE,
                'htseq_file': HTSEQ_FILE,
                'htseq_table': HTSEQ_TABLE,
                'edger_dirpath': EDGER_DIRPATH,
                'edger_metadata_file': EDGER_METADATA_FILE,
                'edger_log_file': EDGER_LOG_FILE,
                'edger_group_file': EDGER_GROUP_FILE,
                'edger_mdsplot_file': EDGER_MDSPLOT_FILE,
                'edger_mvplot_file': EDGER_MVPLOT_FILE,
                'edger_bcvplot_file': EDGER_BCVPLOT_FILE,
                'edger_maplot_file': EDGER_MAPLOT_FILE,
                'edger_toptags_file': EDGER_TOPTAGS_FILE,
                'edger_dbtoptags_file': EDGER_DBTOPTAGS_FILE,
                'edger_toptags_fdr_file': EDGER_TOPTAGS_FDR_FILE,
                'deseq_dir': DESEQ_DIR,
                'deseq_dirpath': DESEQ_DIRPATH,
                'deseq_log_file': DESEQ_LOG_FILE,
                'deseq_metadata_file': EDGER_METADATA_FILE,
                'deseq_group_file': EDGER_GROUP_FILE,
                'degene_table': DEGENE_TABLE,
                'de_hh_file': DE_HH_FILE
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


