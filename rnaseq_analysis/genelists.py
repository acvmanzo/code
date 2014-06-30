
SFARI_PARAMS = [
'/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/sfari/autism_sfari_list_diopt.txt',
'sfari']

AUTKB_PARAMS = [
'/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/autkb/all_entrezid_unique_diopt.txt',
'autkb']

WILLIAMS_PARAMS = [
'/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/williams/williams_njem_diopt.txt',
'williams'
]

SARAH_WILLIAMS_PARAMS = [
'/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/williams/sarah_williams_genes_diopt_output.txt',
'sarah_williams'
]

def dbfilter_diopt_list(dioptfile, source):
    '''Removes entries for which there are 0 reported homologs (prints the #
    of entries at the end), removes the header, puts braces around the
    homology databases used, and adds a new column with the source of the
    gene lists (e.g., sfari, autkb, williams).
    '''

    noscore = 0
    filteredfile = dioptfile.replace('.txt','') + '_filtered.txt'
    with open(filteredfile, 'w') as g:
        with open(dioptfile, 'r') as f:
            l1 = next(f)
            for i, item in enumerate(l1.split('\t')):
                    if 'DIOPT Score' in item:
                        scoreindex = i
                    if 'Prediction Derived From' in item:
                        dbindex = i
            for l in f:
                llist = l.rstrip('\n').split('\t')
                if int(llist[scoreindex]) == 0:
                    noscore +=1
                elif int(llist[scoreindex]) > 0:
                    llist[dbindex] = '{'+llist[dbindex]+'}'
                    llist.append(source)
                    newline = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(*llist)
                    g.write(newline)
                            #g.write(l)
    print(noscore)


def main():
    #dbfilter_diopt_list(SFARI_PARAMS[0], SFARI_PARAMS[1])
    #dbfilter_diopt_list(AUTKB_PARAMS[0], AUTKB_PARAMS[1])
    #dbfilter_diopt_list(WILLIAMS_PARAMS[0], WILLIAMS_PARAMS[1])
    dbfilter_diopt_list(SARAH_WILLIAMS_PARAMS[0], SARAH_WILLIAMS_PARAMS[1])

if __name__ == '__main__':
    main()
