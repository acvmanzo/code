############ TESTING PLOTTING OF DIFFERENCE IN ROI INTENSITIES ###########

from piltest2 import *

IMNUMS = np.arange(1, 21014, 1)
IMAGES = ['mov{0:05}'.format(n) for n in IMNUMS]

# center_a, center_p, side_al, side_ar, side_pl, side_pr
#os.chdir('submoviedir')
#for img in IMAGES:
    #for comp_label in COMP_LABEL:
        #imfile = img+EXT
        #orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTSUBTHDIR, plot='no')
        #try:
            #orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
        #except:
            #continue
        #w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
        #imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        #plot_wingimage(w_im, imrois, img, comp_label, OUTWINGDIR)
        #plt.close()

def plot_ca_frame():
    
    cma = []
    
    for img in IMAGES:
        #print(img)
        flycma = []
        for comp_label in COMP_LABEL:
            imfile = img+EXT
            orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTSUBTHDIR, plot='no')
            #plt.close()
            try:
                orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
            except:
                continue
            #plot_rotimage(orient_im, ROTIMSHAPE, FLY_OFFSET, comp_label, img, OUTROTDIR)
            #plt.close()
            w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
            imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
            #plot_wingimage(w_im, imrois, img, comp_label, OUTWINGDIR)
            plt.close()
            roi_int = np.array(roimeans(w_im, imrois))
            center_a = roi_int[0]
            center_p = roi_int[1]
            side_a = np.sum(roi_int[2:4])
            side_p = np.sum(roi_int[4:6])

            if ((center_p+side_p) - (center_a+side_a)) > 0:
                flycma.append(side_p - center_p)
            
            else:
                flycma.append(side_a - center_a)
        try:
            cma.append(np.max(flycma))
        except ValueError:
            continue

    plt.figure()
    plt.plot(cma)
    plt.savefig(PARDIR+'/'+'side-center.png')
    
    with open(PARDIR+'/'+'cma', 'w') as h:
        pickle.dump(cma, h)
    
    return(cma)


def window(winlen):
    
    wind = list(np.ones(winlen)/winlen)
    return(wind)
    


#cma = plot_ca_frame()

with open('cma', 'r') as h:
    cma = pickle.load(h)

#plt.figure()
#plt.subplot(121)
#plt.plot(cma)
##hcma = hmsub(cma)
#dcma = dft(cma, DFTSIZE)
##dncma = dcma/max(dcma)
##dntcma = dncma[0:DFTSIZE/2]
##plt.plot(dncma)
##dntcma[4000:] = 0

#plt.subplot(122)
#fil = np.fft.ifft(dcma)
#new = np.hstack((fil[8000:], fil[:2000]))
##plt.plot(fil)
#plt.plot(new)
##plt.xlim(0/4, DFTSIZE/2)
#plt.show()
#FPS = 30
WINLEN = 90
wind = window(WINLEN)
#print(wind)
#plt.subplot(121)
#plt.plot(cma/max(cma))
#plt.subplot(122)
#plt.plot(np.convolve(cma/max(cma), wind, 'same'))
#plt.savefig('cma_conv.png')
#plt.close()
conv_cma = np.convolve(cma/max(cma), wind, 'same')

#xvals = np.linspace(11.67, 11.67+len(cma)/30/60, len(cma))
#plt.plot(xvals, conv_cma)
#ax = plt.gca()
#ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(12))
##plt.xlim(0, len(cma)/30/60)
#plt.xlabel('Minutes')
#plt.ylabel('side-center')
#plt.savefig('cma_conv_{0}_min.png'.format(WINLEN))
#plt.close()

##xvals = np.linspace(11.67, 11.67+len(cma)/30/60, len(cma))
plt.figure()
plt.subplot(221)
print(len(conv_cma/4))
print(len(conv_cma[0:len(conv_cma)/4]))
plt.plot(conv_cma[0:len(conv_cma)/4])
#ax = plt.gca()
##ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(12))
###plt.xlim(0, len(cma)/30/60)
#plt.xlabel('Frames')
#plt.ylabel('side-center')
plt.ylim(0, 0.7)

plt.subplot(222)
plt.plot(conv_cma[len(conv_cma)/4:len(conv_cma)/2])
plt.ylim(0, 0.7)
ax = plt.gca()
ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))

plt.subplot(223)
plt.plot(conv_cma[len(conv_cma)/2:3*len(conv_cma)/4])
plt.ylim(0, 0.7)
ax = plt.gca()
ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))

plt.subplot(224)
plt.plot(conv_cma[3*len(conv_cma)/4:len(conv_cma)])
plt.ylim(0, 0.7)
ax = plt.gca()
ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))


plt.savefig('cma_conv_{0}_frames.png'.format(WINLEN))


#y = conv_cma > 0
#newcma = np.where(y)
#print(list(newcma))
#with open('cma_morethanzero.txt', 'w') as f:
    #f.write('{0}'.format(list(newcma[0])))
#print(newcma)
#plt.show()

#b, a = scis.butter(1, 10, 'low')
#output_signal = scis.filtfilt(b, a, cma)
#plt.plot(output_signal)
