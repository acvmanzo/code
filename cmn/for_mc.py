#! /usr/bin/env python

from mn.cmn.writefiles import *
import sys

print('arg1 = kind (capdata, peakf, volperpump, deltatime, gcpeak, gcarea, gcduration, gcdyearea, dtrpa1pumps, dtrpa1diffarea, percentfilltime, percentemptytime), arg2 = readfile, arg3 = writefile')

kind = sys.argv[1]
readfile = sys.argv[2]
writefile = sys.argv[3]

reformat_mc(kind, readfile, writefile)
