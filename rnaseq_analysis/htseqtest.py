#Functions useful for preparing files for analysis using htseq.


import os

def add_berkid(berkid, fpkm_path, berkid_fpkm_path):
    '''adds the berkid to the last columns of an
    fpkm file output by cufflinks.
    '''
    with open(berkid_fpkm_path, 'w') as g:
        with open(fpkm_path, 'r') as f:
            next(f)
            for l in f:
                newline = l.strip('\n') + '\t{0}\n'.format(berkid)
                g.write(newline) 

#berkid = 'RGSJ007D'
berkid = 'RGSJ006H'
fpkm_path = '/home/andrea/bookmarks/analysis/results_tophat/{}/tophat_out/htseq_results_edit.txt'.format(berkid)
new_fpkm_path = '/home/andrea/bookmarks/analysis/results_tophat/{}/tophat_out/htseq_results_edit_gene.txt'.format(berkid)
berkid_fpkm_path = '/home/andrea/bookmarks/analysis/results_tophat/{}/tophat_out/htseq_results_edit_gene_berkid.txt'.format(berkid)


#d = {}
#with open(fpkm_path, 'r') as f:
    #for l in f:
        #llist = l.strip('\n').split('\t')
        #gene = llist[0].split(':')[0]
        #if gene not in d:
            #d[gene] = 0
        #d[gene] = d[gene] + int(llist[1])


#with open(new_fpkm_path, 'w') as g:
    #g.write('gene\t{}\n'.format(berkid))
    #for gene, count in sorted(d.items()):
        #g.write('{}\t{}\n'.format(gene, count))
   

#add_berkid(berkid, new_fpkm_path, berkid_fpkm_path)
