# Run with python2. Functions for parsing gff files.

import itertools
import os
import HTSeq 

REF_DIR = '/home/andrea/rnaseqanalyze/references'
LIST_DIR = 'dmel-r5.50_r5.57_lists'

R557_GFF_FILE = os.path.join(REF_DIR, 'dmel-r5.57', 'dmel-all-filtered-r5.57.gff')
R557_FBGN_NAME_FILE = os.path.join(REF_DIR, LIST_DIR, 'fbgn_name_r5.57')
R557_FNA_FILE = os.path.join(REF_DIR, LIST_DIR, 'fbgn_name_annID_r5.57')

R550_GFF_FILE = os.path.join(REF_DIR, 'dmel-r5.50-mingus', 'dmel-all-r5.50.gff')
R550_FBGN_NAME_FILE = os.path.join(REF_DIR, LIST_DIR, 'fbgn_name_r5.50')
R550_FNA_FILE = os.path.join(REF_DIR, LIST_DIR, 'fbgn_name_annID_r5.50')

def main():
    open(R550_FNA_FILE, 'w')
    open(R557_FNA_FILE, 'w')
    for og in [(R557_FNA_FILE, R557_GFF_FILE),
           (R550_FNA_FILE, R550_GFF_FILE)]:
        try:
            get_fbgn_name_annid(og[0], og[1])
        except ValueError:
            continue

def batch_fbgn_name():
    '''Applies get_fbgn_name to multiple gff files'''

    open(R550_FBGN_NAME_FILE, 'w')
    open(R557_FBGN_NAME_FILE, 'w')
    for og in [(R557_FBGN_NAME_FILE, R557_GFF_FILE),
           (R550_FBGN_NAME_FILE, R550_GFF_FILE)]:
        try:
            get_fbgn_name(og[0], og[1])
        except ValueError:
            continue

    
    #get_fbgn_name(R550_FBGN_NAME_FILE, R550_GFF_FILE)

def get_fbgn_name(outfile, gff_file):
    '''From gff_file, writes the fbgn, gene name, and gff_file name of each
    gene in gff_file into the file called 'outfile'. Also returns a list of 
    (fbgn, gene name) tuples. 
    '''
    gf = HTSeq.GFF_Reader(gff_file, end_included=True)
    fbgn_name = []
    counter = 0

    with open(outfile, 'a') as g:
        for feature in itertools.islice(gf, None):
            #print(feature.name, feature.attr['ID'], feature.attr
            #print(feature.type)
            #print(counter)
            counter +=1
            if feature.type == 'gene':
                #print(feature.name, feature.attr.keys(), feature.attr['ID'], feature.attr['Name']) 
                fbgn = feature.attr['ID']
                name = feature.attr['Name']
                fbgn_name.append((fbgn, name))
                g.write('{}\t{}\t{}\n'.format(fbgn, name, os.path.basename(gff_file)))
    return(fbgn_name)

def get_fbgn_name_annid(outfile, gff_file):
    '''From gff_file, writes the fbgn, gene name, annotation ID, and gff_file
    name of each gene in gff_file into the file called 'outfile'. Also returns
    a list of (fbgn, gene name) tuples. 
    '''
    gf = HTSeq.GFF_Reader(gff_file, end_included=True)
    fbgn_name_annid = []
    counter = 0

    with open(outfile, 'a') as g:
        for feature in itertools.islice(gf, None):
            #print(feature.name, feature.attr['ID'], feature.attr
            #print(feature.type)
            #print(counter)
            counter +=1
            if feature.type == 'gene':
                #print(feature.name, feature.attr.keys(), feature.attr['ID'], feature.attr['Name']) 
                fbgn = feature.attr['ID']
                name = feature.attr['Name']
                dbxref = feature.attr['Dbxref'].split(',')
                #print(dbxref)
                for i, item in enumerate(dbxref):
                    if 'FlyBase_Annotation_IDs' in item:
                        annid_index = i 
                annid = dbxref[annid_index].split(':')[1]
                #print(annid)
                fbgn_name_annid.append((fbgn, name, annid))
                g.write('{}\t{}\t{}\t{}\n'.format(fbgn, name, annid, os.path.basename(gff_file)))
    return(fbgn_name_annid)


if __name__ == '__main__':
    main()
