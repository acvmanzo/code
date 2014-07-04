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

REFSEQ_PATH = '/home/andrea/rnaseqanalyze/references/dmel-r5.57' 
GFF_FILE = 'dmel-all-filtered-r5.57.gff'
MITOGFF_FILE = 'dmel-dmel_mitochondrion_genome-r5.57.gff'
BTINDEX = 'dmel-all-chromosome-r5.57'

TH_RESDIR = 'results_tophat'
TH_DIR = 'tophat_out'
THCMD_FILE = 'tophatcmd.txt'
BAM_FILE = 'accepted_hits.bam'
TH_LOG_FILE = 'tophat.log'
TH_SET_FILE = 'tuxedo_settings.py'

CUFFLINKS_DIR = 'cufflinks_out'
CUFFLINKSLOG_FILE = 'cufflinks.log'
CUFFLINKSCMD_FILE = 'cufflinkscmd.txt'

SAMPLEINFO_TABLE = 'autin'

BERKIDLEN = 8

    
seqdict = {'seq_dir': SEQ_PATH,
            'seq_subdir': SEQ_SUBDIR,
            'seqbatchglob': SEQBATCHGLOB,
            'sampleseqglob': SAMPLESEQGLOB,
            'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX
            }
analysisdict = {'analysis_path': ANALYSIS_PATH}

refseqdict =    {'refseq_path': REFSEQ_PATH,
                 'gff_path': os.path.join(REFSEQ_PATH, GFF_FILE),
                 'mitogff_path': os.path.join(REFSEQ_PATH, MITOGFF_FILE),
                 'btindex_path': os.path.join(REFSEQ_PATH, BTINDEX)
                }

th_resdir = os.path.join(d['analysis_path'], 'TH_RESDIR')

tophatdict = {'th_resdir': th_resdir,
                'th_log_file': th_resdir, TH_LOG_FILE),
                'th_dir': TH_DIR,
                'th_cmd': THCMD_FILE,
                'bam_file': '{}/{}'.format(th_resdir, BAM_FILE),
                'th_settings_path': os.path.join(th_resdir,
                    TH_SET_FILE)
                }

cufflinkdict = {'cufflinks_dir': CUFFLINKS_DIR,
                'cufflinkslog_file': CUFFLINKSLOG_FILE,
                'cufflinkscmd_file': CUFFLINKSCMD_FILE
                }



