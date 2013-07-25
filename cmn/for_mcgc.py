#! /usr/bin/env python

from mn.cmn.writefiles import *
import sys

print('arg1 = readfile-gc, arg2 = readfile-dyearea')
# arg1 is the file with all of the gc data (including files with multiple neurons responding), 
#and arg2 is the file with the area data also included.

readfile = sys.argv[1]
readfile2 = sys.argv[2]

expt = os.path.basename(os.path.abspath('../'))

reformat_mc('gcpeak', readfile, expt+'_gcpeak_mc.txt')
reformat_mc('gcarea', readfile, expt+'_gcarea_mc.txt')
reformat_mc('gcduration', readfile, expt+'_gcduration_mc.txt')
reformat_mc('gcdyearea', readfile2, expt+'_dyearea_mc.txt')
