import os

def update_seq_date(infofile, outfile):
    '''Make sure the infofile is named so that the format is 'YYYY-MM-DD_foo.bar. Also make sure that the first five columns are the berkid, sample, indexnum, indexseq, datesent in that order. There should be one header row.
    '''
    dateseq = os.path.splitext(infofile)[0].split('_')[0]
    print(dateseq)
    with open(outfile, 'w') as g:
        with open(infofile, 'r') as f:
            next(f)
            for l in f:
                berkid, sample, indexnum, indexseq, datesent = l.split(',')[:5]
                if sample == '':
                    continue 
                g.write("UPDATE autin SET toseq=True, seqd='{0}' WHERE sample = '{1}' AND berkid = '{2}';\n".format(dateseq, sample, berkid))

def add_samplenum(tabledata, outfile):
    n = 999
    with open(tabledata, 'r') as f:
        with open(outfile, 'w') as g:
            for l in f:
                g.write(l.strip('\n') + ',{0}\n'.format(n))
                n = n+1
               
#update_seq_date('2014-05-13_RGAM_samples_for_seq.csv', '2014-0513_sql_code.sql')
update_seq_date('2014-06-25_andrea_seq.csv', '2014-0625_sql_code.sql')
#add_samplenum('2014-0403_autindb_copy_nosn.csv', '2014-0403_autindb_copy_newsn.csv')
