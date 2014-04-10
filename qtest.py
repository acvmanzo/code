import os
import glob

FNAMES = sorted(glob.glob('*.csv'))
#FNAMES = ['2013-1029_1_mut_sarah.csv', '2014-0226_1_mut_andrea.csv']
gname = os.path.dirname(os.path.abspath('.')) + '/2014-0408_alldata_fmt.csv'
print gname


dataid = 999
with open(gname, 'w') as g:
    g.write('DataID,Date,Well,Target,Content,Sample,Cq\n')
    for fname in FNAMES:
        date = fname.split('_')[0][:7] + '-' + fname.split('_')[0][7:]
        with open(fname, 'r') as f:
                for l in f:
                    dataid = dataid + 1
                    blank, well, fluor, target, content, sample, biolset, cq, cqmean, cqstd = l.split(',')[:10]
                    if well == 'Well':
                        continue
                    newlist = [str(dataid), date, well, target, content, sample, cq]
                    newline = ','.join(newlist) + '\n'
                    g.write(newline)
