import libs.htseqlib as hl
import libs.rnaseqlib as rl
import libs.delib as dl
import os
import psycopg2
import rnaseq_settings as rs 
import sys

genesubset = sys.argv[1]
gene = sys.argv[2]

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
        
def print_rep_counts_de(d_repcounts, d_derep):
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
        ps = '{}\t{}\t{:.3f}\t{:.3f}'.format(k, vcounts, vde[1], vde[2])
        print(ps)

#write_sql_countf(SQLCMDFILE, DEGROUPS.females, 0.10, 'decountf', GENESUBSET, 'edger')
#write_sql_countf(SQLCMDFILE, DEGROUPS.males, 0.10, 'decountm', GENESUBSET, 'edger')
#print(hl.get_gene_count(cur, htseqtable, gene, berkid))
#print(hl.get_counts(cur=cur, genotype='NrxIV_M', gene='klu', 
    #sampleinfo_table='autin', htseqtable=htseqtable))

def print_gene_info(cur, gene, degroups, htseqtable, detable, tool, genesubset):
    d_repcounts = hl.compare_replicate_counts(cur, 
            degroups.females + ['CS_F'], gene, sampleinfo_table='autin', 
            htseqtable=htseqtable)
    d_derep = dl.compare_replicate_de(cur, degroups.females, 
        'CS_F', gene, detable, tool, genesubset)
    print_rep_counts_de(d_repcounts, d_derep)

def main():
    align = '2str'
    #genesubset = 'prot_coding_genes'

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
    cur = conn.cursor()

    print(gene)
    print_gene_info(cur, gene, degroups, htseqtable, detable, tool, genesubset)

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
