#Script to convert probe name to gene name from FlyAtlas data.
#Column names in PGFILE:
#Probe Set ID	GeneChip Array	Species Scientific Name	Annotation Date	Sequence Type	Sequence Source	Transcript ID(Array Design)	Target Description	Representative Public ID	Archival UniGene Cluster	UniGene ID	Genome Version	Alignments	Gene Title	Gene Symbol	Chromosomal Location	Unigene Cluster Type	Ensembl	Entrez Gene	SwissProt	EC	OMIM	RefSeq Protein ID	RefSeq Transcript ID	FlyBase	AGI	WormBase	MGI Name	RGD Name	SGD accession number	Gene Ontology Biological Process	Gene Ontology Cellular Component	Gene Ontology Molecular Function	Pathway	InterPro	Trans Membrane	QTL	Annotation Description	Annotation Transcript Cluster	Transcript Assignments	Annotation Notes

#PGFILE = 'probset_to_gene2.txt'
PGFILE = 'test_annot.txt'
#DATAFILE = 'microarray_data.txt'
DATAFILE = 'test_microarray.txt'
#NEWFILE = 'gene+data.txt'
NEWFILE = 'test_annot_microarray.txt'

#PGFILE = 'probes.txt'
#DATAFILE = 'test.txt'
#NEWFILE = 'newtest.txt'
def probe_to_fbgn_gene():
    d = {}
    with open(PGFILE, 'r') as f:
        gs = next(f).split('\t')
        probei = gs.index('Probe Set ID')
        gnamei = gs.index('Gene Title')
        gsymi = gs.index('Gene Symbol')
        fbgni = gs.index('FlyBase')

        #print(probei, gnamei, gsymi, fbgni)
        print('gnamei', gnamei)
        
        for l in f:
            gs = l.split('\t')
            probe, gname, gsym, fbgn = map('{0}'.format, [gs[probei], gs[gnamei], gs[gsymi], 
                gs[fbgni]])
            print(probe, gname, gsym, fbgn)
            d[probe] = [fbgn, gname, gsym]
    with open(NEWFILE, 'w') as h:
        with open(DATAFILE, 'r') as g:
            label = next(g)
            llist = label.split('\t')
            print(llist[0])
            print(llist[1])
            for i, item in enumerate(llist):
                if 'brain' in item:
                    print('brain', i)
                elif 'Brain' in item:
                    print('Brain', i)
            llist.insert(1, 'FBgn\tGene\tGene Abbr')
            h.write('\t'.join(llist))
            nline = 0
            for l in g:
                nline = nline+1
                #print nline
                ds = l.split('\t')
                probe = ds[0]
                #try:
                for i in reversed(range(len(d[probe]))):
                    ds.insert(1, d[probe][i])  
                newline = '\t'.join(ds)
                h.write(newline)
                #except KeyError:
                    #pass

if __name__ == '__main__':
    probe_to_fbgn_gene()
