import os
import itertools
import numpy as np

#pdftk A=one_big_file.pdf cat 18-22 output new_file_name.pdf

pdfs = ['test2.pdf']

samples = []
for pdf in pdfs:
    pdfname, ext = os.path.splitext(pdf)
    cmd = 'pdf2txt.py -o {0}.txt {0}.pdf'.format(pdfname)
    os.system(cmd)
    pointer = False
    pages = []
    with open(pdfname+'.txt', 'r') as f:
        log = []
        pagenums = []
        samplepage = []        
        #for l in f:
            #if l.strip('\n') == 'Ladder':
                #break
            #if pointer == True:
                #samples.append(l.strip('\n'))
            #if l.strip('\n') == 'Label':
                #pointer = True
        
        samples = [y.strip('\n') for y in list(itertools.takewhile(lambda x: x !='Ladder\n', \
        itertools.dropwhile(lambda x: x !='Label\n', f)))][1:]
        print samples

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
                samplepage.append([pagenum, l.strip('\n')])
        print samplepage
    
    sp, s = zip(*samplepage)

    endsp = [x-1 for x in sp[1:]]
    endsp.append(sp[-1]+1)
    
    fp = zip(sp, endsp, s)
    print fp
        
    for i in fp:
        cmd = 'pdftk A={0} cat {1}-{2} output {3}.pdf'.format(pdf, i[0], i[1], 
        i[2])
        os.system(cmd)
#pdftk A=one_big_file.pdf cat 18-22 output new_file_name.pdf
