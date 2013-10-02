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

    outtestdir = '/home/andrea/Documents/auto/results/testimgs/'
    cmn.makenewdir(outtestdir)

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



        
