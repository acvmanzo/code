#!/usr/bin/python

# Runs tophat and cufflinks on all sequence files.

import libs.tuxedolib as tl
import libs.rnaseqlib as rl
import logging
import shutil
import sys
import datetime
import argparse 
import cmn.cmn as cmn
import rnaseq_settings as rs
import os


parser = argparse.ArgumentParser()

#parser.add_argument('strand', choices=['fr-secondstrand', 'fr-unstranded'],
        #help='specify library type for tophat')
parser.add_argument('alignment', choices=['unstranded', '2str', 'r6_2str'], 
        help='Option for which data to analyze')
parser.add_argument('-c', '--cufflinks', action="store_true", 
        help='option to run cufflinks')
args = parser.parse_args()
print(args)

if args.alignment == 'unstranded':
    strand = 'fr-unstranded'
elif args.alignment == '2str' or args.alignment == 'r6_2str':
    strand = 'fr-secondstrand'

def main():

    rnaset = rs.RNASeqData(alignment=args.alignment, genesubset='')
    rnaseqdict = rnaset.__dict__
    
    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logpath = os.path.join(rnaset.th_resdirpath, '{}_'.format(curtime) + 
            rnaseqdict['th_log_file'])
    rl.logginginfo(logpath)

    ## Writes output to mrun.log and specifies format of logging output.

    tl.seqdir_run_tophat_cufflinks(rnaseqdict, args.cufflinks, strand)
    shutil.copy(rnaseqdict['set_path_orig'], '{}_{}'.format(rnaseqdict['th_set_path_copy'], curtime))

if __name__ == '__main__':
    main()
