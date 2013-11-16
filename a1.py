from libs.aglib import *
import libs.courtshiplib as cl

#KINDLIST = ['charge', 'escd', 'escm']
KINDLIST = ['escd', 'escm']
#FNAME = 'ag2.csv'
FNAME = 'agall.csv'
CTRLKEY = 'cs-Apr'
KEYFILE = 'keylist'
#kind = 'escd'

#d = dictaglat(kind, FNAME)
#print('d', d)
#mwd = dictmw(d, CTRLKEY)
#print('mwd', mwd)
#adjpd = cl.mcpval(mwd, 'fdr', 'True', KEYFILE)
#print('adjpd', adjpd)

for kind in KINDLIST:
    print(kind)
    d = dictagnum(kind, FNAME)
    d = dictagdur(kind, FNAME)
    #print(d)
    #md = cl.dictmeans(d)
    #print(md)
    fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    plotagdur(kind, d)
    plt.savefig('{0}_dur.png'.format(kind))
