from libs.bglib import *
import matplotlib.pyplot as plt

files = sorted(os.listdir('movie'))
#os.chdir('movie')
#bg = np.array(Image.open(files[0])).astype(float)
bg = np.array(Image.open('background.tif')).astype(float)
plt.subplot(411)
plt.imshow(bg, cmap=plt.cm.gray)

plt.subplot(412)
thbg = np.copy(bg)
tih = thbg > 175 
#til = thbg < 5
#tib = np.intersect1d(tih, til)
#thbg[tib] = 0
thbg[tih] = 0
#thbg[til] = 0
#thbg[tih] = 0
plt.imshow(thbg, cmap=plt.cm.gray)

plt.subplot(413)
rthbg = np.copy(bg)
#rtih = rthbg < 100
rtih = rthbg < 175
rthbg[rtih] = 0
plt.imshow(rthbg, cmap=plt.cm.gray)

#plt.xlim(0, 300)
plt.subplot(414)
hist, bin_edges = np.histogram(bg, bins=60)
bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
plt.plot(bin_centers, hist, lw=2)
plt.ylim(0, 20000)

plt.savefig('bgthreshold.png', dpi=500)
plt.close()


files = sorted(os.listdir('movie'))
os.chdir('movie')
im = np.array(Image.open(files[11])).astype(float)



#negi = c < 0
#c[negi] = 0

#c = im-bg
#c = c-c.min()
#print(c.max())
#print(c.min())
#c = c/c.max()*255.0 #optional
#carr = np.uint8(c)
#plt.figure()
#plt.imshow(carr, cmap=plt.cm.gray)
#plt.savefig('../bgsub.png')

c = im - rthbg
print(c.max())
print(c.min())
c = c-c.min()
print(c.max())
print(c.min())
c = c/c.max()*255.0 #optional
print(c.max())
print(c.min())
carr = np.uint8(c)
plt.figure()
plt.imshow(carr, cmap=plt.cm.gray)
plt.savefig('../bgrthsub.png')
