import os
import glob


FDIR = '.'

os.chdir(FDIR)
fs = glob.glob('*.MTS')
print(fs)

for x, f in enumerate(fs):
    with open('moviekey.txt', 'a') as g:
        g.write('{0:03d}\t{1}\n'.format(x, f))
    os.rename(f, '{0:03d}.MTS'.format(x))
