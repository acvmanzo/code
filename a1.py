from libs.aglib import *
import libs.courtshiplib as cl
import libs.rstatslib as rl
import scipy.stats as stats

#KINDLIST = ['charge']
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


#d = dictagnum(kind, FNAME)
#x = d['cg30116']
#y = d['cs-Apr']
#x = [int(z) for z in x]
#print(x)
#print(y)
#t = rl.ttest(x, y)
#print(t)
#print(t.rx('p.value')[0][0])

kind = 'charge'
print(kind)
d = dictagnum(kind, FNAME)
md = cl.dictttest(d, ctrlkey='cs-Apr')
mtd = cl.mcpval(md)
cl.createmwfile(kind+'_num_ttest_results.txt')
cl.writemwfile(kind+'_num_ttest_results.txt', mtd, kind)

cl.createshapfile('shapfile_num.txt')
cl.writeshapfile('shapfile_num.txt', d, kind)

#fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
#plotagdur(kind, d)
#plt.savefig('{0}_num.png'.format(kind))

    
for kind in KINDLIST:
    print(kind)
    d = dictagdur2(kind, FNAME)
    print(d)
    md = cl.dictmw(d, ctrlkey='cs-Apr')
    mtd = cl.mcpval(md)
    print('mtd', mtd)
    cl.createmwfile(kind+'_dur_mw_results.txt')
    cl.writemwfile(kind+'_dur_mw_results.txt', mtd, kind)
    #fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    #plotagdur(kind, d)
    #plt.savefig('{0}_dur.png'.format(kind))
