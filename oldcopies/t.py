####### TESTING CODE FOR FINDING INTENSITY DIFFERENCES IN ROI AND PLOTTING THE 
#RESULTING DATA ################### 


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
    ((50, 1), (False, True))]

#data = [
#    ((14, 1), (True, False)),
#    ((36, 2), (True, True)),
#    ((19, 1), (False, False)),
#    ((23, 2), (False, True))]

CONDS = {
    (True, False):     'flies_up_closed',
    (True, True):      'flies_up_ext',
    (False, True):     'flies_down_ext',
    (False, False):    'flies_down_closed'}

INFO = [
    ('flies_up_closed', 221),
    ('flies_up_ext', 222),
    ('flies_down_ext', 223),
    ('flies_down_closed', 224)]
    
#CONDS = [
#('flies_down_ext', flies_down_ext)
#]


# center_a, center_p, side_al, side_ar, side_pl, side_pr

def test_findint():

    #outtestdir = '/home/andrea/Documents/auto/results/testimgs/'
    #cmn.makenewdir(outtestdir)

    roi_ints = []
    for (filen, flyn), _ in data:
        img = 'subm00{0}'.format(filen)
        print(img)
        roi_ints.extend(find_roi_ints(img, (flyn,), outtestdir))

    d = {}
    for name in CONDS.itervalues():
        d[name] = []
    for (_, label), roi_int in zip(data, roi_ints):
        d[CONDS[label]].append(roi_int)

    with open(OUTRESDIR+'test_int', 'w') as h:
        pickle.dump(d, h)

    return d


def test_plotsome():
    
    #outtestdir = '/home/andrea/Documents/auto/results/testimgs/'
    #cmn.makenewdir(outtestdir)

    roi_ints = []
    for (filen, flyn), _ in data:
        img = 'subm00{0}'.format(filen)
        print(img)
        roi_ints.extend(find_roi_ints(img, (flyn,), OUTTESTDIR))
    
    m = np.array(roi_ints)
    side_a = np.sum(m[:, 2:4], axis=1)
    side_p = np.sum(m[:, 4:6], axis=1)
    roi_ints = np.hstack((m[:,0:2], side_a[:, np.newaxis], side_p[:, np.newaxis]))

    cond = np.array([cond for _, cond in data], dtype=np.bool)
    # center_a, center_p, side_al, side_ar, side_pl, side_pr
    
    up_ext = np.logical_and(cond[:, 0], cond[:, 1])
    up_closed = np.logical_and(cond[:, 0], np.logical_not(cond[:, 1]))
    down_ext = np.logical_and(np.logical_not(cond[:, 0]), cond[:, 1])
    down_closed = np.logical_and(np.logical_not(cond[:, 0]), np.logical_not(cond[:, 1]))

    #print(roi_ints)
    #print(roi_ints[up_closed][:, 0])
    
    plt.figure()
    plt.subplot(121)
    plt.plot(roi_ints[up_closed][:, 0], roi_ints[up_closed][:, 2], 'ro')
    plt.plot(roi_ints[up_ext][:, 0], roi_ints[up_ext][:, 2], 'bx')
    plt.xlabel('center')
    plt.ylabel('side')
    plt.title('Up')
    
    plt.subplot(122)
    plt.plot(roi_ints[down_closed][:, 1], roi_ints[down_closed][:, 3], 'ro')
    plt.plot(roi_ints[down_ext][:, 1], roi_ints[down_ext][:, 3], 'bx')
    plt.xlabel('center')
    plt.ylabel('side')
    plt.title('Down')
    plt.savefig(OUTRESDIR+'test_plotsome.png')
    
    
def test_plotsome_fly():
    
    #outtestdir = '/home/andrea/Documents/auto/results/testimgs/'
    #cmn.makenewdir(outtestdir)

    fwd_aminusp = []
    rev_aminusp = []

    extlist = []
    cllist = []

    rev_ext = []
    rev_cl = []
    fwd_ext = []
    fwd_cl = []
    
    
    for (filen, flyn), (rev, ext) in data:
        img = 'subm00{0}'.format(filen)
        print(img)
        imfile = img+EXT
        orig_im, label_im, nb_labels, coms = findflies(imfile, BODY_TH, OUTRESDIR, plot='no')
        comp_label = flyn
        orient_im = orientflies(orig_im, label_im, comp_label, coms, FLY_OFFSET, ROTIMSHAPE, img)
        w_im = findwings(orient_im, WING_TH_LOW, WING_TH_HIGH)
        imrois = defrois(CENTER_A, SIDE_AL, TMAT_FLY_IMG)
        roi_int = np.array(roimeans(w_im, imrois))
        #print(roi_int)
        center_a = roi_int[0]
        center_p = roi_int[1]
        side_a = np.sum(roi_int[2:4])
        side_p = np.sum(roi_int[4:6])
        #print(center_a, side_a)


        if rev == True:
            xc = center_a
            yc = side_a
            xw = center_p
            yw = side_p       
            rev_aminusp.append((center_p+side_p) - (center_a+side_a))

            if ext == True:
                rev_ext.append(xc-yc)
                extlist.append(xc-yc)
            else:
                rev_cl.append(xc-yc)       
                cllist.append(xc-yc)     
            
        if rev == False:
            xc= center_p
            yc = side_p
            xw = center_a
            yw = side_a
            fwd_aminusp.append((center_p+side_p) - (center_a+side_a))
            
            if ext == True:
                fwd_ext.append(xc-yc)
                extlist.append(xc-yc)
            if ext == False:
                fwd_cl.append(xc-yc)
                cllist.append(xc-yc)

        #plt.figure()
        #plt.subplot(131)
        #plt.imshow(orient_im, cmap=plt.cm.gray)
        #plt.subplot(132)       
        #plt.plot(xc, yc, 'ro')
        #plt.xlim(0, 50)
        #plt.ylim(0, 60)
        #plt.xlabel('center')
        #plt.ylabel('side')
        #plt.title('Correct orientation\n c-a={0:4f}'.format(xc-yc))
        
        #plt.subplot(133)
        #plt.plot(xw, yw, 'ro')
        #plt.xlim(0, 50)
        #plt.ylim(0, 60)
        #plt.xlabel('center')
        #plt.ylabel('side')
        #plt.title('Incorrect orientation\n c-a={0}'.format(xw-yw))
        #plt.savefig(OUTROITESTDIR+img+'_{0}.png'.format(comp_label))
        #plt.close()
        
        #plt.figure()
        #plt.imshow(orient_im, cmap=plt.cm.gray)
        #plt.title('A - P = {0}'.format((center_a+side_a) - (center_p+side_p))) 
        #plt.savefig(OUTROITESAMPTDIR+img+'_{0}.png'.format(comp_label))
        #plt.close()
        
        #plt.figure()
        #plt.imshow(orient_im, cmap=plt.cm.gray)
        #plotrois(imrois)
        #plt.title('Cl vs Ext = {0}'.format((xc-yc))) 
        #plt.savefig(OUTROITESTCETDIR+img+'_{0}.png'.format(comp_label))
        
        
        
        
    #plt.figure()
    #x_vals = np.hstack((np.tile(1, len(fwd_cl)), np.tile(2, len(fwd_ext)), np.tile(3, len(rev_cl)), np.tile(4, len(rev_ext))))
    #y_vals = fwd_cl + fwd_ext + rev_cl + rev_ext
    #plt.scatter(x_vals, y_vals)
    #plt.xticks([1,2,3,4], ['fwd_cl', 'fwd_ext', 'rev_cl', 'rev_ext'])
    #plt.savefig(OUTROITESTDIR+'comprois.png')
        
    #plt.figure()
    #x_vals = np.hstack((np.tile(1, len(fwd_cl+fwd_ext)), np.tile(2, len(rev_cl+rev_ext))))
    #y_vals = fwd_cl + fwd_ext + rev_cl + rev_ext
    #plt.scatter(x_vals, y_vals)
    #plt.xticks([1,2], ['fwd', 'rev'])
    #plt.savefig(OUTROITESTDIR+'comprois_fvsr.png')
 
    #plt.figure()
    #x_vals = np.hstack((np.tile(1, len(fwd_aminusp)), np.tile(2, len(rev_aminusp))))
    #y_vals = fwd_aminusp + rev_aminusp
    #plt.scatter(x_vals, y_vals)
    #plt.xticks([1,2], ['fwd', 'rev'])
    #plt.title('Anterior ROIs - Posterior ROIs')
    #plt.savefig(OUTROITESTDIR+'comprois_avsp.png')
   
    plt.figure()
    x_vals = np.hstack((np.tile(1, len(cllist)), np.tile(2, len(extlist))))
    y_vals = cllist + extlist
    plt.scatter(x_vals, y_vals)
    plt.xticks([1,2], ['closed', 'extended'])
    plt.title('Center-Side')
    plt.savefig(OUTROITESTDIR+'comprois_clvsext.png')


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


#d = test_findint()
#with open(OUTRESDIR+'test_int', 'r') as h:
    #d = pickle.load(h)
#print(np.array(d['flies_down_closed']).shape)

test_plotsome_fly()

#test_plotint(d, INFO)

    
    
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



        
