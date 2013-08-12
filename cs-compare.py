from courtshiplib import *
import cmn.writefiles as wf

KINDLIST = ['wing', 'copsuc', 'copatt1'] # List of behaviors; wing = wing extension; copsuc = successful copulation; copatt1 = first attempted copulation.
FNAME = '2013-0718_courtship_comp_cs.csv'
KEYFILE = 'keylist'


#for KIND in KINDLIST:
    #d = dictlat(KIND, FNAME)
    #md = dictmeans(d)
    #wf.writemeans(md, 'mean'+KIND+'.txt')

for KIND in KINDLIST:
    ifname = 'mean'+KIND+'.txt'
    md = cmn.loadmeans(ifname)

    conds = []
    means = []
    stdevs = []
    stderrs = []
    ns = []

    # Loads keys in order of plotting from keyfile.
    keylist = cmn.load_keys(KEYFILE)

    # Loads data from fname into a dictionary and generates lists from that data.

    for condition in keylist:
        mean, stdev, sterr, n = md[condition]
        means.append(mean)
        stdevs.append(stdev)
        stderrs.append(sterr)
        conds.append(condition + '\n' + 'n=' + str(n))

    xvals = np.linspace(1, 2*len(means), len(means))
    xlabels = [x + 0.5 for x in xvals]

    plt.bar(xvals, means, width=1, yerr=stderrs, ecolor='k')
    plt.xlim(0, 2+2*len(means))

    plt.xticks(xlabels, conds, fontsize=14)


    if KIND == 'wing':
        ftitle = 'Latency to wing extension'

    if KIND == 'copsuc':
        ftitle = 'Latency to copulation'

    if KIND == 'copatt1':
        ftitle = 'Latency to first copulation attempt'

    plt.ylabel('Latency (s)', fontsize=14)
    plt.title(ftitle, fontsize=18)
    plt.ylim(0, 1.25*np.max(means))

    plt.savefig('mean'+KIND+'.png')
    plt.close()
