from piltest2 import *

IMNUMS = [str(x) for x in [14, 44, 50, 75]]
IMAGES = ['subm00'+n for n in IMNUMS]
BODY_TH = 120
COMP_LABEL = [1, 2]
FLY_OFFSET = np.array([75, 75])
ROTIMSHAPE = (150, 150)
CENTER_A = np.array([[45, 10], [65, -10]]) # top left corner and bottom diagonal corner of square
SIDE_AL = np.array([[25, 30], [55, 15]]) # top left corner and bottom diagonal corner of square
TMAT_FLY_IMG = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [FLY_OFFSET[0], FLY_OFFSET[1], 1]])
WING_TH_LOW = 20
WING_TH_HIGH = 60

m_roi_ints = [] # Eventually a 2x2 array with the rows as the flies and the columns as the different ROIs.

# center_a, center_p, side_al, side_ar, side_pl, side_pr

for img in IMAGES:
    imfile = img+EXT
    orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH)
    for comp_label in COMP_LABEL:
        orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
        imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        plot_rotimage(orient_im, ROTIMSHAPE, FLY_OFFSET, comp_label, img)
        w_im = thwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
        plot_wingimage(w_im, imrois, img, comp_label)
        roi_int = roimeans(w_im, imrois)
        m_roi_ints.append(roi_int)




        #twc_vals = []
        #twl_vals = []
        #twr_vals = []

        #d[cond[0]] = {}

        #for val in cond[1]:      
            #imgname = 'subm00{0}'.format(val[0])
            #print(imgname)
            #orig_im, label_im, nb_labels, coms = findflies(imgname+'.tif', BODY_TH)
            #rotimage = rotateflies(orig_im, label_im, val[1], coms, imgname)

        ## Figuringout how to distinguish fly orientation.
        ##plt.plot(rotimage[:, 75].T)

            ## Thresholding image to pick out wings.
            #throtimage = np.copy(rotimage)
            #low_values_indices = throtimage < 20  # Where values are low
            #high_values_indices = throtimage > 60
            #throtimage[low_values_indices] = 0
            #throtimage[high_values_indices] = 0

            ##thheadthor = throtimage[45:75, 65:85]
            ##print(thheadthor)
            ##thabd = throtimage[75:110, 65:85]
            #twc = [120, 140, 70, 90]
            #twcwing = throtimage[twc[0]:twc[1], twc[2]:twc[3]]
            #twc_vals.append(np.mean(twcwing))

            #twl = [110, 130, 40, 60]
            #twlwing = throtimage[twl[0]:twl[1], twl[2]:twl[3]]
            #twl_vals.append(np.mean(twlwing))

            #twr = [110, 130, 100, 120]
            #twrwing = throtimage[twr[0]:twr[1], twr[2]:twr[3]]
            #twr_vals.append(np.mean(twrwing))
                    
            #plt.figure()
            #plt.subplot(121)
            #plt.imshow(throtimage, cmap=plt.cm.gray)
            #plotrect(twc, 'g')
            #plotrect(twl, 'b')
            #plotrect(twr, 'b')

            #plt.subplot(122)
            #plt.plot(throtimage[:, 75].T)
            #plt.savefig('{0}{1}_test_fly{2}.png'.format(rotimgdir, imgname, val[1]))
            #plt.close()

            ##with open(areafile, 'a') as f:
                ##for area in [('twcwing', twcwing), ('twlwing', twlwing), ('twrwing', twrwing)]:
                    ##f.write('{0}\tfly {1}\t{2}\t{3}\n'.format(imgname, x, area[0], np.mean(area[1])))
                        
            #with open('{0}{1}'.format(outdir, areasumfile), 'w') as g:
                #g.write('Summary of area intensity means\n')
                #g.write('Mean intensity middle\t{0}\n'.format(np.mean(twc_vals)))
                #g.write('Mean intensity left\t{0}\n'.format(np.mean(twl_vals)))
                #g.write('Mean intensity right\t{0}\n'.format(np.mean(twr_vals)))

        #d[cond[0]]['twc_vals'] = twc_vals
        #d[cond[0]]['twl_vals'] = twl_vals
        #d[cond[0]]['twr_vals'] = twr_vals
