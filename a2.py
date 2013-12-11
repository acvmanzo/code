import sys
import libs.aglib as al

FNAME = sys.argv[1] # File with data to be analyzed.


with open(FNAME) as f:
    for l in f:
        adict = al.agline2(l)
        #print(adict['gen'])
        
        if adict['gen'] == 'cg30116-Apr':
            print(adict['escdur'])
            #print(adict['escdur'])
            #print(l)
            #print(adict['gen'])
            #print(adict)
        
        #if adict['agdur'] == '' and 'Apr' not in adict['gen'] and 'JW' not in adict['gen']:
            #print(l)


        #if adict['agtype'] == '-':
            #print(l)

        #if adict['gen'] == '':
            #print(l)
