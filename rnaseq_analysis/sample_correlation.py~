import correlationlib as corl
import logging
import os
import cmn.cmn as cmn
import psycopg2
import shutil
import sys
from sample_correlation_settings import *

def main():
    # Settings for logging.
    logging.basicConfig(filename=CORRLOGPATH,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w',
                        level=logging.DEBUG)
    console = logging.StreamHandler()  # Displays output to screen.
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    # Create correlation output files.
    pearson_corrfile, spearman_corrfile = create_corrfiles()
    # Find paths to the cufflink output files for each condition.
    cufflink_path_dict = gen_cufflink_path_dict(ALLREPS_OR_BERKIDS, BERKIDLIST,
           COND_DIR)

    for condition, cufflink_fpkm_paths in sorted(cufflink_path_dict.items()):
        # Define and create figure directory.
        fig_dir = os.path.join(CORRELATION_DIR, condition)
        cmn.makenewdir(fig_dir)

        # Create a new list of paths only to the files that exist.
        logging.info('Condition: %s', condition)    
        extant_cufflink_fpkm_paths = prune_cufflink_path(cufflink_fpkm_paths)
        if not extant_cufflink_fpkm_paths:
            continue
        # Copies data into the database table in CUFF_TABLE if sys.argv is 'y'
        # or 'yes'
        if COPY_TO_TABLE == 'y' or COPY_TO_TABLE == 'yes':
            corl.copy_data_to_table(extant_cufflink_fpkm_paths, BERKID_FPKM_FILE, CUFF_TABLE)
        # Finds correlations if sys.argv is 'y' # or 'yes'
        if FIND_CORRELATIONS == 'y' or FIND_CORRELATIONS == 'yes':
            try:
                # Generates a list of arrays in which each array has the gene FPKM
                # data for two samples.
                joined_arrays = corl.get_joined_arrays(extant_cufflink_fpkm_paths, 
                        SELECTLIST, CUFF_TABLE, MAXFPKM, GENE_SUBSET_TABLE) 
                # Finds the correlations between each sample within a condition and
                # generates plots.
                corl.get_sample_correlations(joined_arrays, fig_dir, 
                        pearson_corrfile, spearman_corrfile, SELECTLIST,
                        SCATTER_INFO, HIST_INFO)
            except FileNotFoundError:
                logging.info("File Not Found '%s'", cufflink_fpkm_paths)
                continue

        shutil.copyfile(CORRELATION_SETTINGS_PATH, SAVED_CORRELATION_SETTINGS_PATH)
