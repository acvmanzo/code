# Contains various functions used for reading information from one file and 
# then writing them in a new order/format to another file.

import os
import mn.plot.genplotlib as gpl
import glob


def writemeans(dictmeans, meansfile):
    with open(meansfile, 'w') as f:
        f.write('Condition,Mean,StdDev,StdError,N,Label\n')
    
        for k, v in dictmeans.iteritems():
            f.write(k + ',')
            for x in v:
                f.write(str(x) + ',')
            f.write('\n')


def writemeans_gc(gcfname, dyeareafname):

    peakd, aread, durd = gpl.gendictgc(gcfname)
    percentpeakd = {}
    for k, val in peakd.iteritems():
        vpercent = [v*100 for v in val]
        percentpeakd[k] = vpercent
    
    percentaread = {}
    for k, val in aread.iteritems():
        vpercent = [v*100 for v in val]
        percentaread[k] = vpercent
    
    dicts = percentpeakd, percentaread, durd
    mpeakd, maread, mdurd, = map(gpl.genlist, dicts)
    print(mpeakd)
    print(maread)
    
    dyearead = gpl.gendictgc2(dyeareafname)[3]
    mdyearead = gpl.genlist(dyearead)

    #wf.writemeans(mpeakd, expt+'_peakf_means.txt')
    #wf.writemeans(maread, expt+'_area_means.txt')
    #wf.writemeans(mdurd, expt+'_dur_means.txt')
    #wf.writemeans(mdyearead, expt+'_dyearea_means.txt')

    writemeans(mpeakd, 'peakf_means.txt')
    writemeans(maread, 'area_means.txt')
    writemeans(mdurd, 'dur_means.txt')
    writemeans(mdyearead, 'dyearea_means.txt')


def writemeans_deltatime(fnameread, fnamewrite):
    
    d = gpl.gendict_phase(fnameread, 'deltatime')
    md = gpl.genlist(d)
    
    writemeans(md, fnamewrite)
    
    
    


def writed(fnameread, fnamewrite):

    f = open(fnameread)
    f.next()

    g = open(fnamewrite, 'a')
    for l in f:
        if len(l.split(',')) == 5:
            movie, ratio11, ratio12, ratio13, c = l.split(',')
            g.write(c.strip('\n') + ',' + str(ratio12) + ',' + str(ratio13) + '\n')
        if len(l.split(',')) == 4:
            movie, ratio11, ratio12, c = l.split(',')
            g.write(c.strip('\n') + ',' + str(ratio12) + '\n')


def writedpf(fnameread, fnamewrite):

    f = open(fnameread)
    f.next()

    g = open(fnamewrite, 'w')
    g.close()
    g = open(fnamewrite, 'a')
    for l in f:
        movie, peakf, c = l.split(',')
        g.write(c.strip('\n') + ',' + peakf + '\n')


def writedgf(fnameread, fnamewrite):
    f = open(fnameread)
    f.next()

    g = open(fnamewrite, 'w')
    g.close()
    g = open(fnamewrite, 'a')
    
    for l in f:
        movie, cib, g1, g2, npump, c = l.split(',')[0:6]
        
        g.write(c + ',' + cib + ',' + npump +'\n')
    

def writeoldvals(fnameread, fnamewrite, condition, new='no'):
    """Written to write peakf values from old 762 cd8-gfp TNT summary files to new file."""
     
    f = open(fnameread)
    f.next()
    
    if new == 'yes':
        g = open(fnamewrite, 'w')
        g.write('Movie' + ',' + 'Peakf' + ',' + 'Condition' + '\n')
        g.close()
    
    g = open(fnamewrite, 'a')

    for l in f:
        name, peakf = l.split()
    
        g.write(name + ',' + peakf + ',' + condition + '\n')

def writeoldvals2(fnameread, fnamewrite):
    """Written to rewrite peakf file for 721 x TNT experiment from 5/24/10."""
    
    f = open(fnameread)
    
    g = open(fnamewrite, 'w')
    g.write('Movie' + ',' + 'Peakf' + ',' + 'Condition' + '\n')
    
    for l in f:
        condition, peakf = l.split()
        g.write('name' + ',' + peakf + ',' + condition + '\n')
    
    
def changemoviename(fnameread, fnamewrite):
    """Change the movie names for files in which that is a problem, like the 2010-0624 sucrose  series."""
    
    f = open(fnameread)
    f.next()
    
    g = open(fnamewrite, 'w')
    g.write('Movie' + ',' + 'Frame 1' + ',' + 'Frame2' + ',' + 'Condition' + '\n')
    
    for l in f:
        name, f1, f2, condition = l.split(',')[0:4]
        newname = 'r180_r_AviTest' + name + '-0000'
        g.write('\n' + newname + ',' + f1 + ',' + f2 + ',' + condition + ',' + 'end')
    
    
def reformat_mc(kind, fnameread, fnamewrite):
    
    #~ r, ext = os.path.splitext(fnameread)
    #~ fnamewrite = r + '_mc.txt'
    
    if kind == 'dtrpa1area':
        dicts = gpl.gendict_cibgf(fnameread)
        dmean, ddiffa = dicts
        
        for k, val in dmean.iteritems():
            for v in val:
                with open(fnamewrite, 'a') as g:
                    k = k.rstrip()
                    g.write('{0}\t{1}\n'.format(k, v))
        
        
    
    else:
        with open(fnameread) as f:
            f.next()
            with open(fnamewrite, 'w') as g:
                for l in f:
                    entries = l.strip('\n').split(',')
                    
                    
                    if kind == 'capdata':
                        cond = entries[5]
                        val = entries[4]
                    
                    if kind == 'freq':
                        cond = entries[2]
                        val = entries[1]
                    
                    if kind == 'deltatime':
                        cond = entries[7]
                        val = entries[3]
                    
                    if kind == 'volperpump':
                        cond = entries[4]
                        val = entries[3]
                    
                    if kind == 'gcpeak':
                        cond = entries[1]
                        val = entries[5]
                    
                    if kind == 'gcarea':
                        cond = entries[1]
                        val = entries[6]
                    
                    if kind == 'gcduration':
                        cond = entries[1]
                        val = entries[7]
                    
                    if kind == 'gcdyearea':
                        cond = entries[1]
                        val = entries[9]
                    
                    if kind == 'dtrpa1pumps':
                        cond = entries[3]
                        val = entries[5]
                    
                    if kind == 'dtrpa1diffarea':
                        cond = entries[6]
                        cond = cond.rstrip()
                        val = entries[5]
                    
                    if kind == 'percentfilltime':
                        cond = entries[6]
                        cond = cond.rstrip()
                        val = entries[4]
                    
                    if kind == 'percentemptytime':
                        cond = entries[6]
                        cond = cond.rstrip()
                        val = entries[5]

                    
                        
                    if val != 'x' and val != '':
                        g.write(cond + '\t' + val + '\n')

