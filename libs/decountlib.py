import libs.htseqlib as hl
import libs.rnaseqlib as rl
import libs.delib as dl
import logging
import os
import psycopg2
import rnaseq_settings as rs 
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.spatial
import scipy.cluster

#def get_gene_info(cur, gene, grouplist, ctrllist, sex, htseqtable, detable, tool, 
        #genesubset, toprint='no'):
    #'''For each group in degroups, gets the number of counts for the given gene.
    #'''
    #if sex == 'F':
        #groups = degroups.females 
        #ctrl = ['CS_F']
    #elif sex == 'M':
        #groups = degroups.males 
        #ctrl = ['CS_M']

    #d_repcounts = hl.compare_replicate_counts(cur, 
            #groups + ctrl, gene, sampleinfo_table='autin', 
            #htseqtable=htseqtable)
    #d_derep = dl.compare_replicate_de(cur, groups, ctrl[0],
         #gene, detable, tool, genesubset)
    #allinfo,alllist = get_rep_counts_de(d_repcounts, d_derep)
    #if toprint == 'yes':
        #for i in allinfo:
            #logging.info(i)
    #return(allinfo, alllist)

#def write_decount_info(cur, outfile, align, fdr, sex, tool, genesubset, gff_file,
        #degroups, minfdr):

    #htseqtable = 'htseq_'+align
    #detable = 'degenes_'+align

    #if fdr == 0.10 or fdr == .10:
        #sfdr = '10'
    #decounttable = 'decount{}_{}_{}_fdr{}_{}'.format(sex, genesubset, tool, 
            #sfdr, align)

    #entries = get_decount(cur, decounttable, gff_file) 
    #with open(outfile, 'w') as g:
        #g.write('FDR = {}, Gene subset = {}, Tool = {}, Release = {}\n'.format(sfdr, genesubset, tool, gff_file))
        #for entry in entries:
            #g.write('\n{}\t{}\t{}\t{}\n'.format(*entry))
            #gene = entry[2]
            #g.write('Genotype\thtseq counts\tFold change\tFDR\n')
            #slist, ilist = get_gene_info(cur, gene, groups, sex,
                   #htseqtable, detable, tool, genesubset)
            #for i, ps in enumerate(slist):
                #if minfdr:
                    #if ilist[i][-1] < fdr:
                        #g.write(ps)
                #else:
                    #g.write(ps)

def write_sql_decount(cmdfile, degroups, fdr, decounttable, genesubset, tool,
        gff_file):
    with open(cmdfile, 'w') as h:
        for g in degroups:
            cmd = (" \copy ( "
            "select * from "
            "find_decount('{0}', '{2}', '{4}', '{3}', {1}, '{5}')) "
            "to '{}' "
            "header csv;\n").format(g, fdr, decounttable, genesubset, tool, 
                   gff_file)
            h.write(cmd)

def print_rep_counts(d_repcounts):
    for k in sorted(d_repcounts.keys()):
        vcounts = [x[1] for x in d_repcounts[k]]
        ps = '{}\t{}'.format(k, vcounts)
        print(ps)

def print_compare_replicate(d_derep):
    for k in sorted(d_derep.keys()):
        v = d_derep[k]
        ps = '{}\t{:.3f}\t{:.3f}'.format(k, v[1], v[2])
        print(ps)
        
def get_rep_counts_de(d_repcounts, d_derep):
    pslist = []
    itemlist = []
    for k in sorted(d_repcounts.keys()):
        vcounts = [x[1] for x in d_repcounts[k]]
        if k=='CS_F' or k=='CS_M':
            vde = [0,0,1]
        else:
            try:
                vde = d_derep[k]
            except KeyError:
                logging.info('%s Not in list', k)
                continue
        ps = '{}\t{}\t{:.3f}\t{:.3f}\n'.format(k, vcounts, vde[1], vde[2])
        pslist.append(ps)
        itemlist.append([k, vcounts, vde[1], vde[2]])
    return(pslist, itemlist)


def get_decount(cur, decounttable, gff_file):

    cmd = " select row_number, fbgn_id, gene, count from {} inner join gff_genes on (gene = name_name) where gff_file = '{}' order by count DESC ;".format(decounttable, gff_file)
    cur.execute(cmd)
    entries = cur.fetchall()
    return(entries)

        

def get_decount_for_clusters(cur, align, fdr, sex, tool, genesubset, gff_file,
        degroups, minfdr):

    htseqtable = 'htseq_'+align
    detable = 'degenes_'+align

    if fdr == 0.10 or fdr == .10:
        sfdr = '10'
    decounttable = 'decount{}_{}_{}_fdr{}_{}'.format(sex, genesubset, tool, 
            sfdr, align)

    entries = get_decount(cur, decounttable, gff_file) 
    genes = []
    foldchanges = []
    for entry in entries:
        gene = entry[2]
        genes.append(gene)

        slist, ilist = get_gene_info(cur, gene, degroups,
                htseqtable, detable, tool, genesubset, sex)
        genefc = []
        genotypes = []
        for i, val in enumerate(ilist):
            genotype, vcounts, gfc, gfdr = val
            genotypes.append(genotype)
            if minfdr:
                if gfdr < fdr:
                    genefc.append(gfc)
                else:
                    genefc.append(1)
        foldchanges.append(genefc)
    return(genotypes, genes, foldchanges)

def plot_declusters(genotypes, genes, foldchanges):
    
    genotypes = np.array(genotypes)
    foldchanges = np.transpose(np.array(foldchanges))
    print(np.shape(foldchanges))
    print(np.shape(genotypes))
    dist_fc = scipy.spatial.distance.pdist(foldchanges, 'euclidean')
    avg_cluster = scipy.cluster.hierarchy.average(dist_fc)
    plt.figure(figsize=[70,40])
    dend = scipy.cluster.hierarchy.dendrogram(avg_cluster, labels=genotypes, leaf_rotation=90)
    plt.savefig('males_cluster_by_foldchange.png')

#def get_decvlist(cur, align, fdr, sex, tool, genesubset, gff_file,
        #degroups):

    #htseqtable = 'htseq_'+align
    #detable = 'degenes_'+align

    #if fdr == 0.10 or fdr == .10:
        #sfdr = '10'
    #decounttable = 'decount{}_{}_{}_fdr{}_{}'.format(sex, genesubset, tool, 
            #sfdr, align)
    #entries = get_decount(cur, decounttable, gff_file) 

    #cvlist = []
    #for entry in entries:
        #gene = entry[2]
        #ilist = get_gene_info(cur, gene, degroups,
                #htseqtable, detable, tool, genesubset, sex)[1]
        
        #genfc = []

        #for i in ilist:
            #genotype, vcounts, gfc, gfdr = i
            #if gfdr < fdr:
                #genfc.append(gfc)

        #mgfc = np.mean(genfc)
        #sgfc = np.std(genfc)
        #cv_gfc = sgfc/mgfc
        #if cv_gfc > 0:
            #cvlist.append((cv_gfc, gene))
    #cvlist = sorted(cvlist)
    #cvlist.reverse()
    #return(cvlist)
    ##print(cvlist[:top])
    ##print(genes[:top])

#def write_decount_cv(cvlist, outfile, topnum, cur, align, degroups, tool, genesubset,
        #sex, fdr, minfdr):

    #cvs, genes = zip(*cvlist)
    #top = int(len(cvlist)/(100/topnum))
    #topcvlist = cvlist[:top]
    ##print(outfile)
    #with open(outfile, 'w') as h:
        #for g in genes[:top]:
            #h.write('{}\n'.format(g))
            #h.write('Genotype\thtseq counts\tFold change\tFDR\n')
            #write_gene_count(h, g, cur, degroups, align, tool, genesubset, 
                    #sex, fdr, minfdr)
            #h.write('\n')

#def write_gene_count(openfile, gene, cur, degroups, align, tool, genesubset, 
        #sex, fdr, minfdr):

    #htseqtable = 'htseq_'+align
    #detable = 'degenes_'+align

    #slist, ilist = get_gene_info(cur, gene, degroups,
            #htseqtable, detable, tool, genesubset, sex)
    #for i, ps in enumerate(slist):
        #if minfdr:
            #genotype = ilist[i][0]
            #if ilist[i][-1] < fdr: 
                #openfile.write(ps)
            #elif genotype == 'CS_F' or genotype == 'CS_M':
                #openfile.write(ps)
        #else:
            #openfile.write(ps)
       

def cmd_create_decount(viewname, detable, tool, gene_subset, fdr, sex):
    '''SQL command for generating decount tables.
    '''
    cmd_create = ("create or replace view {} as ("
                "select row_number() OVER (ORDER BY count (*) DESC), "
                "gene, count (*) from {} " 
                "where tool = '{}' and gene_subset = '{}' "
                "and fdr < {} "
                "and group1 ~ '.._{}' "
                "group by gene "
                "order by count (*) DESC)"
                ";").format(viewname, detable, tool, gene_subset, fdr, sex)
    return(cmd_create)


def cmd_decount_samples_mf(decount_table1, decount_table2, degenes_table,
        gff_table, defdr, tool, gff_file, gene_subset):
    '''SQL command for writing a file with joined male and female decount table
    '''
    cmd_get = \
    (" COPY (select gene, g.fbgn_id, "
    "avg(coalesce(df.count,0)) as avg_f, avg(coalesce(dm.count, 0)) as avg_m, "
    "avg(coalesce(df.count, 0) + coalesce(dm.count, 0)) as avg_mf, "
    "array_agg(group1) "
    "from {} as df "
    "full outer join "
    "{} as dm "
    "using (gene) "
    "inner join "
    "{} as d "
    "using (gene) "
    "inner join  "
    "{} as g "
    "on (gene = g.name_name) "
    "where d.fdr < {} and d.tool = '{}' "
    "and g.gff_file = '{}' "
    "and (group2 = 'CS_M' or group2 = 'CS_F') "
    "and d.gene_subset = '{}' "
    "group by gene, g.fbgn_id "
    "order by avg_mf DESC)"
    "TO STDOUT CSV HEADER;").format(decount_table1, decount_table2, degenes_table,
            gff_table, defdr, tool, gff_file, gene_subset)
    logging.debug('Command for joined male/female table: %s', cmd_get)
    return(cmd_get)

# For a given fdr, gene subset, tool, alignment, get output files.

def create_decount_tables(conn, rnaset, tool, fdr):
    '''Create decount tables'''
    cmd_decountf = cmd_create_decount(rnaset.decount_table_female, rnaset.degene_table,
            tool, rnaset.genesubset, fdr, 'F')
    cmd_decountm = cmd_create_decount(rnaset.decount_table_male, rnaset.degene_table,
            tool, rnaset.genesubset, fdr, 'M')
    loggin.debug('Command for creatiing decount tables: %s') 

    cur = conn.cursor()
    cur.execute(cmd_decountf)
    cur.execute(cmd_decountm)
    cur.close()
    conn.commit()


def write_decount_samples_mf(conn, rnaset, tool, fdr):
    '''Writes a file with joined male and female decount table data''' 
    cur = conn.cursor()
    cmd_get = cmd_decount_samples_mf(rnaset.decount_table_female, 
            rnaset.decount_table_male, rnaset.degene_table, rnaset.gff_table,
            fdr, tool, rnaset.gff_file, rnaset.genesubset)
    outfile = '{}_{}_{}_{}.csv'.format(rnaset.decount_mf_base, rnaset.genesubset,
            tool, fdr)
    outpath = os.path.join(rnaset.decount_dirpath, outfile)
    with open(outpath, 'w') as g:
        cur.copy_expert(cmd_get, g)
    cur.close()

def cmd_group_decount(group, decounttable, degenetable, genesubset, 
        tool, fdr, gff_file):
    '''Command for writing a file with the count number for each gene 
    for each genotype.'''

    cmd = (" copy ( "
    "select * from "
    "find_decount('{}', '{}', '{}', '{}', '{}', {}, '{}')) "
    "to stdout "
    "header csv;\n").format(group, decounttable, degenetable, genesubset, 
            tool, fdr, gff_file)
    logging.info('Command for getting decount info for a genotype: %s')
    return(cmd)

def write_group_decount(conn, exptlist, rnaset, fdr, tool):
    '''For each experiment in exptlist, writes a file with the count number
    for each gene.'''

    for e in exptlist:
        os.chdir(e)
        group = os.path.basename(e)
        sex = group.split('_')[1]
        if sex == 'F':
            decount_table = rnaset.decount_table_female
        elif sex == 'M':
            decount_table = rnaset.decount_table_male
        cmd = cmd_group_decount(group, decount_table, rnaset.degene_table, 
                rnaset.genesubset, tool, fdr, rnaset.gff_file)
        cur = conn.cursor()
        outfile = 'counts_{}{:.2f}_gene'.format(rnaset.edger_toptags_fdr_file, 
                fdr)
        with open(outfile, 'w') as g:
            cur.copy_expert(cmd, g)
        cur.close()
     
def get_gene_counts(cur, gene, grouplist, ctrllist, sampleinfo_table, 
        htseqtable, detable, tool, genesubset, toprint='no'):
    '''For each group in degroups, gets the number of counts for the given gene.
    '''
    d_repcounts = hl.compare_replicate_counts(cur, 
            grouplist + ctrllist, gene, sampleinfo_table, 
            htseqtable)
    d_derep = dl.compare_replicate_de(cur, grouplist, ctrllist[0],
         gene, detable, tool, genesubset)
    allinfo,alllist = get_rep_counts_de(d_repcounts, d_derep)
    if toprint == 'yes':
        for i in allinfo:
            print(i)
    return(allinfo, alllist)


def write_decount_gene_counts(conn, rnaset, degroups, sex, fdr, tool, minfdr):
    '''Writes a new file (outfile) with the htseq-count data for each gene 
    selected as DE, sorted by the number of samples that the gene was DE in.
    '''
    if sex == 'F':
        grouplist = degroups.females
        ctrllist = [degroups.females_ctrl]
        outfile = '{}_{}_{}_{}.txt'.format(rnaset.decount_info_f, 
                rnaset.genesubset, tool, fdr)
        decounttable = rnaset.decount_table_female
    if sex == 'M':
        grouplist = degroups.males
        ctrllist = [degroups.males_ctrl]
        outfile = '{}_{}_{}_{}.txt'.format(rnaset.decount_info_m, 
                rnaset.genesubset, tool, fdr)
        decounttable = rnaset.decount_table_male

    cur = conn.cursor()
    entries = get_decount(cur, decounttable, rnaset.gff_file) 
    print(outfile)
    with open(outfile, 'w') as g:
        g.write(("FDR = {}, Gene subset = {}, Tool = {}, "
                "Release = {}\n").format(fdr, rnaset.genesubset, tool, 
                    rnaset.gff_file))
        for entry in entries:
            g.write('Genotype\thtseq counts\tFold change\tFDR\n')
            g.write('Rownum\tFBgn\tGene\t# samples\n')
            g.write('\n{}\t{}\t{}\t{}\n'.format(*entry))
            gene = entry[2]
            slist, ilist = get_gene_counts(cur, gene, grouplist, ctrllist, 
                    rnaset.sampleinfo_table, rnaset.htseq_table, 
                    rnaset.degene_table, tool, rnaset.genesubset)
            for i, ps in enumerate(slist):
                if minfdr:
                    if ilist[i][-1] < fdr:
                        g.write(ps)
                else:
                    g.write(ps)
    cur.close()

def get_decvlist(cur, grouplist, ctrllist, sampleinfo_table, htseqtable,
        detable, decounttable, fdr, tool, genesubset, gff_file):
    '''Finds the coefficient of variation of the fold change for each
    gene considered DE.
    '''

    entries = get_decount(cur, decounttable, gff_file) 

    cvlist = []
    for entry in entries:
        gene = entry[2]

        ilist = get_gene_counts(cur, gene, grouplist, ctrllist, sampleinfo_table, 
            htseqtable, detable, tool, genesubset, toprint='no')[1]
        
        genfc = []
        for i in ilist:
            genotype, vcounts, gfc, gfdr = i
            if gfdr < fdr:
                genfc.append(gfc)

        mgfc = np.mean(genfc)
        sgfc = np.std(genfc)
        cv_gfc = sgfc/mgfc
        if cv_gfc > 0:
            cvlist.append((cv_gfc, gene))
    cvlist = sorted(cvlist)
    cvlist.reverse()
    return(cvlist)
    #print(cvlist[:top])
    #print(genes[:top])


def write_decount_fc_cv(conn, rnaset, degroups, sex, fdr, tool, minfdr):

    if sex == 'F':
        grouplist = degroups.females
        ctrllist = [degroups.females_ctrl]
        outfile = '{}_{}_{}_{}.txt'.format(rnaset.decount_fccv_f, 
                rnaset.genesubset, tool, fdr)
        decounttable = rnaset.decount_table_female

    if sex == 'M':
        grouplist = degroups.males
        ctrllist = [degroups.males_ctrl]
        outfile = '{}_{}_{}_{}.txt'.format(rnaset.decount_fccv_m, 
                rnaset.genesubset, tool, fdr)
        decounttable = rnaset.decount_table_male

    cur = conn.cursor()
    topnum = rnaset.decount_top
    cvlist = get_decvlist(cur, grouplist, ctrllist, rnaset.sampleinfo_table, 
            rnaset.htseq_table, rnaset.degene_table, decounttable, 
            fdr, tool, rnaset.genesubset, rnaset.gff_file)

    cvs, genes = zip(*cvlist)
    top = int(len(cvlist)/(100/topnum))
    topcvlist = cvlist[:top]
    with open(outfile, 'w') as h:
        h.write(("FDR = {}, Gene subset = {}, Tool = {},"
                "Release = {}\n\n").format(fdr, rnaset.genesubset, tool, 
                    rnaset.gff_file))

        for cv, gene in cvlist[:top]:
            h.write('Gene\tCV of fold change\n')
            h.write('{}\t{:.4f}\n'.format(gene, cv))
            h.write('Genotype\thtseq counts\tFold change\tFDR\n')

            slist, ilist = get_gene_counts(cur, gene, grouplist, ctrllist, 
                    rnaset.sampleinfo_table, rnaset.htseq_table, 
                    rnaset.degene_table, tool, rnaset.genesubset)
            for i, ps in enumerate(slist):
                if minfdr:
                    if ilist[i][-1] < fdr:
                        h.write(ps)
                else:
                    h.write(ps)
            h.write('\n')
    cur.close()

def main():
#write_sql_countf(SQLCMDFILE, DEGROUPS.females, 0.10, 'decountf', GENESUBSET, 'edger')
#write_sql_countf(SQLCMDFILE, DEGROUPS.males, 0.10, 'decountm', GENESUBSET, 'edger')
#print(hl.get_gene_count(cur, htseqtable, gene, berkid))
#print(hl.get_counts(cur=cur, genotype='NrxIV_M', gene='klu', 
    #sampleinfo_table='autin', htseqtable=htseqtable))

    #genesubset = sys.argv[1]
    #gene = sys.argv[2]
    align = '2str'
    genesubset = 'prot_coding_genes'

    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    rnaset = rs.RNASeqData(alignment=align, 
            genesubset=genesubset)
    degroups = rs.DEGroups()
    htseqtable = 'htseq_2str'
    edger_dirpath = os.path.join(rnaset.edger_dirpath, genesubset)

    berkid = 'RGAM009A'
    group1 = 'NrxIV_M'
    group2 = 'CS_M'
    detable = 'degenes_2str'
    tool = 'edger'
    gff_file = 'dmel-all-filtered-r5.57.gff'
    decounttable = 'decountf_pcg_edger_fdr10_2str'
    fdr = .10

    sex = 'M'
    minfdr = True
    cur = conn.cursor()
    

    #print(gene)

    #x = get_gene_info(cur=cur, gene='klu', degroups=degroups, 
        #htseqtable=htseqtable, 
        #detable='degenes_2str',
        #tool='edger', genesubset='prot_coding_genes', sex='F', toprint='no')
    #print(x)
    #print(len(x))
    
    #write_decount(cur=cur, outfile='decountf_fdr10_fbgns_info_minfdr', align=align, 
        #fdr=fdr, sex='F', tool=tool, genesubset=genesubset, gff_file=gff_file,
        #degroups=degroups, minfdr=True)
    #get_decount_cv(cur=cur, outfile='decountf_fdr10_fbgns_info_minfdr', align=align, 
        #fdr=fdr, sex='F', tool=tool, genesubset=genesubset, gff_file=gff_file,
        #degroups=degroups, minfdr=True)

    #outfile='decountf_fdr10_fbgns_info_minfdr_top20percentcv' 
    #cvlist = get_decvlist(cur=cur, align=align, fdr=fdr, sex=sex, tool=tool,
            #genesubset=genesubset, gff_file=gff_file, degroups=degroups)
    #write_decount_cv(cvlist=cvlist, outfile=outfile, topnum=20, cur=cur, 
            #align=align, degroups=degroups, tool=tool, genesubset=genesubset, sex=sex,
            #fdr=fdr, minfdr=True)

    #gene = 'CG4928'
    #get_gene_info(cur, gene, degroups, htseqtable, detable, tool, 
        #genesubset, sex, toprint='yes')

    genotypes, genes, foldchanges = (get_decount_for_clusters(cur, align, fdr, sex, tool, genesubset, gff_file, degroups, minfdr))
    plot_declusters(genotypes, genes, foldchanges)
    #get_decount(cur, decounttable, gff_file)

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
def get_gene_info(cur, gene, grouplist, ctrllist, sex, htseqtable, detable, tool, 
        genesubset, toprint='no'):
    '''For each group in degroups, gets the number of counts for the given gene.
    '''
    if sex == 'F':
        groups = degroups.females 
        ctrl = ['CS_F']
    elif sex == 'M':
        groups = degroups.males 
        ctrl = ['CS_M']

    d_repcounts = hl.compare_replicate_counts(cur, 
            groups + ctrl, gene, sampleinfo_table='autin', 
            htseqtable=htseqtable)
    d_derep = dl.compare_replicate_de(cur, groups, ctrl[0],
         gene, detable, tool, genesubset)
    allinfo,alllist = get_rep_counts_de(d_repcounts, d_derep)
    if toprint == 'yes':
        for i in allinfo:
            logging.info(i)
    return(allinfo, alllist)

def write_decount_info(cur, outfile, align, fdr, sex, tool, genesubset, gff_file,
        degroups, minfdr):

    htseqtable = 'htseq_'+align
    detable = 'degenes_'+align

    if fdr == 0.10 or fdr == .10:
        sfdr = '10'
    decounttable = 'decount{}_{}_{}_fdr{}_{}'.format(sex, genesubset, tool, 
            sfdr, align)

    entries = get_decount(cur, decounttable, gff_file) 
    with open(outfile, 'w') as g:
        g.write('FDR = {}, Gene subset = {}, Tool = {}, Release = {}\n'.format(sfdr, genesubset, tool, gff_file))
        for entry in entries:
            g.write('\n{}\t{}\t{}\t{}\n'.format(*entry))
            gene = entry[2]
            g.write('Genotype\thtseq counts\tFold change\tFDR\n')
            slist, ilist = get_gene_info(cur, gene, groups, sex,
                   htseqtable, detable, tool, genesubset)
            for i, ps in enumerate(slist):
                if minfdr:
                    if ilist[i][-1] < fdr:
                        g.write(ps)
                else:
                    g.write(ps)
