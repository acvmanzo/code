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

