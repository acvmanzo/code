#!/usr/bin/python

#Runs tophat and cufflinks on a fixed set of samples.
import argparse 
import cmn.cmn as cmn
import datetime
import libs.tuxedolib as tl
import libs.rnaseqlib as rl
import logging
import os
import rnaseq_settings_custom as rs
import shutil
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cufflinks', action="store_true", 
        help='option to run cufflinks')
args = parser.parse_args()

COLQUERY = ['genotype', 'tube', 'sex', 'frozend', 'rnad', 'rnaconc', 
            'mrnad', 'cdnad', 'indexnum', 'sample', 'seqd', 'thawed',
            'toseq', 'samplenum', 'sentd', 'qbitngul', 'qbitd', 'seq_received']

def main():
    rnaset = rs.RNASeqData()
    rnaseqdict = rnaset.__dict__
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    cmn.makenewdir(rnaset.th_resdirpath)
    logpath = os.path.join(rnaset.th_resdirpath, '{}_'.format(curtime) + 
            rnaseqdict['th_log_file'])
    rl.logginginfo(logpath)


    seqpaths, respaths = rl.get_berkid_seq_res_paths(rnaset.berkidlist, \
        rnaset.sampleinfo_table, COLQUERY, rnaseqdict['seq_path'],
        rnaseqdict['seq_subdir'], rnaseqdict['th_resdirpath'])
    #print(seqpaths, respaths)

    berkid_params = zip(rnaset.berkidlist, seqpaths, respaths) 
    for berkid, sample_seqdir, sample_resdir in berkid_params:
        tl.run_tophat_cufflinks(berkid, sample_seqdir, sample_resdir, rnaseqdict, 
        args.cufflinks, rnaset.strand, rnaset.minintron)

    shutil.copy(rnaseqdict['set_path_orig'], '{}_{}'.format(rnaseqdict['th_set_path_copy'], curtime))

if __name__ == '__main__':
    main()
