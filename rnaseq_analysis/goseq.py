import os


def get_GOcat(goobo_file):
    with open(goobo_file, 'r') as e:
        #lines = e.readlines()
        #print(lines[:100])
        goids = []
        gonames = []
        nspaces = []
        for l in e:
            if ':' not in l:
                continue
            llist = l.strip('\n').split(': ')
            #print(llist)
            field = llist[0]
            val = llist[1]
            if field  == 'id':
                goids.append(val)
            if field == 'name':
                #print(val)
                gonames.append(val)
            if field == 'namespace':
                nspaces.append(val)
        gotup = zip(goids, gonames, nspaces)
        #print(len(goids), len(gonames))

        dgo = {}
        for item in gotup:
            dgo[item[0]] = [item[1], item[2]]
        #print(dgo)
        return(dgo)

def get_gene_goids(assoc_file, out_file):
    with open(out_file, 'w') as g:
        with open(assoc_file, 'r') as f:
            d = {}
            for l in f:
                if l[0] == '!':
                    continue
                gene_name = l.split('\t')[2]
                qual = l.split('\t')[3]
                goid  = l.split('\t')[4]
                if qual == 'NOT':
                    continue
                g.write('{}\t{}\n'.format(gene_name, goid))

def get_gene_categories(dictgo, assoc_file, out_file):

    with open(out_file, 'w') as g:
        with open(assoc_file, 'r') as f:
            d = {}
            for l in f:
                if l[0] == '!':
                    continue
                gene_name = l.split('\t')[2]
                qual = l.split('\t')[3]
                goid  = l.split('\t')[4]
                catname = dictgo[goid][0]
                nspace = dictgo[goid][1]
                if qual == 'NOT':
                    continue
                g.write('{}\t{}\t{}\t{}\n'.format(gene_name, goid, catname, 
                    nspace))

def get_go_categories(goobo_file, out_file):
    d = get_GOcat(goobo_file)
    with open(out_file, 'w') as g:
        for k, v in d.items():
            g.write('{}\t{}\t{}\n'.format(k, v[0], v[1]))


assoc_file = 'gene_association.fb'
goobo_file = 'gene_ontology.obo'
#out_file = 'gene_GOcateg.txt'
#out_file = 'gene_goid.txt'
#out_file = 'gene_goid_gocat.txt'
out_file = 'goid_gocat.txt'

#get_gene_categories(goobo_file, assoc_file, out_file)
#get_gene_goids(assoc_file, out_file)
#d = get_GOcat(goobo_file)
#get_gene_categories(d, assoc_file, out_file)
get_go_categories(goobo_file, out_file)
