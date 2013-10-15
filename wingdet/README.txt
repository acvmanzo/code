Files in the 'wingdet' folder are used to identify frames in aggression
movies where wing threat is occurring.

I. Directory structure:

..aggression/
    newmovies/
        movie1.MTS
        movie2.MTS
    wingdet/
        expts/
            genotype_date_PFxx_A_side/
                0_thfigs/
                1_rotims/
                2_wingims/
                background.tif
                genotype_date_PFxx_A_side_1.MTS
                genotype_date_PFxx_A_side_2.MTS
                movie/
                    mov00001.jpeg
                    mov00002.jpeg
                pickled/
                    bgarray.npy
                    wellcoords
                    wellparams
                text/
                    wellcoords.txt
                    wellparams.txt
                wells.png
                
            genotype_date_PFxx_B_side/




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


IV. Observations

1. How matplotlib treats images and points:
To display an array representing an image in matplotlib, the function imshow()
is used, with the array as the argument. In this case, matplotlib plots the 
array such that the top left corner is [0,0], the vertical (y) axis corresponds 
to the rows of the array, and the horizontal (x) axis corresponds to the columns 
of the array. When plotting points on the image using plot(), the normal 
convention of giving the x coordinate followed by the y coordinate is 
maintained, but the points are plotted on this image axis. The axis limits [xmin, xmax, ymin, ymax] of this plot is: [0, #cols, #rows, 0].
