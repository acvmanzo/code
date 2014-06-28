# Converts the precomputed FBgn <-> Annotation ID file into a format that
# can be imported by postgresql using the \copy function. 

FBGN_FILE = '/home/andrea/rnaseqanalyze/references/fbgn_annot_ID/fbgn_annotation_ID_fb_2014_03_fordb.tsv' # Manually deleted header from original file.

def add_braces():
    '''Puts brackets around lists so that they can be imported as arrays
    '''
    with open(fbgn_file.rstrip('.tsv') + '_braces.tsv', 'w') as g:
        with open(fbgn_file, 'r') as f:
            for l in f:
                llist = l.rstrip('\n').split('\t')
                llist[2] = '{'+llist[2]+'}'
                llist[4] = '{'+llist[4]+'}'
                #newline = '{}\t{}\t{{}}\t{}\t{{}}\n'.format(llist[0], llist[1],
                        #llist[2], llist[3], llist[4])
                newline = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(*llist)
                g.write(newline)

def gen_index_fbgn(fbgn_file):
    '''Copies data into new file with 3 columns:  
    primary fbgn, primary/secondary fbgn, gene symbol
    '''
    new_fbgn_file = fbgn_file.rstrip('.tsv') + '_2ndid.tsv'
    with open(new_fbgn_file, 'w') as g:
        with open(fbgn_file, 'r') as f:
            for l in f:
                llist = l.rstrip('\n').split('\t')
                sym, pfbgn = llist[:2]
                sfbgns = llist[2].split(',')
                #print(sfbgns)
                g.write('{}\t{}\t{}\n'.format(pfbgn, pfbgn, sym))
                for s in sfbgns:
                    if s != '':
                        g.write('{}\t{}\t{}\n'.format(pfbgn, s, sym))

def gen_index_annid(fbgn_file):
    '''Copies data into new file with 3 columns:  
    primary fbgn, primary/secondary fbgn, gene symbol
    '''
    new_fbgn_file = fbgn_file.rstrip('.tsv') + '_2annid.tsv'
    with open(new_fbgn_file, 'w') as g:
        with open(fbgn_file, 'r') as f:
            for l in f:
                llist = l.rstrip('\n').split('\t')
                sym, pfbgn, sfbgn, annid = llist[:4]
                sannids = llist[4].split(',')
                #print(sfbgns)
                g.write('{}\t{}\t{}\n'.format(annid, annid, sym))
                for s in sannids:
                    if s != '':
                        g.write('{}\t{}\t{}\n'.format(annid, s, sym))
if __name__ == '__main__':
    gen_index_annid(FBGN_FILE)


