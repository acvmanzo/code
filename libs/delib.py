#Functions for differential expression analysis using edgeR and DESeq.

import sys
import glob
import numpy as np
import os
import psycopg2
import cmn.cmn as cmn
import libs.rnaseqlib as rl
import rnaseq_settings as rs
import logging



def remove_htseqcount_files(conn, rnaset):
    '''Removes old htseqcount files.
    rnaset: object of class RNASeqData in the rnaseq_settings module
    '''
    fn = "print(os.getcwd()), os.remove('htseqcount_brain_aut_will_r557_ralph_mt_excluded')"
    hl.batch_fn_thdir(rs.rnaset.th_resdirpath, rs.rnaset.htseq_dir, 
            rs.rnaset.res_sample_glob, conn, fn)
    conn.close()

def get_count_paths(rnaset, berkids, gene_subset):
    '''Returns a list of paths to the extant htseqcount files for each berkid
    in berkids. If gene_subset is given, the gene_subset is appended to the
    htseqcount file name. 
    rnaset: object of class RNASeqData in the rnaseq_settings module
    '''
    paths = []
    for berkid in berkids:
        countpath = rnaset.GetResultsFiles(berkid)['htseq_count_path']
        if gene_subset != 'all':
            countpath = countpath+'_{}'.format(gene_subset)
        else:
            countpath = countpath
        paths.append(countpath)
    return(paths)

def get_metadata(conn, allgenlist, sampleinfo_table, rnaset, gene_subset):
    '''Gets metadata for use in writing a metadata file with write_metadata().
    Inputs:
    conn = connection to database using psycopg2
    allgenlist = list of all genotypes (e.g., CS_F), experimental and controls
    sample_infotable = table in the database that contains info about the 
    genotypes (usually autin)
    rnaset: object of class RNASeqData in the rnaseq_settings module
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
    paths = get_count_paths(rnaset, berkids, gene_subset)
    #for i, b in enumerate(berkids):
        #print(b, paths[i])
    return(zip(berkids, samples, paths))
   

def write_metadata(allgenlist, controllist, metadatafile, sampleinfo_table, 
        rnaset, gene_subset, tool):
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
    rnaset = object of class RNASeqData in the rnaseq_settings module
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    ''' 
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    items = get_metadata(conn, allgenlist, sampleinfo_table, rnaset, gene_subset) 
    with open(metadatafile, 'w') as f:
        if tool == 'edger':
            f.write('Sample\tBerkid\tCorE\tHTSeqPath\n')
        elif tool == 'deseq':
            f.write('Sample\tHTSeqPath\tCorE\n')
        for berkid, sample, path in items:
            if os.path.exists(path):
                if sample[:-1] in controllist:
                    core = 'ctrl'
                else:
                    core = 'expt'
                if tool == 'edger':
                    f.write('{}\t{}\t{}\t{}\n'.format(sample, berkid, core, path))
                elif tool == 'deseq':
                    f.write('{}\t{}\t{}\n'.format(sample, path, core))
    conn.close()



def write_groups(groups, groupinfofile):
    '''Writes a file (groupinfofile) that lists the groups being compared; the
    experimental group is on the first line and the control group is on the
    second line.
    Input:
    groups = list or dictionary specifying groups
    groupinfofile = output file name
    '''

    if type(groups) == list:
        group1 = groups[0]
        group2 = groups[1]
    elif type(groups) == dict:
        for k in groups.keys():
            if 'ctrl' in k:
                group2 = k
            else:
                group1 = k

    with open(groupinfofile, 'w') as g:
        g.write('{}\n{}'.format(group1, group2))

def pairwise_DE(expt, ctrl, rnaset, gene_subset, de_file_dict, tool):
    '''Runs edgeR comparing expt and control genotypes. Writes a metadata file
    and calls the edgeR.R script.  
    Input:
    exptlist = list of genotypes that will be compared against control
    ctrl = length-1 list containing control genotype
    edger_dirpath = path to edger directory
    metadatafile = name of the metadata file that will be written
    sample_infotable = string specifying table in the database that contains
        info about the genotypes (usually autin)
    rnaset: object of class RNASeqData in the rnaseq_settings module
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    de_file_dict = dictionary containing the file names for the plots and 
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
        data output by edgeR.R
    '''
    
    de_dirpath = de_file_dict['{}_dirpath'.format(tool)] 
    metadatafile = de_file_dict['{}_metadata_file'.format(tool)]
    sampleinfo_table = de_file_dict['sampleinfo_table']
    groupinfofile = de_file_dict['{}_group_file'.format(tool)]

    deresdir = os.path.join(de_dirpath, gene_subset)
    cmn.makenewdir(deresdir)
    os.chdir(deresdir)
    condlist = [expt, ctrl]
    logging.info("%s", condlist)
    cmn.makenewdir(expt)
    os.chdir(expt)
    write_metadata(condlist, ctrl, metadatafile, sampleinfo_table, 
            rnaset, gene_subset, tool)
    write_groups(condlist, groupinfofile)
    run_descript(de_file_dict, tool)


def batch_pairwise_DE(exptlist, ctrl, rnaset, gene_subset, de_file_dict, tool):
    '''Runs edgeR for each genotype given in exptlist against the control
    given in ctrl. Writes a metadata file and calls the edgeR.R script.
    Input:
    exptlist = list of genotypes that will be compared against control
    ctrl = length-1 list containing control genotype
    edger_dirpath = path to edger directory containing all the results
    metadatafile = name of the metadata file that will be written
    sample_infotable = string specifying table in the database that contains
        info about the genotypes (usually autin)
    rnaset = object of class RNASeqData in the rnaseq_settings module
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    de_file_dict = dictionary containing the file names for the plots and 
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
        data output by edgeR.R
    '''
    for cond in exptlist:
        pairwise_DE(cond, ctrl, rnaset, gene_subset, de_file_dict, tool)



def run2groups_DE(exptdict, rnaset, gene_subset, de_file_dict, tool):
    '''Runs edgeR to find DE genes between two groups of samples.
    Input:
    exptdict = dictionary where the keys are the groups to be compared
        and the values are the list of genotypes for each group. One key is
        'ctrl' and specifies the control genotypes. 
    rnaset = object of class RNASeqData in the rnaseq_settings module
    gene_subset = string specifying the subset of genes that will be analyzed
        (e.g., prot_coding_genes, bwa_r557)
    de_file_dict = dictionary containing the file names for the plots and 
        data output by edgeR.R
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
    '''

    for k,v in exptdict.items():
        logging.info("%s,%s", k,v)
        if 'ctrl' in k:
            ctrllist = v
            ctrlname = k
        else:
            exptlist = v
            exptname = k
    allgenlist = exptlist + ctrllist
    #print('allgenlist', allgenlist)
    #print('ctrllist', ctrllist)
    
    de_dirpath = de_file_dict['{}_dirpath'.format(tool)] 
    metadatafile = de_file_dict['{}_metadata_file'.format(tool)]
    sampleinfo_table = de_file_dict['sampleinfo_table']
    groupinfofile = de_file_dict['{}_group_file'.format(tool)]

    deresdir = os.path.join(de_dirpath, gene_subset)
    cmn.makenewdir(deresdir)
    os.chdir(deresdir)
    cmn.makenewdir(exptname)
    os.chdir(exptname)

    write_metadata(allgenlist, ctrllist, metadatafile, sampleinfo_table, 
            rnaset, gene_subset, tool)
    write_groups(exptdict, groupinfofile)
    run_descript(de_file_dict, tool)


def run_descript(de_file_dict, tool):
    '''Runs edgeR using the script edgeR.R or deseq using the script deseq.R. 
    Input is a dictionary containing
    the file names for the plots and data output by edgeR.R
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
    '''
    d = de_file_dict
    if tool == 'edger':
        cmd = 'Rscript ~/Documents/lab/code/rnaseq_analysis/edgeR.R {0} {1} {2} {3} {4} {5} > edgeR.log 2>&1'.format(d['edger_mdsplot_file'], 
                d['edger_mvplot_file'], d['edger_bcvplot_file'], 
                d['edger_maplot_file'], d['edger_toptags_file'],
                d['edger_toptags_fdr_file'])
    elif tool == 'deseq':
        cmd = 'Rscript ~/Documents/lab/code/rnaseq_analysis/deseq.R > deseq.log 2>&1'
    logging.debug(cmd)
    os.system(cmd)

def gen_de_dict(sample_list, degenedir, degenefile):
    degenes = {}
    for sample in sample_list:
        os.chdir(os.path.join(degenedir, sample))
        with open(degenefile, 'r') as f:
            degenes[sample] = f.read().split('\n')[:-1]
    return(degenes)

def gen_db_degenefile(degenefile, db_degenefile, tool, gene_subset, group1, 
        group2, delim=','):
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
                g.write('{1}{0}{2}{0}{3}{0}{4}{0}{5}\n'.format(delim, 
                    l.rstrip('\n'), tool, gene_subset, group1, group2))

def batch_makecopy_db_degenefile(de_file_dict, tool, gene_subset, conn):
    '''Batch function for rewriting DE analysis output files for inclusion
    in the database.
    Input:
    de_file_dict = dictionary containing the file names for the DE directories
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
    gene_subset = subset of genes analyzed
    conn = open connection to database using psycopg2
    degenetable = name of table in the database that will hold de gene data
    '''
    
    de_resdir = os.path.join(de_file_dict['{}_dirpath'.format(tool)], gene_subset)
    groupfile = de_file_dict['{}_group_file'.format(tool)]
    degenefile = de_file_dict['{}_toptags_file'.format(tool)]
    db_degenefile = de_file_dict['{}_dbtoptags_file'.format(tool)]
    degenetable = de_file_dict['degene_table']

    os.chdir(de_resdir)
    logging.info('Copying DE files for database')
    for rd in [os.path.abspath(x) for x in sorted(glob.glob('*/'))]:
        logging.info(os.path.basename(rd))
        os.chdir(rd)
        if os.path.exists(groupfile):
            with open(groupfile, 'r') as f:
                group1 = next(f).rstrip('\n')
                group2 = next(f).rstrip('\n')
            gen_db_degenefile(degenefile, db_degenefile, tool, gene_subset,
                    group1, group2)
            cur = conn.cursor()
            rl.copy_degenes_dbtable(db_degenefile, degenetable, cur) 
            cur.close()
            conn.commit()

        else:
            logging.info('No groups file')


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
        logging.info("%s", os.path.basename(resdir))
        cur = conn.cursor()
        if os.path.exists(db_degenefile):
            with open(db_degenefile, 'r') as f:
                group1, group2 = next(f).rstrip('\n').split(',')[-2:]
            cmd = gen_dbgene_copyfrom_cmd(table, group1, group2, fdr_th)
            logging.info(cmd)
            copy_dbgenes_from_db(cur, out_degenefile, cmd)
            with open(out_degenefile, 'r') as f:
                if not list(f):
                    print('empty file')
            cur.close()
        else:
            cur.close()
            conn.commit()
            print('No db_degenfile exists')


def gen_hh_cmd(degenetable, fdr_th, gene_subset, group1, group2, tool, gff_file):
    cmd = "select distinct hom.fly_sym, hom.human_sym, final.logfc, hom.weighted_score, hom.prediction_db from ( select hp.fly_sym, hid.logfc from (select de.gene as gene, gff.fbgn_id as fbgn_id, de.logfc as logfc from {0} as de inner join gff_genes as gff on (de.gene = gff.name_name) where de.fdr < {1} and de.gene_subset = '{2}' and de.group1 = '{3}' and de.group2 = '{4}' and de.tool = '{5}' and gff.gff_file = '{6}') as hid inner join homolog_pfbgns as hp on (hp.pfbgn = hid.fbgn_id)) as final inner join homologs as hom on (final.fly_sym = hom.fly_sym) order by final.logfc desc".format(degenetable, fdr_th, gene_subset, group1, group2, tool, gff_file)
    return(cmd)


def get_human_homologs(degenetable, fdr_th, gene_subset, group1, group2, tool, gff_file, cur):
    selcmd = gen_hh_cmd(degenetable, fdr_th, gene_subset, group1, group2, tool, gff_file, cur)
    cur.execute(selcmd + ';')
    human_homs = cur.fetchall()
    return(human_homs)

def write_human_homologs(hhfile, degenetable, fdr_th, gene_subset, group1, group2, tool, gff_file, cur):

    selcmd = gen_hh_cmd(degenetable, fdr_th, gene_subset, group1, group2, tool, gff_file)
    copycmd = "COPY ({0}) to STDOUT;".format(selcmd)
    
    with open(hhfile, 'w') as f:
        cur.copy_expert(copycmd, f)


def batch_write_human_homologs(de_file_dict, fdr_th, tool, gene_subset, gff_file, conn):
    '''Batch function for rewriting DE analysis output files for inclusion
    in the database.
    Input:
    de_file_dict = dictionary containing the file names for the DE directories
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
    gene_subset = subset of genes analyzed
    conn = open connection to database using psycopg2
    degenetable = name of table in the database that will hold de gene data
    '''
    
    de_resdir = os.path.join(de_file_dict['analysis_path'], tool, gene_subset)
    groupfile = de_file_dict['{}_group_file'.format(tool)]
    degenetable = de_file_dict['degene_table']
    hhfile = "{}{}_{}.txt".format(de_file_dict['de_hh_file'], tool, fdr_th)

    os.chdir(de_resdir)
    logging.info('Writing human homologs')
    for rd in [os.path.abspath(x) for x in sorted(glob.glob('*/'))]:
        #logging.info(os.path.basename(rd))
        print(os.path.basename(rd))
        os.chdir(rd)
        if os.path.exists(groupfile):
            with open(groupfile, 'r') as f:
                group1 = next(f).rstrip('\n')
                group2 = next(f).rstrip('\n')
            cur = conn.cursor()
            write_human_homologs(hhfile, degenetable, fdr_th, gene_subset,
                    group1, group2, tool, gff_file, cur) 
            cur.close()
            conn.commit()
        else:
            print('No group file exists')

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


def custom_DE(de_file_dict, tool):
    '''Runs analysis to find DE genes between two groups of samples. Metadata
    file and groups file are manually created.
    Input:
    tool = software used (e.g., edger or deseq)
    de_file_dict = dictionary containing the file names for the plots and 
        data output by edgeR.R
    '''
    run_descript(de_file_dict, tool)
