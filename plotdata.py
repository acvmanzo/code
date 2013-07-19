import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import glob
import genplotlib as gpl
import cmn.cmn as cmn


def convtosec (minvalue, secvalue):
    return(60*minvalue + secvalue)


def dictcourt(fname):
    """Generates two dictionaries from the data in fname, with the conditions as keywords.

    fname is of the following format:
    Data, Offset (s), Well #, Genotype, Wing ext (m), Wing ext (s), Cop
    Suc (m),Cop Suc (s),Cop Att 1 (m),Cop Att 1 (s),Cop Att 2 (m),Cop
    Att 2 (s),Cop Att 3 (m),Cop Att 3 (s),Cop Att 4 (m),Cop Att 4
    (s),Cop Att 5 (m),Cop Att 5 (s),Cop Att 6 (m),Cop Att 6 (s),Cop Att 7 (m),Cop Att 7 (s),Cop Att 8 (m),Cop Att 8 (s),Cop Att 9 (m),Cop Att 9 (s),Cop Att 10 (m),Cop Att 10 (s),Cop Att 11 (m),Cop Att 11 (s),Notes


    Generates three dictionaries with latency to wing extension,
    latency to successful copulation, and latency to first copulation
    attempt.
    """


    winglat = {}
    copsuclat = {}
    copattlat = {}

    f = open(fname)
    f.next()

    for l in f:
        date, offset, well, gen, wingm, wings, copsucm, copsucs, copatt1m, copatt1s = l.split(',')[0:10]

        for x in [winglat, copsuclat, copattlat]:
            if gen not in x:
                x[gen] = []

        if wingm != 'x':
            try:
                winglat[gen].append(convtosec(float(wingm),
                float(wings))-float(offset))
            except ValueError:
                continue

        if copsucm != 'x':
            try:
                copsuclat[gen].append(convtosec(float(copsucm),
                float(copsucs))-float(offset))
            except ValueError:
                continue

        if copatt1m != 'x':
            try:
                copattlat[gen].append(convtosec(float(copatt1m),
                float(copatt1s))-float(offset))
            except ValueError:
                continue

    return(winglat, copsuclat, copattlat)


def means(dict, label='data'):
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


def plotlat(kind, fname, keyfile='keylist', type='b'):

    winglat, copsuclat, copattlat = dictcourt(fname)
    mwinglat, mcopsuclat, mcopattlat = map(means,[winglat, copsuclat, copattlat])

    if kind == 'wing':
        keylist = sorted(mwinglat.keys())
        fig1 = gpl.plotdata(winglat, mwinglat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to wing extension', ylim=50, ymin=0)

    if kind == 'copsuc':

        keylist = sorted(mcopsuclat.keys())
        fig1 = gpl.plotdata(copsuclat, mcopsuclat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to copulation', ylim=400, ymin=0)

    if kind == 'copatt':
        keylist = sorted(mcopattlat.keys())
        fig1 = gpl.plotdata(copattlat, mcopattlat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to first copulation attempt', ylim=400, ymin=0)


def savebar(fname = 'bargraph'):
    """Saves the bar graph plotted with 'plotbar'."""
    plt.savefig(fname)


fname = 'alldata.csv'
plotlat('wing', fname)
savebar('winglat')
plotlat('copsuc', fname)
savebar('copsuclat')
plotlat('copatt', fname)
savebar('copattlat')





