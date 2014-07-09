#!/usr/bin/python

# Runs tophat and cufflinks on all sequence files.

import libs.tuxedolib as tl
import libs.rnaseqlib as rl
import logging
import shutil
import sys
import datetime
from rnaseq_settings import *
import argparse 
import cmn.cmn as cmn


parser = argparse.ArgumentParser()
parser.add_argument('strand', choices=['fr-secondstrand', 'fr-unstranded'],
        help='specify library type for tophat')
parser.add_argument('-c', '--cufflinks', action="store_true", 
        help='option to run cufflinks')
args = parser.parse_args()
print(args)


def main():

    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logpath = os.path.join(TH_RESDIRPATH, '{}_'.format(curtime) + RNASEQDICT['th_log_file'])
    rl.logginginfo(logpath)

    ## Writes output to mrun.log and specifies format of logging output.

    tl.seqdir_run_tophat_cufflinks(RNASEQDICT, REFSEQDICT, args.cufflinks,
        args.strand)
    shutil.copy(RNASEQDICT['th_set_path_orig'], '{}_{}'.format(RNASEQDICT['th_set_path_copy'], curtime))

if __name__ == '__main__':
    main()
