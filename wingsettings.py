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
ROTFIGBASE = '1_rotims'
WINGFIGBASE = '2_wingims'

BGFILE = 'background.bmp'
#BGFILE = 'background.tif'
WELLPARAMSN = 'wellparams'
WELLCOORDSN = 'wellcoords'

CONFIG = (3,4)


#BODY_TH = 150
BODY_TH = 120
#WING_TH_LOW = 20
WING_TH_LOW = 25
#WING_TH_HIGH = 90
WING_TH_HIGH = 120

CENTER_A = np.array([[45, 10], [65, -10]]) # top left corner and bottom diagonal corner of square
SIDE_AL = np.array([[25, 40], [45, 25]]) # top left corner and bottom diagonal corner of square
MID_L = np.array([[-15, 65], [15, 25]])


