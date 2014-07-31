import re
import os
import glob

bsfile = 'basecall_summary.txt'
dbbsfile = 'db_basecall_summary.txt'

with open(bsfile, 'r') as f:
    with open(dbbsfile, 'w') as g:
        next(f)
        for l in f:
            newl = re.sub(r'_index[0-9]{0,}', '', l)
            newl2 = newl[:7] + '-' + newl[7:]
            g.write(newl2)

