#! /usr/bin/env python

import os
import shutil
import mn.plot.genplotlib as genplotlib
import matplotlib.pyplot as plt
import mn.phase.peaklib as phaselib
import mn.cap.pcapm as pcapm
import mn.cmn.cmn as cmn
import glob
import mn.gof.gfplot as gfplot
import mn.paper as paper

#EXPTS = ['2010-1130_tnt_180f', '2010-1201_113990_tnt_180f', '2010-1210_tnt_180f', '2010-1213_tnt_180f']

#EXPTS = ['2011-0329_423_tnt_180f', '2011-0331_423_tnt_180f', '2011-0406_423_tnt_180f']

EXPTS = ['2011-0313_112204_tnt_180f', '2011-0316_112204_tnt_180f']

NAME = '112204'
#EXPTS = ['2011-0217', '2011-0218', '2011-0222', '2011-0223_10h', '2011-0830', '2011-0901', '2011-0903', '2011-1007'] # Experiments that need to be pooled.
#EXPTS = ['2011-0111', '2011-0113', '2011-0831'] # Experiments that need to be pooled.
#EXPTS = ['2011-0329_423_tnt', '2011-0331_423_tnt', '2011-0406_tnt']
#EXPTS = ['2011-0313_tnt', '2011-0316_112204_tnt']

#ROIS = [('roi1', 'muscle 12'), ('roi2', ' muscle 11')]
ROIS = [('roi1', 'muscle 12')]
#TYPES = ['bin', 'fly']
KEYFILES = ['keyfile_c', 'keyfile_s', 'keyfile_v']
COMPARE = ['ph_1max_1min', 'ph_1min_1max']


def bg_key(p_peakf_file, keyfile, roi):
    dictdata = genplotlib.gendict(p_peakf_file)
    dictmeans = genplotlib.genlist(dictdata)
    keylist = cmn.load_keys(keyfile)
    
    dictdata2 = {}
    for k in keylist:
        dictdata2[k] = dictdata[k]
    
    genplotlib.plotdata(dictdata2, dictmeans, keylist, 'b', ylabel='Hz', ftitle='Mean pumping frequency', xlabelsize = 'medium')
    plt.savefig('pooled_dftf_freq_bar_'+roi)
    
def plotandsavepooledbargraph(p_peakf_file, roi):
    """Plots bar graph from data in 'peakf.txt' and saves it in the summary directory. Run from a 
    data/ or summary/ folder."""
    
    dictdata = genplotlib.gendict(p_peakf_file)
    dictmeans = genplotlib.genlist(dictdata)
    keylist = genplotlib.genkeylist(dictdata)
    genplotlib.plotdata(dictdata, dictmeans, keylist, 'b', ylabel='Hz', ftitle='Mean pumping ' + 
    'frequency '+roi)
    plt.savefig('pooled_dftf_freq_bar_'+roi)

def sp_key(p_peakf_file, keyfile, roi):
    
    dictdata = genplotlib.gendict(p_peakf_file)
    dictmeans = genplotlib.genlist(dictdata)
    keylist = cmn.load_keys(keyfile)
    
    dictdata2 = {}
    for k in keylist:
        dictdata2[k] = dictdata[k]
    
    genplotlib.plotdata(dictdata2, dictmeans, keylist, 's', ylabel='Hz', ftitle='Mean pumping ' + 
    'frequency '+roi, xlabelsize = 'medium')
    plt.savefig('pooled_freq_scatter_'+roi)


def plotandsavepooledscatterplot(p_peakf_file, roi):
    """Plots scatter plot from data in 'peakf.txt' and saves it in the summary directory. Run from a 
    data/ or summary/ folder."""
    
    dictdata = genplotlib.gendict(p_peakf_file)
    dictmeans = genplotlib.genlist(dictdata)
    keylist = genplotlib.genkeylist(dictdata)
    genplotlib.plotdata(dictdata, dictmeans, keylist, 's', ylabel='Hz', ftitle='Mean pumping ' + 
    'frequency '+roi)
    plt.savefig('pooled_freq_scatter_'+roi)


def plotandsavepooledpdfig(file, type, ms):
    """Plots and saves the phase vs. frequency plots; run from the 'summary' folder."""
    
    plt.figure()
    d = phaselib.phasefreqdict(file)    
    title = 'Phase vs. freq ({0})'.format(type)
    genplotlib.plot_phase_freq_oneplot(d, 'Phase vs. freq (bin) ', ms)
    
    name = 'pooled_phasevsfreq_{0}'.format(type)
    plt.savefig(name)


def plotphases(file, type):
    """Plots the phases taken from the summary text files (fname') with the title 'ftitle'; can 
    either be by bin or by fly depending on the summary file."""
    
    ftitle = 'Phases ({0})'.format(type)
    d = genplotlib.gendict_pd(file)
    genplotlib.plot_phaseplot(d, ftitle)    
    name = 'pooled_phases_{0}'.format(type)
    plt.savefig(name)


def plotphasesl(fname):
    """Plots the 'average' phases taken from the summary text files ('fname') with the title 'ftitle'; takes 
    into account the lengths of the 'average' phase vector ."""
    
    d = genplotlib.gendict_pd(fname)
    nd = {}
    for i, condition in enumerate(iter(d)):
        avgpd, avgl = phaselib.pd_avg(d[condition])
        nd[condition] = []
        nd[condition].append((avgpd, avgl))
    
    genplotlib.plot_phaseplot_l(nd, 'Phases - summary', withn='no')
    plt.savefig('pooled_phases_condition')


def plotfreqs(file, type):
    """Plots the frequencies taken from the summary text files ('fname') with the title 'ftitle'; 
    can plot either per bin or per fly depending on the summary file."""
    
    ftitle = 'Frequencies ({0})'.format(type)
    
    d = genplotlib.gendict_freq(file)
    md = genplotlib.genlist(d)
    keylist = genplotlib.genkeylist(d)
    genplotlib.plotdata(d, md, keylist, 's', ftitle=ftitle, err='stdev', ylim=8, ylabel='Hz')
    name = 'pooled_freqs_{0}'.format(type)
    plt.savefig(name)


def plotpixpersec(capfile):
    
    p = pcapm.gendictpps(capfile)
    mp = pcapm.genlist(p)
    k = p.keys()
    genplotlib.plotdata(p, mp, k, 's', 'pix/sec', 'Amount consumed \n pixels/sec', ylim=10, titlesize='x-large', xlabelsize='medium', xstart=0.25)
    plt.savefig('pooled_cap_pixpersec')
    plt.close()

def plotnlpersec(capfile):
    n = pcapm.gendictnps(capfile)
    mn = pcapm.genlist(n)
    l = n.keys()
    genplotlib.plotdata(n, mn, l, 's', 'nL/sec', 'Amount consumed \n nL/sec', ylim=10, titlesize='x-large', xlabelsize='medium', xstart=0.25)
    plt.savefig('pooled_cap_nlpersec')
    #plt.show()


def pool_dftf_results():
    for roi in ROIS:
        p_peakf_file = 'pooled_peakf_{0}.txt'.format(roi[0])  
        
        if os.path.exists(p_peakf_file) == True:
            os.remove(p_peakf_file)
       
        for expt in EXPTS:
            print(expt)
            try:
                peakf_file = '../../{0}/summary/peakf_{1}.txt'.format(expt, roi[0])
                
                with open(peakf_file) as f:
                    f.next()
                
                    if os.path.exists(p_peakf_file)!=True:
                        with open(p_peakf_file, 'w') as g:
                            g.write('Movie,Peak frequency,Condition\n')
                    
                    for l in f: 
                        name, peakf, cond = l.strip('\n').split(',')[0:3]
                        #print(cond)
                        try:
                            condi = condcurr.index(cond)
                            #print(condi)
                            cond = condnew[condi]
                        except:
                            pass
                        #print(cond)
                        
                        with open(p_peakf_file, 'a') as g:
                            g.write(name+','+peakf+','+cond+'\n')
            
            except IOError as e:
                if e.errno == 2:
                    print('Cannot find file or directory.')
                    continue

        plotandsavepooledbargraph(p_peakf_file, roi[1])
        plt.close()
        plotandsavepooledscatterplot(p_peakf_file, roi[1])
        plt.close()

        for roi in ROIS:
            p_peakf_file2 = 'pooled_peakf_{0}.MOD'.format(roi[0])  
            
            for keyfile in KEYFILES:
                try:
                    sp_key(p_peakf_file2, keyfile, keyfile)
                    plt.close()
                    bg_key(p_peakf_file2, keyfile, keyfile)
                    plt.close()
                except IOError:
                    continue
        
        return(p_peakf_file)


def pool_per_results():
    
    homefol = os.path.abspath('.')
    
    pooled_perfile = 'pooled_perfile.txt'
    if os.path.exists(pooled_perfile) == True:
        os.remove(pooled_perfile)
    
    
    
    for expt in EXPTS:
        exptpath = os.path.join(os.path.abspath('../../'), expt)
        print(exptpath)
        os.chdir(exptpath)
        perfiles = glob.glob('*percheck.txt')
        #print(perfiles)
        try:
            perfile = os.path.join(exptpath, perfiles[0])
        except IndexError:
            print('No perfile')
            os.chdir(homefol)
            continue
        
        
        os.chdir(homefol)
        with open(pooled_perfile, 'a') as g:
            with open(perfile, 'r') as f:
                f.next()
                for l in f:
                    name, cond, per = l.strip('\n').split(',')[0:3]
                    print(cond)
                    try:
                        condi = condcurr.index(cond)
                        cond = condnew[condi]
                    except:
                        pass
                    print(cond)
                    
                    g.write(name+','+cond+','+per+'\n')
                    
        
        
    os.chdir(homefol)
    d = genplotlib.gendictper2(pooled_perfile)
    md = gfplot.genpercent_noci(d)
    k = genplotlib.genkeylist(md)
    
    print(md)
    genplotlib.plotdata(d, md, k, 'b', ylabel='Probability of PER', ftitle='PER', ylim=120, xlabelsize='large')
    plt.savefig('pooled_per_bar')
    plt.close()
    genplotlib.plotdata(d, md, k, 's', ylabel='Probability of PER', ftitle='PER', ylim=120, xlabelsize='large')
    plt.savefig('pooled_per_scatter')
    

def pool_phase_results():
    
    #Pool phase results.
    for type in TYPES:
        p_file = 'pooled_phasediffs_{0}.txt'.format(type)
        
        if os.path.exists(p_file) == True:
            os.remove(p_file)
        
        for expt in EXPTS:
            file = '../../{0}/summary/phasediffs_{1}.txt'.format(expt, type)
            
            if os.path.exists(p_file) != True:
                    with open(p_file, 'w') as g:
                        g.write('Movie,Bin,PhaseDiff,Freq,Condition\n')
            
            with open(file) as f:
                f.next()
                
                with open(p_file, 'a') as g:
                    for l in f:
                        g.write(l)
        
        
        plotandsavepooledpdfig(p_file, type, 10)
        plt.close()
        plotphases(p_file, type)
        plt.close()
        plotphasesl(p_file)


def pool_deltatime_results():
    pfiles = []
    for comp in COMPARE:
        cmn.makenewdir(comp)
        p_file = os.path.join(comp, 'pooled_delta_summ')
        
        if os.path.exists(p_file) == True:
            os.remove(p_file)
    
        for expt in EXPTS:
            print(expt)
            summfol = 'summary_' + comp
            dsfile = '../../{0}/{1}/delta_summ'.format(expt, summfol)
            #print(os.path.abspath(dsfile))
            if os.path.exists(p_file) != True:
                with open(p_file, 'w') as g:
                    g.write('Movie,AvgDF,StDev(AvgDF),AvgDT,StdDev(AvgDT),AvgDP,PeakF,Condition\n')
            
            with open(dsfile) as f:
                f.next()
                
                with open(p_file, 'a') as g:
                    for l in f:
                        g.write(l)
        
        pfiles.append(os.path.basename(p_file))
    return(pfiles)
    

def pool_cap_results():
    
    p_capfile = 'pooled_capdata.txt'
    
    if os.path.exists(p_capfile) == True:
        os.remove(p_capfile)
        
    for expt in EXPTS:
        capfile = '../../{0}/summary/capdata.txt'.format(expt)
        
        if os.path.exists(p_capfile) != True:
            with open(p_capfile, 'w') as g:
                g.write('Movie,Deltacaplength,Duration,Pixpersec,nLpersec,Condition\n')
               
        with open(capfile) as f:
            f.next()
             
            with open(p_capfile, 'a') as g:
                for l in f:
                    g.write(l)
        
    plotpixpersec(p_capfile)
    plotnlpersec(p_capfile)
    return(p_capfile)
        

def pool_volperpump_results():
    
    p_volperpump = 'pooled_volperpump.txt'
    
    if os.path.exists(p_volperpump) == True:
        os.remove(p_volperpump)
    
    for expt in EXPTS:
        volppfile = '../../{0}/summary/cap_peakf_roi1_summ.txt'.format(expt)
        
        if os.path.exists(p_volperpump) != True:
            with open(p_volperpump, 'w') as g:
                g.write('Movie,nlpersec,peakf_roi1,volperpump,condition\n')
        
        with open(volppfile) as f:
            f.next()
            
            with open(p_volperpump, 'a') as g:
                for l in f:
                    g.write(l)
    
    return(p_volperpump)

if __name__ == '__main__':
    
    #condcurr = ['500 mM + 2% mc', '500 mM', '24 hours/500 mM sucrosews', '10h/100 mM sucrose', '1 M sucrose', '2 M sucrose']
    #condnew = ['2% MC', '0% MC', '24 hours/500 mM sucrose', '10 hours/100 mM sucrose', '1 M', '2 M']

    
    homefol = os.path.abspath('.')
    
    print('Pooling pump freq data')
    pumpfol = cmn.makenewdir('freq')
    os.chdir(pumpfol)
    pf = pool_dftf_results()
    print(pf)
    os.system('python ~/python/mn/paper/plotfreqfile.py {0} {1} {2} {3}'.format(pf, '../keylist', NAME + '_freq.png', NAME + '_freq_means.txt'))
    
    print('Pooling cap data')
    os.chdir(homefol)
    capfol = cmn.makenewdir('capdata')
    os.chdir(capfol)
    pf = pool_cap_results()
    os.system('python ~/python/mn/paper/plotcapfile.py {0} {1} {2} {3}'.format(pf, '../keylist', NAME + '_capdata.png', NAME + '_capdata_means.txt'))
    
    print('Pooling volperpump data')
    os.chdir(homefol)
    volppfol = cmn.makenewdir('volperpump')
    os.chdir(volppfol)
    pf = pool_volperpump_results()
    os.system('python ~/python/mn/paper/plotvolperpumpfile.py {0} {1} {2} {3}'.format(pf, '../keylist', NAME + '_volperpump.png', NAME + '_volperpump_means.txt'))
    
    #print('Pooling deltatime data')
    #os.chdir(homefol)
    #phasefol = cmn.makenewdir('phase')
    #os.chdir(phasefol)
    #pfiles = pool_deltatime_results()
    #print(pfiles)
    #files_fol = zip(pfiles, COMPARE)
    #print(files_fol)
    #for c in files_fol:
        #os.chdir(c[1])
        #os.system('python ~/python/mn/paper/plotdeltatimefile.py {0} {1} {2} {3}'.format(c[0], '../../keylist', NAME + '_{0}.png'.format(c[1]), NAME + '_{0}_means.txt'.format(c[1]))) 
        #os.chdir('../')
   
