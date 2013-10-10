# This module defines functions useful for sorting, processing and converting .MTS 
# files.

import os
import os.path
import glob
import sys
import shutil
import re
import subprocess
import numpy as np
import cmn.cmn as cmn


WINGDETBASE = 'wingdet'
EXPTSBASE = 'expts'

class FileError(Exception):
    def __init__(self, value):
       self.value = value
    def __str__(self):
       return repr(self.value)


def check(obj, overwrite):
    """Checks whether obj (file, directory) exists.
    Inputs:
    moviedir = folder with sequence of image files
    overwrite = 'yes' or 'no'; 'yes' to ovewrite image files
    """
    if os.path.exists(obj) and overwrite == 'no':
        m = '{0} already exists'.format(obj)
        raise FileError(m)
    try:
        if os.path.exists(obj) and overwrite == 'yes':
            shutil.rmtree(obj)
    except OSError as e:
        if e.errno == 20:
            os.remove(obj)

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
    cmd = 'ffmpeg -i {0} -v quiet -f image2 mov%0{1}d.{2}'.format(infile, num, ext)
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
    os.rename(avifile, os.path.join(moviedir, aviname))
    os.chdir(moviedir)
    movietoim(aviname, ext, num)
    os.rename(aviname, os.path.join(exptdir, aviname))


def b_avitoim(fdir, ext='tif', overwrite='no', num=5):
    """Converts multiple avi files to multiple sequences of images using 
    ffmpeg; images are placed in a folder based on the names of the avi files.
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
    print(moviedir)
    # Checks to make sure the movie hasn't already been converted.
    check(moviedir, overwrite)
    print('Converting MTS file to avi')
    avifile = moviename + '.avi'
    # Converting MTS to avi file.
    mtstoavi(mtsfile, avifile, start, dur, specdur, overwrite)
    print(os.getcwd())
    # Makes a new directory for image files and converts avi file to image 
    #files
    print('Converting avi to image sequence')
    avitoim(avifile, ext, overwrite)


def concatims(fdir, moviebase='movie'):
    """Combines images from two image sequences into one image sequence; 
    renames the image files of the second image sequence to be continuous 
    with the first image sequence and places them in a single folder. Often 
    for one experiment, there will be two MTS files because of the SD card
    limit (2 GB). Run from the expts/exptxx/ directory.
    Inputs:
    fdir = expts/exptxx folder containing folders with image sequences
    moviebase = name of new folder with renamed image sequence
    """
    
    exptdir = os.path.abspath(fdir)
    movies = [os.path.splitext(x)[0] for x in 
    sorted(glob.glob('*{0}'.format('MTS')))]
    newmoviedir = 'movie'
    cmn.makenewdir('movie')

    imlist1 = sorted(os.listdir(movies[0]))
    imlist2 = sorted(os.listdir(movies[1]))
    
    # Finds the number of digits in the image names.
    imn = imlist1[0] 
    l = \
    len((os.path.splitext(imn)[0].lstrip('mov').rstrip(os.path.splitext(imn)[1])))
    
    # Generates new names for the movie files in the second image folder.
    start = len(imlist1)+1
    stop = start + len(imlist2)
    newnums = ['mov{0:0{1}d}.tif'.format(n, l) for n in np.arange(start, stop, 1)]

    # Renames movies in the second image folder and moves them to the first 
    # image folder.
    os.chdir(movies[1])
    for i, imfile in enumerate(imlist2):
        newname = newnums[i]
        os.rename(imfile, os.path.join(exptdir, movies[0], newname))
    # Renames first image folder as moviebase and removes second image folder.
    os.chdir(exptdir)
    os.renames(movies[0], moviebase)
    os.rmdir(movies[1])


def exptmtstoimconcat(fdir, start1, dur1, start2, dur2, specdur, ext, overwrite, 
removeavi='no', moviebase = 'movie'):
    """Converts MTS files in the expts/exptxx/ directories to a series of images 
    using ffmpeg. Renames image files so they are contiguous and places them 
    in the folder 'movie'.
    Inputs:
    fdir - expts/exptxx/ directory
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    ext - type of image file (default is tif)
    overwrite - 'yes' or 'no'; if 'no', then the for loop will continue to the 
    next iteration if the movie/ folder already exists
    removeavi - 'yes' or 'no'; specifies whether to delete avifiles
    """
    fdir = os.path.abspath(fdir)
    check(moviebase, overwrite)
    os.chdir(fdir)
    exptmtstoavi(fdir, start1, dur1, start2, dur2, specdur)
    b_avitoim(fdir, ext, overwrite)
    os.chdir(fdir)
    concatims(fdir, moviebase)
    
    if removeavi == 'yes':
        avifiles = glob.glob('*{0}'.format('avi'))
        for avi in avifiles:
            os.remove(avi)


