def agfreqcmd_old(kind, blist, genlist):
    '''Helper function used in dictagfreq2() that appends values to a list depending on whether a specific behavior has occurred.

    Input:
    kind = kind of behavior
    blist = list of behaviors
    genlist = list of occurrences of each behavior; if a behavior has occurred, genlist is extended
    '''
    
    if kind == 'wingthreat':
        if blist.count('wt') > 0 or blist.count('xwt') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
    
    if kind == 'charge':
        if blist.count('c') > 0 or blist.count('o') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
    
    if kind == 'anyag':
        if blist.count('c') > 0 or \
        blist.count('o') > 0 or \
        blist.count('p') > 0 or \
        blist.count('l') > 0 or \
        blist.count('ch') > 0 or \
        blist.count('g') > 0 or \
        blist.count('h') > 0 or \
        blist.count('d') > 0 or \
        blist.count('m') > 0 or \
        blist.count('wr') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
        
    
    if kind == 'escd':
        if blist.count('d') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
    
    if kind == 'escm':
        if blist.count('m') > 0:
            genlist.append(100)
        else:
            genlist.append(0)
def agdurcmd_old(kind, blist, durlist, genlist):
    
    blist, durlist = map(np.array, [blist, durlist])
    durlist = durlist.astype(int)
    
    if len(durlist) > 0:
    
        
        if kind == 'charge':
            val = np.sum(durlist[blist=='c'])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)

        if kind == 'chase':
            ind = (blist=='ch')
            val = np.sum(durlist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='escd':
            val = np.sum(durlist[blist=='d'])
            if val > 0:
                genlist.append(val)        
        if kind =='escm':
            val = np.sum(durlist[blist=='m'])
            if val > 0:
                genlist.append(val)   

def agnumcmd_old(kind, blist, genlist):
    
    blist = np.array(blist)
    
    if len(blist) > 0:    
        
        if kind == 'charge':
            ind = (blist=='c')+(blist=='o')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind == 'chargeonly':
            ind = (blist=='c')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='wingthreat':
            ind = (blist=='wt')+(blist=='xwt')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)
        
        if kind =='anyag':
            ind = (blist=='c')+(blist=='o')+(blist=='p')+(blist=='l')+\
            (blist=='g')+(blist=='h')+(blist=='g')+(blist=='wr')+(blist=='b')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind == 'chase':
            ind = (blist=='ch')
            val = len(blist[ind])
            if val > 0:
                genlist.append(val)

        if kind =='escd':
            val = len(blist[blist=='d'])
            if val > 0:
                genlist.append(val)        
        if kind =='escm':
            val = len(blist[blist=='m'])
            if val > 0:
                genlist.append(val)   
                         

