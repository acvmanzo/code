import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import genplotlib as gpl
import cmn.cmn as cmn


def convtosec (minvalue, secvalue):
    return(60*minvalue + secvalue)


def courtshipline(string):

    cvals = {}
    x = ['date', 'movie', 'offset', 'well', 'gen', 'wingm', 'wings', 'copsucm', 'copsucs', 'copatt1m', 'copatt1s']
    y = string.split(',')[0:11]
    z = zip(x, y)

    for item in z:
        cvals[item[0]] = item[1]

    return(cvals)


def dictlat(kind, fname):

    """kind = 'wing', 'copatt1', 'copsuc'

    """

    d = {}

    f = open(fname)
    f.next()
    for l in f:
        cd= courtshipline(l)

        gen = cd['gen']
        if gen not in d:
            d[gen] = []

        sm = kind + 'm'
        ss = kind + 's'

        if cd[sm] != 'x' and cd[sm] != '-':
            d[gen].append(convtosec(float(cd[sm]), float(cd[ss]))-float(cd['offset']))

    return(d)




#def dictlat(fname):
    #"""Generates three dictionaries from the data in fname, with the conditions as keywords.

    #fname is of the following format:
    #Data, Offset (s), Well #, Genotype, Wing ext (m), Wing ext (s), Cop
    #Suc (m),Cop Suc (s),Cop Att 1 (m),Cop Att 1 (s)

    #Generates three dictionaries with latency to wing extension,
    #latency to successful copulation, and latency to first copulation
    #attempt.
    #"""


    #winglat = {}
    #copsuclat = {}
    #copattlat = {}

    #f = open(fname)
    #f.next()


    #for l in f:
        #d = courtshipline(l)
        #print(d)

        #gen = d['gen']
        #wingm = d['wingm']


        #for x in [winglat, copsuclat, copattlat]:
            #if gen not in x:
                #x[gen] = []

        #if wingm != 'x':
            #try:
                #winglat[gen].append(convtosec(float(wingm),
                #float(wings))-float(offset))
            #except ValueError:
                #continue

        #if copsucm != 'x':
            #try:
                #copsuclat[gen].append(convtosec(float(copsucm),
                #float(copsucs))-float(offset))
            #except ValueError:
                #continue

        #if copatt1m != 'x':
            #try:
                #copattlat[gen].append(convtosec(float(copatt1m),
                #float(copatt1s))-float(offset))
            #except ValueError:
                #continue

    #return(winglat, copsuclat, copattlat)



def dictmeans(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the values are lists of
    the mean frequency, standard deviation, standard error, and n for that condition.
    """

    mean_dict = {}

    for condition, value in dict.iteritems():
        meanval = np.mean(value)
        stdev = np.std(value)
        n = len(value)
        sterr = stdev/np.sqrt(n)

        if condition not in mean_dict:
            mean_dict[condition] = []

        mean_dict[condition].append(meanval)
        mean_dict[condition].append(stdev)
        mean_dict[condition].append(sterr)
        mean_dict[condition].append(n)
        mean_dict[condition].append('{0}'.format(label))

    return(mean_dict)


#def plotlat(kind, fname, keyfile='keylist', type='b'):

    #winglat, copsuclat, copattlat = dictlat(fname)
    #mwinglat, mcopsuclat, mcopattlat = map(dictmeans,[winglat, copsuclat, copattlat])

    #if kind == 'wing':
        #keylist = sorted(mwinglat.keys())
        #fig1 = gpl.plotdata(winglat, mwinglat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to wing extension', ylim=60, ymin=0)

    #if kind == 'copsuc':

        #keylist = sorted(mcopsuclat.keys())
        #fig1 = gpl.plotdata(copsuclat, mcopsuclat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to copulation', ylim=400, ymin=0)

    #if kind == 'copatt':
        #keylist = sorted(mcopattlat.keys())
        #fig1 = gpl.plotdata(copattlat, mcopattlat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to first copulation attempt', ylim=300, ymin=0)


def plotlat(kind, fname, iskeyfile = 'true', keyfile='keylist', type='b'):

    d = dictlat(kind, fname)
    md = dictmeans(d)

    if iskeyfile == 'true':
        keylist = cmn.load_keys(keyfile)
    else:
        keylist = sorted(d.keys())

    ylabel = 'Latency (s)'

    if kind == 'wing':
        ftitle = 'Latency to wing extension'

    if kind == 'copsuc':
        ftitle = 'Latency to copulation'

    if kind == 'copatt1':
        ftitle = 'Latency to first copulation attempt'

    fig1 = gpl.plotdata(d, md, keylist, type, ylabel=ylabel, ftitle=ftitle)


def dictfreq(fname):
    """Generates  dictionaries from the data in fname, with the conditions as keywords.

    fname is of the following format:
    Data, Offset (s), Well #, Genotype, Wing ext (m), Wing ext (s), Cop
    Suc (m),Cop Suc (s),Cop Att 1 (m),Cop Att 1 (s)

        """

    wingfreq = {}
    copsucfreq = {}
    copattfreq = {}

    f = open(fname)
    f.next()

    for l in f:
        date, movie, offset, well, gen, wingm, wings, copsucm, copsucs, copatt1m, copatt1s = l.split(',')[0:11]

        for y in [wingfreq, copsucfreq, copattfreq]:
            if gen not in y:
                y[gen] = []

        for y in [(wings, wingfreq), (copsucs, copsucfreq), (copatt1s, copattfreq)]:
            try:
                if float(y[0]) >= 0:
                    y[1][gen].append(100)
            except:
                pass
            if y[0] == 'x':
                y[1][gen].append(0)

    print(len(copsucfreq['Nhe3']))
    return(wingfreq, copsucfreq, copattfreq)



def plotfreq(kind, fname, keyfile='keylist', type='b'):

    wingfreq, copsucfreq, copattfreq = dictfreq(fname)
    mwingfreq, mcopsucfreq, mcopattfreq = map(dictmeans,[wingfreq, copsucfreq, copattfreq])

    if kind == 'wing':
        keylist = sorted(mwingfreq.keys())
        fig1 = gpl.plotdata(wingfreq, mwingfreq, keylist, type, ylabel='%', ftitle = 'Percentage of flies courting', ylim=120, ymin=0)

    if kind == 'copsuc':
        keylist = sorted(mcopsucfreq.keys())
        fig1 = gpl.plotdata(copsucfreq, mcopsucfreq, keylist, type, ylabel='%', ftitle = 'Percentage of flies copulating', ylim=120, ymin=0)

    if kind == 'copatt':
        keylist = sorted(mcopattfreq.keys())
        fig1 = gpl.plotdata(copattfreq, mcopattfreq, keylist, type, ylabel='%', ftitle = 'Percentage of flies attempting copulation', ylim=120, ymin=0)


def savegraph(fname = 'graph'):
    """Saves the bar graph plotted with 'plotbar'."""
    plt.savefig(fname)



KINDLIST = ['wing', 'copsuc', 'copatt1']
FNAME = '2013-07_courtship_inprog.csv'

for KIND in KINDLIST:
    plotlat(KIND, FNAME)
    savegraph(KIND+'lat')

#plotfreq('wing', FNAME)
#savegraph('wingfreq')
#try:
    #plotlat('wing', FNAME)
    #savegraph('winglat')
    #plotfreq('wing', FNAME)
    #savegraph('wingfreq')
#except:
        #pass

#try:
    #plotlat('copsuc', FNAME)
    #savegraph('copsuclat')
    #plotfreq('copsuc', FNAME)
    #savegraph('copsucfreq')
#except:
    #pass

#try:
    #plotlat('copatt', FNAME)
    #savegraph('copattlat')
    #plotfreq('copatt', FNAME)
    #savegraph('copattfreq')
#except:
    #pass




