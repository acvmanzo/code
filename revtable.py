import re

OLDTABLE = 'table1.txt'
NEWTABLE = 'revtable.txt'
KEYTABLE = '../berkeley_manifests/2014-0218_samples.csv'
DATE = '[[RNASeq-Autism-Berkeley#2014-0218|2014-0218]]'

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
    

def addcols(oldtable, newtable):
    
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

def csvtowikitable(oldtable, newtable):
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split(',')
                newelist = '||' + '||'.join(elist) + '||\n'
                g.write(newelist)

csvtowikitable(OLDTABLE, NEWTABLE)

#add_berkeley_labeldate(KEYTABLE, NEWTABLE, OLDTABLE, DATE)
