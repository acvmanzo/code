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
        date, offset, well, gen, wingm, wings, copsucm, copsucs, 
        copatt1m, copatt1s = l.split(',')[0:8]
               
        
        if gen not in winglat:
            winglat[gen] = []
        
        if gen not in copsuc:
            copsuclat[gen] = []
        
        if wingm != 'x':
            try:
				winglat[gen].append(convtosec(wingm, wings)-float(offset))
            except ValueError:
                continue
               
        if copsucm != 'x':
            try:
				copsuclat[gen].append(cop-float(offset))
            except ValueError:
                continue
       
    return(winglat, copsuc)


def means(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the values are lists of 
    the mean frequency, standard deviation, standard error, and n for that condition.
    """
    
    mean_dict = {}
    
    for condition, value in dict.iteritems():
        print(condition)
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


def plotwinglat(fname, keyfile='keylist', type='b', ylim=60):
    
    winglat, copsuc = dictcourt(fname)
    mwinglat = means(winglat)
    #keylist = sorted(mpumps.keys())
    keylist = cmn.load_keys(keyfile)
    
    fig1 = gpl.plotdata(winglat, mwinglat, keylist, type, ylabel='Latency (s)', ftitle = 'Latency to wing extension', ylim=ylim, ymin=0)


def savebar(fname = 'bargraph'):
    """Saves the bar graph plotted with 'plotbar'."""
    plt.savefig(fname)


winglat, copsuc = dictcourt('alldata.csv')
print(winglat)
winglatm = means(winglat)
print(winglatm)
plotwinglat('alldata.csv')
savebar()



