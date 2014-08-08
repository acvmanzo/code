import libs.htseqlib as hl
import libs.rnaseqlib as rl
import libs.delib as dl
import os
import psycopg2
import rnaseq_settings as rs 
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.spatial
import scipy.cluster


def write_sql_countf(cmdfile, degroups, fdr, decounttable, genesubset, tool):
    with open(cmdfile, 'w') as h:
        for g in degroups:
            cmd = " \copy ( select * from find_decount('{0}', '{2}', '{4}', '{3}', {1}, 'dmel-all-filtered-r5.57.gff') ) to '/home/andrea/Documents/lab/RNAseq/analysis/{4}/results_tophat_2str/{3}/{0}/{0}_toptags_edgeR_{1}_decount' header csv;\n".format(g, fdr, decounttable, genesubset, tool)
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
                print(k, 'Not in list')
                continue
        ps = '{}\t{}\t{:.3f}\t{:.3f}\n'.format(k, vcounts, vde[1], vde[2])
        pslist.append(ps)
        itemlist.append([k, vcounts, vde[1], vde[2]])
    return(pslist, itemlist)

def get_gene_info(cur, gene, degroups, htseqtable, detable, tool, 
        genesubset, sex, toprint='no'):
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
            print(i)
    return(allinfo, alllist)


def get_decount(cur, decounttable, gff_file):

    cmd = " select row_number, fbgn_id, gene, count from {} inner join gff_genes on (gene = name_name) where gff_file = '{}' order by count DESC ;".format(decounttable, gff_file)
    cur.execute(cmd)
    entries = cur.fetchall()
    return(entries)

def write_decount(cur, outfile, align, fdr, sex, tool, genesubset, gff_file,
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
            slist, ilist = get_gene_info(cur, gene, degroups,
                   htseqtable, detable, tool, genesubset, sex)
            for i, ps in enumerate(slist):
                if minfdr:
                    if ilist[i][-1] < fdr:
                        g.write(ps)
                else:
                    g.write(ps)
        

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

def get_decvlist(cur, align, fdr, sex, tool, genesubset, gff_file,
        degroups):

    htseqtable = 'htseq_'+align
    detable = 'degenes_'+align

    if fdr == 0.10 or fdr == .10:
        sfdr = '10'
    decounttable = 'decount{}_{}_{}_fdr{}_{}'.format(sex, genesubset, tool, 
            sfdr, align)
    entries = get_decount(cur, decounttable, gff_file) 

    cvlist = []
    for entry in entries:
        gene = entry[2]
        ilist = get_gene_info(cur, gene, degroups,
                htseqtable, detable, tool, genesubset, sex)[1]
        
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

def write_decount_cv(cvlist, outfile, topnum, cur, align, degroups, tool, genesubset,
        sex, fdr, minfdr):

    cvs, genes = zip(*cvlist)
    top = int(len(cvlist)/(100/topnum))
    topcvlist = cvlist[:top]
    print(outfile)
    with open(outfile, 'w') as h:
        for g in genes[:top]:
            h.write('{}\n'.format(g))
            h.write('Genotype\thtseq counts\tFold change\tFDR\n')
            write_gene_count(h, g, cur, degroups, align, tool, genesubset, 
                    sex, fdr, minfdr)
            h.write('\n')

def write_gene_count(openfile, gene, cur, degroups, align, tool, genesubset, 
        sex, fdr, minfdr):

    htseqtable = 'htseq_'+align
    detable = 'degenes_'+align

    slist, ilist = get_gene_info(cur, gene, degroups,
            htseqtable, detable, tool, genesubset, sex)
    for i, ps in enumerate(slist):
        if minfdr:
            genotype = ilist[i][0]
            if ilist[i][-1] < fdr: 
                openfile.write(ps)
            elif genotype == 'CS_F' or genotype == 'CS_M':
                openfile.write(ps)
        else:
            openfile.write(ps)
       




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
