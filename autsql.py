import os

def update_seq_date(infofile, outfile):
    dateseq = os.path.splitext(infofile)[0].split('_')[0]
    print dateseq
    with open(outfile, 'w') as g:
        with open(infofile, 'r') as f:
            f.next()
            for l in f:
                berkid, sample, indexnum, indexseq, datesent, readtype, length, numlanes, qpcr = l.split(',')
                g.write("UPDATE autin SET toseq=True, seqd='{0}' WHERE sample = '{1}';\n".format(dateseq, sample))

def add_samplenum(tabledata, outfile):
    n = 999
    with open(tabledata, 'r') as f:
        with open(outfile, 'w') as g:
            for l in f:
                g.write(l.strip('\n') + ',{0}\n'.format(n))
                n = n+1
                
#update_seq_date('2014-04-01_samples_for_sequencing.csv', '2014-0401_sql_code.sql')
add_samplenum('2014-0403_autindb_copy_nosn.csv', '2014-0403_autindb_copy_newsn.csv')
