from libs.aglib import *
import libs.courtshiplib as cl
import libs.rstatslib as rl
import scipy.stats as stats

#KINDLIST = ['charge']
KINDLIST = ['charge', 'escd', 'escm']
#FNAME = 'ag2.csv'
FNAME = 'agall.csv'
CTRLKEY = 'cs-June'
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

for kind in KINDLIST:
    print(kind)
    d = dictagnum(kind, FNAME)
    print d
    #md = cl.dictttest(d, ctrlkey=CTRLKEY)
    md = cl.dictmw(d, ctrlkey=CTRLKEY)
    mtd = cl.mcpval(md)
    #cl.createmwfile(kind+'_num_ttest_results.txt')
    #cl.writemwfile(kind+'_num_ttest_results.txt', mtd, kind)
    #cl.createmwfile(kind+'_num_mw_results.txt')
    #cl.writemwfile(kind+'_num_mw_results.txt', mtd, kind)
    cl.createstatfile(kind+'_num_mw_results.txt', 'Mann Whitney test')
    cl.writestatfile(kind+'_num_mw_results.txt', mtd, kind)
   
    cl.createinfonum(kind+'_num_info.txt')
    cl.writeinfonum(kind+'_num_info.txt', d, kind, CTRLKEY, 'median')

    cl.createshapfile('shapfile_num.txt')
    cl.writeshapfile('shapfile_num.txt', d, kind)

    fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    plotagnum(kind, d, type='bw')
    plt.ylim( [-1, 30] )
    plt.savefig('{0}_num.png'.format(kind))

    
#for kind in KINDLIST:
    #print(kind)
    #d = dictagdur(kind, FNAME)
    #print(d)
    #md = cl.dictmw(d, ctrlkey='cs-Apr')
    #mtd = cl.mcpval(md)
    #print('mtd', mtd)
    #cl.createmwfile(kind+'_dur_mw_results.txt')
    #cl.writemwfile(kind+'_dur_mw_results.txt', mtd, kind)
    #fig1 = plt.figure(figsize=(8, 6), dpi=1200, facecolor='w', edgecolor='k')
    #plotagdur(kind, d)
    #plt.savefig('{0}_dur.png'.format(kind))
