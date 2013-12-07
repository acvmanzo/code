from libs.aglib import *


LNAME = 'testlist1.csv'
COMBFILE = '20131119_agdata_wms_all.csv'

if os.path.exists(COMBFILE) == True:
    os.remove(COMBFILE)

bname = '20131119_agdata_wms_part'
nums = np.arange(1, 8)
files = ['{0}{1}.csv'.format(bname, n) for n in nums]
print(files)

with open(COMBFILE, 'a') as g:
    for fil in files:
        with open(fil) as f:
            f.next()
            f.next()
            for l in f:
                g.write(l)
            

