import os
import logging
import psycopg2

#globstring = 'RG*'

#def batch_fn_thdir(batchdir, globstring, conn, fn):
    #os.chdir(batchdir)
    #resdirs = sorted([os.path.abspath(x) for x in glob.glob(globstring)])
    #for resdir in resdirs:
        #cur = conn.cursor()
        #print(resdir)
        #os.chdir(os.path.join(resdir, TOPHAT_DIR))
        #berkid = os.path.basename(resdir)
        #print(berkid)
        #eval(fn)
        #cur.close()


def batch_fn(pardir, globstring, subdir, conn, fn):
    os.chdir(pardir)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob(globstring)])
    for resdir in resdirs:
        cur = conn.cursor()
        print(resdir)
        os.chdir(os.path.join(resdir, subdir))
        berkid = os.path.basename(resdir)
        print(berkid)
        eval(fn)
        cur.close()


def add_berkid(berkid, file_path):
    '''adds the berkid to the last columns of a file
    '''
    berkid_file_path = file_path + '_berkid'
    with open(berkid_file_path, 'w') as g:
        with open(file_path, 'r') as f:
            #print(file_path)
            #print('current working dir', os.getcwd())
            if file_path == 'genes.fpkm_tracking':
                next(f)
            for l in f:
                if '__' in l.split('\t')[0]:
                    continue
                newline = l.strip('\n') + '\t{0}\n'.format(berkid)
                g.write(newline) 


def madd_berkid(berkid_filepath_tuples):
    '''Input is list of tuples of the following form:
    (berkid, file path)
    '''
    for berkid, fp in berkid_filepath_tuples:
        if not os.path.exists(cf):
            logging.info('%s does not exist', cf)
            continue
        add_berkid(berkid, fp)



def get_num_genes(dbtable, berkid, cur):
    '''Finds the number of genes in dbtable with berkid berkid'''
    checkrowscmd = "select count (*) from (select * from {} where berkid = '{}') as foo;".format(dbtable, berkid)
    cur.execute(checkrowscmd)
    return(cur.fetchone()[0])

def get_num_degenes(dbtable, tool, gene_subset, group1, group2):
    '''Checks if the table already contains data from a DE analysis experiment
    with the given tool, gene_subset, group1, and group2.
    '''
    checkrowscmd = "select count (*) from (select * from {} where berkid = '{}') as foo;".format(dbtable, berkid)
    cur.execute(checkrowscmd)
    return(cur.fetchone()[0])

def copy_to_dbtable(berkid_file_path, dbtable, cur):
    '''copies data from the modfied file output by rl.add_berkid() into the sql
    table dbtable using the cursor cur.
    '''
    #print(berkid_fpkm_p_ath)
    logging.debug('cwd', os.getcwd())
    with open(berkid_file_path, 'r') as f:
        info = next(f)
    berkid = info.strip('\n').split('\t')[-1]
    logging.debug('copy_to_db', berkid)
    checkrows = int(get_num_genes(dbtable, berkid, cur))
    logging.debug(checkrows, 'checkrows')
    logging.debug(berkid_file_path)
    logging.debug(dbtable)
    if checkrows != 0:
        delcmd = "delete from {} where berkid = '{}';".format(dbtable, berkid)
        cur.execute(delcmd)
    cur.copy_from(open(berkid_file_path), dbtable)


def mcopy_to_dbtable(sample_file_paths, dbtable, cur):
    '''applies copy_to_dbtable() to multiple files.
    '''
    logging.info('copying data to table')
    for sample_file_path in sample_file_paths:
        copy_to_dbtable(sample_file_path, dbtable, cur)

def get_replicate_berkid_dict(cur, genotype, sampleinfo_table):

    '''Queries the database to identify the biological replicates for the
    given genotype.
    Inputs:
    cur = cursor for querying using psycopg2
    genotype = e.g., CS_M or CS_F
    sampleinfo_table = name of table being queries
    Outputs:
    A dictionary in which the keys are the genotypes and the values are the
    berkids
    '''
    genotype, sex = genotype.split('_')
    selcmd = "SELECT berkid FROM {} WHERE genotype = '{}' AND sex = '{}' AND use_seq = true ORDER BY berkid;".format(sampleinfo_table, genotype, sex)
    logging.debug('%s', selcmd)
    cur.execute(selcmd)
    berkids = [x[0] for x in cur.fetchall()]
    logging.debug('berkids for genotype %s: %s', genotype, berkids) 
    return(berkids)


def get_all_replicate_berkid_dict(cur, sampleinfo_table):
    '''Queries the database to identify all the biological replicates for all 
    genotypes (e.g., CS_M or en_F).
    Inputs:
    cur = cursor for querying using psycopg2
    sampleinfo_table = name of table being queries
    Outputs:
    A dictionary in which the keys are the genotypes and the values are the
    berkids
    '''
    cur.execute("SELECT DISTINCT genotype, sex FROM {} ORDER BY genotype, sex;".format( sampleinfo_table))
    genotype_lists = cur.fetchall()
    all_berkid_dict = {}
    for cl in genotype_lists:
        genotype = '_'.join(cl)
        berkids = get_replicate_berkid_dict(cur, genotype, sampleinfo_table)
        all_berkid_dict[genotype] = berkids
    return(all_berkid_dict)



#def get_sample_results_files(berkid, exp_results_dir):

def get_sample_results_dir(berkid, exp_results_dir):
    '''Returns the path to a sample results directory by joining the berkid
    with the exp_results_dir
    ex., If exp_results_dir = .../results_tophat and berkid = RGAM010H, 
    returns ../results_tophat/RGAM010H.
    '''
    return(os.path.join(exp_results_dir, berkid))


def get_fpkm_path(berkid, exp_results_dir, exp_dir, berkid_fpkm_file):
    '''Returns the path to an experiment fpkm file given a berkid'''
    return(os.path.join(get_sample_results_dir(berkid, exp_results_dir),
        exp_dir, berkid_fpkm_file))



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
        replicate_path_dict[condition] = \
                [get_results_files(b)['cuff_gfpkm_path'] for b in berkids]
    return(replicate_path_dict)

def get_some_cufflink_paths(berkidlist, key):
    '''Returns a dictionary of paths to the cufflink output FPKM files for 
    the berkids in the berkidlist; key is given by key'''
    return({key: [get_results_files(b)['cuff_gfpkm_path'] for b in berkids]})

### OLD VERSIONS
#def get_replicate_cufflink_paths(condition_berkid_dict, exp_results_dir,
        #exp_dir, berkid_fpkm_file):
    #'''Returns a dictionary of paths to the cufflink output FPKM files for
    #every condition in condition_berkid_dict. This dictionary has keywords
    #that are conditions and values that are berkids.
    #'''
    #replicate_path_dict = {} 
    #for condition, berkids in condition_berkid_dict.items():
        #replicate_path_dict[condition] = [get_cufflink_path(b, 
            #exp_results_dir, exp_dir, berkid_fpkm_file) for b in berkids]
    #return(replicate_path_dict)

#def get_some_cufflink_paths(berkidlist, exp_results_dir, exp_dir,
    #berkid_fpkm_file, key):
    #'''Returns a dictionary of paths to the cufflink output FPKM files for 
    #the berkids in the berkidlist; key is given by key'''
    #return({key: [get_cufflink_path(berkid, exp_results_dir, exp_dir,
        #berkid_fpkm_file) for berkid in berkidlist]})


def get_all_replicate_cufflink_paths(cur, sampleinfo_table, exp_results_dir, 
        exp_dir, berkid_fpkm_file):
    '''Returns a dictionary of paths to the cufflink output FPKM files for
    every condition in the queried table.
    Inputs:
    cur = cursor used to execute SQL commands with psycopg2
    sampleinfo_table = table to be queried
    exp_results_dir = directory containing all the results files all samples
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
    return(get_replicate_cufflink_paths(replicate_berkid_dict, 
        exp_results_dir, exp_dir, berkid_fpkm_file))

def get_cufflink_berkid_fpkm_path(cufflink_fpkm_path, berkid_fpkm_file):
    berkid = get_berkid(cufflink_fpkm_path)
    berkid_fpkm_path = os.path.join(os.path.dirname(cufflink_fpkm_path), 
            berkid_fpkm_file) 
    return(berkid_fpkm_path)

def get_samplename(berkid, cur):
    '''given a berkid, returns the sample by querying a sql database
    using the cursor cur.'''
    samplecmd = "select sample from autin where berkid = '{}'".format(berkid)
    cur.execute(samplecmd)
    sample = cur.fetchone()[0]
    return(sample)


def get_berkid(cufflink_fpkm_path, berkidlen):
    '''return a berkid extracted from a cufflink_fpkm_path'''
    cf = exp_results_path
    return(cf[cf.find('RG'):cf.find('RG')+berkidlen])

def get_berkidlist(cufflink_fpkm_paths):
    '''returns a list of berkids extracted from a list of cufflink output paths'''
    return([get_berkid(cf) for cf in cufflink_fpkm_paths])


def check_table_exists(table, cur):
    cmd = "SELECT EXISTS( SELECT 1 FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relname = '{}');;".format(table)

    cur.execute(cmd)
    result = cur.fetchone()[0]
    return(result)

def logginginfo(logpath):
    logging.basicConfig(filename=logpath, 
            format='%(asctime)s %(levelname)s %(message)s', 
            datefmt='%m/%d/%Y_%I-%M-%S %p', 
            filemode='w', 
            level=logging.DEBUG)
    console = logging.StreamHandler() # Displays output to screen.
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

