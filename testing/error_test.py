#!/usr/bin/python
import sys

testin = sys.argv[1]

for i in range(3):
    if testin == '1':
        print('ERROR YOU SHOULD SEE')
        raise NameError('testin = 1')
    else:
        sys.stdout.write('Test stdout write\n')
