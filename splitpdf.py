import os
import itertools
import numpy as np
import glob

# Get list of pdfs.
pdfs = glob.glob('2100*.pdf')
for pdf in pdfs:
    pdfname, ext = os.path.splitext(pdf)
    newname = pdfname.replace(' ', '_')
    os.rename(pdf, newname+ext)
print pdfs

samples = []
pdfs = glob.glob('2100*.pdf')
for pdf in pdfs:
    pdfname, ext = os.path.splitext(pdf)
    # Converts pdf to a text file.
    cmd = 'pdf2txt.py -o {0}.txt {0}.pdf'.format(pdfname)
    os.system(cmd)
    #samples = []
    #pointer = False
    pages = []
    with open(pdfname+'.txt', 'r') as f:
        log = [] # List of lines in the text.
        pagenums = [] # List of page numbers that the sample traces are on.
        startpage_sample = [] # List of tuples: (pagenum, samplename).
        # Loads samples into the list samples.   
        #for l in f:
            #if l.strip('\n') == 'Ladder':
                #break
            #if pointer == True:
                #samples.append(l.strip('\n'))
            #if l.strip('\n') == 'Label':
                #pointer = True
        
        # Reads pdf file and adds sample names to list samples.
        samples = [y.strip('\n') for y in list(itertools.takewhile(lambda x: x !='Ladder\n', \
        itertools.dropwhile(lambda x: x !='Label\n', f)))][1:]
                
        print samples

        # Finds the page number that each sample trace is on.
        for l in f:
            log.append(l.strip('\n'))

            if l.strip('\n') == 'Page':
                try:
                    pagenum = int(log[-5])
                except ValueError:
                    pagenum = int(log[-3])
                #print count
                #print log
                pagenums.append(pagenum)
                log = []
            
            if l.strip('\n') in samples:
                startpage_sample.append([pagenum, l.strip('\n')])
        #print startpage_sample
    
    startpages, s = zip(*startpage_sample)
    s = list(s)
    #print (s)
    for i, sample in enumerate(s):
        slist = list(sample)
        print slist
        if len(sample) < 8:
            print sample
            slist.insert(-2, '0')
            slist.insert(-2, '0')
        s[i] = ''.join(slist)

    #print s
    
    endpages = [x-1 for x in startpages[1:]]
    endpages.append(startpages[-1]+1)
    
    startpage_endpage_sample = zip(startpages, endpages, s)
    print startpage_endpage_sample
    
    date = os.path.basename(os.path.abspath('.'))
    for sp, ep, sa in startpage_endpage_sample:
        cmd = 'pdftk A={0} cat {1}-{2} 4-5 output {3}_{4}.pdf'.format(pdf, sp, ep, 
        date, sa)
        os.system(cmd)
