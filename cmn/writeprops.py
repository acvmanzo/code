
from mn.cmn.writefiles import *
import mn.plot.genplotlib as genplotlib
import mn.gof.gfplot as gfplot

d = genplotlib.gendictper2('pooled_perfile.txt')
md = gfplot.genpercent_m(d)
gfplot.writedata_matlab(md)
#writemeans(md, 'means_cs_per.txt')

