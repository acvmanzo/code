import os
from libs.qrtpcrlib import combinedata

dirname = os.path.dirname(os.path.abspath('.')) + '/' 
gfilename =  '2014-0410_allmutdata_fmt.csv'
gname = dirname + gfilename

combinedata(gname)
