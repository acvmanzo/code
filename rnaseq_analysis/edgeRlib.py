import sys
import glob
import numpy as np
import os
#import htseqlib as hl
import de_settings
import psycopg2

def get_count_paths(berkids):
    paths = []
    for berkid in berkids:
        paths.append(rdl.get_cufflink_path(berkid, ALIGN_DIR, TOPHAT_DIR,
            COUNTFILE))
    return(paths)

def get_metadata(conn, condlist, sample_infotable):
    cur = conn.cursor()
    berkids = []
    samples = []
    for cond in condlist:
        berkids.extend(rdl.get_replicate_berkid_dict(cur, cond, sample_infotable))
    cur.close()
    cur = conn.cursor()
    for b in berkids:
        samples.append(rdl.get_samplename(b, cur))
    cur.close()
    paths = get_count_paths(berkids)
    return(zip(berkids, samples, paths))
    
def write_metadata(metadatafile, condlist, sample_infotable, controllist):

    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    items = get_metadata(conn, condlist, sample_infotable) 
    with open(metadatafile, 'w') as f:
        f.write('Sample\tBerkid\tCorE\tHTSeqPath\n')
        for berkid, sample, path in items:
            if sample[:-1] in controllist:
                core = 'ctrl'
            else:
                core = 'expt'
            f.write('{}\t{}\t{}\t{}\n'.format(sample, berkid, core, path))
    conn.close()

def batch_edger_pairwise_DE(exptlist, ctrl):
    for cond in exptlist:
        os.chdir(EDGER_DIR)
        condlist = [ctrl, cond]
        print(condlist)
        cmn.makenewdir(cond)
        os.chdir(cond)
        write_metadata(METADATAFILE, condlist, INFODBTABLE, [ctrl])
        run_edger()


def run_edger():
        cmd = 'Rscript ~/Documents/lab/code/rnaseq_analysis/edgeR.R'
        os.system(cmd)


def groups_edger_DE():

    condstotest = ['CG34127_M', 'en_M', 'NrxI_M']
    #controls = ['Betaintnu_M', 'Nhe3_M', 'NrxIV_M', 'pten_M', 'CS_M']
    controls = ['CS_M']
    conditions = condstotest + controls
    
    write_metadata(METADATAFILE, conditions, INFODBTABLE, controls)
    run_edger()


def gen_de_dict(sample_list, degenedir, degenefile):
    degenes = {}
    for sample in sample_list:
        os.chdir(os.path.join(degenedir, sample))
        with open(degenefile, 'r') as f:
            degenes[sample] = f.read().split('\n')[:-1]
    return(degenes)

def gen_db_degenefile(degenefile, db_degenefile, tool, group1, group2):
    with open(db_degenefile, 'w') as g:
        with open(degenefile, 'r') as f:
            next(f)
            for l in f:
                g.write('{},{},{},{}\n'.format(l.rstrip('\n'), tool, group1, group2))

def batch_db_degenefile(degenedir, degenefile, db_degenefile, dirs, group1list, group2list, tool):
    degenepaths = [os.path.join(degenedir, d, degenefile) for d in dirs]
    db_degenepaths = [os.path.join(degenedir, d, db_degenefile) for d in dirs]

    if len(group2list) == 1:
        group2list = np.tile(group2list[0], len(group1list))

    groups = list(zip(group1list, group2list, degenepaths, db_degenepaths))
    print(groups)
    for i, group in enumerate(groups):
        #print(i, group)
        gen_db_degenefile(degenefile=group[2], db_degenefile=group[3], 
                tool=tool, group1=group[0], group2=group[1])
    
def copy_dbgenes_to_db(cur, db_degenefile, table):
    with open(db_degenefile, 'r') as f:
        cur.copy_from(f, table, sep=',')

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

def batch_copy_dbgenes_to_db(degenedir, conn, db_degenefile, table):
    os.chdir(degenedir)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('*/')])
    for resdir in resdirs:
        os.chdir(resdir)
        print(os.path.basename(resdir))
        cur = conn.cursor()
        if os.path.exists(db_degenefile):
            try:
                copy_dbgenes_to_db(cur, db_degenefile, table)
            except psycopg2.IntegrityError:
                cur.close()
                conn.commit()
                continue
        else:
            print('No dbgene file')



def gen_dbgene_copyfrom_cmd(table, group1, group2, fdr_th):
    cmd =  "COPY (select * from {} where group1 = '{}' and group2 = '{}' and fdr < {}) to STDOUT;".format(table, group1, group2, fdr_th)
    return(cmd)

def copy_dbgenes_from_db(cur, out_degenefile, cmd):
    #a = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/CG34127_M/test.csv'
    with open(out_degenefile, 'w') as f:
        cur.copy_expert(cmd, f)
            
    
def batch_copy_dbgenes_from_db(conn, degenedir, db_degenefile, out_degenefile, table, fdr_th):

    os.chdir(degenedir)
    resdirs = sorted([os.path.abspath(x) for x in glob.glob('*/')])
    for resdir in resdirs:
        os.chdir(resdir)
        print(os.path.basename(resdir))
        cur = conn.cursor()
        if os.path.exists(db_degenefile):
            with open(db_degenefile, 'r') as f:
                group1, group2 = next(f).rstrip('\n').split(',')[-2:]
            cmd = gen_dbgene_copyfrom_cmd(table, group1, group2, fdr_th)
            print(cmd)
            copy_dbgenes_from_db(cur, out_degenefile, cmd)
            with open(out_degenefile, 'r') as f:
                if not list(f):
                    print('empty file')
            cur.close()
        else:
            cur.close()
            conn.commit()
            print('No db_degenfile exists')

     


MALES = ['Betaintnu_M', 'CG34127_M', 'en_M', 'Nhe3_M', 'NrxI_M', 'NrxIV_M', 'pten_M']
MALES_CTRL = ['CS_M']
dirmales = MALES
male_params = (dirmales, MALES, MALES_CTRL)

FEMALES = ['Betaintnu_F', 'CG34127_F', 'en_F', 'Nhe3_F', 'NrxI_F', 'NrxIV_F', 'pten_F']
FEMALES_CTRL = ['CS_F']
dirfemales = FEMALES
female_params = (dirfemales, FEMALES, FEMALES_CTRL)

LOWAGG = ['lowagg', 'lowagg']
NORMAGG = ['CS', 'normagg']
diraggs = ['lowagg_vs_CS', 'lowagg_vs_normagg_CS']
agg_params = (diraggs, LOWAGG, NORMAGG)

DEGENETABLE = 'degenes'
DEGENEDIR = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes'
DEGENEFILE = 'toptags_edgeR.csv'
DB_DEGENEFILE = 'db_toptags_edgeR.csv'
FDR_TH = 0.05
FDR_DEGENEFILE = 'toptags_edgeR_fdr{}.csv'.format(FDR_TH)

#degenefile_for_db(DEGENEFILE, 'db_'+DEGENEFILE, 'edgeR', 'Betaintnu_F', 'CS_F')

#Generates files formatted so they can be copied to the database.
#for params in [male_params, female_params, agg_params]:
    #dirs, group1list, group2list = params
    #batch_db_degenefile(DEGENEDIR, DEGENEFILE, DB_DEGENEFILE, dirs, 
    #group1list, group2list, 'edgeR')

#Copies DE gene data to the database.
#conn = psycopg2.connect("dbname=rnaseq user=andrea")
#batch_copy_dbgenes_to_db(DEGENEDIR, conn, DB_DEGENEFILE, 'degenes')
#conn.commit()
#conn.close()



# Copies DE gene data from the database into a file.
#conn = psycopg2.connect("dbname=rnaseq user=andrea")
#batch_copy_dbgenes_from_db(conn, DEGENEDIR, DB_DEGENEFILE, FDR_DEGENEFILE,
        #DEGENETABLE, FDR_TH)
#cur = conn.cursor()
#with open('test.csv', 'w') as f:
    #cmd = "COPY (select * from degenes where group1 = 'pten_M' and group2 = 'CS_M' and fdr < 0.05) to STDOUT;"
    #cur.copy_expert(cmd, f)
#conn.commit()
#conn.close()


############UNUSED##############
#ded = gen_de_dict(SAMPLE_LIST, DEGENEDIR, DEGENEFILE)

#npded = np.array(ded.items())
#print(npded)
#print(npded.shape)
#print(len(npded))
##np.savetxt('test.txt', npded)

#def write_de_dict(degene_dict, all_degene_file):
    #for sample, genes in degene_dict.items():

#def add_degenes_db():
