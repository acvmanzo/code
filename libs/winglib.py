
import os
import numpy as np
from scipy import ndimage
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import cmn.cmn as cmn
import pickle
import libs.genplotlib as gpl
from wingsettings import *
import cv2
import cv

MIRRY = np.array([[-1, 0], [0, 1]])
MIRRX = np.array([[1, 0], [0, -1]])
START = time.time()

######### FUNCTIONS FOR BACKGROUND SUBTRACTION ########

def bgsub(bgarray, imfile):
    '''Loads background array from pickle file and image from imfile. 
    Subtracts background from image.
    Inputs:
    bgpickle = pickled file containing background array (pickled/bgarray)
    imfile = one file from the movie image sequence
    '''
    
    bg = bgarray
    im = cv2.imread(imfile, 0)
    subimarr = np.clip(bg-im, 0, 255).astype(np.uint8)
    #print('subim max', np.max(subimarr))
    #print('subim min', np.min(subimarr))
    return(subimarr)


############# FUNCTIONS FOR DETECTING FLIES AND WINGS ##############

####### HELPER FUNCTIONS ###########

def loadwells(wcfile):
    with open(wcfile, 'r') as f:
        wells = pickle.load(f)
    return(wells)


def findflies(subimarray, well, t):

    # Load the image.
    r1, r2, c1, c2 = well
    nrows = r2-r1
    ncols = c2-c1

    orig_im = subimarray[r1:r2, c1:c2]
    img = np.copy(orig_im)
    # Threshold image.
    th_im = np.copy(img)
    cv2.threshold(src=img, thresh=t, maxval=255, 
    type=cv2.THRESH_BINARY, dst=th_im)
    # Binary closing.
    close_im = np.copy(th_im)
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    cv2.morphologyEx(src=th_im, op=cv2.MORPH_CLOSE, kernel=structure, 
    dst=close_im)
    # Find contours.
    contim = np.copy(close_im)
    contours, hier = cv2.findContours(contim, mode=cv2.RETR_LIST, 
    method=cv2.CHAIN_APPROX_NONE)
    # Find areas and centers of mass of contours.
    contpics = []
    ccoms = []
    #careas = []
    careascv = []
       
    for x, contour in enumerate(contours):
        #print('x', x)
        contpic = np.zeros(np.shape(img))
        cv2.drawContours(image=contpic, contours=contours, contourIdx=x, 
        color=(255,255,255), thickness=cv.CV_FILLED)
        
        # Finding COM another way:
        #origdim = np.shape(orig_im)
        #posarray = np.rollaxis(np.mgrid[0:origdim[0], 0:origdim[1]], 0, 3)
        #comppos = posarray[contpic==255]
        #cmean = np.mean(comppos, axis=0)
        #cmean = [cmean[1], cmean[0]]
        
        cmean = np.mean(contour, axis=0)

        # Two ways of finding areas of contour.
        #carea = np.sum(contpic)/255.
        careacv = cv2.contourArea(contours[x])
        
        #if carea > 0.0011*(nrows*ncols):
            #contpics.append(contpic)
            #ccoms.extend(cmean)
            #careascv.append(carea)
        if careacv > 0.0011*(nrows*ncols):
            contpics.append(contpic)
            ccoms.extend(cmean)
            #ccoms.append(cmean)
            careascv.append(careacv)
    #print('careascv', careascv)
    #print('ccoms', ccoms)
    d = {'orig_im':orig_im, 'th_im':th_im, 'close_im':close_im, 
    'contim':contim, 'contpics':contpics, 'contareas':careascv, 
    'coms':np.array(ccoms), 'contours':contours, 'dim':np.shape(orig_im)}
    
    return(d)


def orientflies(orig_im, contpics, coms, flynum, fly_offset, rotimshape):

    # Create an array where each entry is the index.
    origdim = np.shape(orig_im)
    posarray = np.rollaxis(np.mgrid[0:origdim[0], 0:origdim[1]], 0, 3)
    # Find the coordinates of the points comprising each connected component.
    comppos = posarray[contpics[flynum] == 255]
    #centroid = np.mean(comppos, axis=0)
    centroid = [coms[flynum][1], coms[flynum][0]]
    # Mean subtract data.
    comppos = comppos - centroid
    # Singular value decomposition
    u, singval, eigenv = np.linalg.svd(comppos, full_matrices=False)
    #print('Eigenshape', eigenv.shape)
    # Orient image.
    flyoffset = fly_offset*-1
    imgoffset = np.dot(flyoffset, 0.5*eigenv)
    rotimage = ndimage.interpolation.affine_transform(orig_im, 0.5*eigenv.T, 
    centroid + imgoffset, output_shape = rotimshape, order=1)
    return(rotimage)


def findwings(orient_im, low_value, high_value):
    ''' Thresholds image to pick out wings.
    Input:
    orient_im = image of oriented fly
    low_value = scalar; values below this are set to 0
    high_value = scalar; values above this set to 0
    Output:
    w_im = thresholded image
    '''   
    w_im = orient_im
    low_values_indices = w_im < low_value  # Where values are below low_value
    high_values_indices = w_im > high_value
    w_im[low_values_indices] = 0
    w_im[high_values_indices] = 0
    
    return(w_im)

############# FUNCTIONS FOR PLOTTING FLY IMAGES #############

def plotfindflies(d, imname, wellnum):
    '''Plots a figure showing different processing steps in findflies().
    Input:
    d = dictionary; output of findflies()
    imname = name of image frame
    wellnum = number of well
    '''
    # Plots original image.
    plt.subplot2grid((2,3), (0,0), colspan=1)
    plt.imshow(Image.fromarray(d['orig_im']), cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('BGsub')

    # Plot a histogram of the intensities.
    plt.subplot2grid((2,3), (1,0), colspan=3)
    hist, bin_edges = np.histogram(d['orig_im'], bins=60)
    bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
    plt.plot(bin_centers, hist, lw=2)
    plt.ylim(0, 400)
    plt.xlim(0, 300)
    plt.title('Intensity histogram')

    # Plot the threshholded image.
    plt.subplot2grid((2,3), (0,1), colspan=1)
    plt.imshow(d['th_im'], cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('Thresholded')

    # Plots the smoothed image.
    #plt.subplot2grid((2,3), (1,1), colspan=1)
    #plt.imshow(d['close_im'], cmap=plt.cm.gray)
    #plt.axis('off')
    #plt.title('Binary closing')
    
    # Plots the smoothed image.
    plt.subplot2grid((2,3), (0,2), colspan=1)
    plt.imshow(d['close_im'], cmap=plt.cm.gray)
    plt.plot(d['coms'].T[0], d['coms'].T[1], 'ro', markersize=3)
    #print(d['coms'])
    #print(np.shape(d['coms']))
    for x in range(len(d['coms'].T[0])):
        s = '{0}'.format(x)
        plt.text(d['coms'][x, 0], d['coms'][x, 1]-25, s, color='r', fontsize=9,
        weight='bold')
    #plt.axis('off')
    plt.title('Flies={0}'.format(len(d['coms'])))
    rows, cols = d['dim']
    plt.axis((0, cols, rows, 0))


def expt_findplotflies(bgpickle, movbase, wells):
    '''Start from experiment folder.
    Input:
    bgpickle = pickled file containing bgarray
    movbase = name of movie/ directory
    wells = list of well coordinates
    '''
    os.chdir(movbase)
    files = cmn.listsortfs(fdir)
    #print('load bgpickle', time.time()-START)
    bgarray = np.load(bgpickle).astype(np.int16) + 5
    for f in files:
        # To compute for each image:
        subim = bgsub(bgarray, f)
        # To load from a saved image:
        #subimfile = os.path.join('../'+SUBMOVBASE, 'sub'+f)
        #subim = np.array(Image.open(subimfile)).astype(float)
        imanme = os.path.splitext(f)[0]
        for n, well in enumerate(wells):
            #print('Well', n)
            try:
                d = findflies(subim, imfile, well, BODY_TH, 'no')
                plotfindflies(d, imname, n)
                saveexptfig(THFIGDIR, imname, n)
            except IndexError:
                print('No connected components')
                continue  


def plotrotim(orient_im, rotimshape, fly_offset, wellnum, flynum, imname, outdir):
    # Plot oriented image.
    welldir = os.path.join(outdir, 'well{0:02d}'.format(wellnum))
    cmn.makenewdir(welldir)
    #plt.figure()
    plt.imshow(orient_im, cmap=plt.cm.gray)
    plt.plot([0, rotimshape[1]], fly_offset, 'r-') 
    plt.plot(fly_offset, [0, rotimshape[0]], 'r-') 

    
def plotrois(imrois):
    cols = np.tile(['b', 'g', 'r', 'c', 'm', 'y', 'w'], 2)
    cols = cols[:np.shape(imrois)[0]+1]
    for x, ((r1,c1), (r2,c2)) in enumerate(np.sort(imrois, axis=1)):
        gpl.plotrect([r1, r2, c1, c2], color=cols[x])
        plt.text(c1, r1, '{0}'.format(x), color=cols[x])


def plotwingim(w_im, imrois, imname, flynum, outdir, wellnum):
    cmn.makenewdir(outdir)
    #plt.figure()
    plt.imshow(w_im, cmap=plt.cm.gray)
    plotrois(imrois)
    

def saveexptfig(figdir, imname, wellnum, flynum):
    welldir = os.path.join(figdir, 'well{0:02d}'.format(wellnum))
    cmn.makenewdir(welldir)  
    
    if flynum == 'none':
        plt.savefig(os.path.join(welldir, '{0}_thfig.png'.format(imname)))
    else:
        plt.savefig(os.path.join(welldir, '{0}_fly{1}.png'.format(imname, 
        flynum)))
    
    plt.close()

def savetestfig(figdir, imname, wellnum, flynum):
    cmn.makenewdir(figdir)
    
    if flynum == 'none':
        plt.savefig(os.path.join(figdir, '{0}_{1:02d}.png'.format(imname, 
        wellnum)))
    else:
        plt.savefig(os.path.join(figdir, '{0}_{1:02d}_fly{2}.png'.format(imname, 
        wellnum, flynum)))
    
    plt.close()

def plotwellint(d, imname, thfigdir, rotfigdir, wingfigdir):
    # Plotting functions.
    print("Plotting")
    plotfindflies(d, imname, thfigdir)
    saveexptfig(thfigdir, imname, d['wellnum'], 'none')

    for flyn in range(len(d['flyims'])):
        #plotrotim(d['flyims'][flyn]['orient_im'], d['rotimshape'], 
        #d['flyoffset'], d['wellnum'], flyn, imname, rotfigdir)
        #saveexptfig(rotfigdir, imname, d['wellnum'], flyn)
        plotwingim(d['flyims'][flyn]['w_im'], d['imrois'], imname, flyn, 
        wingfigdir, d['wellnum'])
        saveexptfig(wingfigdir, imname, d['wellnum'], flyn)
        
        plt.close()

def plotwellinttest(d, imname, thfigdir, rotfigdir, wingfigdir):
    # Plotting functions.
    plotfindflies(d, imname, thfigdir)
    savetestfig(thfigdir, imname, d['wellnum'], 'none')

    for flyn in range(len(d['flyims'])):
        plotrotim(d['flyims'][flyn]['orient_im'], d['rotimshape'], 
        d['flyoffset'], d['wellnum'], flyn, imname, rotfigdir)
        savetestfig(rotfigdir, imname, d['wellnum'], flyn)
        plotwingim(d['flyims'][flyn]['w_im'], d['imrois'], imname, flyn, 
        wingfigdir, d['wellnum'])
        savetestfig(wingfigdir, imname, d['wellnum'], flyn)
        
        plt.close()


######### FUNCTIONS FOR DEFINING ROIS #################

def tmatflyim(flyoffset):
    
    a = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [flyoffset[0], flyoffset[1], 1]])
    return(a)


def region(center_a, side_al, mid_l):

    ''' Input:
    center: 2x2 numpy array with x, y coordinates of two opposite corners of 
    center rectangle: [[x1, y1], [x2, y2]]
    side: 2x2 numpy array with x, y coordinates of two opposite orners of 
    side rectangle
    
    Ccoordinates are written so that AP axis is x (so that angle 0 is when the
    fly is pointing along x axis, positive is in the anterior direction), and 
    the ML axis is y, positive is going to the left).
    '''
    center_p = np.dot(center_a, MIRRY)
    side_ar = np.dot(side_al, MIRRX)
    side_pl = np.dot(side_al, MIRRY)
    side_pr = np.dot(side_pl, MIRRX)
    mid_r = np.dot(mid_l, MIRRX)
    
    return(center_a, center_p, side_al, side_ar, side_pl, side_pr, mid_l, mid_r)
    

def changecoord(tmat, pts):
    '''
    Inputs: 
    tmat = transformation matrix (homogenous coordinates)
        ex. tmat = np.array([
        [0, 1, 0],
        [-1, 0, 0],
        [offsetx, offsety, 1]])
        where offsetx, offsety are the center of the new axes. This matrix 
        transforms points in fly coordinates to fly image coordinates.
        
    pts = coordinates in original axes (2x2 numpy array)
    '''
    return np.dot(pts, tmat[:-1, :-1]) + tmat[-1, :-1]


def defrois(center_a, side_al, mid_l, tmat):
    '''
    Input: 
    orient_im = image in which fly is aligned vertically along its AP axis; 
    output of orientflies()
    '''
  
    # Define regions of interest in fly coordinates.
    #center_a = [[30, 65], [10, 85]] # In image coordinates
    #side_al = [[40, 40], [20, 60]]

    rois = region(center_a, side_al, mid_l) 
    # center_a, center_p, side_al, side_ar, side_pl, side_pr, mid_l, mid_r  = rois
    
    # Convert regions of interest to fly image coordinates.
    imrois = changecoord(tmat, rois)
    
    return(imrois)

######### FUNCTIONS FOR ANALYZING ROI INTENSITIES #################

def roimeans(w_im, imrois):
    '''
    Input:
    w_im = image of oriented fly, threshholded to isolate wings
    imrois = list of points that define regions of interest in the image 
    coordinates; returned by defrois(); the order or rois are: 
        center_a, center_p, side_al, side_ar, side_pl, side_pr, mid_l, mid_r
    Output:
    roi_int: list of mean intensities 
    '''
       
    ## Measure mean intensity over each ROI.
    roi_int = []
    for (r1,c1), (r2,c2) in np.sort(imrois, axis=1):
        roi_int.append(np.mean(w_im[r1:r2, c1:c2]))
    return(roi_int)


def subroi(roi_int):
    center_a = roi_int[0]
    center_p = roi_int[1]
    side_a = np.sum(roi_int[2:4])
    side_p = np.sum(roi_int[4:6])
    med = np.sum(roi_int[6:8])
    
    return(center_a, center_p, side_a, side_p, med)


########### COMBINED FUNCTIONS FOR ANALYSIS ###################

def wellint(subim, well, wellnum):
    '''Finds the difference in ROI intensities for each fly in one well of 
    one movie frame.
    Inputs:
    subim = background-subtracted image array
    well = coordinates of well
    plotfile = 'yes' or 'no'; indicates whether to plot files
    thfigdir = directory to plot threshold figures
    
    '''
    #subim = np.array(Image.open(os.path.join('submovie', 'sub'+imfile))).astype(float)
    
    # Finding flies.
    #print('Finding flies', time.time()-START)
    d = findflies(subim, well, BODY_TH)
    if len(d['contareas']) == 0:
        print(wellnum, 'No connected components')
    
    # Defines roi coordinates.
    rotimshape = 0.5*np.array(d['dim'])
    flyoffset = np.array(0.5*rotimshape)        
    tmatfly = tmatflyim(flyoffset)
    imrois = defrois(CENTER_A, SIDE_AL, MID_L, tmatfly)
    
    d['rotimshape'] = rotimshape
    d['flyoffset'] = flyoffset
    d['wellnum'] = wellnum
    d['imrois'] = imrois
    d['flyims'] = {}

    flysmc = []
    flymmc = []
    flyroi = []
    # Finds data for each fly in the well.
    #for flyn, comp_label in enumerate(d['uselab']):
    for flyn, com in enumerate(d['coms']):
        #print('flyn', flyn)
        #print('coms', com)
        # Orients flies.
        orient_im = orientflies(d['orig_im'], d['contpics'], d['coms'], 
        flyn, flyoffset, rotimshape)
        orient_pic = np.copy(orient_im)
        # Thresholds fly image to find wings.
        #print('Finding wings', time.time()-START)
        w_im = findwings(orient_pic, WING_TH_LOW, WING_TH_HIGH)      
        # Analyzes ROI intensities.
        #print('Analyzing ROI intensities', time.time()-START)
        roi_int = np.array(roimeans(w_im, imrois))
        center_a, center_p, side_a, side_p, med = subroi(roi_int)

        if ((center_p+side_p) - (center_a+side_a)) > 0:
            flysmc.append(side_p - center_p)
            flymmc.append(med - center_p)

        else:
            flysmc.append(side_a - center_a)
            flymmc.append(med - center_a)
    
        flyroi.append(roi_int)

        #d['flyims'][flyn]['orient_im'] = orient_im
        d['flyims'][flyn] = {}
        d['flyims'][flyn]['orient_im'] = orient_im
        d['flyims'][flyn]['w_im'] = w_im
        
    return(flysmc, flymmc, flyroi, d)


def frameint(exptfiles, bgarray, imfile, plotfiles):
    '''Finds the difference in ROI intensities for each fly in each well 
    in one movie frame. 
    Inputs:
    exptfiles = exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, extfigdir, bgpickle, wcpickle (output of 
    wingsettings.getexptfiles())
    bgarray = array of background file
    imfile = image from movie
    plotfiles = 'yes' or 'no'; whether or not to plot files
    '''

    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, extfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    #print('Finding subtracted movie', time.time()-START)
    subim = bgsub(bgarray, imfile)
    wells = loadwells(wcpickle)
    framesmc = np.empty((1, len(wells)))
    framemmc = np.empty((1, len(wells)))
    frameroi = []
    imname = os.path.splitext(os.path.basename(imfile))[0]
    
    for n, well in enumerate(wells):
        #print(n, time.time()-START)
        try:
            flysmc, flymmc, flyroi, d = wellint(subim, well, n)
            #print('Appending mov ROI intensities', time.time()-START)
            framesmc[0,n] = np.max(flysmc)
            framemmc[0,n] = np.max(flymmc)
            frameroi.append(flyroi)
            
            if plotfiles == 'yes':
                plotwellint(d, imname, thfigdir, rotfigdir, wingfigdir)
        except ValueError:
            print(imname)
            continue

    return(framesmc, framemmc, frameroi)


def multimint(exptfiles, images, plotfiles, savemc):
    '''Finds the difference in ROI intensities for each fly in each well 
    in multiple images.
    Inputs:
    exptfiles = exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, bgpickle, wcpickle (output of 
    wingsettings.getexptfiles())
    images = list of image names
    plotfiles = 'yes' or 'no'; whether or not to plot files
    picklefiles = 'yes' or 'no'; whether or not to pickle output
    '''
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, extfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    bgarray = np.load(bgpickle).astype(np.int16) + 5
    fps = int(getfps(exptdir))

    movlen = len(images)
    wells = loadwells(wcpickle)
    movsmc = np.empty((len(images), len(wells)))
    movmmc = np.empty((len(images), len(wells)))
    movroi = []
    
    for frame, imfile in enumerate(images):
        if frame % (60.*fps) == 0:
            
            print(os.path.basename(imfile), '{0} min'.format(frame/(60.*fps)),
            time.strftime("%H:%M:%S", time.localtime()))
        framesmc, framemmc, frameroi = frameint(exptfiles, bgarray, imfile, 
        plotfiles)
        movsmc[frame,:] = framesmc
        movmmc[frame,:] = framemmc
        movroi.append(frameroi)
    #print('Saving arrays', time.time()-START)
    if savemc == 'yes':
    # Save as .npy arrays.
        smcfile = os.path.join(pickledir, SMCFILE)
        mmcfile = os.path.join(pickledir, MMCFILE)
        roifile = os.path.join(pickledir, ROIFILE)
        np.save(smcfile, movsmc)
        np.save(mmcfile, movmmc)
        np.save(roifile, movroi)
    
    return(movsmc, movmmc, movroi)
        

def exptint(exptfiles, plotfiles, save):
    '''Finds the difference in ROI intensities for each fly in each well 
    in multiple movieframes.
    '''
    exptdir, movdir, submovdir, pickledir, textdir, plotdir, thfigdir, \
    rotfigdir, wingfigdir, extfigdir, bgpickle, wcpickle, smcfile, mmcfile = exptfiles
    
    frames = cmn.listsortfs(movdir)

    movsmc, movmmc, movroi = multimint(exptfiles, frames, plotfiles, save)

    return(movsmc, movmmc, movroi)


########## FUNCTIONS FOR PLOTTING ROI INTENSITY DIFFERENCES ###############

def window(winlen):    
    wind = list(np.ones(winlen)/winlen)
    return(wind)


def getfps(exptdir):
    '''Finds fps from the name of the exptdir.
    '''
    info = os.path.basename(os.path.abspath(exptdir)).split('_')
    if info.count('PF24') == 1:
        fps = 24
    if info.count('PF30') == 1:
        fps = 30
    return(fps)


def movavg(dur, fps, trace):
    '''Applies a moving average filter to a trace.
    Inputs:
    dur = duration of filter in seconds
    fps = frames per second of movie
    trace = 1d array to convolve
    Output:
    ctrace = convolved trace
    '''
    frames = dur*fps
    wind = window(frames)
    ctrace = np.convolve((trace), wind, 'same')
    return(ctrace)


def plotextwell(smc, mmc, fps, plotlen, usemovavg, movavgdur):
    '''Plots the difference traces.
    smc, mmc = arrays (frames x well) showing the difference between ROIs for 
    each well over a movie; output of multimint() or exptint()
    fps = fps of movie
    plotlen = duration of each subplot, in seconds
    movavg = whether or not a moving average filter should be applied
    movavgdur = duration of moving average filter in seconds
    '''
    
    if usemovavg == 'yes':
        smc, mmc = [movavg(movavgdur, fps, x) for x in [smc, mmc]]
    
    # Duration of signal in seconds.
    dur = len(smc)/float(fps)
    # List of subplots.
    numplots = range(np.int(np.ceil(dur/plotlen)))
    subplots = (len(numplots), 1)
    # X-values in seconds.
    xvals = np.linspace(0, dur, len(smc))
    # Max value of smc and mmc.
    plotmax = np.max([np.max(smc), np.max(mmc)])
    
    # Set initial figure and font properties.
    mpl.rc('axes', linewidth=2)
    fontv = mpl.font_manager.FontProperties()
    fontv.set_size(25)
    figh = 5*len(numplots)
    plt.figure(figsize=(30,figh), dpi=200)
       
    for x in numplots:
        # Indices for each subplot.
        li = 0 + x*plotlen*fps
        ri = plotlen*fps + x*plotlen*fps
        #Plot smc and mmc. 
        ax = plt.subplot2grid(subplots, (x,0), colspan=1)    
        plt.plot(xvals[li:ri], smc[li:ri], 'r', lw=2, label='side-center')  
        plt.plot(xvals[li:ri], mmc[li:ri], 'b', lw=2, label='middle-center')
        # Set x-limits and y-limits.
        xmin = xvals[li]
        xmax = plotlen*x+plotlen
        plt.xlim(xmin, xmax)    
        plt.ylim(0, 1.2*plotmax)
        # Change x-axis labels to time format.
        xlist = np.linspace(xmin, xmax, 10)
        xtime = [time.strftime('%M:%S', time.gmtime(x)) for x in xlist]
        plt.xticks(xlist, xtime, fontproperties=fontv)

    plt.suptitle('Wing extension', fontsize=30)
    plt.legend(fontsize=20)


def saveextwell(wellnum, figdir):
    '''Save intensity plot for each well.'''
    cmn.makenewdir(figdir)
    plt.savefig(os.path.join(figdir, 'wingext_well{0:02d}.png'.format(wellnum)))
    plt.close()

      
def plotextexpt(exptdir, smcfile, mmcfile, figdir, plotlen, usemovavg, movavgdur):
    '''For each experiment, plots the ROI intensity differences for each well 
    and saves each plot.
    '''
    movsmc, movmmc = map(np.load, [smcfile, mmcfile])
    
    fps = getfps(exptdir)
    for well in range(np.shape(movsmc)[1]):
        smc = movsmc[:,well]
        mmc = movmmc[:,well]
        plotextwell(smc, mmc, fps, plotlen, usemovavg, movavgdur)
        saveextwell(well, figdir)


