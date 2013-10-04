from PIL import Image
import os
from PIL import ImageMath
import numpy as np
import cmn.cmn as cmn

SUBMOVIEDIR = 'submoviedir/'

submoviedir = os.path.join(os.path.abspath('.'), SUBMOVIEDIR)
cmn.makenewdir(submoviedir)
os.chdir('movie')

print(submoviedir)
# Background subtracts from movie.
nframes = 100
files = sorted(os.listdir('.'))
moviel = len(files)
#c = np.array(Image.open(files[int(1)])).astype(float)
#bg = np.array(Image.open(files[0])).astype(float)

#for x in np.linspace(1, moviel-1, nframes):
    #c = np.array(Image.open(files[int(x)])).astype(float)
    #bg = bg+c

#bg = np.uint8(bg/nframes)

#im = Image.fromarray(bg)
#im.show()

############################
bg = np.array(Image.open(files[0])).astype(float)

for x in np.linspace(1, moviel-1, nframes):
    c = np.array(Image.open(files[int(x)])).astype(float)
    bg = np.dstack((bg, c))

#print(np.shape(bg))
bgnew = np.median(bg, 2)
#############################


#im = Image.fromarray(np.uint8(bgnew))
#im.show()

#for x in np.linspace(1, newframes, newframes):
    #outfile = 'new/' + files[int(x)] + 'new' + '.tif'
    #c = np.array(Image.open(files[int(x)])).astype(float)
    #subarr = c-bgnew
    #subim = Image.fromarray(np.uint8(np.absolute(subarr)))
    #subim.save(outfile)
    
for x in np.arange(0, len(files), 1):
    print(x)
    outfile = submoviedir + files[int(x)]
    c = np.array(Image.open(files[int(x)])).astype(float)
    subarr = c-bgnew
    subim = Image.fromarray(np.uint8(np.absolute(subarr)))
    subim.save(outfile)
    
