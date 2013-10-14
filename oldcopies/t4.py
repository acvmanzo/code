from piltest2 import *

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


for (imnum, flyn),_ in data:
    img = 'subm00{0}'.format(imnum)
    print(img, flyn)
    comp_labels = [flyn,]
    x = find_roi_ints(img, comp_labels, OUTWINGDIR)
    plt.close()
