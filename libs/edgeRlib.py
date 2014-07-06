import sys
import glob
import numpy as np
import os
import psycopg2
import cmn.cmn as cmn
import libs.rnaseqlib as rl
#import htseqlib as hl
#import de_settings
import rnaseq_settings as rs
#from edger_settings import *

def get_count_paths(berkids, gene_subset):
    '''Returns a list of paths to the extant htseqcount files for each berkid
    in berkids. If gene_subset is given, the gene_subset is appended to the
    htseqcount file name.
    '''
    paths = []
    for berkid in berkids:
        countpath = rs.get_results_files(berkid)['htseq_count_path']
        if gene_subset:
            countpath = countpath+'_{}'.format(gene_subset)
        paths.append(countpath)
    return(paths)

def get_metadata(conn, allgenlist, sampleinfo_table, gene_subset):
    '''Gets metadata for use in writing a metadata file with write_metadata().
    Inputs:
    conn = connection to database using psycopg2
    allgenlist = list of all genotypes (e.g., CS_F), experimental and controls
    sample_infotable = table in the database that contains info about the 
    genotypes (usually autin)
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    Output:
    zip object with (berkid, sample, path) tuples for each sample with the
    genotype in allgenlist.
    '''
    cur = conn.cursor()
    berkids = []
    samples = []
    for gen in allgenlist:
        berkids.extend(rl.get_replicate_berkid_dict(cur, gen, sampleinfo_table))
    cur.close()
    cur = conn.cursor()
    for b in berkids:
        samples.append(rl.get_samplename(b, cur))
    cur.close()
    paths = get_count_paths(berkids, gene_subset)
    #for i, b in enumerate(berkids):
        #print(b, paths[i])
    return(zip(berkids, samples, paths))
   

def write_metadata(allgenlist, controllist, metadatafile, sampleinfo_table, 
        gene_subset):
    '''Writes a file called metadatafile that contains information for edgeR
    analysis. The metadata file has 4 columns: Sample, Berkid, CorE (control or 
    experimental sample), and HTSeqPath (path to htseqfile)

    Input:
    allgenlist = list of all genotypes (e.g., CS_F), experimental and
    controls. 
    controllist = list of the samples that will be used as controls
    metadatafile = name of the metadata file that will be written
    sample_infotable = table in the database that contains info about the 
    genotypes (usually autin)
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    ''' 
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    items = get_metadata(conn, allgenlist, sampleinfo_table, gene_subset) 
    with open(metadatafile, 'w') as f:
        f.write('Sample\tBerkid\tCorE\tHTSeqPath\n')
        for berkid, sample, path in items:
            if os.path.exists(path):
                if sample[:-1] in controllist:
                    core = 'ctrl'
                else:
                    core = 'expt'
                f.write('{}\t{}\t{}\t{}\n'.format(sample, berkid, core, path))
    conn.close()


def edger_pairwise_DE(expt, ctrl, gene_subset, edger_file_dict):
    '''Runs edgeR comparing expt and control genotypes. Writes a metadata file
    and calls the edgeR.R script.  
    Input:
    exptlist = list of genotypes that will be compared against control
    ctrl = length-1 list containing control genotype
    edger_dirpath = path to edger directory
    metadatafile = name of the metadata file that will be written
    sample_infotable = string specifying table in the database that contains
        info about the genotypes (usually autin)
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    edger_file_dict = dictionary containing the file names for the plots and 
        data output by edgeR.R
    '''
    edger_dirpath = edger_file_dict['edger_dirpath'] 
    metadatafile = edger_file_dict['edger_metadata_file']
    sampleinfo_table = edger_file_dict['sampleinfo_table']

    edgerresdir = os.path.join(edger_dirpath, gene_subset)
    cmn.makenewdir(edgerresdir)
    os.chdir(edgerresdir)
    condlist = [ctrl, expt]
    print(condlist)
    cmn.makenewdir(expt)
    os.chdir(expt)
    write_metadata(condlist, ctrl, metadatafile, sampleinfo_table, 
            gene_subset)
    run_edger(edger_file_dict)


def batch_edger_pairwise_DE(exptlist, ctrl, gene_subset, edger_file_dict):
    '''Runs edgeR for each genotype given in exptlist against the control
    given in ctrl. Writes a metadata file and calls the edgeR.R script.
    Input:
    exptlist = list of genotypes that will be compared against control
    ctrl = length-1 list containing control genotype
    edger_dirpath = path to edger directory containing all the results
    metadatafile = name of the metadata file that will be written
    sample_infotable = string specifying table in the database that contains
        info about the genotypes (usually autin)
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    edger_file_dict = dictionary containing the file names for the plots and 
        data output by edgeR.R
    '''
    for cond in exptlist:
        edger_pairwise_DE(cond, ctrl, gene_subset, edger_file_dict)



def edger_2groups_DE(exptdict, gene_subset, edger_file_dict):
    '''Runs edgeR to find DE genes between two groups of samples.
    Input:
    exptdict = dictionary where the keys are the groups to be compared
        and the values are the list of genotypes for each group. One key is
        'ctrl' and specifies the control genotypes. 
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    edger_file_dict = dictionary containing the file names for the plots and 
        data output by edgeR.R
    '''

    #condstotest = ['CG34127_M', 'en_M', 'NrxI_M']
    #controls = ['Betaintnu_M', 'Nhe3_M', 'NrxIV_M', 'pten_M', 'CS_M']
    #controls = ['CS_M'] 
    
    ctrlname = 'ctrl' 
    for k,v in exptdict.items():
        print(k,v)
        if k == 'ctrl':
            ctrllist = v
        else:
            exptlist = v
            exptname = k
    allgenlist = exptlist + ctrllist
    #print('allgenlist', allgenlist)
    #print('ctrllist', ctrllist)
    
    edger_dirpath = edger_file_dict['edger_dirpath'] 
    metadatafile = edger_file_dict['edger_metadata_file']
    sampleinfo_table = edger_file_dict['sampleinfo_table']

    edgerresdir = os.path.join(edger_dirpath, gene_subset)
    cmn.makenewdir(edgerresdir)
    os.chdir(edgerresdir)
    cmn.makenewdir(exptname)
    os.chdir(exptname)

    write_metadata(allgenlist, ctrllist, metadatafile, sampleinfo_table, 
            gene_subset)
    run_edger(edger_file_dict)


def run_edger(edger_file_dict):
    '''Runs edgeR using the script edgeR.R. Input is a dictionary containing
    the file names for the plots and data output by edgeR.R
    '''
    d = edger_file_dict 
    cmd = 'Rscript ~/Documents/lab/code/rnaseq_analysis/edgeR.R {0} {1} {2} {3} {4} {5} > edgeR.log 2>&1'.format(d['edger_mdsplot_file'], 
            d['edger_mvplot_file'], d['edger_bcvplot_file'], 
            d['edger_maplot_file'], d['edger_toptags_file'],
            d['edger_toptags_fdr_file'])
    print(cmd)
    os.system(cmd)

def gen_de_dict(sample_list, degenedir, degenefile):
    degenes = {}
    for sample in sample_list:
        os.chdir(os.path.join(degenedir, sample))
        with open(degenefile, 'r') as f:
            degenes[sample] = f.read().split('\n')[:-1]
    return(degenes)

def gen_db_degenefile(degenefile, db_degenefile, tool, gene_subset, group1, 
        group2):
    '''Rewrites a file containing the results of DE analysis to add a 
    column specifying the tool (e.g., edgeR), the gene subset (e.g., 
    prot_coding_genes) and two columns specifying the groups being compared
    (ex., group1=Betaintnu_F, group2=CS_F).
    
    Input:
    degenefile = file with results of DE analysis (e.g., toptags_edgeR.csv, 
        output by edgeR.R
    db_degenefile = name of new file that will be written 
    tool = name of DE analysis tool (e.g., edgeR)
    gene_subset = subset of genes analyzed
    group1 = name of 1 group being compared (usually experimental group, like
        Betaintnu_F or lowagg)
    group2 = name of second group being compared (usually control group, like
        CS_F or normalagg)

    '''
    with open(db_degenefile, 'w') as g:
        with open(degenefile, 'r') as f:
            next(f)
            for l in f:
                g.write('{},{},{},{},{}\n'.format(l.rstrip('\n'), tool, 
                    gene_subset, group1, group2))

def batch_db_degenefile(degenedir, degenefile, db_degenefile, gendirs, group1list, group2list, tool):
    '''Batch function for rewriting DE analysis output files for inclusion
    in the database.

    degenedir = main directory containing the results of DE analysis (e.g., 
        analysis/edgeR)
    degenefile = name of file with the DE analysis results (e.g., 
        toptags_edgeR.csv)
    db_degenefile = name of output file
    gendirs = list of directories with genotypes/condition
    group1list = 
    '''
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
