from aglib import *
import courtshiplib as cl

KINDLIST = ['flare', 'charge', 'escd', 'escm']
FNAME = 'allag.csv'
CTRLKEY = 'cs-Apr'
KEYFILE = 'keylist'
kind = 'charge'

d = dictaglat(kind, FNAME)
print('d', d)
mwd = dictmw(d, CTRLKEY)
print('mwd', mwd)
adjpd = cl.mcpval(mwd, 'fdr', 'True', KEYFILE)
print('adjpd', adjpd)
