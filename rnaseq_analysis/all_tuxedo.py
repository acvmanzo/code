#!/usr/bin/python

# Runs tophat and cufflinks on all sequence files.

import tuxedolib as tl
import logging
import shutil
from tuxedo_settings import *

def main():
    # Writes output to mrun.log and specifies format of logging output.
    logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y_%I-%M-%S %p', filemode='w', level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    tl.seqdir_run_tophat_cufflinks(DIR_INFO, TOPHAT_CUFFLINKS_INFO)
    shutil.copy(SETTINGS_FILE, NEW_SETTINGS_FILE)

if __name__ == '__main__':
    main()
