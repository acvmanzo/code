from piltest2 import *

#imgnums = [str(x) for x in np.arange(10, 100, 20)]
#imgnums = [str(x) for x in [50]]
#images = ['subm00{0}'.format(n) for n in imgnums]


#comp_labels = [1, 2]


for x in [OUTRESDIR, OUTROTDIR, OUTWINGDIR, OUTTESTDIR]:
    cmn.makenewdir(x)

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
    ((50, 1), (False, True))][:2]


for (imnum, flyn),_ in data:
    img = 'subm00{0}'.format(imnum)
    print(img, flyn)
    imfile = img+EXT
    orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTRESDIR, plot='no')
    comp_label = flyn
    orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
    w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
    imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
    plot_wingimage(w_im, imrois, img, comp_label, OUTWINGDIR)
    plt.close()

    
    #w_im_cl = ndimage.binary_opening(w_im, structure=np.ones((5,5)).astype(w_im.dtype))
    w_im_op = ndimage.binary_opening(w_im, structure=np.ones((5,5)).astype(w_im.dtype))
    w_im_op_cl = ndimage.binary_opening(w_im, structure=np.ones((5,5)).astype(w_im.dtype))
    #w_im_cl_op = ndimage.binary_closing(w_im_cl, structure=np.ones((5,5)).astype(w_im.dtype))

    # Select the connected components.
    w_label_im, w_nb_labels = ndimage.label(w_im_op_cl)
    w_onesimage = np.ones(ROTIMSHAPE)
    sizes = ndimage.sum(w_onesimage, w_label_im, np.arange(1, w_nb_labels+1))
    w_coms = np.array(ndimage.measurements.center_of_mass(w_onesimage, w_label_im, np.arange(1, w_nb_labels+1)))

    #print(w_nb_labels)
    #print(sizes)
    #print(w_coms)
    
    # Plots images into a figure.
    plt.figure()
    plt.subplot(121)
    plt.imshow(w_im, cmap=plt.cm.gray)
    plt.title('Wing image')
   
    # Plot the connected components and their centers of mass.
    plt.subplot(122)
    plt.imshow(w_label_im, cmap=plt.cm.gray)
    try:
        plt.plot(w_coms.T[1], w_coms.T[0], 'ro', lw=1)
    except IndexError:
        pass
    plt.title('Connected comp = {0}'.format(w_nb_labels))
    imgname = os.path.splitext(imfile)[0]
    plt.savefig(OUTTHTESTDIR+img+'_{0}.png'.format(comp_label))
    plt.close()
        
        ##imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        ##plot_wingimage(w_im, imrois, img, comp_label, outwingdir)
        #roi_int = np.array(roimeans(w_im, imrois))
        ##fly_roi_int = np.vstack((fly_roi_int, roi_int[np.newaxis]))
        #fly_roi_int.append(roi_int)
   
    #return(fly_roi_int)   
