from piltest2 import *

# ((file, fly), (reversed, extended))
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
    ((50, 1), (False, True)),
]


CONDS = [
('flies_up_closed', flies_up_closed),
( 'flies_up_ext', flies_up_ext), 
( 'flies_down_ext', flies_down_ext), 
( 'flies_down_closed', flies_down_closed)
]

INFO = [
    ('flies_up_closed', 221),
    ( 'flies_up_ext', 222), 
    ( 'flies_down_ext', 223), 
    ( 'flies_down_closed', 224)
    ]
    
#CONDS = [
#('flies_down_ext', flies_down_ext)
#]


# center_a, center_p, side_al, side_ar, side_pl, side_pr

def test_findint():

    d = {}
    for cond in CONDS:
        outtestdir = '/home/andrea/Documents/auto/results/testimgs_'+cond[0]+'/'
        cmn.makenewdir(outtestdir)
        
        d[cond[0]] = {}
        roi_ints = []
        for val in cond[1]:
            img = 'subm00{0}'.format(val[0])
            print(img)
            roi_ints.extend(find_roi_ints(img, np.array(val[1])[np.newaxis], outtestdir))
        d[cond[0]] = roi_ints

    with open(OUTRESDIR+'test_int', 'w') as h:
        pickle.dump(d, h)

    return(d)
    

def test_plotint(d, info):
    fig = plt.figure()
    
    for i in info:
        m = np.array(d[i[0]])
        
        side_a = np.sum(m[:, 2:4], axis=1)
        side_p = np.sum(m[:, 4:6], axis=1)
        newm = np.hstack((m[:,0:2], side_a[:, np.newaxis], side_p[:, np.newaxis]))

        xvals = np.ravel([np.tile(x, newm.shape[0]) for x in np.arange(1, newm.shape[1]+1)])
        #print(xvals)
        yvals = np.ravel(newm, order='F')
        #print(yvals)
        
        plt.subplot(i[1])
        plt.scatter(xvals, yvals)
        plt.xticks([1,2,3,4], ['ctr-front', 'ctr-back', 'side-front', 'side-back'])
        plt.ylabel('Mean_intensity')
        plt.title(i[0])
        plt.ylim(0, 120)
    plt.savefig(OUTRESDIR+'test_int.png')
    
d = test_findint()
#with open(OUTRESDIR+'test_int', 'r') as h:
    #d = pickle.load(h)
test_plotint(d, INFO)

    
    
#m_roi_ints = [] # Eventually a 2x2 array with the rows as the flies and the columns as the different ROIs.

#for img in IMAGES:
    #m_roi_ints.extend(find_roi_ints(img, COMP_LABEL, OUTWINGDIR))    

#print(m_roi_ints)
#print(np.array(m_roi_ints).shape)




#with open(outdir+'temp', 'w') as h:
    #pickle.dump(m_roi_ints, h)

#with open(outdir+'temp', 'r') as h:
    #m_roi_ints = pickle.load(h)

#m = np.array(m_roi_ints)

#side_a = np.sum(m[:, 2:4], axis=1)
#side_p = np.sum(m[:, 4:6], axis=1)
#newm = np.hstack((m[:,0:2], side_a[:, np.newaxis], side_p[:, np.newaxis]))


#xvals = np.ravel([np.tile(x, newm.shape[0]) for x in np.arange(1, newm.shape[1]+1)])
##print(xvals)
#yvals = np.ravel(newm, order='F')
##print(yvals)
#plt.scatter(xvals, yvals)
#plt.xticks([1,2,3], ['ctr-front', 'ctr-back', 'side-front', 'side-back'])
#plt.ylabel('Mean_intensity')
#plt.title(datum[0])
#plt.ylim(0, 50)



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
