#!/usr/bin/python

#Runs tophat and cufflinks on a fixed set of samples.

import libs.tuxedolib as tl
import logging 
import datetime
import os
import psycopg2
import cmn.cmn as cmn
from tuxedo_settings import *
from rnaseq_settings import *

curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print(curtime)

BERKIDLIST = ['RGAM009H', 'RGAM010A']
TUXLOG_PATH = os.path.join(RNASEQDICT['th_resdirpath'], '{}_tux.log'.format(curtime))
COLQUERY = ['genotype', 'tube', 'sex', 'frozend', 'rnad', 'rnaconc', 
            'mrnad', 'cdnad', 'indexnum', 'sample', 'seqd', 'thawed',
            'toseq', 'samplenum', 'sentd', 'qbitngul', 'qbitd', 'seq_received']

def main():
    cmn.makenewdir(RNASEQDICT['th_resdirpath'])
    # Writes output to mrun.log and specifies format of logging output.
    logging.basicConfig(filename=TUXLOG_PATH,\
        format='%(asctime)s %(levelname)s %(message)s',\
        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', level=logging.INFO)
    console = logging.StreamHandler() # Displays output to screen.
    logging.getLogger('').addHandler(console)

    seqpaths, respaths = tl.get_berkid_seq_res_paths(BERKIDLIST, \
        SAMPLEINFO_TABLE, COLQUERY,RNASEQDICT['seq_dir'],RNASEQDICT['seq_subdir'], 
        RNASEQDICT['th_resdirpath'])
    print(seqpaths, respaths)

    berkid_params = zip(BERKIDLIST, seqpaths, respaths) 
    for berkid, sample_seqdir, sample_resdir in berkid_params:
        tl.run_tophat_cufflinks(berkid, sample_seqdir, sample_resdir, 
            RNASEQDICT, REFSEQDICT)
    shutil.copy(SETTINGS_FILE, NEW_SETTINGS_FILE)

if __name__ == '__main__':
    main()
