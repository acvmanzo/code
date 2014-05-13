import numpy as np
import matplotlib as mpl
import os
import psycopg2
from scipy import stats
import itertools

cuffpaths = ['/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out']
CUFF_TABLE_PREFIX = 'cuff_genes_fpkm'

def get_cuff_info(cuffpath):
    cuffpath = os.path.abspath(cuffpath)
    sample = cuffpath.split('/')[6].split('_')[1]
    cufffile = os.path.join(cuffpath, 'genes.fpkm_tracking')
    newcufffile = os.path.join(cuffpath, 'genes_sample.fpkm_tracking')
    return(sample, cufffile, newcufffile)

def add_id(cuffpath):

    sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    with open(newcufffile, 'w') as g:
        with open(cufffile, 'r') as f:
            next(f)
            for l in f:
                newline = l.strip('\n') + '\t{0}\n'.format(sample)
                g.write(newline) 

                #trackid = l.split('\t')[0]
                #fpkm = l.split('\t')[9]
                #status = l.split('\t')[-1]

#for cuffpath in cuffpaths:
    #add_id(cuffpath) 


def make_db_table(cuffpath, cur):
    os.chdir(cuffpath)
    sample, cufffile, newcufffile = get_cuff_info(cuffpath)
    print(sample)

    table_name = '{0}_{1}'.format(CUFF_TABLE_PREFIX, sample) 
    tablecmd_create = 'DROP TABLE IF EXISTS {0} CASCADE; CREATE TABLE {0} (tracking_id character varying(20), class_code character varying(2), nearest_ref_id character varying(2), gene_id character varying(20), gene_short_name character varying(100), tss_id character varying(2), locus character varying(100), length character varying(2), coverage character varying(2), FPKM double precision , FPKM_conf_lo double precision, FPKM_conf_hi double precision, FPKM_status character varying(5), sample character varying(20));'.format(table_name)
    
    print(table_name)
    cur.execute("{0}".format(tablecmd_create))
    cur.copy_from(open(newcufffile), table_name)
    conn.commit()

def join_and_copy_db_table(samples, comp_index, cur, joindir):

    joinpaths = []
    comparisons = []
    for i,j in comp_index:
        table1_name = '{0}_{1}'.format(CUFF_TABLE_PREFIX, samples[i])
        table2_name = '{0}_{1}'.format(CUFF_TABLE_PREFIX, samples[j])
        print(table1_name, table2_name)
        joinname = 'joined_fpkm_{0}_{1}'.format(samples[i], samples[j])
        joinpath = os.path.join(os.path.abspath(joindir), joinname)
        
        viewcmd_create = 'CREATE OR REPLACE VIEW {0} AS SELECT t1.tracking_id, t1.fpkm as t1fpkm, t1.fpkm_status as t1fpkmstatus, t2.fpkm as t2fpkm, t2.fpkm_status as t2fpkmstatus from {1} t1 inner join {2} t2 using (tracking_id);'.format(joinname, table1_name, table2_name)
        #copycmd = "COPY (SELECT t1.tracking_id, t1.fpkm as t1fpkm, t1.fpkm_status as t1fpkmstatus, t2.fpkm as t2fpkm, t2.fpkm_status as t2fpkmstatus FROM {1} t1 INNER JOIN {2} t2 ON t1.tracking_id = t2.tracking.id ORDER BY tracking_id) TO '{0}' header csv;".format(joinpath, table1_name, table2_name)

        joincmd = "SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status, t1.sample, t2.sample FROM {1} t1 INNER JOIN {2} t2 USING (tracking_id) WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' ORDER BY tracking_id".format(joinpath, table1_name, table2_name)

        copycmd = "COPY ({0}) TO '{1}' header csv;".format(joincmd, joinpath)
        #cur.execute('{0}'.format(viewcmd_create))
        #cur.copy_to(open(joinpath, 'w'), joinname) 
        cur.execute(joincmd)
        allrows = cur.fetchall()
        print(allrows[0])
        #print(np.shape(allrows))
        
        cur.execute(copycmd)
        joinpaths.append(joinpath)
        comparisons.append(np.array(allrows))
    conn.commit()
    return(joinpaths, comparisons)   
        



conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

#for cuffpath in cuffpaths:
    #make_db_table(cuffpath, cur)

samples = ('rgam009b', 'rgam010f', 'rgsj006g')
comp_index = itertools.combinations(range(len(samples)), 2)
joinpaths, data = join_and_copy_db_table(samples, comp_index, cur, '/tmp')
print(np.shape(data))

for array in data:
    print("SAMPLES") 
    print(np.transpose(array)[5][0], np.transpose(array)[6][0])
    #print(type(array))
    sample1 = np.transpose(array)[1][:].astype(np.float)
    sample2 = np.transpose(array)[3][:].astype(np.float)
    slope, intercept, r, p, std_err = stats.linregress(sample1, sample2)
    print('r', r)
    print('r^2', np.square(r))
    #print(np.shape(sample1))
    #print(sample1[:4])

cur.close()
conn.close()
