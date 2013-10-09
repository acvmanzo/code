import os
import cmn.cmn as cmn
import mtslib as ml
import glob
import numpy as np

wingdetdir = os.path.join(cmn.defpardir('.'), 'wingdet', 'expts')

def sortmtsfile2(mtsfile, wingdetdir):
    """Moves an MTS file to a directory in the folder 'wingdet'; new directory 
    has the same name as the MTS file.
    """
    files = cmn.listsortfs('.')
    print(files)

    #for i, f in enumerate(files):
        #mov = os.path.splitext(os.path.basename(f))[0][:-2]
        #print(mov)
        #for j, g in enumerate(files):
            #gtest = os.path.splitext(os.path.basename(f))[0][:-2]
            #print(x, gtest)
    for f in files:
        mtsfile = os.path.basename(f)
        print(mtsfile)
        expt = os.path.splitext(os.path.basename(f))[0][:-2]
        newdir = cmn.makenewdir(os.path.join(wingdetdir, expt))
        newmtsfile = os.path.join(wingdetdir, expt, mtsfile)
        print(newmtsfile)
        os.rename(f, newmtsfile)
    
def convfiles():
    names = glob.glob('*{0}'.format('MTS'))
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    
    for x,f in enumerate(names):
        outfile = os.path.splitext(f)[0] + '.avi'
        if x == 0:
            ml.mtsconv(f, outfile, 0, 0.5, 'yes')
        if x == 1:
            ml.mtsconv(f, outfile, 0, 0.3, 'yes')

def convimg(infile, ext='tif'):
    """Converts an avi file to a sequence of images using ffmpeg.
    Inputs:
    infile - name of avi file
    ext - type of image file (default is tif)
    """
    cmd = 'ffmpeg -i {0} -f image2 mov%05d.{1}'.format(infile, ext)
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)

def bconvimg():
    files = sorted(glob.glob('*{0}'.format('avi')))
    exptdir = os.getcwd()
    for f in files:
        os.chdir(exptdir)
        mdir = os.path.splitext(f)[0]
        cmn.makenewdir(mdir)
        os.rename(f, os.path.join(mdir, f))
        os.chdir(mdir)
        ml.convimg(f)
        os.rename(f, os.path.join(exptdir, f))

def concattifs():
    exptdir = os.getcwd()
    fs = sorted(glob.glob('*{0}'.format('avi')))
    fs = [os.path.splitext(x)[0] for x in fs]
    fd = os.path.abspath(fs[0])
    print(fd)
    tiflist1 = sorted(os.listdir(fs[0]))
    tiflist2 = sorted(os.listdir(fs[1]))

    
    start = len(tiflist1)+1
    stop = len(tiflist1)+1 + len(tiflist2)
    x = np.arange(start, stop, 1)
    x = ['mov{0:05d}.tif'.format(n) for n in x]
    

    os.chdir(fs[1])
    for i, m in enumerate(tiflist2):
        newname = x[i]
        print(m)
        print(newname)
        os.rename(m, os.path.join(fd, newname))
    
    os.chdir(exptdir)
    os.rmdir(fs[1])
    
    #for f in files:
        #os.chdir(f)
        #tifs = sorted(os.listdir('.'))
        #print(tifs)
        #os.chdir(exptdir)

#convfiles()
#bconvimg()
#concattifs()
os.rename('cs_20130619_ag_A_l_1/', 'movie')
