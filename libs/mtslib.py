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


def sortmtsexpt(mtsfile, exptsdir):
    """Moves an MTS file to a directory in the expts/ folder; new 
    directory has the same name as the experiment that the MTS file refers to. 
    For example, if the MTS file is called 'cs_20130619_ag_A_l_1.MTS' then it is 
    moved to the directory 'wingdet/expt/cs_20130619_ag_A_l_1/'.
    """
    expt = os.path.splitext(os.path.basename(mtsfile))[0][:-2]
    cmn.makenewdir(os.path.join(exptsdir, expt))
    newmtsfile = os.path.join(exptsdir, expt, os.path.basename(mtsfile))
    os.rename(mtsfile, newmtsfile)
    

def b_sortmtsexpt(fdir, wingdetbase, exptsbase):
    """Moves each MTS file in a directory with multiple MTS files to a new 
    directory with the same name as the experiment referred to by the MTS 
    file (see sortmtsexpt()).
    Input:
    fdir = directory with multiple MTS files
    wingdetbase = name of wingdet/ directory
    exptsbase = name of expts/ directory
    """
    fdir = os.path.abspath(fdir)
    exptsdir = os.path.join(cmn.defpardir(fdir), wingdetbase, exptsbase)
    cmn.batchfiles(sortmtsexpt, exptsdir, ftype='MTS')
    return(exptsdir)


def mtstoavi(mtsfile, outfile, start, dur, newxdim, newydim, 
specdur='no', overwrite='no', scale='yes'):
    """Converts a single MTS file to another file format such as 'avi' using 
    mplayer. Can convert files recorded in telecine (e.g., PF24). Scales to 
    newxdim, newydim.
    Inputs:
    mtsfile - name of MTS file
    outfile - name of output file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    newxdim - new x dimension
    newydim - new y dimension
    specdur - 'no' if duration is not specified (will convert the whole movie)
    overwrite = 'yes' or 'no'; 'yes' to ovewrite avifile
    """
    cmn.check(outfile, overwrite)
    mtsinfo = mtsfile.split('_')
      
    if mtsinfo.count('PF24') == 1:
        fps = 24
    if mtsinfo.count('PF30') == 1:
        fps = 30
    
    if scale == 'yes':
        if specdur == 'yes':
            cmd = 'mencoder -ss {0} -endpos {1} {2} -noskip -nosound -quiet \
            -vf pullup,softskip,hue=0:0,scale={3}:{4} -ofps {5}/1001 -ovc raw -o \
            {6}'.format(start, dur, mtsfile, newxdim, newydim, fps*1000, outfile)
        
        if specdur == 'no':
            cmd = 'mencoder {0} -noskip -nosound -quiet \
            -vf pullup,softskip,hue=0:0,scale={1}:{2} -ofps {3}/1001 -ovc raw -o \
            {4}'.format(mtsfile, newxdim, newydim, fps*1000, outfile)
    
    if scale == 'no':
        if specdur == 'yes':
             cmd = 'mencoder -ss {0} -endpos {1} {2} -noskip -nosound -quiet \
            -vf pullup,softskip,hue=0:0 -ofps {5}/1001 -ovc raw -o \
            {6}'.format(start, dur, mtsfile, newxdim, newydim, fps*1000, outfile)           

    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)

   
def exptmtstoavi(fdir, start1, dur1, start2, dur2, specdur1, specdur2, 
newxdim, newydim, overwrite, scale):
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
            mtstoavi(n, outfile, start1, dur1, newxdim, newydim, specdur1, 
            overwrite, scale)
        if suff == '2':
            mtstoavi(n, outfile, start2, dur2, newxdim, newydim, specdur2, 
            overwrite, scale)


def movietoim(infile, ext, qscale, num):
    """Converts a movie file to a sequence of images with ext 'ext'.
    Inputs:
    infile - name of movie file
    ext - type of image file
    qscale - quality of jpeg conversion (see ffmpeg documentation)
    num - number of placeholders in the numerical part of the image name
    """
    if ext == 'jpeg':
        cmd = 'ffmpeg -i {0} -loglevel quiet -f image2 -qscale {1} \
        mov%0{2}d.{3}'.format(infile, qscale, num, ext)
    else:
        cmd = 'ffmpeg -i {0} -loglevel quiet -f image2 mov%0{1}d.{2}'.format(infile,\
        num, ext)
    
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)
    

def avitoim(avifile, ext, overwrite, num, qscale):
    """Converts an avi file to a sequence of images; images are placed in a 
    folder based on the name of the avi file.
    Input:
    avifile = avifile to convert
    ext = extension of image file
    overwrite = 'yes' or 'no'; 'yes' to ovewrite image files
    num = number of placeholders in the numerical part of the image name
    qscale = quality of jpeg conversion (1-highest; use either 1 or 3)
    """
    exptdir = os.path.abspath('.')
    aviname = os.path.basename(avifile)
    moviedir = os.path.splitext(aviname)[0]
    cmn.check(moviedir, overwrite)
    cmn.makenewdir(moviedir)
    os.rename(avifile, os.path.join(moviedir, aviname))
    os.chdir(moviedir)
    movietoim(aviname, ext, qscale, num)
    os.rename(aviname, os.path.join(exptdir, aviname))


def b_avitoim(fdir, ext, overwrite, num, qscale):
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
        cmn.check(moviedir, overwrite)
        print('Converting avi to image sequence')
        avitoim(avifile, ext, overwrite, num, qscale)
        os.chdir(fdir)
    return(avis)


def mtstoim(mtsfile, start, dur, specdur, newxdim, newydim, ext, overwrite):
    """Converts a single MTS file to a series of images using ffmpeg. Run 
    from folder containing MTS file.
    Inputs:
    mtsfile - name of MTS file
    avifile - name of avi file, including extension
    start - time to start conversion, in seconds
    dur - duration of movie to be converted, in seconds
    ext - type of image file
    overwrite - 'yes' or 'no'; if no, then the script will exit if the movie 
    folder already exists
    """
    # Defines directories.
    exptdir = os.path.abspath('.')
    moviename = os.path.splitext(os.path.basename(mtsfile))[0]
    moviedir = moviename + '_movie'
    print(moviedir)
    # Checks to make sure the movie hasn't already been converted.
    cmn.check(moviedir, overwrite)
    print('Converting MTS file to avi')
    avifile = moviename + '.avi'
    # Converting MTS to avi file.
    mtstoavi(mtsfile, avifile, start, dur, specdur, newxdim, newydim, \
    overwrite, scale)
    print(os.getcwd())
    # Makes a new directory for image files and converts avi file to image 
    #files
    print('Converting avi to image sequence')
    avitoim(avifile, ext, overwrite)


def concatims(fdir, ext, movbase):
    """Combines images from two image sequences into one image sequence; 
    renames the image files of the second image sequence to be continuous 
    with the first image sequence and places them in a single folder. Often 
    for one experiment, there will be two MTS files because of the SD card
    limit (2 GB). Run from the expts/exptxx/ directory.
    Inputs:
    fdir = expts/exptxx/ folder containing folders with image sequences
    movbase = name of new folder with renamed image sequence
    """
    
    exptdir = os.path.abspath(fdir)
    movies = [os.path.splitext(x)[0] for x in 
    sorted(glob.glob('*{0}'.format('MTS')))]
    newmoviedir = movbase
    cmn.makenewdir(movbase)

    imlist1 = sorted(os.listdir(movies[0]))
    print('test')
    try:
        imlist2 = sorted(os.listdir(movies[1]))
        # Finds the number of digits in the image names.
        imn = imlist1[0] 
        l = \
        len((os.path.splitext(imn)[0].lstrip('mov').rstrip(os.path.splitext(imn)[1])))
        
        # Generates new names for the movie files in the second image folder.
        start = len(imlist1)+1
        stop = start + len(imlist2)
        newnums = ['mov{0:0{1}d}.{2}'.format(n, l, ext) for n in np.arange(start, stop, 1)]

        # Renames movies in the second image folder and moves them to the first 
        # image folder.
        os.chdir(movies[1])
        for i, imfile in enumerate(imlist2):
            newname = newnums[i]
            os.rename(imfile, os.path.join(exptdir, movies[0], newname))
        # Removes second image folder.
        os.chdir(exptdir)
        os.rmdir(movies[1])
    except NameError:
        pass
    
    # Renames first image folder as movbase.
    os.renames(movies[0], movbase)
    


def exptmtstoimconcat(fdir, start1, dur1, start2, dur2, specdur1, specdur2, 
newxdim, newydim, ext, overwrite, scale, removeavi, movbase, num=5, qscale=3):
    """Converts MTS files in one expts/exptxx/ directory to a series of images 
    using ffmpeg. Renames image files so they are contiguous and places them 
    in the folder 'movie'.
    Inputs:
    fdir - expts/exptxx/ directory
    start1, start2 - time to start conversion, in seconds, for movies 1 and 2
    dur1, dur2 - duration of movie to be converted, in seconds, for movies 1 
    and 2
    specdur = 'yes' or 'no'; indicates whether duration is specified
    ext - type of image file
    overwrite - 'yes' or 'no'; if 'no', then the for loop will continue to the 
    next iteration if the movie/ folder already exists
    removeavi - 'yes' or 'no'; specifies whether to delete avifiles
    movbase = name of 'extxx/movie/' directory
    num = # digits for image name
    qscale = quality of jpeg (1-highest; use either 1 or 3)
    """
    fdir = os.path.abspath(fdir)
    cmn.check(movbase, overwrite)
    os.chdir(fdir)
    exptmtstoavi(fdir, start1, dur1, start2, dur2, specdur1, specdur2, 
    newxdim, newydim, overwrite, scale)
    avifiles = b_avitoim(fdir, ext, overwrite, num, qscale)
    os.chdir(fdir)
    try:
        concatims(fdir, ext, movbase)
    except IndexError:
        print('Only one MTS file')
        print(os.getcwd())
        moviefold = os.path.splitext(avifiles[0])[0]
        os.renames(moviefold, movbase)
    
    if removeavi == 'yes':
        for avi in avifiles:
            os.remove(avi)


    


def convmovies(fdir, start1, dur1, start2, dur2, specdur1, specdur2, newxdim, 
newydim, ext, overwrite, scale, removeavi, movbase, num=5, qscale=3):
    
    """Converts MTS files in the expts/exptxx/ directories to a series of images 
    using ffmpeg. Renames image files so they are contiguous and places them 
    in the folder 'movie'.
    Inputs:
    fdir - expts/ directory
    start1, start2 - time to start conversion, in seconds, for movies 1 and 2
    dur1, dur2 - duration of movie to be converted, in seconds, for movies 1 
    and 2
    specdur = 'yes' or 'no'; indicates whether duration is specified
    ext - type of image file
    overwrite - 'yes' or 'no'; if 'no', then the for loop will continue to the 
    next iteration if the movie/ folder already exists
    removeavi - 'yes' or 'no'; specifies whether to delete avifiles
    movbase = name of 'extxx/movie/' directory
    num = # digits for image name
    qscale = quality of jpeg (1-highest; use either 1 or 3)
    """
    
    dirs = cmn.listsortfs(fdir)
    for d in dirs:
        os.chdir(d)
        print(os.path.basename(d))
        print(d)
        try:
            exptmtstoimconcat(d, start1, dur1, start2, dur2, specdur1, specdur2,
            newxdim, newydim, ext, overwrite, scale, removeavi, movbase, num, qscale)
        except cmn.FileError:
            print('movie exists')
            continue

