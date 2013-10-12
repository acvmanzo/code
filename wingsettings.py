import numpy as np

WINGDETBASE = 'wingdet'
EXPTSBASE = 'expts'
MOVBASE = 'movie'
SUBMOVBASE = 'submovie'
PICKLEBASE = 'pickled'
PIMAGEBASE = 'images'
TEXTBASE = 'text'
PLOTBASE = 'plots'
THFIGBASE = '0_thfigs'

#BGFILE = 'background.bmp'
BGFILE = 'background.tif'
WELLPARAMSN = 'wellparams'
WELLCOORDSN = 'wellcoords'


BODY_TH = 150
#BODY_TH = 120
WING_TH_LOW = 20
WING_TH_HIGH = 90

COMP_LABEL = [1, 2]

FLY_OFFSET = np.array([75, 75])
CENTER_A = np.array([[45, 10], [65, -10]]) # top left corner and bottom diagonal corner of square
SIDE_AL = np.array([[25, 40], [45, 25]]) # top left corner and bottom diagonal corner of square
MID_L = np.array([[-15, 65], [15, 25]])
TMAT_FLY_IMG = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [FLY_OFFSET[0], FLY_OFFSET[1], 1]])

