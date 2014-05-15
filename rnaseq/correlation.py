import numpy as np
import matplotlib as mpl
import os
import psycopg2
from scipy import stats
import itertools
import cProfile

CUFF_TABLE_PREFIX = 'cuff_genes_fpkm'

def get_cuff_info(cuffpath):
    cuffpath = os.path.abspath(cuffpath)
    sample = cuffpath.split('/')[6].split('_')[1]
    cufffile = os.path.join(cuffpath, 'genes.fpkm_tracking')
    newcufffile = os.path.join(cuffpath, 'genes_sample.fpkm_tracking')
    return(sample, cufffile, newcufffile)

def add_berkid(cuffpath):
    sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    with open(newcufffile, 'w') as g:
        with open(cufffile, 'r') as f:
            next(f)
            for l in f:
                newline = l.strip('\n') + '\t{0}\n'.format(sample)
                g.write(newline) 

#for cuffpath in cuffpaths:
    #add_id(cuffpath) 

def make_db_table(cuffpath, cur):
    os.chdir(cuffpath)
    sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    table_name = '{0}_{1}'.format(CUFF_TABLE_PREFIX, sample) 
    tablecmd_create = 'DROP TABLE IF EXISTS {0} CASCADE; CREATE TABLE {0} (tracking_id character varying(20), class_code character varying(2), nearest_ref_id character varying(2), gene_id character varying(20), gene_short_name character varying(100), tss_id character varying(2), locus character varying(100), length character varying(2), coverage character varying(2), FPKM double precision , FPKM_conf_lo double precision, FPKM_conf_hi double precision, FPKM_status character varying(5), berkid character varying(20));'.format(table_name)
    cur.execute("{0}".format(tablecmd_create))
    cur.copy_from(open(newcufffile), table_name)
    conn.commit()

def join_colnames():
    selectlist = ['t0.tracking_id', 't0.berkid', 'a0.sample', 't0.fpkm', \
    't0.fpkm_status', 't1.berkid', 'a1.sample', 't1.fpkm', 't1.fpkm_status']
    selectstring = ", ".join(selectlist)
    return(selectstring, selectlist)

def join_db_table(table0, table1, cur, maxfpkm=False):
    selectstring = join_colnames()[0]
    if maxfpkm:
        mfstring = ' AND t1.fpkm < {0} AND t2.fpkm < {0}'.format(maxfpkm)
    else:
        mfstring = ''

    createviewcmd = 
    joincmd = "SELECT {2} FROM {0} as t0 INNER JOIN autin as a0 using (berkid) FULL OUTER JOIN {1} as t1 INNER JOIN autin as a1 using (berkid) USING (tracking_id) WHERE t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK'{3} ORDER BY tracking_id;".format(table0, table1, selectstring, mfstring)
    print(joincmd)
    #joincmd = "SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status, t1.berkid, t2.berkid FROM {0} t1 FULL OUTER JOIN {1} t2 USING (tracking_id) WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' ORDER BY tracking_id".format(table1, table2)
    cur.execute(joincmd)
    jointable = np.array(cur.fetchall())
    #print(len(jointable))
    return(jointable)


def mjoin_db_table(berkidlist, conn):
    '''Input:
    samples = list of berkids to compare 
    '''
    comp_index = itertools.combinations(range(len(berkidlist)), 2) # List of indices for all pairwise comparisons of each sample.
    comparisons = []
    for i in comp_index:
        cur = conn.cursor()
        table1, table2 = ['{0}_{1}'.format(CUFF_TABLE_PREFIX, berkidlist[x]) for x in i]
        jointable = join_db_table(table1, table2, cur)
        comparisons.append(jointable)
        cur.close()
    return(comparisons)   

def get_correlation(joinedarray):
    '''
    Input:
    joinedarray = an array containing the FPKM for genes in two samples; returned by join_db_table()
    '''
    array = np.transpose(joinedarray)
    colnames = join_colnames()[1] 
    fpkm0, fpkm1 = [array[x][:].astype(np.float) for x in [colnames.index('t0.fpkm'),colnames.index('t1.fpkm')]]
    berkid1, berkid2, sample1, sample2 = [array[x][0] for x in [colnames.index('t0.berkid'), colnames.index('t1.berkid'), colnames.index('a0.sample'), colnames.index('a1.sample')]] 
    slope, intercept, r, p, std_err = stats.linregress(fpkm0, fpkm1)
    return(r, berkids, samples)


def create_corr_file(correlationfile):
    with open(correlationfile, 'w') as g:
        g.write('Berkid1\tSample1\tBerkid\tSample2\tr\tr^2\n')

def save_corr_file(r, berkids, samples, correlationfile):
    with open(correlationfile, 'a') as g:
        g.write('{},{},{},{},{}'.format(berkids[0], samples[0], berkids[1], samples[1], r))


if __name__ == '__main__':

    cuffpaths = ['/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out']
    corrfile = 'correlations.txt'

    print('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    print('making tables')
    for cuffpath in cuffpaths:
        make_db_table(cuffpath, cur)
    cur.close()
    conn.close()

    create_corr_file(corrfile)
    samples = ('rgam009b', 'rgam010f', 'rgsj006g')
    
    conn=psycopg2.connect("dbname=rnaseq user=andrea")
    print('joining and querying tables')
    data = mjoin_db_table(samples, conn)

    #print('finding correlations')
    #for array in data:
        #r, berkids, samples =  get_correlation(array)
        #print(samples, r, np.square(r))
        #save_corr_file(r, berkids, samples, corrfile)

    conn.close()
