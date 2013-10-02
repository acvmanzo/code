from piltest2 import *

imgnums = [str(x) for x in np.arange(10, 100, 5)]
images = ['submovie00{0}'.format(n) for n in imgnums]

PARDIR = os.path.dirname(os.path.abspath('.'))
OUTRESDIR = PARDIR+'/results/'
OUTROTDIR = PARDIR+'/rotimgs/'
OUTWINGDIR = PARDIR+'/wingimgs/'
OUTTESTDIR = PARDIR+'/test/'
comp_labels = [1, 2]


for x in [OUTRESDIR, OUTROTDIR, OUTWINGDIR, OUTTESTDIR]:
	cmn.makenewdir(x)

for img in images: 
	print(img)
    imfile = img+EXT
    orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTRESDIR, plot='yes')
    fly_roi_int = []
    for comp_label in comp_labels:
        orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
        imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        plot_rotimage(orient_im, ROTIMSHAPE, FLY_OFFSET, comp_label, img, OUTROTDIR)
        w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
        plot_wingimage(w_im, imrois, img, comp_label, OUTWINGDIR)
        roi_int = np.array(roimeans(w_im, imrois))
        #fly_roi_int = np.vstack((fly_roi_int, roi_int[np.newaxis]))
        fly_roi_int.append(roi_int)
