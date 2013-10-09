Files in the 'wingdet' folder are used to identify frames in aggression
movies where wing threat is occurring.

I. Directory structure:

..aggression/
    newmovies/
        movie1.MTS
        movie2.MTS
    wingdet/
        expts/
            movie1/
                background.tif
                movie1.MTS
                movie/
                    mov_00001.tif
                    mov_00002.tif
                picklefiles/
                    bgarray
                    wellcoords
                    wellparams
                submovie/
                    submov_00001.tif
                    submov_00002.tif
                text/
                    wellcoords.txt
                    wellparams.txt
                
            movie2/
                background.tif
                movie2.MTS
                movie/
                    mov_00001.tif
                    mov_00002.tif
                picklefiles/
                    bgarray
                    wellcoords
                    wellparams
                submovie/
                    submov_00001.tif
                    submov_00002.tif
                text/
                    wellcoords.txt
                    wellparams.txt




III. Pipeline:

1. Sorting MTS files:
Place all new files in the folder 'newmovies/'. To sort and convert the MTS 
files, run the executable file 'sortmts.py'. This file moves each MTS file 
into a new folder in the directory 'wingdet', converts each file into an avi, 
converts the avi into a seqeuence of tifs, and then deletes the avi file. The 
start and duration of the portion of the MTS file to be converted can be 
specified.
    a. Python files used: sortmts.py (executable), mtslib.py

2. Background subtraction:
Generates a background image from a sequence of image files and subtracts it 
from each image. The background image and the pickled background image array 
are saved in the movie folders as 'background.tif' and 'bgarray', 
respectively. Subtracted images are placed in the 'submovie' folder. The 
number of frames and the method used to generate the background image 
(median, average) can be specified.
    a. Python files used: bgsubbatch.py (executable), bgsublib.py

3. Partitioning movie into individual wells:
Each movie has multiple wells; the rows and columns defining ROIs corresponding 
to each well must be identified. After adding new movies, run autopart.py to 
use the default parameters to partition the images. Manually alter the 
parameter files and then run manpart.py to change the ROI positions. Pickled 
parameters and coordinates are in the 'pickled' folder and text files with 
parameters and coordinates are in the 'text' folder.
    a. Python files used: autopart.py (executable), manpart.py (executable), 
    partimlib.py

4. Finding flies.
