#! /usr/bin/env python

import re
import itertools

OLDTABLE = 'table.txt'
NEWTABLE = 'revtable.txt'
KEYTABLE = '../berkeley_manifests/2014-0218_samples.csv'
#DATE = '[[RNASeq-Autism-Berkeley#2014-0218|2014-0218]]'
DATE = '[[RNASeq-Autism-Berkeley#2014-0225|2014-0225]]'
KEYFILE = '20140225_seq.csv'
QUBITFILE = '140221_SarahJ.csv'

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
    

def addcolstoend(oldtable, newtable):
    
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


def addcol(oldtable, newtable, newcol, newcolentry):
    
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                elist.insert(newcol, '{0}'.format(newcolentry))
                newline = '||'.join(elist) + '\n'
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
    
    


def add_berkeley_labeldate(keytable, newtable, oldtable, date):
    d = {}
    with open(keytable, 'r') as h:
        h.next()
        for l in h:
            #print l
            alist = l.strip('\n').split(',')
            #print alist[1]
            d[alist[1]] = alist[0]
    #print d['Bintnu_MA']

    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            #f.next()
            for l in f:
                #print l
                elist = l.strip('\n').split('||')
                #print elist[12]
                #print d[elist[12].strip(' ')]
                try:
                    elist[13] = d[elist[12].strip(' ')]
                    elist[11] = date
                except KeyError:
                    pass
                

                newline = '||'.join(elist) + '\n'
                g.write(newline)


#def insert_berkeley_label2(keytable, oldtable, newtable):
    
    
    


def txttowikitable(oldtable, newtable, delimiter):
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split(delimiter)
                newelist = '||' + '||'.join(elist) + '||\n'
                g.write(newelist)

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
                    bioanalyzerlink = '[[attachment:RNASeq-Autism-BioanalyzerResults/{0}_{1}.pdf|ok]]'.format(datesent, blabel)
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

def get_qubit(qubitfile):
    d = {}
    with open(qubitfile, 'r') as h:
        h.next()
        for l in h:
            elist = l.strip('\n').strip(' ').split(',')
            d[elist[0].strip(' ')] = elist[2]
        
    return d

def insert_qubit(oldtable, newtable, qubitfile, col):
    
    d = get_qubit(qubitfile)
        

    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                sample = elist[13].strip(' ')

                if sample in d:
                    print 'yes'
                    elist.insert(col, d[sample])
                else:
                    elist.insert(col, ' ')
                newline = '||'.join(elist) + '||\n'
                g.write(newline)
    


txttowikitable(OLDTABLE, NEWTABLE, '\t')
#add_berkeley_labeldate(KEYTABLE, NEWTABLE, OLDTABLE, DATE)
#add_bioanalyzer_attachment(OLDTABLE, NEWTABLE)
#switch_columns(OLDTABLE, NEWTABLE, 10, 11)
#add_berkeley_seq_date(OLDTABLE, NEWTABLE, KEYFILE, 14, DATE)
#insert_qubit(OLDTABLE, NEWTABLE, QUBITFILE, 12)
