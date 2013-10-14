############# TESTING APPLYING A MOVING AVERAGE TO INTENSITY DIFFERENCE PLOTS ###########

from piltest2 import *

IMNUMS = np.arange(4300, 4699, 1)
IMAGES = ['mov{0:05}'.format(n) for n in IMNUMS]
OUTDIR1 = PARDIR+'/xthreat_hist'
cmn.makenewdir(OUTDIR1)

WINLEN = 60

def window(winlen):
    
    wind = list(np.ones(winlen)/winlen)
    return(wind)
#center_a, center_p, side_al, side_ar, side_pl, side_pr

os.chdir('submovie_sub')

smc = []
mmc = []

for img in IMAGES:
    #print(img)
    flysmc = []
    flymmc = []
    for comp_label in [1,2]:
        imfile = img+EXT
        orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTSUBTHDIR, plot='no')
        try:
            orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
        except:
            continue
        
        x = np.copy(orient_im)
        w_im = findwings(x, WING_TH_LOW, WING_TH_HIGH)
        imrois = defrois(CENTER_A, SIDE_AL, MID_L, TMAT_FLY_IMG)
        
        #plt.figure()
        #plt.subplot(131)
        #plt.imshow(orient_im, cmap=plt.cm.gray)
        #plt.plot([0, ROTIMSHAPE[1]], FLY_OFFSET, 'r-') 
        #plt.plot(FLY_OFFSET, [0, ROTIMSHAPE[0]], 'r-')
        #plt.subplot(132)
        #plt.imshow(w_im, cmap=plt.cm.gray)      
        #plotrois(imrois)
        #plt.subplot(133)   
        #hist, bin_edges = np.histogram(orig_im, bins=60)
        #bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])     
        #plt.plot(bin_centers, hist, lw=2)
        #plt.ylim(0, 300)
        #plt.title('Intensity histogram')
        #plt.savefig('{0}{1}_fly{2}.png'.format(OUTDIR1, img, comp_label))
        #plt.close()


        roi_int = np.array(roimeans(w_im, imrois))
        center_a = roi_int[0]
        center_p = roi_int[1]
        side_a = np.sum(roi_int[2:4])
        side_p = np.sum(roi_int[4:6])
        med = np.sum(roi_int[6:8])

        if ((center_p+side_p) - (center_a+side_a)) > 0:
            flysmc.append(side_p - center_p)
            flymmc.append(med - center_p)
        
        else:
            flysmc.append(side_a - center_a)
            flymmc.append(med - center_a)
    try:
        smc.append(np.max(flysmc))
    except ValueError:
        pass
    try:
        mmc.append(np.max(flymmc))
    except ValueError:
        continue

wind = window(WINLEN)
conv_smc = np.convolve(smc/max(smc), wind, 'same')        
conv_mmc = np.convolve(mmc/max(mmc), wind, 'same')        

plt.figure()
plt.subplot(211)
plt.plot(conv_smc/max(conv_smc))
plt.ylim(0, 1.2)

plt.subplot(212)
plt.plot(conv_mmc/max(conv_mmc))
plt.ylim(0, 1.2)

plt.savefig(PARDIR+'/'+'s-c_m-c_60.png')

