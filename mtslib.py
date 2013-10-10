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

class FileError(Exception):
    def __init__(self, value):
       self.value = value
    def __str__(self):
       return repr(self.value)
    
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
    """Moves an MTS file to a directory in the folder 'wingdet/expts/'; new 
    directory has the same name as the experiment that the MTS file refers to. 
    For example, if the MTS file is called 'cs_20130619_ag_A_l_1.MTS' then it is 
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
    names = sorted(names)
    
    for n in names:
        root, ext = os.path.splitext(n)
        suff = root[-1]
        print(suff)
        outfile = root + '.avi'
        if suff == '1':
            mtstoavi(n, outfile, start1, dur1, specdur)
        if suff == '2':
            mtstoavi(n, outfile, start2, dur2, specdur)


def movietoim(infile, ext, num=5):
    """Converts a movie file to a sequence of images with ext 'ext'.
    Inputs:
    infile - name of movie file
    ext - type of image file
    num - number of placeholders in the numerical part of the image name, 
    default is 5
    """
    cmd = 'ffmpeg -i {0} -f image2 mov%0{1}d.{2}'.format(infile, num, ext)
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)


def avitoim(avifile, ext='tif', overwrite='no', num=5):
    """Converts an avi file to a sequence of images; images are placed in a 
    folder based on the name of the avi file.
    Input:
    avifile = avifile to convert
    ext = extension of image file
    overwrite = 'yes' or 'no'; 'yes' to ovewrite image files
    num = number of placeholders in the numerical part of the image name, 
    default is 5
    """
    exptdir = os.path.abspath('.')
    aviname = os.path.basename(avifile)
    moviedir = os.path.splitext(aviname)[0]
    check(moviedir, overwrite)
    cmn.makenewdir(moviedir)
    print(os.getcwd())
    os.rename(avifile, os.path.join(moviedir, aviname))
    os.chdir(moviedir)
    print(os.getcwd())
    movietoim(aviname, ext, num)
    os.rename(aviname, os.path.join(exptdir, aviname))


def b_avitoim(fdir, ext='tif', overwrite='no', num=5):
    """Converts multiple avi files to multiple sequences of images using 
    ffmpeg; images are placed in a older based on the names of the avi files.
    Inputs:
    fdir = directory containing avi files
    ext = extension of image files
    overwrite = 'yes' or 'no'; 'yes' to ovewrite image files
    """
    fdir = os.path.abspath(fdir)
    os.chdir(fdir)
    avis = sorted(glob.glob('*{0}'.format('avi')))
    for x, avifile in enumerate(avis):
        print(x, avifile)
        moviedir = os.path.splitext(avifile)[0]
        check(moviedir, overwrite)
        print('Converting avi to image sequence')
        avitoim(avifile, ext, overwrite, num)
        os.chdir(fdir)
        print(os.getcwd())

def check(obj, overwrite):
    """Checks whether obj (file, directory) exists.
    Inputs:
    moviedir = folder with sequence of image files
    overwrite = 'yes' or 'no'; 'yes' to ovewrite image files
    """
    if os.path.exists(obj) and overwrite == 'no':
        m = '{0} already exists'.format(obj)
        raise FileError(m)
    if os.path.exists(obj) and overwrite == 'yes':
        shutil.rmtree(obj)    


def mtstoim(mtsfile, start, dur, specdur, ext='tif', overwrite='no'):
    """Converts a single MTS file to a series of images using ffmpeg. Run 
    from folder containing MTS file.
    Inputs:
    mtsfile - name of MTS file
    avifile - name of avi file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    ext - type of image file (default is tif)
    overwrite - 'yes' or 'no'; if no, then the script will exit if the movie 
    folder already exists
    """
    # Defines directories.
    exptdir = os.path.abspath('.')
    moviename = os.path.splitext(os.path.basename(mtsfile))[0]
    moviedir = moviename + '_movie'
    # Checks to make sure the movie hasn't already been converted.
    check(moviedir, overwrite)
    print('Converting MTS file to avi')
    avifile = moviename + '.avi'
    # Converting MTS to avi file.
    mtstoavi(mtsfile, avifile, start, dur, specdur)
    # Makes a new directory for image files and converts avi file to image 
    #files
    cmn.makenewdir(moviedir)
    os.rename(avifile, os.path.join(moviedir, avifile))
    os.chdir(moviedir)
    print('Converting avi to image sequence')
    avitoim(avifile, ext)
    # Moves avi file to original directory.
    os.rename(avifile, os.path.join(exptdir, os.path.basename(avifile)))


def exptmtstoim(fdir, start1, dur1, start2, dur2, specdur, ext, overwrite):
    """Converts MTS files in the expts/exptxx/ directories to a series of images 
    using ffmpeg. 
    Inputs:
    fdir - expts/exptxx/ directory
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    ext - type of image file (default is tif)
    boverwrite - 'yes' or 'no'; if 'no', then the for loop will continue to the 
    next iteration if the movie/ folder already exists
    """
    os.chdir(fdir)
    exptmtstoavi(fdir, start1, dur1, start2, dur2, specdur)
    b_avitoim(fdir, ext, overwrite)


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
