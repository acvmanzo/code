#!/usr/bin/python

#Finds the correlation of gene expression values between biological replicates 

import correlationlib as corl
import logging
import os
import cmn.cmn as cmn
import psycopg2
import shutil
import sys
from all_correlations_settings import *

COPY_TO_TABLE = sys.argv[1] # 'y' to copy data into database table
FIND_CORRELATIONS = sys.argv[2] # 'y' or 'yes' to find correlations

def create_corrfiles():
    # Creates files for pearson and spearman correlation coefficients.
    pearson_corrfile = os.path.join(CORRELATION_DIR, PEARSON_CORRFILE)
    spearman_corrfile = os.path.join(CORRELATION_DIR, SPEARMAN_CORRFILE)
    corl.create_corr_file(pearson_corrfile)
    corl.create_corr_file(spearman_corrfile)
    return(pearson_corrfile, spearman_corrfile)
   
def gen_cufflink_path_dict(whichberkids, berkidlist, key):
    '''
    If whichberkids = 'all':
        Generates a dictionary where they keys are conditions (e.g., CS_M or
        en_F) and the values are the paths to the cufflinks gene FPKM files for
        the relevant samples.
    If whichberkids = 'subset':
        Still generates a dictionary but there is only one key given by the
        value key.
    '''
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    if whichberkids == 'allreps':
        cufflink_path_dict = corl.get_all_replicate_cufflink_paths(
            cur, SAMPLEINFO_TABLE, RESULTS_DIR, CUFFLINKS_DIR, FPKM_FILE)
    if whichberkids == 'berkids':
        assert key != None
        assert berkidlist != None
        cufflink_path_dict = corl.get_some_cufflink_paths(berkidlist, 
            RESULTS_DIR, CUFFLINKS_DIR, FPKM_FILE, key)
    cur.close()
    conn.close()
    return(cufflink_path_dict)


def prune_cufflink_path(cufflink_fpkm_paths):
    # Removes paths to files that don't exist.
    logging.debug('Cufflink paths: %s', cufflink_fpkm_paths)
    extant_cufflink_fpkm_paths = []
    for cp in cufflink_fpkm_paths:
        if os.path.exists(cp):
            extant_cufflink_fpkm_paths.append(cp)
        else:
            logging.info('%s does not exist', cp)
    if len(extant_cufflink_fpkm_paths) < 2:
        logging.info('Fewer than 2 samples')
    else:
        logging.debug('Cufflink paths used for analysis: %s', 
        extant_cufflink_fpkm_paths)
        return(extant_cufflink_fpkm_paths)


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
                        SCATTER_INFO, HIST_INFO, PC_LOG)
            except FileNotFoundError:
                logging.info("File Not Found '%s'", cufflink_fpkm_paths)
                continue

        shutil.copyfile(CORRELATION_SETTINGS_PATH, SAVED_CORRELATION_SETTINGS_PATH)
               



if __name__ == '__main__':
    main()
