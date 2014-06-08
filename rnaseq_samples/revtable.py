#! /usr/bin/env python

# Functions for manipulating a wiki table containing information about the 
# RNA-Seq samples.
import re
import itertools
import os

OLDTABLE = 'table.txt'
NEWTABLE = 'revtable.txt'
COLNAMES = {
'berk_sample_name': "\'\'\'Berk Label1\'\'\' ",
'berk_id_name': "\'\'\'Berk Label2\'\'\' ",
'qubit': "\'\'\'[[RNASeq-Autism-BioanalyzerResults|Qubit]]\'\'\' ",
'bioanalyzer': "\'\'\'[[RNASeq-Autism-BioanalyzerResults|Bioanalyzer]]\'\'\' ",
'berk_send_date': "\'\'\'Date sent to UCB\'\'\' ",
'berk_seq_date': "\'\'\'Date seq\'\'\' "
}


### CONVERT TABLE TO WIKI FORMAT ###

def txttowikitable(oldtable, newtable, delimiter):
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split(delimiter)
                newelist = '||' + '|| '.join(elist) + '||\n'
                g.write(newelist)

def wikitocsv(oldtable, newtable):
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                elist = [x.strip(' ') for x in elist]
                newline = ','.join(elist[1:-1]) + '\n'
                g.write(newline)

### FUNCTIONS FOR MANIPULATING TABLE SHAPE ###

def addcol(oldtable, newtable, newcol, newcolentry):
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                elist.insert(newcol, '{0}'.format(newcolentry))
                newline = '||'.join(elist) + '\n'
                g.write(newline)


def add_cols_to_end(oldtable, newtable):
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                print elist
                print len(elist)
                if len(elist) < 14:
                    elist.append(' ')
                    elist.append('2014-02-17')
                    elist.append(' ')
                print elist
                newline = '||'.join(elist) + '\n'
                g.write(newline)


def remove_cols_from_end(oldtable, newtable, colstokeep):
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')[:colstokeep]
                newline = '||'.join(elist) + '||\n'
                g.write(newline)


def switch_columns(oldtable, newtable, col1, col2):
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                ecol1 = elist[col1]
                ecol2 = elist[col2]
                elist[col1] = ecol2
                elist[col2] = ecol1
                newline = '||'.join(elist) + '||\n'
                g.write(newline)


def shortdate(oldtable, newtable):
    '''In a table, changes the notation [[Andrea's Notebook/2014-02-14]] to [[Andrea's 
    Notebook/2014-02-14|2014-02-14]].
    '''

    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.split('||')
                newelist = []
                for e in elist:
                    p = re.search('201.-..-..', e)
                    if p != None:
                        date = p.group()
                        e = e.replace('[[Andrea\'s Notebook/{0}'.format(date), 
                        '[[Andrea\'s Notebook/{0}|{1}'.format(date, date))
                
                    newelist.append(e)
                newline = '||'.join(newelist)
                g.write(newline)




### FUNCTIONS FOR INSERTING/ADDING VALUES TO AUTISM PREP TABLE ###

def add_values(oldtable, newtable, infodict, keycolname, valcolname):
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            colnames = f.next().strip('\n').split('||')
            keycol = colnames.index(keycolname)
            valcol = colnames.index(valcolname)
            g.write('||'.join(colnames) + '||\n')
            
            for l in f:
                elist = l.strip('\n').split('||')
                key = elist[keycol].strip(' ')
                if key in infodict:
                    print 'yes'
                    elist[valcol] = infodict[key]

                newline = '||'.join(elist) + '||\n'
                g.write(newline)


def get_samples_for_seq(keyfile):
    with open(keyfile, 'r') as h:
        h.next()
        #for l in f:
        #elist = l.strip('\n').strip(' ').split(',')
        
        forseqlines = list(itertools.takewhile(lambda x: x !='Samples we don\'t plan to sequence,,,,,,,\n', \
        h))

    forseq = [x.split(',')[0] for x in forseqlines]
    return forseq


def insert_berkeley_seq_date(oldtable, newtable, keyfile, newcol, newentry):
    
    forseq = get_samples_for_seq(keyfile)
    print forseq[7]
    #print forseq
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                sample = elist[13]

                if sample.strip(' ') in forseq:
                    print 'yes'
                    elist.insert(newcol, newentry)
                else:
                    elist.insert(newcol, ' ') 
                #print elist
                newline = '||'.join(elist) + '\n'
                g.write(newline)

    
def add_berkeley_seq_date(oldtable, newtable, keyfile, col, entry):
    
    forseq = get_samples_for_seq(keyfile)
    print forseq[7]
    #print forseq
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                sample = elist[13]

                if sample.strip(' ') in forseq:
                    print 'yes'
                    elist[col] = entry

                #print elist
                newline = '||'.join(elist) + '\n'
                g.write(newline)
 

def get_berkeley_id(orderfile):
    '''Generates a dictionary where the keys are the sample names (ex., 
    "Bintnu-MD") and the values are the Berkeley ID (ex., "RGAM009A") using 
    info in the file "orderfile" with delimiter "delimiter". Orderfile must be in
    the following format: Berkeley #, Sample Name, Index #, Index Sequence
    '''
    d = {}
    with open(orderfile, 'r') as h:
        colnames = h.next().strip('\n').strip(' ').split(',')
        samplecol = colnames.index("Sample Name")
        idcol = colnames.index("Berkeley #")

        for l in h:
            elist = l.strip('\n').strip(' ').split(',')
            d[elist[samplecol]] = elist[idcol]

    return d


def add_berkeley_id(oldtable, newtable, orderfile):
    '''For use with autism library preps table. Generates a new table where 
    the Berkeley ID (ex., "RGAM009A") is inserted into the table based on 
    info in the csv file "orderfile". Orderfile must be in
    the following format: Berkeley #, Sample Name, Index #, Index Sequence.
    '''
    
    infodict = get_berkeley_id(orderfile)
    add_values(oldtable, newtable, infodict, 
    COLNAMES['berk_sample_name'], COLNAMES['berk_id_name'])           


def add_berkeley_send_date(oldtable, newtable, orderfile):
    
    d = get_berkeley_id(orderfile)
    
    date1 = os.path.basename(orderfile).split('_')[0]
    date = date1[:7] + '-' + date1[7:]
    date_entry = '[[RNASeq-Autism-Berkeley#A{0}|{0}]]'.format(date)
    
    infodict = {}
    for k in d.iterkeys():
        infodict[k] = date_entry

    print infodict
    
    add_values(oldtable, newtable, infodict, COLNAMES['berk_sample_name'], 
    COLNAMES['berk_send_date'])


def get_qubit(qubitfile):
    '''Generates a dictionary where the keys are the Berkeley ID 
    (ex., "RGAM009A") and the values are the qubit results. Sample column 
    header must be "Sample" and Qubit column header must include the term 'ng'.
    '''
    
    d = {}
    with open(qubitfile, 'r') as h:
        colnames = h.next().strip('\n').strip(' ').split(',')
        samplecol = colnames.index("Sample")
        for i, x in enumerate(colnames):
            if 'ng' in x:
               qubitcol = i
        for l in h:
            elist = l.strip('\n').strip(' ').split(',')
            d[elist[samplecol].strip(' ')] = elist[qubitcol]
    return d


def add_qubit(oldtable, newtable, qubitfile):
    
    infodict = get_qubit(qubitfile)
    add_values(oldtable, newtable, infodict, 
    COLNAMES['berk_id_name'], COLNAMES['qubit'])

               
def add_bioanalyzer_attachment(oldtable, newtable):
    
     with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.split('||')
                blabel = elist[13].rstrip(' ')
                #print l
                try:
                    datesent = elist[11].split('|')[1].replace('-', '').rstrip(']] ')
                    print datesent
                    bioanalyzerlink = '[[attachment:RNASeq-Autism-BioanalyzerResults/{0}_{1}.pdf|ok]]'.format(datesent, 
                            blabel)
                    print bioanalyzerlink
                    elist[10] = bioanalyzerlink
                    
                except IndexError:
                    pass
                g.write('||'.join(elist))
                    #p = re.search('201.-..-..', e)
                    #if p != None:
                        #date = p.group()
                        #e = e.replace('[[Andrea\'s Notebook/{0}'.format(date), 
                        #'[[Andrea\'s Notebook/{0}|{1}'.format(date, date))
                
                    #newelist.append(e)
                #newline = '||'.join(newelist)
                #g.write(newline)   

def replace_link_with_date(oldtable, newtable):
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            n = 1
            for l in f:
                n = n+1
                #print n
                elist = l.split(',')
                #print elist
                for i, e in enumerate(elist):
                    if '|' in e and 'Bioanalyzer' not in e:
                        elist[i] = e.strip(']]').split('|')[1]
                        #print elist[i]
                        #if elist[i][-1] != 'i':
                    if 'Bioanalyzer' in e:
                        #print elist[i]
                        elist[i]= e.strip(']]').split('|')[0].split('/')[1]
                
                newelist = ','.join(elist)
                    #print newelist
                g.write(newelist)

def add_date_to_end(samplefile):
    
    date1 = os.path.basename(samplefile).split('_')[0]
    date = date1[:7] + '-' + date1[7:]
    
    root, ext = os.path.splitext(samplefile)
    newfile = root+'_date'+ext
    
    with open(newfile, 'w') as g:
        with open(samplefile, 'r') as f:
            header = f.next().strip('\n')+',Date\n'
            g.write(header)
            for l in f:
                newline = l.strip('\n') +',' + date + ('\n')
                g.write(newline)
                
    
if __name__ == "__main__":
    for x in ['qubit/2014-0324_qubit.csv']:
        add_date_to_end(x)

    #remove_excess_cols('misc/table.txt', 'misc/revtable.txt', 17)
    #add_berkeley_send_date('misc/table.txt', 'misc/revtable2.txt', 
    #'berkeley_orders/2014-0311_samples.csv'
    #add_berkeley_send_date('misc/table.txt', 'misc/revtable2.txt', 
    #'berkeley_orders/2014-0311_samples.csv')
    #txttowikitable('2014-0317_qubit.csv', '2014-0317_qubit_wiki.txt', ',')
    #get_qubit('2014-0317_qubit.csv')
    #insert_qubit('misc/tab mle.txt', 'misc/revtable.txt', 
    #'bioanalyzer_results/2014-0311/2014-0317_qubit.csv')
    #add_berkeley_labeldate(KEYTABLE, NEWTABLE, OLDTABLE, DATE)
    #add_bioanalyzer_attachment(OLDTABLE, NEWTABLE)
    #switch_columns(OLDTABLE, NEWTABLE, 10, 11)
    #replace_link_with_date('20140320_db.csv', '20140320_db_date.csv')
