from libs.aglib import *


FNAME = '20131119_agdata_wms_all.csv' # File with all the data.
LNAME = 'movielist.csv' # File with list of movies.
NEWFILE = '20131119_agdata_wms_sorted.csv' # Sorted file.

# Deletes the sorted file if present.
if os.path.exists(NEWFILE):
    os.remove(NEWFILE)


with open(NEWFILE, 'a') as h:

    # Using the movie list, defines the names of the two movies for each assay.
    with open(LNAME) as g:
        for k in g:
            if k.strip('\n')[-5] == '2':
                continue
            assay = k.strip('\n')[:-8]
            movie1 = k.strip('\n')
            movie2 = movie1.replace('1.MTS', '2.MTS')
            print(movie1, movie2)
            
            for x in np.arange(1, 13).tolist(): # Number of wells.
            
                # Copies the data into a new file. The data is sorted and 
                #the two movies for each assay are combined so that there is 
                #contiguous scoring for each well. So, for well 1 of assay 1, 
                #data from the first movie is followed by data from the 
                #second movie, followed by data for well 2 and so forth.
                
                for y in [movie1, movie2]:
                    with open(FNAME) as f:
                        f.next()
                        f.next()
                        for l in f:
                            #print(l)
                            lmovie = l.split(',')[0]
                            lassay = l.split(',')[0][:-8]
                            lwell = l.split(',')[3]
                            if lmovie == y and lwell == str(x):
                                h.write(l)


#with open(FNAME) as f:
    #f.next()
    #f.next()
    #f.next()
    #l = f.next()
    #adict = agline2(l)

#print(adict)

#fpos = []

#with open(LNAME) as g:
    #for l in g:
        #assay = l.strip('\n')[:-8]
        #print(assay)

        #with open(FNAME) as f:
            #f.next()
            #f.next()
            #for k in f:
                #m = k.split(',')[0][:-8]
                #if assay == m:
                    #print('match')


#print(fpos)
#print(len(fpos))


#with open(FNAME) as f:
    #f.next()
    #f.next()
    #for k in f:
        #test = k.strip('\n').split(',')[0][-5]
        #if test == '1':
            #agdict = agline2(k)
            #print(agdict)


                        
                

                    
                    
            
            
