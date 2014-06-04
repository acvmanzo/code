#! /usr/bin/env python

#Code for converting tables to and from wiki format.

import os
import sys

print 'Input filename and delimiter as follows: mytable.txt \t'

oldtable = sys.argv[1]
delim = sys.argv[2] 

if delim == 'tab' or delim == 't':
    delimiter = '\t'
else:
    delimiter = delim


### CONVERT TABLE TO WIKI FORMAT ###

def tabletowiki(oldtable, delimiter):
    root, ext = os.path.splitext(oldtable)
    newtable = root + '_wiki' + ext
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split(delimiter)
                newelist = '||' + '|| '.join(elist) + '||\n'
                g.write(newelist)

### CONVERT WIKI TABLE TO DELMITED FORMAT ###

def wikitotable(oldtable, delimiter):
    print repr(delimiter)
    root, ext = os.path.splitext(oldtable)
    newtable = root + '_table' + ext
    with open(newtable, 'w') as g:
        with open(oldtable, 'r') as f:
            for l in f:
                elist = l.strip('\n').split('||')
                elist = [x.strip(' ') for x in elist]
                newline = delimiter.join(elist[1:-1]) + '\n'
                g.write(newline)

if __name__ == "__main__":
    wikitotable(oldtable, delimiter)
