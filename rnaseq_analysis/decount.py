#!/usr/bin/python

#Code for finding/ analyzing number of DE genes.

import argparse 
import cmn.cmn as cmn
import datetime
import glob
import libs.decountlib as dl
import libs.rnaseqlib as rl
import logging
import os
import psycopg2
import rnaseq_settings as rs
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('expts', 
        help="'all' = all DE directories, else list of directories separated \
        by commas")
parser.add_argument('tool', choices=['edger', 'deseq'],
        help='selects DE analysis tool used')
parser.add_argument('alignment', choices=['unstranded', '2str', 'r6_2str'], 
        help='Option for which data to analyze')
parser.add_argument('genesubset', choices=['all', 'prot_coding_genes',
        'prot_coding_genes_ralph_mt_ex', 'brain_r557', 'bwa_r557',
        'bwa_r557_ralph_mt_ex', 'sfari_r557', 'bwa_r601', 'sfari_r601', 
        'pcg_r601'], 
        help='set of genes on which DE analysis was run')
parser.add_argument('-r', '--run', action="store_true", 
        help='runs decount analysis')

args = parser.parse_args()
tool = args.tool

rnaset = rs.RNASeqData(alignment=args.alignment, genesubset=args.genesubset)
rnaseqdict = rnaset.__dict__
degroups = rs.DEGroups()
cmn.makenewdir(rnaset.decount_dirpath)

exptdir = os.path.join(rnaseqdict['{}_dirpath'.format(tool)], args.genesubset)
os.chdir(exptdir)
if args.expts == 'all':
    exptlist = sorted([os.path.abspath(e) for e in glob.glob('*/')])
else:
    exptlist = sorted([os.path.abspath(e) for e in args.expts.split(',')])



if args.run:
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logpath = os.path.join(rnaset.decount_dirpath, '{}_{}'.format(curtime, 
        rnaseqdict['decount_log_file']))
    rl.logginginfo(logpath)

    conn = psycopg2.connect("dbname={} user=andrea".format(rnaset.rsdbname))
    shutil.copy(rnaseqdict['set_path_orig'], '{}_{}'.format(rnaseqdict['decount_set_path_copy'], curtime))

    for fdr in [0.01, 0.05, 0.10]:
        logging.info(fdr) 
        logging.info("Creating decount tables")
        dl.create_decount_tables(conn, rnaset, tool, fdr)

        if args.genesubset != 'all' or args.genesubset != 'pcg_r601' or \
                args.genesubset != 'prot_coding_genes':
            logging.info("Writing homologs of decount genes") 
            dl.write_homologs_obj(conn, rnaset, tool, fdr)
        logging.info("Writing joined male/female decount file")
        dl.write_decount_samples_mf(conn, rnaset, tool, fdr)
        logging.info("Writing decount files for each group")
        dl.write_group_decount(conn, exptlist, rnaset, fdr, tool)
        logging.info(("Plotting histograms of decount"))
        dl.plot_decount_hist(rnaset, fdr, tool)
        dl.plot_cv_hist(rnaset, fdr, tool)

        for sex in ['M', 'F']:
            logging.info(sex) 
            logging.info("Writing files with counts for each gene in the DE gene files")
            dl.write_decount_gene_counts(conn, rnaset, degroups, sex, fdr, tool, 
                    minfdr=True)
            logging.info("Writing files for number of DE genes")
            dl.write_num_degenes(conn, rnaset, tool, fdr, sex)
            logging.info(("Writing files with DE counts for each sex and "
                "coefficient of variation of fold change"))
            dl.write_decount_fccv(conn, rnaset, degroups, sex, fdr, tool)
            dl.write_decount_fccv_gene(conn, rnaset, degroups, sex, fdr, tool, 
                    minfdr=True)
