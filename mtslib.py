# This module defines functions useful for sorting, processing and converting .MTS 
# files.

import os
import os.path
import glob
import sys
import shutil
import cmn.cmn as cmn

WINGDETBASE = 'wingdet'
EXPTSBASE = 'expts'

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


def sortmtsexpt(mtsfile, exptsdir):
    """Moves an MTS file to a directory in the folder 'wingdet/expts/'; new  directory 
    has the same name as the experiment that the MTS file refers to. For 
    example, if the MTS file is called 'cs_20130619_ag_A_l_1.MTS' then it is 
    moved to the directory 'wingdet/expt/cs_20130619_ag_A_l_1/'.
    """
    
    expt = os.path.splitext(os.path.basename(mtsfile))[0][:-2]
    cmn.makenewdir(os.path.join(exptsdir, expt))
    newmtsfile = os.path.join(exptsdir, expt, os.path.basename(mtsfile))
    os.rename(mtsfile, newmtsfile)
    

def b_sortmtsexpt():
    """Run in a directory with multiple MTS files. Moves each MTS file to a new 
    directory with the same name as the experiment referred to by the MTS 
    file (see sortmtsexpt()).
    """
    exptsdir = os.path.join(cmn.defpardir('.'), WINGDETBASE, EXPTSBASE)
    cmn.batchfiles(sortmtsexpt, exptsdir, ftype='MTS')


def mtstoavi(mtsfile, outfile, start, dur, specdur='no'):
    """Converts a single MTS file to another file format such as 'avi' using 
    ffmpeg.
    Inputs:
    mtsfile - name of MTS file
    outfile - name of output file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    specdur - 'no' if duration is not specified (will convert the whole movie)
    """
    if specdur == 'no':
        cmd = 'ffmpeg -ss {0} -i "{1}" -pix_fmt gray \
        -vf yadif -vcodec rawvideo -y -an "{2}"'.format(start, mtsfile, 
        outfile)
    if specdur == 'yes':
        cmd = 'ffmpeg -ss {0} -t {1} -i "{2}" -pix_fmt gray \
        -vf yadif -vcodec rawvideo -y -an "{3}"'.format(start, dur, mtsfile, 
        outfile)
    
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)


def exptmtstoavi(fdir, start1, dur1, start2, dur2, specdur='yes'):
    """Converts two MTS files in the same experiment folder into avi files. 
    Often for one experiment, there will be two MTS files because of the SD 
    card limit (2 GB). The two MTS files can be converted with different 
    parameters; for instance, in some later experiments, I filmed the flies 
    during the acclimation period and so scoring should occur after that 
    point. 
    Inputs:
    fdir = expts/exptxx folder containing MTS files
    start1, dur1 = Start time and duration for conversion of MTS file 
    'exptxx_1.MTS'
    start2, dur2 = Start time and duration for conversion of MTS file 
    'exptxx_2.MTS'
    specdur - 'no' if duration is not specified (will convert the entire movie)
    """
    
    names = glob.glob('*{0}'.format('MTS'))
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    
    for f in enumerate(names):
        root, ext = os.path.splitext(f)
        outfile = root + '.avi'
        if ext == '1':
            if specdur == 'yes':
                ml.mtstoavi(f, outfile, start1, dur1, specdur)
        if ext == '2':
            ml.mtstoavi(f, outfile, start2, dur2, specdur)


def avitoim(avifile, ext='tif'):
    """Converts an avi file to a sequence of images using ffmpeg.
    Inputs:
    infile - name of avi file
    ext - type of image file (default is tif)
    """
    cmd = 'ffmpeg -i {0} -f image2 mov%05d.{1}'.format(avifile, ext)
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)
   

def mtstoim(mtsfile, avifile, start, dur, specdur, ext='tif', overwrite='no'):
    """Converts a single MTS file to a series of images using ffmpeg.
    Inputs:
    mtsfile - name of MTS file
    outfile - name of output file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    ext - type of image file (default is tif)
    overwrite - 'yes' or 'no'; if no, then the script will exit if the movie 
    folder already exists
    """
    
    moviedir = os.path.splitext(os.path.basename(mtsfile))[0]
    if os.path.exists(moviedir) and overwrite == 'no':
        sys.exit('MTS file already converted.')
    if os.path.exists(moviedir) and overwrite == 'yes':
        shutil.rmtree(moviedir)
    print('Converting MTS file to avi')
    mtstoavi(mtsfile, avifile, start, dur, specdur)
    cmn.makenewdir(moviedir)
    os.rename(avifile, os.path.join(moviedir, avifile))
    os.chdir(moviedir)
    print('Converting avi to image sequence')
    avitoim(avifile, ext)



def b_mtstoim(fdir, start, dur, specdur, boverwrite):
    """Converts MTS files in the expts/exptxx directories to a series of images 
    using ffmpeg.
    Inputs:
    fdir - expt/ directory
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    ext - type of image file (default is tif)
    boverwrite - 'yes' or 'no'; if 'no', then the for loop will continue to the 
    next iteration if the movie/ folder already exists
    """
    
    dirs = cmn.listsortfs(fdir)
    for d in dirs:
        os.chdir(d)
        print(d)
        mtsfile = glob.glob('*{0}'.format('MTS'))[0]
        avifile = os.path.splitext(mtsfile)[0] + '.avi'
        movdir = os.path.join(d, 'movie')
        if os.path.exists(movdir) and boverwrite == 'no':
            print('Already converted.')
            continue
        if os.path.exists(movdir) and boverwrite == 'yes':
            shutil.rmtree(movdir)
        mtstoim(mtsfile, avifile, start, dur, specdur)


def concatims(fdir):
    """Combines images from two image sequences into one image sequence; 
    renames the image files of the second image sequence to be continuous 
    with the first image sequence and places them in a single folder. Often 
    for one experiment, there will be two MTS files because of the SD card
    limit (2 GB). Run from the expts/exptxx/ directory.
    Inputs:
    fdir = expts/exptxx folder containing MTS files
    start1, dur1 = Start time and duration for conversion of MTS file 
    'exptxx_1.MTS'
    start2, dur2 = Start time and duration for conversion of MTS file 
    'exptxx_2.MTS'
    specdur - 'no' if duration is not specified (will convert the entire movie)
    """
    
    exptdir = os.getcwd()
    movies = sorted(glob.glob('*{0}'.format('avi')))
    movies = [os.path.splitext(x)[0] for x in movies]
    print(movies)
    fd = os.path.abspath(fs[0])
    print(fd)
    #tiflist1 = sorted(os.listdir(fs[0]))
    #tiflist2 = sorted(os.listdir(fs[1]))

    
    #start = len(tiflist1)+1
    #stop = len(tiflist1)+1 + len(tiflist2)
    #x = np.arange(start, stop, 1)
    #x = ['mov{0:05d}.tif'.format(n) for n in x]
    

    #os.chdir(fs[1])
    #for i, m in enumerate(tiflist2):
        #newname = x[i]
        #print(m)
        #print(newname)
        #os.rename(m, os.path.join(fd, newname))
    
    #os.chdir(exptdir)
    #os.rmdir(fs[1])
