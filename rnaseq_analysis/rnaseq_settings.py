# This module contains functions that define classes and objects where the
# object attributes specify the files and directories used in RNA-Seq analysis.

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
        #results_tophat_2str/
            #prot_coding_genes/
                #allgens_date_time/
                    #Betaintnu_F/
                        #Betaintnu_FA-RGAM011D_vs_Betaintnu_FB-RGAM012F_correlation.png
                    #Betaintnu_M/
                    #pearson_correlations.txt
                    #spearman_correlations.txt
                    #rnaseq_settings
                    #correlations.log
                #NrxI_M_date_time/
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
    '''A class where the object attributes are the files, file paths,
    and other user-defined parameters for RNA-Seq analysis.
    '''

    def __init__(self, alignment, genesubset):
        '''
        Inputs:
        alignment = data to analyze, based on alignment settings (choices are
            unstranded, 2str)
        genesubset = subset of genes that are analyzed (all, prot_coding_genes,
            bwa, etc.)
        '''
        self.genesubset = genesubset 

        if alignment == 'unstranded':
            self.th_resdir = 'results_tophat'
            self.cuff_table = 'cufflinks_data_un'
            self.htseq_table = 'htseq_un'
            self.degene_table = 'degenes_un'
            self.htseq_dir = 'htseq_out'
            self.rsdbname = 'rnaseq'

        if alignment == '2str':
            self.th_resdir = 'results_tophat_2str'
            self.cuff_table = 'cufflinks_data_2str'
            self.htseq_table = 'htseq_2str'
            self.degene_table = 'degenes_2str'
            self.htseq_dir = 'htseq_out'
            self.rsdbname = 'rnaseq'

        if alignment == 'r6_2str':
            self.th_resdir = 'results_tophat_r6_2str'
            self.cuff_table = 'cufflinks_data_r6_2str'
            self.htseq_table = 'htseq_r6_2str'
            self.degene_table = 'degenes_r6_2str'
            self.htseq_dir = 'htseq_out_str'
            self.rsdbname = 'sixrna'
        
        self.sampleinfo_table = 'autin'

        #Paths to the reference genome and other files used for alignment
        #by Tophat.
        if alignment == 'r6_2str':
            self.refseq_path = '/home/andrea/rnaseqanalyze/references/dmel-r6.01' 
            self.gff_path = os.path.join(self.refseq_path,
                    'dmel-all-r6.01.gff')
            self.gff_path_nofa = os.path.join(self.refseq_path,
                    'dmel-all-r6.01-nofa.gff')
            self.mitogff_path = os.path.join(self.refseq_path, 
                    'dmel-dmel_mitochondrion_genome-r6.01.gff')
            self.btindex = os.path.join(self.refseq_path,
                    'dmel-all-chromosome-r6.01')

        elif alignment == 'unstranded' or alignment == '2str':
            self.refseq_path = '/home/andrea/rnaseqanalyze/references/dmel-r5.57'
            self.gff_path = os.path.join(self.refseq_path, 
                    'dmel-all-filtered-r5.57.gff')
            self.gff_path_nofa = os.path.join(self.refseq_path, 
                    'dmel-all-filtered-r5.57-nofa.gff')
            self.mitogff_path = os.path.join(self.refseq_path, 
                    'dmel-dmel_mitochondrion_genome-r5.57.gff')
            self.btindex = os.path.join(self.refseq_path, 
                    'dmel-all-chromosome-r5.57')


        #Paths to directories holding sequence data.
        self.seq_path = '/home/andrea/Documents/lab/RNAseq/sequences'
        self.seq_subdir = 'sequences'
        self.seqbatchglob = '2014-*/'
        self.sampleseqglob = 'Sample_*'
        self.combined_fastq_suffix = 'combined.fastq.gz'
       
        #Path to main analysis folder.
        self.analysis_path = '/home/andrea/Documents/lab/RNAseq/analysis'

        #Paths to settings files.   
        self.set_dir_orig = '/home/andrea/Documents/lab/code/rnaseq_analysis'
        self.set_file = 'rnaseq_settings.py'
        self.set_path_orig = os.path.join(self.set_dir_orig, self.set_file)

        #Path to Tophat files. 
        self.th_resdirpath = os.path.join(self.analysis_path, self.th_resdir)
        self.th_dir = 'tophat_out'
        self.th_cmd_file = 'tophatcmd.txt'
        self.bam_file = 'accepted_hits.bam'
        self.th_log_file = 'tophat.log'
        self.th_set_path_copy = os.path.join(self.th_resdirpath, 
                os.path.splitext(self.set_file)[0])

        #Paths to Cufflinks files. 
        self.cuff_dir = 'cufflinks_out'
        self.cufflog_file = 'cufflinks.log'
        self.cuffcmd_file = 'cufflinkscmd.txt'
        self.cuff_gfpkm = 'genes.fpkm_tracking'
        self.berkid_cuff_gfpkm = 'genes_berkid.fpkm_tracking'

        #Paths to output of correlation analysis. 
        self.corr_dir = 'correlations'
        self.corr_dirpath = os.path.join(self.analysis_path, self.corr_dir,
                self.th_resdir, self.genesubset)
        self.pearson_corrfile = 'pearson_correlations.txt' 
        self.spearman_corrfile = 'spearman_correlations.txt' 
        self.corrlog_file = 'correlations.log'
        #selectlist = ['t0.tracking_id', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 
        #'t1.berkid', 't1.fpkm', 't1.fpkm_status']
        self.cuffselectlist = ['t0.gene_short_name', 't0.berkid', 't0.fpkm', 
                't0.fpkm_status', 't1.berkid', 't1.fpkm', 't1.fpkm_status']
        self.htseqselectlist = ['t0.gene_short_name', 't0.berkid', 't0.counts', 
                't1.berkid', 't1.counts']
        self.maxfpkm = False # Only genes with FPKMs below this value will be used to 
        # calculate correlations; if no limit is desired, set to False.
        self.pc_log = True # If set to 'True', adds 1 to each value in the list of 
        # FPKMS for each sample and then log transforms the data (log base 2).
        
        #Paths to htseq-count files.
        self.htseq_cmd_file = 'htseq.info'
        self.htseq_log_file = 'htseq.log'
        self.htseq_file = 'htseqcount'
        self.res_sample_glob = 'RG*'
      
        #Paths to edgeR files.
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
        self.edger_counts_file = 'gene_counts.csv'
        self.de_hh_file = 'human_hom_'
    
        #Paths to DEseq files.
        self.deseq_dir = 'deseq'
        self.deseq_dirpath = os.path.join(self.analysis_path, self.deseq_dir,
                self.th_resdir)
        self.deseq_log_file = 'deseq.log'
        self.deseq_metadata_file = 'metadata.txt'
        self.deseq_group_file = 'groups'
        self.deseq_toptags_file = 'res_DEseq.csv'
        self.deseq_dbtoptags_file = 'db_res_DEseq.csv'
        self.deseq_toptags_fdr_file = 'res_DEseq_'
    
        self.berkidlen = 8 #Length of berkid names.



    def GetResultsFiles(self, berkid):
        '''A method that returns a dictionary of the file paths for a specific
        berkeley id.
        '''
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

class CorrPlotData:
    '''A class where the object attributes specify parameters for plotting
    correlation plots and histograms.'''

    def __init__(self):
        self.scatter_dpi = 1000
        #self.scatter_figsize = (10, 5.5)
        self.scatter_figsize = (5.5, 5.5)
        #self.scatter_subplots = [121, 122]
        self.scatter_subplots = [111]
        self.scatter_maxfpkm = 2000
        
        self.hist_figsize = (10, 14)
        self.hist_dpi = 1250
        self.hist_subplots = [411, 412, 413, 414]
        #self.hist_ylims = [18000, 1000, 25, 5]
        self.hist_ylims = [6000, 1000, 200, 100]
        self.hist_titles = ['All bins', 'Zoom in on bins with very low FPKM',
            'Zoom in on bins with low FPKM', 'Zoom in on bins with high FPKM']
        #self.hist_maxfpkm = 2000
        self.hist_maxfpkm = 4
        self.hist_maxfpkm_frac = 0.01


class DEGroups:
    '''A class where the object attributes specify groups for DE gene
    analysis'''

    def __init__(self):
        self.males = ['Betaintnu_M', 'CG34127_M', 'en_M', 'Nhe3_M', 'NrxI_M', 
                'NrxIV_M', 'pten_M']
        self.males_ctrl = 'CS_M'

        self.females = ['Betaintnu_F', 'CG34127_F', 'en_F', 'Nhe3_F',
                'NrxI_F', 'NrxIV_F', 'pten_F']
        self.females_ctrl = 'CS_F'

        self.agg_dict_all = {   'lowagg_all': ['CG34127_M', 'en_M', 'NrxI_M'],
                                'ctrlagg_all': ['Nhe3_M', 'NrxIV_M', 'pten_M',
                                    'CS_M', 'Betaintnu_M']}
        self.agg_dict_cs = {    'lowagg_CS': ['CG34127_M', 'en_M', 'NrxI_M'],
                                'ctrlagg_CS': ['CS_M']}

        self.mut_dict_males = { 'aut_mut_m': ['Betaintnu_M', 'CG34127_M', 
            'en_M', 'Nhe3_M', 'NrxI_M', 'NrxIV_M', 'pten_M'],
                                'aut_ctrl_m': ['CS_M']}
        self.mut_dict_females =  {  'aut_mut_f': ['Betaintnu_F', 'CG34127_F',
            'en_F', 'Nhe3_F', 'NrxI_F', 'NrxIV_F', 'pten_F'],
                                    'aut_ctrl_f': ['CS_F']}



if __name__ == '__main__':
    testobj = RNASeqData('2str')
    print(testobj.berkidlen)
    print(testobj.set_file)
    resfiles = testobj.GetResultsFiles('RGAM010D')
    print(resfiles['sample_htseq_dir'])
    #print(testobj.__dict__)
    corrobj = CorrPlotData()
    print(corrobj.scatter_maxfpkm)
    
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



