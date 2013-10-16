import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import genplotlib as gpl
import cmn.cmn as cmn
import rstatslib as rsl
import rpy2.robjects as robjects
import os
import pylab
import courtshiplib as cl




def agline(line):

    """Generates dictionary with the values from line, with the parameters as 
    keywords.
    fname is of the following format:
    Date, Movie, Offset (s), Well #, Genotype, 
    flare or wing threat (m), (s), 
    wing threat + charge, orient, or lunge (m), (s),
    escalation - dominant (m), (s), (dur),
    escalation - mutual (m), (s), (dur)
    """

    vals = {}
    x = ['date', 'movie', 'offset', 'well', 'gen', 'flarem', 'flares', 
    'chargem', 'charges', 'escdm', 'escds', 'escddur', 'escmm', 'escms', 
    'escmdur']
    y = line.split(',')[0:15]
    z = zip(x, y)

    for item in z:
        cvals[item[0]] = item[1]

    return(vals)



def dictlat(kind, rawdict):
    """
    Generates a dictionary from data in 'fname' where the keywords are 
    genotypes and the values are the latencies to a behavior specified by 'kind'.

    kind = 'flare' (flare or wing threat alone), 
    'charge' (wing threat + charge, orientation, or lunge),
    'escd' (dominant escalation), 
    'escm' (mutual escalation)
    fname = file with raw data

    """

    d = {}
    f = open(fname)
    f.next()
    for l in f:
        adict = agline(l)

        gen = adict['gen']
        if gen not in d:
            d[gen] = []

        km = kind + 'm'
        ks = kind + 's'

        if adict[km] != 'x' and adict[km] != '-' and adicgt[km] != '':
            d[gen].append(cmn.convtosec(float(cdict[km])) + 
            float(cdict[ks])-float(convtosec(cdict['offset'])))
            
    return(d)


def dictfreq(kind, fname):
    """Generates a dictionary where the keywords are genotypes and the values are a list in which an entry of "100" = success and an entry of "0" = failure.

    kind: 'wing' (wing extension) 'copatt1' (first copulation attempt), 'copsuc' (successful copulation)
    fname: file containing raw data
    """

    d = {}
    f = open(fname)
    f.next()
    for l in f:
        cdict= courtshipline(l)

        gen = cdict['gen']
        if gen not in d:
            d[gen] = []

        ks = kind + 's'

        if cdict[ks] == 'x':
            d[gen].append(0)

        try:
            if float(cdict[ks]) >= 0:
                d[gen].append(100)
        except(ValueError):
            pass

    return(d)
