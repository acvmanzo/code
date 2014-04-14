import os
import sys

#Old Format: 
#Date	Movie	Offset (s)	Well #	Genotype	Wing ext (m)	Wing ext (s)	Cop Suc (m)	Cop Suc (s)	Cop Att 1 (m)	Cop Att 1 (s)	Cop Att 2 (m)	Cop Att 2 (s)	Cop Att 3 (m)	Cop Att 3 (s)	Cop Att 4 (m)	Cop Att 4 (s)	Cop Att 5 (m)	Cop Att 5 (s)	Cop Att 6 (m)	Cop Att 6 (s)	Cop Att 7 (m)	Cop Att 7 (s)	Cop Att 8 (m)	Cop Att 8 (s)	Cop Att 9 (m)	Cop Att 9 (s)	Cop Att 10 (m)	Cop Att 10 (s)	Cop Att 11 (m)	Cop Att 11 (s)	Comments

#New Format:
#Movie	Movie (Ryan's code)	Genotype	Offset	Well	Courtship Behavior				
			#(min)		Min	Sec	Dur	Type	Comments


# Converts data from old autism format to new autism data format.

OLDFILE = sys.argv[1]
C_OR_A = sys.argv[2]

# To combine all the CS data:
NEWFILE_COMBINE = 'newformat_combinecs_' + OLDFILE
D_COMBINE = {
'cs-Apr': 'CS',
'cs-June': 'CS',
'cs-JW': 'CS-JW',
'cs': 'CS',
'cg30116-JW': 'CG30116-JW',
'cg30116': 'CG30116',
'bintnu': 'Betaintnu',
'pten ': 'pten',
'nhe3': 'Nhe3',
'nrxi': 'NrxI',
'nrxiv': 'NrxIV',
'en3db': 'en',
'cg34127': 'CG34127'
}


# To keep CS data separate:
NEWFILE = 'newformat_' + OLDFILE
D = {
'cs-Apr': 'CS-Apr',
'cs-June': 'CS-June',
'cs-JW': 'CS-JW',
'cs': 'CS',
'cg30116-JW': 'CG30116-JW',
'cg30116': 'CG30116',
'bintnu': 'Betaintnu',
'pten ': 'pten',
'nhe3': 'Nhe3',
'nrxi': 'NrxI',
'nrxiv': 'NrxIV',
'en3db': 'en',
'cg34127': 'CG34127'
}

def c_old2new(oldfile, newfile, d_genchange):
    '''Converts old file format to new file format for use with new code.'''

    with open(newfile, 'w') as g:
        # Writes the headers.
        g.write("Movie,Movie (Ryan's code),Genotype,Offset,Well,Courtship Behavior\n")
        g.write(" , , ,(min), ,Min,Sec,Dur,Type,Comments\n")
        with open(oldfile, 'r') as f:
            f.next()
            for l in f:
                date, movie, offset, well, genotype, wem, wes, copsucm, copsucs, copatt1m, copatt1s = l.split(',')[:11]

                if genotype in d_genchange:
                    genotype = d_genchange[genotype]

                #nd = date.split('/')
                #newdate = '{0}{1:02d}{2}'.format(nd[2], int(nd[0]), nd[1])
                newdate = date.replace('-', '')
                newmovie = '{0}T0B_{1}_c_PF24_x_x.MTS'.format(genotype, newdate)
                print newdate

                behavior = [(wem, wes, 'we'), (copatt1m, copatt1s, 'ca'), (copsucm, copsucs, 'cs')]
                
                for b in behavior:
                    # Writes the new line
                    newline = '{0},,{1},{2},{3},{4},{5},,{6}\n'.format(newmovie, genotype, offset, well, b[0], b[1], b[2])
                    g.write(newline)


def agbdict():
    d = {
    'boxing': 'b',
    'charge': 'c',
    'chase': 'ch',
    'chasing': 'ch',
    'fencing': 'f',
    'grab': 'g',
    'lunge': 'l', 
    'lunging': 'l',
    'hold': 'h',
    'push': 'p',
    'singing': 'other',
    'tumble': 't',
    'wt': 'wt',
    'wing threat': 'wt',
    'wrestling': 'w',
    }

    return(d)


def ag_old2new(oldfile, newfile, d_genchange):
    '''Converts old file format to new file format for use with new code.'''

    dbeh = agbdict()

    if os.path.exists(newfile):
        os.remove(newfile)

    with open(newfile, 'w') as g:
        # Writes the headers.
        #g.write("Movie,Movie (Ryan's code),Offset,Well,Aggressive Behavior,Escalation\n")
        #g.write(" , ,(min), ,Min,Sec,Dur,Type,Comments,Min,Sec,Dur,Type,Behaviors,Comments\n")

        btypes = []
        with open(oldfile, 'r') as f:
            #f.next()
            #f.next()
            for l in f:
                #print repr(l)
                #print l.strip('\n').split(',')

                # Define variables.
                date, movie, offset, well, genotype, flarem, flares, chm, chs, cht, otherm, others, othert, escd_m, escd_s, escd_d, escd_b, escm_m, escm_s, escm_d, escm_b = l.strip('\n').split(',')[:21]
                comm = l.split(',')[-1].strip('\n')
                
                gen = movie.strip('.MTS').split('_')[0]
                if gen in d_genchange:
                    gen = d_genchange[gen]
                movie = gen + '_' + '_'.join(movie.strip('.MTS').split('_')[1:])

                
 
                if date == '' or well == '' or movie == '':
                    print 'blank date or well', l 
               
                for k in dbeh.keys():
                    if k in othert:
                        othert = dbeh[k]
                        if dbeh[k] == 'other':
                            comm = k + ';' + comm
                
                        

                #print escd_b
                escdbl = escd_b.split(';')
                new_escdbl = []
                for b in escdbl:
                    for k in dbeh.keys():
                        if k in b:
                            new_escdbl.append(dbeh[k])
                escd_b = ';'.join(new_escdbl)
                #print escd_b

                escmbl = escm_b.split(';')
                new_escmbl = []
                for b in escmbl:
                    for k in dbeh.keys():
                        if k in b:
                            new_escmbl.append(dbeh[k])
                escm_b = ';'.join(new_escmbl)


                btypes.append(othert)
                if escd_b.split(';') != ['']:
                    btypes.extend(escd_b.split(';'))
                if escm_b.split(';') != ['']:
                    btypes.extend(escm_b.split(';'))



                if chm == 'x':
                    chd = 'x'
                elif chm == '-':
                    chd = '-'
                else:
                    chd = ''


                if flarem == 'x':
                    flared = 'x'
                else:
                    flared = ''

                if escd_m != '':
                    escd_t = 'd'
                else: 
                    escd_t = ''

                if escm_m != '':
                    escm_t = 'm'
                else:
                    escm_t = ''

    #with open('checkb.csv', 'w') as h:
        #for b in btypes:
            #if b != '':
                #h.write('{}'.format(b))
            #for k in dbeh.keys():
                #if k in b:
                    #h.write(',{},{}'.format(k, dbeh[k]))
            #if b!= '':
                #h.write('\n')    


                # Put together new lines and write to new file.
                if chm != '' or escd_m != '':
                    newline1 = '{0},,{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},\n'.format(movie, offset, well, chm,
                            chs, chd, cht, comm, escd_m, escd_s, escd_d, escd_t, escd_b)
                    g.write(newline1)
               
                if otherm != '' or escm_m != '':
                    newline2 = '{0},,{1},{2},{3},{4},,{5},{6},{7},{8},{9},{10},{11}\n'.format(movie, offset, well, otherm,
                            others, othert, comm, escm_m, escm_s, escm_d, escm_t, escm_b)
                    g.write(newline2)
                

                if flarem != '' and flarem != '-' and flarem != 'x':
                    newline3 = '{0},,{1},{2},{3},{4},{5},fl,,,,,,,,\n'.format(movie, offset, well, flarem,
                            flares, flared)
                    g.write(newline3)

    #print set(btypes)
    #print btypes

    #with open('checkb.csv', 'w') as h:
        #for b in btypes:
            #if b != '':
                #h.write('{}'.format(b))
            #for k in dbeh.keys():
                #if k in b:
                    #h.write(',{},{}'.format(k, dbeh[k]))
            #if b!= '':
                #h.write('\n')    
                
                #if genotype in d_genchange:
                    #genotype = d_genchange[genotype]

                ##nd = date.split('/')
                ##newdate = '{0}{1:02d}{2}'.format(nd[2], int(nd[0]), nd[1])
                #newdate = date.replace('-', '')
                #newmovie = '{0}T0B_{1}_c_PF24_x_x.MTS'.format(genotype, newdate)
                #print newdate

                #behavior = [(wem, wes, 'we'), (copatt1m, copatt1s, 'ca'), (copsucm, copsucs, 'cs')]
                
                #for b in behavior:
                    ## Writes the new line
                    #newline = '{0},,{1},{2},{3},{4},{5},,{6}\n'.format(newmovie, genotype, offset, well, b[0], b[1], b[2])
                    #g.write(newline)


    

if __name__ == "__main__":
    ag_old2new(OLDFILE, NEWFILE, D)
