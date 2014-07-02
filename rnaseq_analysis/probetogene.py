#Script to convert probe name to gene name from FlyAtlas data.
#Column names in PGFILE:
#Probe Set ID	GeneChip Array	Species Scientific Name	Annotation Date	Sequence Type	Sequence Source	Transcript ID(Array Design)	Target Description	Representative Public ID	Archival UniGene Cluster	UniGene ID	Genome Version	Alignments	Gene Title	Gene Symbol	Chromosomal Location	Unigene Cluster Type	Ensembl	Entrez Gene	SwissProt	EC	OMIM	RefSeq Protein ID	RefSeq Transcript ID	FlyBase	AGI	WormBase	MGI Name	RGD Name	SGD accession number	Gene Ontology Biological Process	Gene Ontology Cellular Component	Gene Ontology Molecular Function	Pathway	InterPro	Trans Membrane	QTL	Annotation Description	Annotation Transcript Cluster	Transcript Assignments	Annotation Notes

PGFILE = 'probset_to_gene2.txt'
DATAFILE = 'microarray_data.txt'
NEWFILE = 'microarray_fbgn_brain.txt'


#PGFILE = 'test_annot.txt'
#DATAFILE = 'test_microarray.txt'
#NEWFILE = 'test_annot_microarray.txt'

def probe_to_fbgn_gene():
    '''Combines the microarray (DATAFILE) and probe set annotation file 
    (PGFILE) so that each row in the NEWFILE contains the probe and gene/fbgn
    number. If a probe matches multiple genes/fbgns, one row is written for 
    each match. Also adds a column called 'Gene Source' for compatibility
    with SQL datbases. Only copies data from genes that are upregulated in 
    brain into the NEWFILE.
    '''
    d = {}
    with open(PGFILE, 'r') as f:
        gs = next(f).split('\t')
        probei = gs.index('Probe Set ID')
        gnamei = gs.index('Gene Title')
        gsymi = gs.index('Gene Symbol')
        fbgni = gs.index('FlyBase')

        #print(probei, gnamei, gsymi, fbgni)
        #print('gnamei', gnamei)
        
        for l in f:
            gs = l.split('\t')
            probe, gname, gsym, fbgn = map('{0}'.format, [gs[probei], gs[gnamei], gs[gsymi], 
                gs[fbgni]])
            #if len(fbgn) > 12:
                #print(fbgn)
            #print(probe, gname, gsym, fbgn)
            d[probe] = [fbgn, gname, gsym]

            
    with open(NEWFILE, 'w') as h:
        with open(DATAFILE, 'r') as g:
            label = next(g)
            llist = label.split('\t')
            #print(llist[0])
            #print(llist[1])
            braini = []
            for i, item in enumerate(llist):
                if 'brain' in item:
                    braini.append(i)
                    #print('brain', i)
                elif 'Brain' in item:
                    braini.append(i)
                    #print('Brain', i)
            maxbraini = max(braini)
            minbraini = min(braini)
            llist.insert(1, 'FBgn\tGene\tGene Abbr')
            h.write('\t'.join(llist[:maxbraini+2])+ '\tGene Source' + '\n')
            nline = 0
            for l in g:
                nline = nline+1
                #print(nline)
                ds = l.split('\t')[:maxbraini+1]
                probe = ds[0]
                upordown = ds[1]
                if probe == '': 
                    continue
                else:
                    print('going')
                    fbgn, gname, gsym = d[probe]
                    fbgnlist, gnamelist, gsymlist = [x.split('///') for x in [fbgn, gname, gsym]]
                    fbgn_gene_sym = list(zip(fbgnlist, gnamelist, gsymlist))
                    print(fbgn_gene_sym)
                    for fgs in fbgn_gene_sym:
                        print('fgs', fgs)
                        dscopy = list(ds)
                        dscopy.insert(1, fgs[2].strip(' '))
                        dscopy.insert(1, fgs[1].strip(' '))
                        dscopy.insert(1, fgs[0].strip(' '))
                        print(dscopy)
                        newline = '\t'.join(dscopy) + '\tfly_atlas\n'
                        print(newline)
                        h.write(newline)

if __name__ == '__main__':
    probe_to_fbgn_gene()
