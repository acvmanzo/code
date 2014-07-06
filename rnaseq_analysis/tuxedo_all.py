#!/usr/bin/python

# Runs tophat and cufflinks on all sequence files.

import libs.tuxedolib as tl
import libs.rnaseqlib as rl
import logging
import shutil
import sys
import datetime
from rnaseq_settings import *

print('Write yes to run Cufflinks or no otherwise')
RUNCUFFLINKS = sys.argv[1] 

def main():

    curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logpath = os.path.join(TH_RESDIRPATH, '{}_'.format(curtime) + RNASEQDICT['th_log_file'])
    rl.logginginfo(logpath)

    # Writes output to mrun.log and specifies format of logging output.

    tl.seqdir_run_tophat_cufflinks(RNASEQDICT, REFSEQDICT, RUNCUFFLINKS)
    shutil.copy(RNASEQDICT['th_set_path_orig'], '{}_{}'.format(curtime, RNASEQDICT['th_set_path_copy']))

if __name__ == '__main__':
    main()
