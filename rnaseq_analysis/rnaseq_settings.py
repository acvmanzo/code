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
            #htseq_out/
                #htseqcount
                #htseqcount_berkid
                #htseqcount.info
                #htseqcount_prot_coding_genes
            #tophat_out
            #cufflinks.info
            #tophat.info
        #RGAM009B/
            #cufflinks_out/
            #htseq_out/
                #htseqcount
                #htseqcount_berkid
                #htseqcount.info
                #htseqcount_prot_coding_genes
            #tophat_out
            #cufflinks.info
            #tophat.info
        #tophat_all_align_summary.txt
        #tuxedo_settings.py



SEQ_PATH = '/home/andrea/Documents/lab/RNAseq/sequences'
SEQ_SUBDIR = 'sequences'
SEQBATCHGLOB = '2014-*/'
SAMPLESEQGLOB = 'Sample_*'
COMBINED_FASTQ_SUFFIX = 'combined.fastq.gz'

ANALYSIS_PATH = '/home/andrea/Documents/lab/RNAseq/analysis'

TH_RESDIR = 'results_tophat_test'
TH_DIR = 'tophat_out'
THCMD_FILE = 'tophatcmd.txt'
BAM_FILE = 'accepted_hits.bam'
TH_LOG_FILE = 'tophat.log'
TH_SET_PATH_ORIG = '/home/andrea/Documents/lab/code/rnaseq_analysis'
TH_SET_FILE = 'tuxedo_settings.py'

CUFFLINKS_DIR = 'cufflinks_out'
CUFFLINKSLOG_FILE = 'cufflinks.log'
CUFFLINKSCMD_FILE = 'cufflinkscmd.txt'

SAMPLEINFO_TABLE = 'autin'

BERKIDLEN = 8

TH_RESDIRPATH = os.path.join(ANALYSIS_PATH, TH_RESDIR)
RNASEQDICT =    {'seq_dir': SEQ_PATH,
                'seq_subdir': SEQ_SUBDIR,
                'seqbatchglob': SEQBATCHGLOB,
                'sampleseqglob': SAMPLESEQGLOB,
                'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX,
                'analysis_path': ANALYSIS_PATH,
                'th_resdirpath': TH_RESDIRPATH,
                'th_log_file': os.path.join(TH_RESDIRPATH, TH_LOG_FILE),
                'th_dir': TH_DIR,
                'th_cmd_file': THCMD_FILE,
                'bam_file': '{}/{}'.format(TH_DIR, BAM_FILE),
                'th_set_path_orig': os.path.join(TH_SET_PATH_ORIG, TH_SET_FILE),
                'th_set_path_copy': os.path.join(TH_RESDIRPATH, TH_SET_FILE),
                'cufflinks_dir': CUFFLINKS_DIR,
                'cufflinkslog_file': CUFFLINKSLOG_FILE,
                'cufflinkscmd_file': CUFFLINKSCMD_FILE
                }
#print(RNASEQDICT)
#SEQDICT = {'seq_dir': SEQ_PATH,
            #'seq_subdir': SEQ_SUBDIR,
            #'seqbatchglob': SEQBATCHGLOB,
            #'sampleseqglob': SAMPLESEQGLOB,
            #'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX
            #}
#ANALYSISDICT = {'analysis_path': ANALYSIS_PATH}

#TH_RESDIR = os.path.join(d['analysis_path'], TH_RESDIR)

#TOPHATDICT = {'th_resdir': th_resdir,
                #'th_log_file': th_resdir, TH_LOG_FILE),
                #'th_dir': TH_DIR,
                #'th_cmd': THCMD_FILE,
                #'bam_file': '{}/{}'.format(th_resdir, BAM_FILE),
                #'th_set_path_orig': os.path.join(TH_SET_PATH_ORIG,
                #'th_set_path_copy': os.path.join(th_resdir,
                    #TH_SET_FILE)
                #}

#CUFFLINKDICT = {'cufflinks_dir': CUFFLINKS_DIR,
                #'cufflinkslog_file': CUFFLINKSLOG_FILE,
                #'cufflinkscmd_file': CUFFLINKSCMD_FILE
                #}



