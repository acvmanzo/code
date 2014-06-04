# Finds correlation between biological replicates using CLCBio output.

from correlationlib import *
import glob


CLC_TABLE = 'clc_data'


def get_clc_fpkm_paths(clc_data_dir):
    os.chdir(clc_data_dir)
    clc_fpkm_paths = sorted(glob.glob('*-Seq.txt'))
    return(clc_fpkm_paths)


def get_clc_berkid_fpkm_path(clc_fpkm_path):
    return(clc_fpkm_path.rstrip('.txt') + '_berkid.txt')

def get_berkid_clc(clc_fpkm_path):
    for part in (os.path.basename(clc_fpkm_path).split('_')):
        if 'RG' in part:
            return(part) 

def copy_clc_data_to_table(clc_fpkm_paths, clc_table):
    '''copies clc data to database table.
    inputs:
    clc_fpkm_paths: paths to CLC output tables 
    cuff_table: database table with CLC data
    '''
    logging.info('opening connection')
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    berkid_clc_fpkm_paths = [get_clc_berkid_fpkm_path(cf) for cf in \
            clc_fpkm_paths]
    berkids = [get_berkid_clc(cf) for cf in clc_fpkm_paths]
    madd_berkid(zip(berkids, clc_fpkm_paths, 
        berkid_clc_fpkm_paths))
    mcopy_to_dbtable(berkid_clc_fpkm_paths, clc_table, cur)
    conn.commit()
    cur.close()
    conn.close()


fpkm_path = '/home/andrea/Documents/lab/RNAseq/analysis/CLC_results/CS_MB_RGAM009B_RNA-Seq.txt'
#berkid_fpkm_file = os.path.basename(fpkm_path).strip('.txt') + '_berkid.txt'
#berkid = os.path.basename(fpkm_path).split('_')[2]

#cufflink_fpkm_paths = ['/home/andrea/Documents/lab/RNAseq/analysis/CLC_results/CS_MA_RGSJ006G_RNA-Seq.txt',
#'/home/andrea/Documents/lab/RNAseq/analysis/CLC_results/CS_MB_RGAM009B_RNA-Seq.txt']

clc_data_dir = '/home/andrea/Documents/lab/RNAseq/analysis/CLC_results'
#clc_fpkm_paths = get_clc_fpkm_paths(clc_data_dir)

#copy_clc_data_to_table(clc_fpkm_paths, CLC_TABLE)


with open(fpkm_path, 'r') as f:
    next(f)
    for l in f:
        print(l)

