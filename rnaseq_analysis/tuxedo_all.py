#!/usr/bin/python

# Runs tophat and cufflinks on all sequence files.

import tuxedolib as tl
import logging
import shutil
import sys
from tuxedo_settings import *
from rnaseq_settings import *

print('Write yes to run Cufflinks or no otherwise')
RUNCUFFLINKS = sys.argv[1] 

def main():
    # Writes output to mrun.log and specifies format of logging output.
    logging.basicConfig(filename=RNASEQDICT['th_log_file'], 
            format='%(asctime)s %(levelname)s %(message)s', 
            datefmt='%m/%d/%Y_%I-%M-%S %p', 
            filemode='w', 
            level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    tl.seqdir_run_tophat_cufflinks(RNASEQDICT, REFSEQDICT, RUNCUFFLINKS)
    shutil.copy(RNASEQDICT['th_set_path_orig'], RNASEQDICT['th_set_path_copy'])

if __name__ == '__main__':
    main()
