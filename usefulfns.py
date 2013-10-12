# This module contains functions that I wrote that aren't super useful right 
#now but might be useful in the future.

############### SORTMTS.PY ####################
### regular expresions; piping ###
# These functions acquire the output from the mplayer or ffplay process and 
#searches them using regular expression syntax.
#Processes have stdin, stdout, and stderr pipes that transmits into or out of 
#the process. When running a process in bash, the stdout pipe sends info to 
#the screen for display. The subprocess module in Python allows you to open a 
#subprocess and to read the stdout and stderr pipes. For instance, 
#subprocess.Popen((blah blah).communicate()[0] gives the stdout output and 
#.communicate[1] gives the stderr output. More info can be found in the pages 
#on the subprocess and re modules.
import re
import subprocess

def getfps(avifile):
    #pattern = re.compile(r'Input')
    mplayerOutput = subprocess.Popen(("mplayer", "-v", avifile), \
    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    print(mplayerOutput)
    #fps = pattern.search(mplayerOutput).group(0)
    #return(fps) 

def getfpsffmpeg(avifile):
    pattern = re.compile(r'Duration: \d*(:\d*)*')
    print(pattern)
    mplayerOutput = subprocess.Popen(("ffplay", "-t", "1", "-an", "-vn", avifile), \
    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1]
    print(mplayerOutput)
    fps = pattern.search(mplayerOutput).group(0)
    print(fps)
    #return(fps) 
    
    
### sorts by file name ###
def sortmtsfile(mtsfile, exptdir):
    """Moves an MTS file to a directory in the folder 'wingdet/expt'; new directory 
    has the same name as the MTS file.
    """
    root, ext = os.path.splitext(os.path.basename(mtsfile))
    newdir = cmn.makenewdir(os.path.join(exptdir, root))
    os.rename(mtsfile, os.path.join(newdir, root+ext))


def b_sortmtsfile(params):
    """Run in a directory with multiple MTS files. Moves each MTS file to a new 
    directory with the same name as the MTS file.
    """
    cmn.batchfiles(sortmtsfile, params, ftype='MTS')


# Uses ffmpeg to convert MTS files to avi files. Now I will be using mencoder.
def mtstoavi(mtsfile, outfile, start, dur, specdur='no', overwrite='no'):
    """Converts a single MTS file to another file format such as 'avi' using 
    ffmpeg.
    Inputs:
    mtsfile - name of MTS file
    outfile - name of output file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    specdur - 'no' if duration is not specified (will convert the whole movie)
    overwrite = 'yes' or 'no'; 'yes' to ovewrite avifile
    """
    check(outfile, overwrite)
    if specdur == 'no':
        cmd = 'ffmpeg -ss {0} -i "{1}" -pix_fmt gray \
        -vf yadif -vcodec rawvideo -y -an -v quiet "{2}"'.format(start, mtsfile, 
        outfile)
    if specdur == 'yes':
        cmd = 'ffmpeg -ss {0} -t {1} -i "{2}" -pix_fmt gray \
        -vf yadif -vcodec rawvideo -y -an -v quiet "{3}"'.format(start, dur, mtsfile, 
        outfile)
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)

# This version uses mencoder, but I am not forcing the ofps.
def mtstoavi(mtsfile, outfile, start, dur, specdur='no', overwrite='no'):
    """Converts a single MTS file to another file format such as 'avi' using 
    mplayer. Can convert files recorded in telecine (e.g., PF24).
    Inputs:
    mtsfile - name of MTS file
    outfile - name of output file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    specdur - 'no' if duration is not specified (will convert the whole movie)
    overwrite = 'yes' or 'no'; 'yes' to ovewrite avifile
    """
    cmn.check(outfile, overwrite)
         
    if specdur == 'yes':
        cmd = 'mencoder -ss {0} -endpos {1} {2} -noskip -nosound \
        -vf pullup,softskip,hue=0:0 -ovc raw -o {3}'.format(start, dur, 
        mtsfile, outfile)
    
    if specdur == 'no':
        cmd = 'mencoder {0} -noskip -nosound -vf pullup,softskip,hue=0:0 \
        -ovc raw -o {1}'.format(mtsfile, outfile)

    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)


####### BGSUBLIB.PY #############

def subbgim(bg, subext, submoviedir, imdir='.'):
    '''Subtracts background from each file in an image sequence.
    bg = numpy array of background image
    subext = extension of subtracted movie images
    imdir = directory containing the sequence of image files; default is 
    current directory
    submoviedir = directory to deposit the background-subtracted image files
    '''
    
    imdir = os.path.abspath(imdir)
    files = sorted(os.listdir(imdir))
    cmn.makenewdir(submoviedir)
    
    # Loads each image, subtracts the background then saves new image into 
    # submovie folder.
    for x in np.arange(0, len(files), 1):
        outbase = 'sub{0}.{1}'.format(files[int(x)], subext)
        outfile = os.path.join(submoviedir, outbase)
        c = np.array(Image.open(files[int(x)])).astype(float)
        print('c', np.shape(c))
        subarr = c-bg
        subim = Image.fromarray(np.uint8(np.absolute(subarr)))
        subim.save(outfile)


def subbgmovie(imdir, bgext, subext, bgdir, pickledir, submovdir, nframes, 
fntype, overwrite='no'):
    '''Generates background image from nframes of movie and saves in bgdir. 
    Subtracts background from each file in movie image sequence.
    Input:
    imdir = directory containing the sequence of image files
    bgdir = directory in which to save background image
    pickledir = directory in which to save pickled background image
    submoviedir = directory to deposit the background-subtracted image files
    nframes = # frames used to generate the background image; these are spread 
    evenly throughout the image sequence
    fntype = 'median, 'average'; method for combining nframes
    '''
    
    files = glob.glob('background*')
    if len(files)>0 and overwrite == 'no':
        sys.exit('Background image already generated.')

    os.chdir(imdir)
    bg = genbgim(imdir, nframes, fntype)
    savebg(bg, bgext, bgdir, pickledir)
    subbgim(bg, subext, submovdir, imdir)


def subbgmovies(fdir, submovbase, movbase, picklebase, bgext, subext, nframes, fntype, 
boverwrite):
    '''Start in folder containing movie folders; see wingdet/README.txt.
    For each movie, generates background image and subtracts background from 
    each image.
    '''
    dirs = cmn.listsortfs(fdir)
    for exptdir in dirs: 
        print(os.path.basename(exptdir))
        movdir = os.path.join(exptdir, movbase)
        submovdir = os.path.join(exptdir, submovbase)
        pickledir = os.path.join(exptdir, picklebase)
        
        if os.path.exists(submovdir) and boverwrite == 'no':
            print('Images are already background-subtracted')
            continue

        os.chdir(movdir)
        try:
            subbgmovie(imdir=movdir, bgext=bgext, subext=subext, 
            bgdir=exptdir, pickledir=pickledir, submovdir=submovdir, 
            nframes=nframes, fntype=fntype, overwrite=boverwrite)
        except AssertionError:
            print('AssertionError')
            continue


######## PARTIMLIB.PY ############

def convparams(self, imsize):
    '''Converts parameters from scaled chamber coordinates to image 
    coordinates.
    Inputs:
    imsize = image size as list [nrows x ncols] (ex., [1080 x 1920])
    '''
    imrows, imcols = imsize
    for y in [d['r'], d['rpad'], self.nrows, self.rshift]:
        y = y*imrows
    for x in [self.c, self.cpad, self.ncols, self.cshift]:
        x = x*imcols 


########### function test ##############
# Sometimes a fly sits still for the whole movie and so is incorporated into 
#the background image. I tried to write some functions to get rid of the fly
#from the background, 
#but I'm not quite sure how. Maybe the best way would be to just photoshop the 
#image to get rid of flies, if it becomes a real problem.


from libs.bglib import *
import matplotlib.pyplot as plt

files = sorted(os.listdir('movie'))
#os.chdir('movie')
#bg = np.array(Image.open(files[0])).astype(float)
bg = np.array(Image.open('background.tif')).astype(float)
plt.subplot(411)
plt.imshow(bg, cmap=plt.cm.gray)

plt.subplot(412)
thbg = np.copy(bg)
tih = thbg > 175 
#til = thbg < 5
#tib = np.intersect1d(tih, til)
#thbg[tib] = 0
thbg[tih] = 0
#thbg[til] = 0
#thbg[tih] = 0
plt.imshow(thbg, cmap=plt.cm.gray)

plt.subplot(413)
rthbg = np.copy(bg)
#rtih = rthbg < 100
rtih = rthbg < 175
rthbg[rtih] = 0
plt.imshow(rthbg, cmap=plt.cm.gray)

#plt.xlim(0, 300)
plt.subplot(414)
hist, bin_edges = np.histogram(bg, bins=60)
bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
plt.plot(bin_centers, hist, lw=2)
plt.ylim(0, 20000)

plt.savefig('bgthreshold.png', dpi=500)
plt.close()


files = sorted(os.listdir('movie'))
os.chdir('movie')
im = np.array(Image.open(files[11])).astype(float)

#negi = c < 0
#c[negi] = 0

#c = im-bg
#c = c-c.min()
#print(c.max())
#print(c.min())
#c = c/c.max()*255.0 #optional
#carr = np.uint8(c)
#plt.figure()
#plt.imshow(carr, cmap=plt.cm.gray)
#plt.savefig('../bgsub.png')

c = im - rthbg
print(c.max())
print(c.min())
c = c-c.min()
print(c.max())
print(c.min())
c = c/c.max()*255.0 #optional
carr = np.uint8(c)
plt.figure()
plt.imshow(carr, cmap=plt.cm.gray)
plt.savefig('../bgrthsub.png')
