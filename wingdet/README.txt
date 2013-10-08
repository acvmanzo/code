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
                bgarray
                movie1.MTS
                movie/
                    mov_00001.tif
                    mov_00002.tif
                submovie/
                    submov_00001.tif
                    submov_00002.tif
                
            movie2/
                background.tif
                bgarray
                movie2.MTS
                movie/
                    mov_00001.tif
                    mov_00002.tif
                submovie/
                    submov_00001.tif
                    submov_00002.tif




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

3. 
