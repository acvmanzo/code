
PGFILE = 'probset_to_gene2.txt'
DATAFILE = 'microarray_data.txt'
NEWFILE = 'gene+data.txt'

#PGFILE = 'probes.txt'
#DATAFILE = 'test.txt'
#NEWFILE = 'newtest.txt'

d = {}
with open(PGFILE, 'r') as f:
    f.next()
    for l in f:
        gs = l.split('\t')
        probe = gs[0].strip('"')
        gname = '"{0}"'.format(gs[13])
        gabb = '"{0}"'.format(gs[14])
        d[probe] = [gname, gabb]

with open(NEWFILE, 'w') as h:
    with open(DATAFILE, 'r') as g:
        label = g.next()
        llist = label.split('\t')
        llist.insert(1, 'Gene\tGene Abbr')
        h.write('\t'.join(llist))
        nline = 0
        for l in g:
            nline = nline+1
            #print nline
            ds = l.split('\t')
            probe = ds[0].strip('"')
            try:
                ds.insert(1, d[probe][1])
                ds.insert(1, d[probe][0])
                newline = '\t'.join(ds)
                h.write(newline)
            except KeyError:
                pass
