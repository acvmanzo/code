import os
import logging
import psycopg2
from rnaseq_settings import *


def batch_fn(conn, fn):
    os.chdir(ALIGN_DIR)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('RG*')])
    for resdir in resdirs:
        cur = conn.cursor()
        print(resdir)
        os.chdir(os.path.join(resdir, TOPHAT_DIR))
        berkid = os.path.basename(resdir)
        print(berkid)
        eval(fn)
        cur.close()


def get_replicate_berkid_dict(cur, condition, sampleinfo_table):
    '''Queries the database to identify the biological replicates for the
    condition.
    Inputs:
    cur = cursor for querying using psycopg2
    condition = e.g., CS_M or CS_F
    sampleinfo_table = name of table being queries
    Outputs:
    A dictionary in which the keys are the conditions and the values are the
    berkids
    '''
    genotype, sex = condition.split('_')
    selcmd = "SELECT berkid FROM {} WHERE genotype = '{}' AND sex = '{}' AND seq_received = true ORDER BY berkid;".format(sampleinfo_table, genotype, sex)
    logging.debug('%s', selcmd)
    cur.execute(selcmd)
    berkids = [x[0] for x in cur.fetchall()]
    logging.debug('berkids for condition %s: %s', condition, berkids) 
    return(berkids)


def get_all_replicate_berkid_dict(cur, sampleinfo_table):
    '''Queries the database to identify all the biological replicates for all 
    conditions (e.g., CS_M or en_F).
    Inputs:
    cur = cursor for querying using psycopg2
    sampleinfo_table = name of table being queries
    Outputs:
    A dictionary in which the keys are the conditions and the values are the
    berkids
    '''
    cur.execute("SELECT DISTINCT genotype, sex FROM {} ORDER BY genotype, sex;".format( sampleinfo_table))
    condition_lists = cur.fetchall()
    all_berkid_dict = {}
    for cl in condition_lists:
        condition = '_'.join(cl)
        berkids = get_replicate_berkid_dict(cur, condition, sampleinfo_table)
        all_berkid_dict[condition] = berkids
    return(all_berkid_dict)


#def get_sample_results_dir(berkid, exp_results_dir):
    #'''Returns the path to a sample results directory by joining the berkid
    #with the exp_results_dir'''
    #return(os.path.join(exp_results_dir, berkid))

#def get_cufflink_path(berkid, exp_results_dir, exp_dir, berkid_fpkm_file):
    #'''Returns the path to an experiment fpkm file given a berkid'''
    #return(os.path.join(get_sample_results_dir(berkid, exp_results_dir),
        #exp_dir, berkid_fpkm_file))


def get_replicate_cufflink_paths(condition_berkid_dict):
    '''Returns a dictionary of paths to the cufflink output FPKM files for
    every condition in condition_berkid_dict.
    Input:
    condition_berkid_dict: keywords are conditions and values are lists of 
    berkids. Output by the functions get_replicate_berkid_dict or 
    get_all_replicate_berkid_dict). 
    Output:
    Dictionary of paths; keywords are conditions and values are lists of
    output FPKM file paths.
    '''
    replicate_path_dict = {} 
    for condition, berkids in condition_berkid_dict.items():
        replicate_path_dict[condition] = 
                [get_results_files(b)['cuff_gfpkm_path'] for b in berkids]
    return(replicate_path_dict)


def get_some_cufflink_paths(berkidlist, key):
    '''Returns a dictionary of paths to the cufflink output FPKM files for 
    the berkids in the berkidlist; key is given by key'''
    return({key: [get_results_files(b)['cuff_gfpkm_path'] for b in berkids]})


def get_all_replicate_cufflink_paths(cur, sampleinfo_table, exp_results_dir, 
        exp_dir, berkid_fpkm_file):
    '''Returns a dictionary of paths to the cufflink output FPKM files for
    every condition in the queried table.
    Inputs:
    cur = cursor used to execute SQL commands with psycopg2
    sampleinfo_table = table to be queried
    exp_results_dir = directory containing all the results files for all samples
    exp_dir = directory containing the expression results output
    berkid_fpkm_file = name of the file containing the cufflink FPKM output;
    not the raw output file but the modified file with the berkid appended to
    the end
    Outputs:
    A dictionary where the keys are the condition names and the values are
    paths to the FPKM file.
    '''
    replicate_berkid_dict = get_all_replicate_berkid_dict(cur, 
        sampleinfo_table)
    return(get_replicate_cufflink_paths(replicate_berkid_dict))

#def get_cufflink_berkid_fpkm_path(cufflink_fpkm_path, berkid_fpkm_file):
    #berkid = get_berkid(cufflink_fpkm_path)
    #berkid_fpkm_path = os.path.join(os.path.dirname(cufflink_fpkm_path), 
            #berkid_fpkm_file) 
    #return(berkid_fpkm_path)

def get_samplename(berkid, cur):
    '''Given a berkid, returns the sample by querying a sql database
    using the cursor cur.'''
    samplecmd = "select sample from autin where berkid = '{}'".format(berkid)
    cur.execute(samplecmd)
    sample = cur.fetchone()[0]
    return(sample)


def get_berkid(cufflink_fpkm_path, berkidlen=BERKIDLEN):
    '''return a berkid extracted from a cufflink_fpkm_path'''
    cf = exp_results_path
    return(cf[cf.find('RG'):cf.find('RG')+berkidlen])

def get_berkidlist(cufflink_fpkm_paths):
    '''returns a list of berkids extracted from a list of cufflink output paths'''
    return([get_berkid(cf) for cf in cufflink_fpkm_paths])
