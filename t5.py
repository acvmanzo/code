from piltest2 import *


#IMNUMS = np.arange(5, 1779)
#IMAGES = ['subm{0:04}'.format(n) for n in IMNUMS]
print(IMAGES)
# center_a, center_p, side_al, side_ar, side_pl, side_pr
    
def plot_ca_frame():
    
    cma = []
    
    for img in IMAGES:
        print(img)
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
            #plt.close()
            roi_int = np.array(roimeans(w_im, imrois))
            center_a = roi_int[0]
            center_p = roi_int[1]
            side_a = np.sum(roi_int[2:4])
            side_p = np.sum(roi_int[4:6])

            if ((center_p+side_p) - (center_a+side_a)) > 0:
                flycma.append(side_p - center_p)
            
            else:
                flycma.append(side_a - center_a)
                
        cma.append(np.max(flycma))

    plt.figure()
    plt.plot(cma)
    plt.savefig(PARDIR+'/'+'side-center.png')
    return(cma)


def hmsub(trace):
    """Mean-subtracts and then multiplies a trace (a numpy array) with a Hamming function of the same size as the 
    trace."""
    
    return(np.hamming(np.size(trace))*(trace - np.mean(trace)))
    
def dft(trace, dftsize):
    """Finds the discrete fourier transform of size 'dftsize' of a trace using the np.fft 
    function."""
    return(np.abs(np.fft.fft(trace, dftsize)))

def window(winlen):
    
    wind = list(np.ones(winlen)/winlen)
    return(wind)
    


DFTSIZE = 10000

#cma = plot_ca_frame()
#with open(PARDIR+'/'+'cma', 'w') as h:
    #pickle.dump(cma, h)
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
WINLEN = 50
wind = window(WINLEN)
#print(wind)
#plt.subplot(121)
#plt.plot(cma/max(cma))
#plt.subplot(122)
#plt.plot(np.convolve(cma/max(cma), wind, 'same'))
#plt.savefig('cma_conv.png')
#plt.close()
plt.plot((np.convolve(cma/max(cma), wind, 'same')))
plt.savefig('cma_conv_{0}.png'.format(WINLEN))
#b, a = scis.butter(1, 10, 'low')
#output_signal = scis.filtfilt(b, a, cma)
#plt.plot(output_signal)
