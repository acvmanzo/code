#!/usr/bin/python

#Runs tophat and cufflinks on a fixed set of samples.

import argparse
import cmn.cmn as cmn
import datetime
import logging 
import os
import psycopg2
import shutil
import libs.rnaseqlib as rl
import libs.tuxedolib as tl
from rnaseq_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('strand', choices=['fr-secondstrand', 'fr-unstranded'],
        help='specify library type for tophat')
parser.add_argument('berkidlist', 
        help='list of berkids to align, separated by commas')
parser.add_argument('-c', '--cufflinks', action="store_true", 
        help='option to run cufflinks')
args = parser.parse_args()

print(repr(args.berkidlist))


curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

TUXLOG_PATH = os.path.join(RNASEQDICT['th_resdirpath'], '{}_tux.log'.format(curtime))
COLQUERY = ['genotype', 'tube', 'sex', 'frozend', 'rnad', 'rnaconc', 
            'mrnad', 'cdnad', 'indexnum', 'sample', 'seqd', 'thawed',
            'toseq', 'samplenum', 'sentd', 'qbitngul', 'qbitd', 'seq_received']

berkidlist = args.berkidlist.split(',')

def main():
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logpath = '{}_'.format(curtime) + RNASEQDICT['htseq_log_file']
    rl.logginginfo(logpath)

    seqpaths, respaths = rl.get_berkid_seq_res_paths(berkidlist, \
        SAMPLEINFO_TABLE, COLQUERY,RNASEQDICT['seq_dir'],RNASEQDICT['seq_subdir'], 
        RNASEQDICT['th_resdirpath'])
    print(seqpaths, respaths)

    berkid_params = zip(berkidlist, seqpaths, respaths) 
    for berkid, sample_seqdir, sample_resdir in berkid_params:
        tl.run_tophat_cufflinks(berkid, sample_seqdir, sample_resdir, 
            RNASEQDICT, REFSEQDICT, args.cufflinks, args.strand)
    shutil.copy(RNASEQDICT['th_set_path_orig'], '{}_{}'.format(RNASEQDICT['th_set_path_copy'], curtime))

if __name__ == '__main__':
    main()
