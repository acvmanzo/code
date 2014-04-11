import numpy as np
import itertools
import glob

fnames = glob.glob('*.mht')
#fname = '/home/andrea/Documents/lab/qRT-PCR/3_analysis/rest/bintnu-GP1.mht'

for fname in fnames:
    with open(fname, 'r') as f:
        
        #samples = list(itertools.dropwhile(lambda x: x !='Legend:<BR><i>P(H1) - Probability of alternate\n', \
        #itertools.takewhile(lambda x: x !='Result<th>\n', f)))
        #samples = list(itertools.takewhile(lambda x: x !='Legend:<BR><i>P(H1) - Probability of alternate\r\n', \
            #itertools.dropwhile(lambda x: x !='Result<th>\r\n', f)))

        data = list(itertools.dropwhile(lambda x: x !='Result</th>\r\n', itertools.takewhile(lambda x: x !=  
            'Legend:<BR><i>P(H1) - Probability of alternate \r\n', f)))
        #for s in samples:
            #print s
        #data = list(itertools.takewhile(lambda x: x == '<TD valign=3Dtop align=3D"left">', f))
        #print data

    d = {}
    newdata = []
    for da in data:
        nd =  da.strip('</TD>\r\n').strip('<TD valign=3Dtop align=3D"left">').strip('<TD valign=3Dtop align=3D"right">')
        newdata.append(nd)    
    print 'new', newdata
    #target, result = newdata[13], newdata[20]
    #targetexp, pval = [float(x) for x in [newdata[16],  newdata[19]]]
    #stderr = [float(x) for x in newdata[17].split(' - ')]
    #ci95 = [float(x) for x in newdata[18].split(' - ')]

    target = newdata[13]
    print target 
    d[target] = {}
    d[target]['result'] = newdata[20]
    d[target]['exp'], d[target]['pval'] = [float(x) for x in [newdata[16],  newdata[19]]]
    d[target]['stderr'] = [float(x) for x in newdata[17].split(' - ')]
    d[target]['ci95'] = [float(x) for x in newdata[18].split(' - ')]

    print d
    #with open(fname, 'r') as f:
        #for l in f:
            ##print repr(l)
            #x = 'Result</th>\r\n'
            #y = 'Legend:<BR><i>P(H1) - Probability of alternate \r\n'
            #if l == y:
            #print 'True'
