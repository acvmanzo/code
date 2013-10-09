# This module defines functions useful for sorting, processing and converting .MTS 
# files.

import os
import os.path
import glob
import sys
import shutil
import cmn.cmn as cmn


def sortmtsfile(mtsfile, wingdetdir):
    """Moves an MTS file to a directory in the folder 'wingdet'; new directory 
    has the same name as the MTS file.
    """

    root, ext = os.path.splitext(os.path.basename(mtsfile))
    newdir = cmn.makenewdir(os.path.join(wingdetdir, root))
    os.rename(mtsfile, os.path.join(newdir, root+ext))


def sortmtsdir(params):
    """Run in a directory with multiple MTS files. Moves each MTS file to a new 
    directory with the same name as the MTS file.
    """
    cmn.batchfiles(sortmtsfile, params, ftype='MTS')


def mtsconv(mtsfile, outfile, start, dur, specdur='no'):
    """Converts a single MTS file to an avi file using ffmpeg.
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
   

def convmovie(mtsfile, outfile, start, dur, specdur, ext='tif', overwrite='no'):
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
    
    if os.path.exists('movie') and overwrite == 'no':
        sys.exit('Already converted.')
    if os.path.exists('movie') and overwrite == 'yes':
        shutil.rmtree('movie')
    print('Converting MTS file to avi')
    mtsconv(mtsfile, outfile, start, dur, specdur)
    cmn.makenewdir('movie')
    os.rename(outfile, 'movie/'+outfile)
    os.chdir('movie')
    print('Converting avi to image sequence')
    convimg(outfile, ext)
    os.remove(outfile)


def convmovies(fdir, start, dur, specdur, boverwrite):
    """Converts MTS files in the moviexxx directories to a series of images 
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
        outfile = os.path.splitext(mtsfile)[0] + '.avi'
        movdir = os.path.join(d, 'movie')
        if os.path.exists(movdir) and boverwrite == 'no':
            print('Already converted.')
            continue
        if os.path.exists(movdir) and boverwrite == 'yes':
            shutil.rmtree(movdir)
        convmovie(mtsfile, outfile, start, dur, specdur)


