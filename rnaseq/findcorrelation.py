import correlationlib as corl
import logging
import os
import cmn.cmn as cmn
from findcorrelationset import *


cufflink_fpkm_files = [
'/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3/genes.fpkm_tracking',
'/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out/genes.fpkm_tracking',
'/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out/genes.fpkm_tracking',
]
fig_dir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlation_test'
cmn.makenewdir(fig_dir)
corrfile = os.path.join(fig_dir, CORRFILE)
corrlog = os.path.join(fig_dir, CORRLOG)

def main():

    logging.basicConfig(filename=corrlog, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    #corl.copy_data_to_table(cufflink_fpkm_files, BERKID_FPKM_FILE, CUFF_TABLE)
    corl.get_sample_correlations(cufflink_fpkm_files, fig_dir, corrfile, CUFF_TABLE, SELECTLIST, MAXFPKM, SCATTER_INFO, HIST_INFO)

if __name__ == '__main__':
    main()
