from mn.cmn.writefiles import *
import sys
import os


DATA = ['capdata', 'freq', 'volperpump']
GENOTYPES = ['112648', '112204', '423']
COMPARE = ['ph_1max_1min', 'ph_1min_1max']

#for gen in GENOTYPES:
    #os.chdir('pooled_{0}_180f'.format(gen))
    #for data in DATA:
        #os.chdir(data)
        #if data == 'freq':
            #readfile = 'pooled_peakf_roi1.txt'
        #else: 
            #readfile = 'pooled_' + data + '.txt'
        
        #writefile = gen + '_' + os.path.splitext(readfile)[0] + '_mc.txt'
        #reformat_mc(data, readfile, writefile)
        #os.chdir('../')
    #os.chdir('../')
    #print(os.getcwd())


for gen in GENOTYPES:
    if gen == '112204':
        continue
    os.chdir('pooled_{0}_180f/phase'.format(gen))

    for comp in COMPARE:
        os.chdir(comp)
        readfile = 'pooled_delta_summ'
        writefile = gen + readfile + '_mc.txt'
        reformat_mc('deltatime', readfile, writefile)
        os.chdir('../')
    os.chdir('../../')
    print(os.getcwd())
