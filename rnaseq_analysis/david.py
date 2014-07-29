import itertools
import libs.correlationlib as cl
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import glob
import psycopg2
import rnaseq_settings as rs 
import sys
import shutil

def batch_get_degenes(fbgnorname, genesubset, fdr, toptagfile):
    os.chdir(edger_dirpath)
    for item in degroups.males + degroups.females:
        os.chdir(os.path.join(edger_dirpath, item))
        print(os.getcwd())
        cur = conn.cursor()
        cmd = "COPY (select g.{} from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = '{}' and d.fdr < {} and gff_file = 'dmel-all-filtered-r5.57.gff' and group1 = '{}' order by fdr) TO STDOUT;".format(fbgnorname, 
                genesubset, fdr, item)
        ttfilename = '{}_{}_{:.2f}_{}'.format(item, toptagfile, fdr, fbgnorname.split('_')[0]) 
        print(ttfilename)
        with open(ttfilename, 'w') as g:
            cur.copy_expert(cmd, g)
        cur.close()

def rename_degene_file(toptagfile, newfile):
    os.chdir(edger_dirpath)
    for item in degroups.males + degroups.females:
        os.chdir(os.path.join(edger_dirpath, item))
        print(item)
        #newtoptagfile = '{}_{}'.format(item, toptagfile)
        oldtoptagfile = '{}_{}'.format(item, toptagfile)
        newtoptagfile = '{}_{}'.format(item, newfile)
        print(newtoptagfile)
        shutil.move(oldtoptagfile, newtoptagfile)

def remove_files(remfile):
    os.chdir(edger_dirpath)
    for item in degroups.males + degroups.females:
        os.chdir(os.path.join(edger_dirpath, item))
        print(os.getcwd())
        newremfile = '{}_{}'.format(item, remfile)
        print(newremfile)
        os.remove(newremfile)

def insert_fbgns(conn, fbgnlist):
    fbgnstring = ','.join(["('{}')".format(fbgn) for fbgn in fbgnlist])
    #print(fbgnstring)
    cmd = "DELETE FROM tempfbgns; INSERT INTO tempfbgns (fbgn) VALUES {};".format(fbgnstring)
    #print(cmd)
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()

def get_fbgnlist_geneclass(geneclassfile, groupnum):
    with open(geneclassfile, 'r') as f:
            #print(l.split('\t')[0])
        lines = itertools.takewhile(lambda x: x.split('\t')[0] != 'Gene Group {}'.format(groupnum+1), 
            itertools.dropwhile(lambda x: x.split('\t')[0] !='Gene Group {}'.format(groupnum), f))
        fbgnlist = []
        for l in lines:
            col1 = l.split('\t')[0]
            if 'FBgn' in col1 and len(col1) < 15:
                fbgnlist.append(col1)
            elif 'FBgn' in col1 and len(col1) < 15:
                mcol1 = col1.split(', ')
                fbgnlist.extend(mcol1)
        return(fbgnlist)

def get_fbgnlist_fncluster(fnclusterfile, groupnum):
    with open(fnclusterfile, 'r') as f:
            #print(l.split('\t')[0])
        lines = itertools.takewhile(lambda x: x.split('\t')[0] != 'Annotation Cluster {}'.format(groupnum+1), 
            itertools.dropwhile(lambda x: x.split('\t')[0] !='Annotation Cluster {}'.format(groupnum), f))
        #print(list(lines))
        runcount = 0
        fbgnlist = []
        numgenes = []
        for l in list(lines)[2:-1]:
            count = int(l.split('\t')[2])
            if count > runcount:
                fbgnlist = l.split('\t')[5].split(', ')
            runcount = count
        if fbgnlist:
            fbgnlist = [x.replace('GN', 'gn') for x in fbgnlist]
            return(fbgnlist)

def query_fbgn_list(conn, genotype):
    query = "select g.fbgn_id, g.name_name, d.logfc, 2^d.logfc, d.fdr \
    from tempfbgns as t \
    inner join \
    gff_genes as g \
    on (t.fbgn = g.fbgn_id) \
    inner join \
    degenes as d \
    on (d.gene = g.name_name) \
    where g.gff_file = 'dmel-all-filtered-r5.57.gff' \
    and d.tool = 'edger'  \
    and d.gene_subset = 'prot_coding_genes'  \
    and d.group1 = '{}' \
    order by @d.logfc DESC \
    ".format(genotype)
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return(results)

def write_query_results(restuple, gcinfofile):
    with open(gcinfofile, 'a') as g:
        g.write('fbgn\tname\tlog2fc\tfc\tfdr\n')
        fcs = []
        adjpvals = []
        for t in restuple:
            fc = t[3]
            adjpval = t[4]
            tstring = '{}\t{}\t{:.4f}\t{:.4f}\t{:.4g}\n'.format(*t)
            g.write(tstring)
            fcs.append(fc)
            adjpvals.append(adjpval)
        g.write('median fc {:.4f}\n'.format(np.median(fcs)))
        g.write('median adj pval {:.4f}\n\n'.format(np.median(adjpvals)))

def get_geneclass_de(conn, geneclassfile, geneclassnum, genotype, gcinfofile):
    fbgnlist = get_fbgnlist_geneclass(geneclassfile, geneclassnum)
    if fbgnlist:
        insert_fbgns(conn, fbgnlist)
        results = query_fbgn_list(conn, genotype)
        with open(gcinfofile, 'a') as g:
            g.write('Gene group {}\n'.format(geneclassnum))
        write_query_results(results, gcinfofile)

def get_fncluster_de(conn, fnclusterfile, classnum, genotype, fncinfofile):
    fbgnlist = get_fbgnlist_fncluster(fnclusterfile, classnum)
    if fbgnlist:
        insert_fbgns(conn, fbgnlist)
        results = query_fbgn_list(conn, genotype)
        with open(fncinfofile, 'a') as g:
            g.write('Functional annotation cluster {}\n'.format(classnum))
        write_query_results(results, fncinfofile)


ALIGN = '2str'
GENESUBSET = 'prot_coding_genes'
TOPTAGFILE = 'toptags_edgeR'
GENECLASSFILE = 'toptags_edgeR_0.10fbgn_geneclass'
FNCLUSTERFILE = 'toptags_edgeR_0.10fbgn_fncluster'

CONN = psycopg2.connect("dbname=rnaseq user=andrea")
RNASET = rs.RNASeqData(alignment=ALIGN, 
        genesubset=GENESUBSET)
DEGROUPS = rs.DEGroups()

EDGER_DIRPATH = os.path.join(RNASET.edger_dirpath, GENESUBSET)
#print(edger_dirpath)


#rename_degene_file(toptagfile)
#batch_get_degenes('name_name', genesubset, 0.1, toptagfile)
#remove_files('toptags_edgeR_0.1name')
#rename_degene_file('toptags_edgeR_0.10fbgn', 'toptags_edgeR_0.10_fbgn')

GCINFOFILE = 'toptags_edgeR_0.10fbgn_geneclass_deinfo.txt'
FNCINFOFILE = 'toptags_edgeR_0.10fbgn_fncluster_deinfo.txt'
GENOTYPE = os.path.basename(os.path.dirname(os.getcwd()))

def gen_info_files():
    if os.path.exists(GCINFOFILE):
        os.remove(GCINFOFILE)
    if os.path.exists(FNCINFOFILE):
        os.remove(FNCINFOFILE)
    for i in range(1,15):
        try:
            get_geneclass_de(CONN, GENECLASSFILE, i, GENOTYPE, GCINFOFILE)
        except FileNotFoundError:
            pass 
        get_fncluster_de(CONN, FNCLUSTERFILE, i, GENOTYPE, FNCINFOFILE)

def get_num_DAVID_IDs(edger_dirpath, degroups):
    os.chdir(edger_dirpath)
    for item in degroups.males + degroups.females:
        os.chdir(os.path.join(edger_dirpath, item))
        print(item)
        os.chdir('DAVID')
        os.system('cat toptags_edgeR_0.10fbgn_fntable | wc -l')
        os.system('cat toptags_edgeR_0.10fbgn_fntable.txt | wc -l')

def get_num_DAVID_fnclusters(edger_dirpath, degroups):
    os.chdir(edger_dirpath)
    for item in degroups.males + degroups.females:
        os.chdir(os.path.join(edger_dirpath, item))
        print(item)
        os.chdir('DAVID')

