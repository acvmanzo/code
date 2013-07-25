
from mn.cmn.writefiles import *
import mn.plot.genplotlib as genplotlib
import mn.gof.gfplot as gfplot

dictdata = genplotlib.gendict('pooled_peakf_roi1.MOD')
dictmeans = genplotlib.genlist(dictdata)
writemeans(dictmeans, 'means_cs_pumpfreq.txt')

