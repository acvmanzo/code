Files in the 'wingdet' folder are used to identify frames in aggression
movies where wing threat is occurring.

I. Directory structure:
..aggression/
    newmovies/
        movie1.MTS
        movie2.MTS
    wingdet/
        movie1/
            movie1.MTS
            movie/
                movie1_00001.tif
                movie1_00002.tif
        movie2/
            movie2.MTS
            movie/
                movie2_00001.tif
                movie2_00002.tif

II. Python files:


III. Pipeline:
1. Sorting MTS files:
Place all new files in the folder 'newmovies/'. To sort and convert the MTS 
files, run the executable file 'sortmts.py'. This file moves each MTS file 
into a new folder in the directory 'wingdet', converts each file into an avi, 
converts the avi into a seqeuence of tifs, and then deletes the avi file. The 
start and duration of the portion of the MTS file to be converted can be 
specified.

