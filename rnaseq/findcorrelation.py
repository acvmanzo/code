import correlationlib as corl
import logging
import os
import cmn.cmn as cmn
import psycopg2
from findcorrelationset import *


#cufflink_fpkm_files = [
#'/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3/genes.fpkm_tracking',
#'/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out/genes.fpkm_tracking',
#'/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out/genes.fpkm_tracking',
#]
#fig_dir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlation_test'


def main():
    logging.basicConfig(filename=CORRLOGPATH, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    pearson_corrfile = os.path.join(CORRELATION_DIR, PEARSON_CORRFILE)
    spearman_corrfile = os.path.join(CORRELATION_DIR, SPEARMAN_CORRFILE)
    corl.create_corr_file(pearson_corrfile)
    corl.create_corr_file(spearman_corrfile)
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    cufflink_path_dict = corl.get_replicate_cufflink_paths(cur, SAMPLEINFO_TABLE, RESULTS_DIR, CUFFLINKS_DIR, FPKM_FILE)
    cur.close()
    conn.close()


    for condition, cufflink_fpkm_paths in cufflink_path_dict.items():
        print(cufflink_fpkm_paths)
        extant_cufflink_fpkm_paths = []
        for cp in cufflink_fpkm_paths:
            if os.path.exists(cp):
                extant_cufflink_fpkm_paths.append(cp)

        if len(extant_cufflink_fpkm_paths) < 2:
            continue
        print(extant_cufflink_fpkm_paths)
        logging.info('%s', condition)    
        fig_dir = os.path.join(CORRELATION_DIR, condition)
        cmn.makenewdir(fig_dir)

        #corl.copy_data_to_table(extant_cufflink_fpkm_paths, BERKID_FPKM_FILE, CUFF_TABLE)

        try:
            joined_arrays = corl.get_joined_arrays(extant_cufflink_fpkm_paths, SELECTLIST, CUFF_TABLE, MAXFPKM) 
            corl.get_sample_correlations(joined_arrays, fig_dir, pearson_corrfile, spearman_corrfile, SELECTLIST, SCATTER_INFO, HIST_INFO)

        except FileNotFoundError:
            logging.info("File Not Found '%s'", cufflink_fpkm_paths)
            continue
       

               



if __name__ == '__main__':
    main()
