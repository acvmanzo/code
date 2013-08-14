#!/usr/bin/env python

# Code for converting tables made in gnumeric to wiki format.
# Save a gnumeric sheet as a .txt file with tab delimiter

import sys
import numpy as np
import re

print('arg = input file (tab-separated .txt)')

ifname=sys.argv[1]
ofname=ifname.strip('.txt')+'_wiki.txt'

def writetableline(l):

    llist = l.strip('\n').strip('\r').split('\t')
    for i, v in enumerate(llist):
        if v.find('FBgn') != -1:
            ind = i
            gene = llist[i+1]
            newv = str.format('[[http://flybase.org/reports/{0}|{1}]]'.format(v, gene))
    try:
        llist.pop(ind+1)
        llist.insert(ind+1, newv)
    except UnboundLocalError:
        pass
    print(llist)
    x = llist

    nentries = len(x)
    seps = np.tile('|| ', nentries+1)
    z = zip(seps, x)
    return(z)


with open(ifname, 'r') as f:
    with open(ofname, 'w') as g:
        m = f.next()
        z = writetableline(m)
        for i, v in enumerate(z):
            x = '\'\'\''+v[1]+'\'\'\''
            g.write('{0}{1}'.format(v[0],x))
        g.write('||\n')

        for l in f:
            z = writetableline(l)
            for i,v in enumerate(z):
                g.write('{0}{1}'.format(v[0],v[1]))
            g.write('||\n')
