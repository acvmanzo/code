#!/usr/bin/python

import tuxedolib as tl
import logging 
from runtuxedoset import *

def main():
    # Writes output to mrun.log and specifies format of logging output.
    logging.basicConfig(filename='/home/andrea/Documents/lab/RNAseq/analysis/results_tophat/mrun.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    tl.seqdir_run_tophat_cufflinks(DIR_INFO, TOPHAT_CUFFLINKS_INFO)

if __name__ == '__main__':
    main()
