#!/usr/bin/env python

# Code for converting tables made in gnumeric to wiki format.
# Save a gnumeric sheet as a .txt file with tab delimiter

import sys
import numpy as np
import re

print('arg = input file (comma-separated .txt)')

ifname=sys.argv[1]
ofname=ifname.strip('.txt')+'_wiki.txt'

def writetableline(l):
    y = l.strip('\n').split('\t')
    x = [t.strip('\"') for t in y]
    nentries = len(x)
    seps = np.tile('||', nentries+1)
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
