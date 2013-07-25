import scipy.stats as stats
import mn.plot.genplotlib as genplotlib

fname = 'summ_dffc_w1.txt'
gname = 'summ_dffc_w1_area_nodup.txt'

dpeak, darea, ddur = genplotlib.gendictgc(fname)
ddye = genplotlib.gendictgc2(gname)[3]

ds = [dpeak, darea, ddur, ddye]
for d in ds:
    a = d['1 M sucrose'] 
    b = d['2 M sucrose']
    
    t, p = stats.ttest_ind(a, b)
    
    print(t, p)

    
