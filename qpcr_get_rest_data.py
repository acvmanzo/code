import numpy as np
import itertools
import glob

fnames = glob.glob('*.mht')
#fname = '/home/andrea/Documents/lab/qRT-PCR/3_analysis/rest/bintnu-GP1.mht'

d = {}
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

    newdata = []
    for da in data:
        print 'old', da
        nd =  da.rstrip('</TD>\r\n').replace('<TD valign=3Dtop align=3D"left"> ', '').replace('<TD valign=3Dtop align=3D"right"> ', '')
        print 'new', nd
        newdata.append(nd)    
    #print 'new', newdata
    #target, result = newdata[13], newdata[20]
    #targetexp, pval = [float(x) for x in [newdata[16],  newdata[19]]]
    #stderr = [float(x) for x in newdata[17].split(' - ')]
    #ci95 = [float(x) for x in newdata[18].split(' - ')]

    target, result = [newdata[13], newdata[20]]
    if result == '&nbsp;':
        result = 'UNCHANGED'
    #print target 
    d[target] = {}
    d[target]['result'] = result
    d[target]['exp'], d[target]['pval'] = [float(x) for x in [newdata[16],  newdata[19]]]
    d[target]['stderr'] = [float(x) for x in newdata[17].split(' - ')]
    d[target]['ci95'] = [float(x) for x in newdata[18].split(' - ')]

#print d.keys()
for k in d.keys():
    print k
    print d[k]
    #with open(fname, 'r') as f:
        #for l in f:
            ##print repr(l)
            #x = 'Result</th>\r\n'
            #y = 'Legend:<BR><i>P(H1) - Probability of alternate \r\n'
            #if l == y:
            #print 'True'
