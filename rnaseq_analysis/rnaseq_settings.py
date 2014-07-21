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

class RNASeqData:

    def __init__(self, option):

        if option == 'unstranded':
            self.th_resdir = 'results_tophat'
            self.cuff_table = 'cufflinks_data_un'
            self.htseq_table = 'htseq_un'
            self.degene_table = 'degenes_un'

        if option == '2str':
            self.th_resdir = 'results_tophat_2str'
            self.cuff_table = 'cufflinks_data'
            self.htseq_table = 'htseq'
            self.degene_table = 'degenes'

        self.sampleinfo_table = 'autin'

        self.refseq_path = '/home/andrea/rnaseqanalyze/references/dmel-r5.57' 
        self.gff_path = os.path.join(self.refseq_path,
                'dmel-all-filtered-r5.57.gff')
        self.gff_path_nofa = os.path.join(self.refseq_path,
                'dmel-all-filtered-r5.57-nofa.gff')
        self.mitogff_path = os.path.join(self.refseq_path, 
                'dmel-dmel_mitochondrion_genome-r5.57.gff')
        self.btindex = os.path.join(self.refseq_path,
                'dmel-all-chromosome-r5.57')

        self.seq_path = '/home/andrea/Documents/lab/RNAseq/sequences'
        self.seq_subdir = 'sequences'
        self.seqbatchglob = '2014-*/'
        self.sampleseqglob = 'Sample_*'
        self.combined_fastq_suffix = 'combined.fastq.gz'
        
        self.analysis_path = '/home/andrea/Documents/lab/RNAseq/analysis'
        
        self.set_dir_orig = '/home/andrea/Documents/lab/code/rnaseq_analysis'
        self.set_file = 'rnaseq_settings.py'
        self.set_path_orig = os.path.join(self.set_dir_orig, self.set_file)
        
        self.th_resdirpath = os.path.join(self.analysis_path, self.th_resdir)
        self.th_dir = 'tophat_out'
        self.thcmd_file = 'tophatcmd.txt'
        self.bam_file = 'accepted_hits.bam'
        self.th_log_file = 'tophat.log'
        self.th_set_path_copy = os.path.join(self.th_resdirpath, 
                os.path.splitext(self.set_file)[0])
        
        self.cuff_dir = 'cufflinks_out'
        self.cufflog_file = 'cufflinks.log'
        self.cuffcmd_file = 'cufflinkscmd.txt'
        self.cuff_gfpkm = 'genes.fpkm_tracking'
        self.berkid_cuff_gfpkm = 'genes_berkid.fpkm_tracking'
        
        self.corr_dir = 'correlations'
        self.corr_dirpath = os.path.join(self.analysis_path, self.corr_dir,
                self.th_resdir)
        self.corr_set_path_copy = os.path.join(self.corr_dirpath,
                os.path.splitext(self.set_file)[0])
        self.corr_figset_file = 'corrfig_settings.py'
        self.corr_figset_path_orig = os.path.join(self.set_dir_orig, 
                self.corr_figset_file)
        self.corr_figset_path_copy = os.path.join(self.corr_dirpath, 
                os.path.splitext(self.corr_figset_file)[0])
        self.pearson_corrfile = 'pearson_correlations.txt' 
        self.spearman_corrfile = 'spearman_correlations.txt' 
        self.pearson_corrpath = os.path.join(self.corr_dirpath,
                self.pearson_corrfile)
        self.spearman_corrpath= os.path.join(self.corr_dirpath,
                self.spearman_corrfile)
        self.corrlog_file = 'correlations.log'
        #selectlist = ['t0.tracking_id', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 
        #'t1.berkid', 't1.fpkm', 't1.fpkm_status']
        self.selectlist = ['t0.gene_short_name', 't0.berkid', 't0.fpkm', 
                't0.fpkm_status', 't1.berkid', 't1.fpkm', 't1.fpkm_status']
        self.maxfpkm = False # Only genes with FPKMs below this value will be used to 
        # calculate correlations; if no limit is desired, set to False.
        self.pc_log = True # If set to 'True', adds 1 to each value in the list of 
        # FPKMS for each sample and then log transforms the data (log base 2).
        
        self.htseq_dir = 'htseq_out'
        self.htseq_cmd_file = 'htseq.info'
        self.htseq_log_file = 'htseq.log'
        self.htseq_file = 'htseqcount'
        self.res_sample_glob = 'RG*'
       
        self.edger_dir = 'edger'
        self.edger_dirpath = os.path.join(self.analysis_path, self.edger_dir,
                self.th_resdir)
        self.edger_log_file = 'edger.log'
        self.edger_metadata_file = 'metadata.txt'
        self.edger_group_file = 'groups'
        self.edger_mdsplot_file = 'mds_plot.png'
        self.edger_mvplot_file = 'mean_var_plot.png'
        self.edger_bcvplot_file = 'biol_cv_plot.png'
        self.edger_maplot_file = 'masmear_plot_'
        self.edger_toptags_file = 'toptags_edgeR.csv'
        self.edger_dbtoptags_file = 'db_toptags_edgeR.csv'
        self.edger_toptags_fdr_file = 'toptags_edgeR_'
        self.de_hh_file = 'human_hom_'
      
        self.deseq_dir = 'deseq'
        self.deseq_dirpath = os.path.join(self.analysis_path, self.deseq_dir,
                self.th_resdir)
        self.deseq_log_file = 'deseq.log'
    
        self.berkidlen = 8



    def GetResultsFiles(self, berkid):

        sample_dir = os.path.join(self.th_resdirpath, berkid)
        sample_th_dir = os.path.join(sample_dir, self.th_dir)
        sample_cuff_dir = os.path.join(sample_dir, self.cuff_dir)
        sample_htseq_dir = os.path.join(sample_dir, self.htseq_dir)

        d =     {'sample_dir': sample_dir,
                'sample_th_dir': sample_th_dir,
                'bam_path': os.path.join(sample_th_dir, self.bam_file),
                'sample_cuff_dir': sample_cuff_dir,
                'cuff_gfpkm_path': os.path.join(sample_cuff_dir,
                    self.cuff_gfpkm),
                'sample_htseq_dir': sample_htseq_dir,
                'htseq_count_path': os.path.join(sample_htseq_dir, self.htseq_file)
                }

        return(d)

def get_replicate_cufflink_paths(condition_berkid_dict):
    '''Returns a dictionary of paths to the cufflink output FPKM files for
    every condition in condition_berkid_dict.
    Input:
    condition_berkid_dict: keywords are conditions and values are lists of 
    berkids. Output by the functions get_replicate_berkid_dict or 
    get_all_replicate_berkid_dict). 
    Output:
    Dictionary of paths; keywords are conditions and values are lists of
    output FPKM file paths.
    '''
    replicate_path_dict = {} 
    for condition, berkids in condition_berkid_dict.items():
        replicate_path_dict[condition] = \
                [get_results_files(b)['cuff_gfpkm_path'] for b in berkids]
    return(replicate_path_dict)

if __name__ == '__main__':
    testobj = RNASeqData('2str')
    print(testobj.berkidlen)
    print(testobj.set_file)
    resfiles = testobj.GetResultsFiles('RGAM010D')
    print(resfiles['sample_htseq_dir'])
    print(testobj.__dict__)
    
#RNASEQDICT =    {'seq_dir': SEQ_PATH,
                #'seq_subdir': SEQ_SUBDIR,
                #'seqbatchglob': SEQBATCHGLOB,
                #'sampleseqglob': SAMPLESEQGLOB,
                #'combined_fastq_suffix': COMBINED_FASTQ_SUFFIX,
                #'sampleinfo_table': SAMPLEINFO_TABLE,
                #'set_path_orig': SET_PATH_ORIG,
                #'analysis_path': ANALYSIS_PATH,
                #'th_resdirpath': TH_RESDIRPATH,
                #'th_log_file': TH_LOG_FILE,
                #'th_dir': TH_DIR,
                #'th_cmd_file': THCMD_FILE,
                #'bam_file': BAM_FILE,
                #'th_set_path_copy': TH_SET_PATH_COPY, 
                #'cuff_dir': CUFF_DIR,
                #'cufflog_file': CUFFLOG_FILE,
                #'cuffcmd_file': CUFFCMD_FILE,
                #'corr_dir': CORR_DIR,
                #'corr_dirpath': CORR_DIRPATH,
                #'corr_set_path_copy': CORR_SET_PATH_COPY,
                #'corr_figset_file': CORR_FIGSET_FILE,
                #'corr_figset_path_orig': CORR_FIGSET_PATH_ORIG,
                #'corr_figset_path_copy': CORR_FIGSET_PATH_COPY,
                #'pearson_corrfile': PEARSON_CORRFILE,
                #'spearman_corrfile': SPEARMAN_CORRFILE,
                #'corrlog_file': CORRLOG_FILE,
                #'htseq_dir': HTSEQ_DIR,
                #'htseq_cmd_file': HTSEQ_CMD_FILE,
                #'htseq_log_file': HTSEQ_LOG_FILE,
                #'htseq_file': HTSEQ_FILE,
                #'htseq_table': HTSEQ_TABLE,
                #'edger_dirpath': EDGER_DIRPATH,
                #'edger_metadata_file': EDGER_METADATA_FILE,
                #'edger_log_file': EDGER_LOG_FILE,
                #'edger_group_file': EDGER_GROUP_FILE,
                #'edger_mdsplot_file': EDGER_MDSPLOT_FILE,
                #'edger_mvplot_file': EDGER_MVPLOT_FILE,
                #'edger_bcvplot_file': EDGER_BCVPLOT_FILE,
                #'edger_maplot_file': EDGER_MAPLOT_FILE,
                #'edger_toptags_file': EDGER_TOPTAGS_FILE,
                #'edger_dbtoptags_file': EDGER_DBTOPTAGS_FILE,
                #'edger_toptags_fdr_file': EDGER_TOPTAGS_FDR_FILE,
                #'deseq_dir': DESEQ_DIR,
                #'deseq_dirpath': DESEQ_DIRPATH,
                #'deseq_log_file': DESEQ_LOG_FILE,
                #'deseq_metadata_file': EDGER_METADATA_FILE,
                #'deseq_group_file': EDGER_GROUP_FILE,
                #'degene_table': DEGENE_TABLE,
                #'de_hh_file': DE_HH_FILE
                #}

#REFSEQDICT =    {'refseq_path': REFSEQ_PATH,
                 #'gff_path': GFF_PATH,
                 #'mitogff_path': MITOGFF_PATH,
                 #'btindex': BTINDEX}



