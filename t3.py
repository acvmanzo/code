from piltest2 import *

#imgnums = [str(x) for x in np.arange(10, 100, 20)]
#imgnums = [str(x) for x in [50]]
#images = ['subm00{0}'.format(n) for n in imgnums]


#comp_labels = [1, 2]

data = [
    # flies_up_closed
    ((14, 1), (True, False)),
    ((14, 2), (True, False)),
    ((17, 1), (True, False)),
    ((17, 2), (True, False)),
    ((18, 1), (True, False)),
    ((18, 2), (True, False)),
    ((40, 1), (True, False)),
    ((40, 2), (True, False)),
    ((60, 1), (True, False)),
    ((60, 2), (True, False)),
    ((67, 1), (True, False)),
    ((67, 2), (True, False)),
    ((78, 1), (True, False)),
    ((78, 2), (True, False)),
    ((82, 1), (True, False)),
    ((82, 2), (True, False)),
    # flies_up_ext
    ((36, 2), (True, True)),
    ((41, 2), (True, True)),
    ((42, 2), (True, True)),
    ((43, 2), (True, True)),
    ((44, 2), (True, True)),
    ((52, 2), (True, True)),
    ((55, 2), (True, True)),
    ((57, 2), (True, True)),
    # flies_down_closed
    ((19, 1), (False, False)),
    ((21, 1), (False, False)),
    ((21, 2), (False, False)),
    ((23, 1), (False, False)),
    ((44, 1), (False, False)),
    ((48, 2), (False, False)),
    ((52, 1), (False, False)),
    ((55, 1), (False, False)),
    ((57, 1), (False, False)),
    ((69, 1), (False, False)),
    ((75, 1), (False, False)),
    # flies_down_ext
    ((23, 2), (False, True)),
    ((25, 2), (False, True)),
    ((26, 2), (False, True)),
    ((27, 2), (False, True)),
    ((28, 2), (False, True)),
    ((47, 1), (False, True)),
    ((48, 1), (False, True)),
    ((50, 1), (False, True))]


def findconn(im, th_low, th_high, imshape):
    
    image = np.copy(im)
    thim = findwings(image, th_low, th_high)
    new_thim = ndimage.binary_opening(thim, structure=np.ones((5,5)).astype(thim.dtype))
    new_thim = ndimage.binary_closing(new_thim, structure=np.ones((5,5)).astype(new_thim.dtype))

    onesimage = np.ones(imshape)
    
    label_im, nb_labels = ndimage.label(new_thim)
    com = np.array(ndimage.measurements.center_of_mass(onesimage, label_im, np.arange(1, nb_labels+1)))
    return(label_im, nb_labels, com)
    


for (imnum, flyn),_ in data:
    img = 'subm00{0}'.format(imnum)
    print(img, flyn)
    imfile = img+EXT
    orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTRESDIR, plot='no')
    comp_label = flyn
    
    orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)

    b_label_im, b_nb_labels, b_coms = findconn(orient_im, BODY_TH, 255, ROTIMSHAPE)
    bw_label_im, bw_nb_labels, bw_coms = findconn(orient_im, 20, 255, ROTIMSHAPE)

    #hist, bin_edges = np.histogram(orig_im, bins=60)
    #bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
    #plt.plot(bin_centers, hist, lw=2)
    #plt.ylim(0, 500)
    #plt.show()
    
    ## Plots images into a figure.
    plt.figure()
    plt.subplot(131)
    plt.imshow(orient_im, cmap=plt.cm.gray)
    plt.title('Orig image')
    
    plt.subplot(132)
    plt.imshow(b_label_im, cmap=plt.cm.gray)
    plt.title('Body')
    plt.plot(b_coms.T[1], b_coms.T[0], 'ro', lw=1)
    
    plt.subplot(133)
    plt.imshow(bw_label_im, cmap=plt.cm.gray)
    plt.title('Body+wing')
    
    try:
        plt.plot(bw_coms.T[1], bw_coms.T[0], 'ro', lw=1)
    except IndexError:
        pass
    plt.savefig(OUTBWTESTDIR+img+'_{0}.png'.format(comp_label))
    plt.close()
        
        ##imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        ##plot_wingimage(w_im, imrois, img, comp_label, outwingdir)
        #roi_int = np.array(roimeans(w_im, imrois))
        ##fly_roi_int = np.vstack((fly_roi_int, roi_int[np.newaxis]))
        #fly_roi_int.append(roi_int)
   
    #return(fly_roi_int)   
