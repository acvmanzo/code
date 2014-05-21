#!/usr/bin/python

import tuxedolib as tl
import logging 
import datetime
import os
import psycopg2
from runtuxedoset import *

curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print(curtime)

BERKIDLIST = ['RGAM009H', 'RGAM010A']
TUXLOG_PATH = os.path.join(RESULTS_DIR, '{}_tux.log'.format(curtime))
COLQUERY = ['genotype', 'tube', 'sex', 'frozend', 'rnad', 'rnaconc', 
            'mrnad', 'cdnad', 'indexnum', 'sample', 'seqd', 'thawed',
            'toseq', 'samplenum', 'sentd', 'qbitngul', 'qbitd', 'seq_received']

def main():
    # Writes output to mrun.log and specifies format of logging output.
    logging.basicConfig(filename=TUXLOG_PATH,\
        format='%(asctime)s %(levelname)s %(message)s',\
        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    seqpaths, respaths = tl.get_berkid_seq_res_paths(BERKIDLIST, \
        SAMPLEINFO_TABLE, COLQUERY, SEQ_DIR, SEQ_SUBDIR, RESULTS_DIR)
    print(seqpaths, respaths)

    berkid_params = zip(BERKIDLIST, seqpaths, respaths) 
    for berkid, sample_seqdir, sample_resdir in berkid_params:
        tl.run_tophat_cufflinks(berkid, sample_seqdir, sample_resdir, 
            TOPHAT_CUFFLINKS_INFO)

if __name__ == '__main__':
    main()
