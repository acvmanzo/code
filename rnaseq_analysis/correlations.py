#!/usr/bin/python

#Finds the correlation of gene expression values between biological replicates 
import argparse
import datetime
import logging
import os
import argparse 
import psycopg2
import shutil
import sys
import cmn.cmn as cmn
import libs.correlationlib as corl
import libs.rnaseqlib as rl
import rnaseq_settings as rs 
from corrfig_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('option', choices=['unstranded', '2str'], 
        help='Option for which data to analyze')
parser.add_argument('-r', '--run', action='store_true', 
        help='run correlation analysis')
parser.add_argument('-a', '--allgens', action='store_true', 
        help='find correlations for all samples')
parser.add_argument('-g', '--genotype',
        help='genotype to analyze')
parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes',
         'brain_r557'])
#parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes',
        #'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        #'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        #help='make new file of htseq-count results for the given subset of genes')
parser.add_argument('-c', '--copytodb', action='store_true', 
        help='copy cufflinks results to database')

args = parser.parse_args()
if args.genesubset == 'all':
    args.genesubset = False

if args.genotype:
    logging.info('Finding correlations for %s', args.genotype)

rnaset = rs.RNASeqData(option=args.option)
rnaseqdict = rnaset.__dict__

def create_corrfiles():
    # Creates files for pearson and spearman correlation coefficients.
    corl.create_corr_file(rnaset.pearson_corrpath)
    corl.create_corr_file(rnaset.spearman_corrpath)
   
def gen_cufflink_path_dict():
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
    if args.allgens:
        cufflink_path_dict = rl.get_all_replicate_cufflink_paths(cur, rnaset)
    if args.genotype:
        berkiddict = {args.genotype: rl.get_replicate_berkid_dict(cur, 
            args.genotype, rnaseqdict['sampleinfo_table'])}
        cufflink_path_dict = rl.get_replicate_cufflink_paths(berkiddict, rnaset)
        #print(cufflink_path_dict)
    #if whichberkids == 'berkids':
        #assert key != None
        #assert berkidlist != None
        #cufflink_path_dict = corl.get_some_cufflink_paths(berkidlist, 
            #RESULTS_DIR, CUFFLINKS_DIR, FPKM_FILE, key)
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
    cmn.makenewdir(rnaset.corr_dirpath)
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logpath = os.path.join(rnaset.corr_dirpath, '{}_'.format(curtime) + rnaseqdict['corrlog_file'])
    rl.logginginfo(logpath)

    # Create correlation output files.
    create_corrfiles()

    # Find paths to the cufflink output files for each condition.
    cufflink_path_dict = gen_cufflink_path_dict()
    #print(cufflink_path_dict)

    for condition, cufflink_fpkm_paths in sorted(cufflink_path_dict.items()):
        # Define and create figure directory.
        fig_dir = os.path.join(rnaset.corr_dirpath, condition)
        cmn.makenewdir(fig_dir)

        # Create a new list of paths only to the files that exist.
        logging.info('Condition: %s', condition)    
        extant_cufflink_fpkm_paths = prune_cufflink_path(cufflink_fpkm_paths)
        if not extant_cufflink_fpkm_paths:
            continue
        # Copies data into the database table in rnaset.cuff_table if sys.argv is 'y'
        # or 'yes'
        if args.copytodb:
            logging.info('Files copied to db %s', extant_cufflink_fpkm_paths)
            corl.copy_data_to_table(extant_cufflink_fpkm_paths, 
                    rnaset.berkid_cuff_gfpkm, rnaset.cuff_table, 
                    rnaset.berkidlen)
        # Finds correlations if sys.argv is 'y' # or 'yes'
        if args.run:
            try:
                # Generates a list of arrays in which each array has the gene FPKM
                # data for two samples.
                joined_arrays = corl.get_joined_arrays(extant_cufflink_fpkm_paths, 
                        rnaset.selectlist, rnaset.cuff_table, rnaset.maxfpkm, 
                        args.genesubset)
                # Finds the correlations between each sample within a condition and
                # generates plots.
                corl.get_sample_correlations(joined_arrays, fig_dir, 
                        rnaset.pearson_corrpath, rnaset.spearman_corrpath, rnaset.selectlist,
                        rnaset.scatter_info, rnaset.hist_info, rnaset.pc_log)
            except FileNotFoundError:
                logging.info("File Not Found '%s'", cufflink_fpkm_paths)
                continue

        #shutil.copy(rnaseqdict['set_path_orig'], '{}_{}'.format(rnaseqdict['corr_set_path_copy'], curtime))
        #shutil.copy(rnaseqdict['corr_figset_path_orig'], '{}_{}'.format(rnaseqdict['corr_figset_path_copy'], curtime))

if __name__ == '__main__':
    main()
