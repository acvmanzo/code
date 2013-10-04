from piltest2 import *

IMNUMS = np.arange(4413, 4438, 1)
IMAGES = ['mov{0:05}'.format(n) for n in IMNUMS]
OUTDIR1 = PARDIR+'/xthreat_hist'
cmn.makenewdir(OUTDIR1)

#center_a, center_p, side_al, side_ar, side_pl, side_pr

for img in IMAGES:
    print(img)
    for comp_label in COMP_LABEL:
        imfile = img+EXT
        orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTSUBTHDIR, plot='no')
        try:
            orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
        except:
            continue
        plt.figure()
        plt.subplot(131)
        x = np.copy(orient_im)
        plt.imshow(orient_im, cmap=plt.cm.gray)
        plt.plot([0, ROTIMSHAPE[1]], FLY_OFFSET, 'r-') 
        plt.plot(FLY_OFFSET, [0, ROTIMSHAPE[0]], 'r-')
        plt.subplot(132)
        w_im = findwings(x, WING_TH_LOW, WING_TH_HIGH)
        plt.imshow(w_im, cmap=plt.cm.gray)      
        imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        plotrois(imrois)
        

        plt.subplot(133)   
        hist, bin_edges = np.histogram(orig_im, bins=60)
        bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])     
        plt.plot(bin_centers, hist, lw=2)
        plt.ylim(0, 500)
        plt.title('Histogram of intensities')
        plt.savefig('{0}{1}_fly{2}.png'.format(OUTDIR1, img, comp_label))
        plt.close()
