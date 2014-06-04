# Code for formatting csv table to add the date.

with open('20140319_db_date.csv', 'w') as g:
    with open('20140319_db.csv', 'r') as f:
        for l in f:
            elist = l.split(',')
            for i, e in enumerate(elist):
                if '|' in e:
                    elist[i] = e.strip(']]').split('|')[1]
                    if elist[i][-1] != 'i':
            newelist = ','.join(elist)
            g.write(newelist)
