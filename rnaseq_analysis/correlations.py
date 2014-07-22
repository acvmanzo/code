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

parser = argparse.ArgumentParser()
parser.add_argument('alignment', choices=['unstranded', '2str'], 
        help='Option for which data to analyze')
parser.add_argument('genesubset', choices=['all', 'prot_coding_genes',
         'brain_r557'])
parser.add_argument('-r', '--run', action='store_true', 
        help='run correlation analysis')
parser.add_argument('-a', '--allgens', action='store_true', 
        help='find correlations for all samples')
parser.add_argument('-g', '--genotype',
        help='genotype to analyze')
#parser.add_argument('-s', '--genesubset', choices=['all', 'prot_coding_genes',
        #'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        #'bwa_r557_ralph_mt_ex', 'sfari_r557'], 
        #help='make new file of htseq-count results for the given subset of genes')
parser.add_argument('-c', '--copytodb', action='store_true', 
        help='copy cufflinks results to database')

args = parser.parse_args()

if args.genotype:
    filenamegs = args.genotype
else:
    filenamegs = 'allgens'
if args.genesubset == 'all':
    args.genesubset = False

rnaset = rs.RNASeqData(alignment=args.alignment, genesubset=args.genesubset)
rnaseqdict = rnaset.__dict__
corrplotset = rs.CorrPlotData()
curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
corrdirpath = os.path.join(rnaset.corr_dirpath, '{}_{}'.format(filenamegs, 
    curtime))
cmn.makenewdir(corrdirpath)

def create_corrfiles():
    # Creates files for pearson and spearman correlation coefficients.
    corrpaths = []
    for cf in [rnaset.pearson_corrfile, rnaset.spearman_corrfile]:
        #corrfile =  '{}_{}_{}'.format(curtime, filenamegs, cf)
        corrpath = os.path.join(corrdirpath, cf)
        corl.create_corr_file(corrpath)
        corrpaths.append(corrpath)
    return(corrpaths) 
   
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
    logpath = os.path.join(corrdirpath, rnaseqdict['corrlog_file'])
    rl.logginginfo(logpath)
    if args.genotype:
        logging.info('Finding correlations for %s', args.genotype)

    # Create correlation output files.
    pearson_corrpath, spearman_corrpath = create_corrfiles()

    # Find paths to the cufflink output files for each condition.
    cufflink_path_dict = gen_cufflink_path_dict()
    #print(cufflink_path_dict)

    for condition, cufflink_fpkm_paths in sorted(cufflink_path_dict.items()):
        # Define and create figure directory.
        fig_dir = os.path.join(corrdirpath, condition)
        cmn.makenewdir(fig_dir)

        # Create a new list of paths only to the files that exist.
        logging.info('Condition: %s', condition)    
        extant_cufflink_fpkm_paths = prune_cufflink_path(cufflink_fpkm_paths)
        if not extant_cufflink_fpkm_paths:
            continue
        # Copies data into the database table in rnaset.cuff_table 
        if args.copytodb:
            logging.info('Files copied to db %s', extant_cufflink_fpkm_paths)
            corl.copy_data_to_table(extant_cufflink_fpkm_paths, 
                    rnaset.berkid_cuff_gfpkm, rnaset.cuff_table, 
                    rnaset.berkidlen)
        # Finds correlations 
        if args.run:
            try:
                logging.info('Finding corelations')
                # Generates a list of arrays in which each array has the gene FPKM
                # data for two samples.
                joined_arrays = corl.get_joined_arrays(extant_cufflink_fpkm_paths, 
                        rnaset.selectlist, rnaset.cuff_table, rnaset.maxfpkm, 
                        args.genesubset, rnaset.berkidlen)
                # Finds the correlations between each sample within a condition and
                # generates plots.
                corl.get_sample_correlations(joined_arrays, fig_dir, 
                        pearson_corrpath, spearman_corrpath, 
                        rnaset.selectlist, corrplotset, rnaset.pc_log)
            except FileNotFoundError:
                logging.info("File Not Found '%s'", cufflink_fpkm_paths)
                continue

            shutil.copy(rnaseqdict['set_path_orig'], os.path.join(corrdirpath, 
                    os.path.splitext(rnaset.set_file)[0]))


if __name__ == '__main__':
    main()
