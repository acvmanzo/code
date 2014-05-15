import numpy as np
import matplotlib as mpl
import os
import psycopg2
from scipy import stats
import itertools
import cProfile
import pstats

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
    print(tablecmd_create)
    cur.execute("{0}".format(tablecmd_create))
    cur.copy_from(open(newcufffile), table_name)

def join_colnames():
    #selectlist = ['t0.tracking_id', 't0.berkid', 'a0.sample', 't0.fpkm', 't0.fpkm_status', 't1.berkid', 'a1.sample', 't1.fpkm', 't1.fpkm_status']

    selectlist = ['t0.tracking_id', 't0.berkid', 't0.fpkm', 't0.fpkm_status', 't1.berkid', 't1.fpkm', 't1.fpkm_status']
    selectstring = ", ".join(selectlist)
    return(selectstring, selectlist)

def join_db_table(table0, table1, cur, maxfpkm=False):
    selectstring = join_colnames()[0]
    tempselect0 = selectstring[:5]
    tempselect1 = selectstring[5:]

    if maxfpkm:
        mfstring = ' AND t1.fpkm < {0} AND t2.fpkm < {0}'.format(maxfpkm)
    else:
        mfstring = ''

    #createview0cmd = "CREATE VIEW {0} AS SELECT {1} FROM {2} as t0 INNER JOIN autin as a0 using (berkid)".format('tempview0', tempselect0, table0)
    #createview1cmd = "CREATE VIEW {0} AS SELECT {1} FROM {2} as t1 INNER JOIN autin as a1 using (berkid)".format('tempview1', tempselect0, table0)
    #joincmd = "SELECT {0} FROM tempview0 as t0 FULL OUTER JOIN tempview1 as t1 USING
    #(tracking_id) WHERE t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND
    #t1.fpkm_status = 'OK'{3} ORDER BY tracking_id;".format(table0, table1, selectstring, mfstring)

    joincmd = "SELECT {2} FROM {0} as t0 FULL OUTER JOIN {1} as t1 USING (tracking_id) WHERE t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK'{3} ORDER BY tracking_id;".format(table0, table1, selectstring, mfstring)
    #joincmd = "SELECT {2} FROM {0} as t0 INNER JOIN autin as a0 using (berkid) FULL OUTER JOIN {1} as t1 INNER JOIN autin as a1 using (berkid) USING (tracking_id) WHERE t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK'{3} ORDER BY tracking_id;".format(table0, table1, selectstring, mfstring)
    print(joincmd)
    #joincmd_old = "SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status, t1.berkid, t2.berkid FROM {0} t1 FULL OUTER JOIN {1} t2 USING (tracking_id) WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' ORDER BY tracking_id".format(table0, table1)
    cur.execute(joincmd)
    jointable = np.array(cur.fetchall())
    #print(len(jointable))
    return(jointable)


def mjoin_db_table(berkidlist, cur):
    '''Input:
    samples = list of berkids to compare 
    '''
    comp_index = itertools.combinations(range(len(berkidlist)), 2) # List of indices for all pairwise comparisons of each sample.
    comparisons = []
    for i in comp_index:
        #cur = conn.cursor()
        table1, table2 = ['{0}_{1}'.format(CUFF_TABLE_PREFIX, berkidlist[x]) for x in i]
        jointable = join_db_table(table1, table2, cur)
        comparisons.append(jointable)
    return(comparisons)   

def get_correlation(joinedarray):
    '''
    Input:
    joinedarray = an array containing the FPKM for genes in two samples; returned by join_db_table()
    '''
    array = np.transpose(joinedarray)
    colnames = join_colnames()[1] 
    fpkm0, fpkm1 = [array[x][:].astype(np.float) for x in [colnames.index('t0.fpkm'),colnames.index('t1.fpkm')]]
    #berkid0, berkid1, sample0, sample1 = [array[x][0] for x in [colnames.index('t0.berkid'), colnames.index('t1.berkid'), colnames.index('a0.sample'), colnames.index('a1.sample')]] 
    berkid0, berkid1, = [array[x][0] for x in [colnames.index('t0.berkid'), colnames.index('t1.berkid')]]
    slope, intercept, r, p, std_err = stats.linregress(fpkm0, fpkm1)
    return(r, berkid0, berkid1)


def create_corr_file(correlationfile):
    with open(correlationfile, 'w') as g:
        g.write('berkid0\tsample0\tberkid1\tsample1\tr\tr^2\n')

def save_corr_file(r, berkid0, berkid1, correlationfile):
    with open(correlationfile, 'a') as g:
        g.write('{}\t{}\t{}\t{}\n'.format(berkid0, berkid1, r, np.square(r)))


def testmain():

    cuffpaths = ['/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out']
    corrfile = 'correlations.txt'

    print('opening connection')
    conn1 = psycopg2.connect("dbname=rnaseq user=andrea")
    cur1 = conn1.cursor()
    print('making tables')
    for cuffpath in cuffpaths:
        make_db_table(cuffpath, cur1)
    conn1.commit()
    cur1.close()
    conn1.close()

    create_corr_file(corrfile)
    samples = ('rgam009b', 'rgam010f', 'rgsj006g')
    
    conn2=psycopg2.connect("dbname=rnaseq user=andrea")
    cur2 = conn2.cursor()
    print('joining and querying tables')
    data = mjoin_db_table(samples, cur2)

    print('finding correlations')
    for array in data:
        r, berkid0, berkid1 =  get_correlation(array)
        print(samples, r, np.square(r))
        save_corr_file(r, berkid0, berkid1, corrfile)
    cur2.close()
    conn2.close()

#cProfile.run('testmain()', 'corrprofile')
cProfile.run('testmain()')
#p=pstats.Stats('conntest')
#p.strip_dirs().sort_stats(-1).print_stats()
#p.sort_stats('cumulative').print_stats(10)

