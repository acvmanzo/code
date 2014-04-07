import psycopg2
import numpy as np
import datetime

conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

cur.execute("SELECT * FROM autdbwiki ORDER BY rnad, genotype;")
allrows = cur.fetchall()
print allrows[0]

#y = [d[0] for d in cur.description]
#print y

colnames = [d[0] for d in cur.description]
print colnames.insert(colnames.index('qubit')+1, 'bioan_pdf')
print colnames

#dt = datetime.date(2013, 9, 15)
#print dt.isoformat()

colnames = ["'''{0}'''".format(colname) for colname in colnames]
header = '||' + '||'.join(colnames) + '||' + '\n'
print header

#with open('autdbwiki.txt' as 'w'):
    #g.write(header)

    
def date_to_link(dt):
    return "[[Andrea's Notebook/{0}|{0}]]".format(dt.isoformat())

def bioanalyzer_pdf_link(berkid, dt):
    return "[[attachment:RNASeq-Autism-BioanalyzerResults/{0}_{1}.pdf]]".format(dt.isoformat, berkid)

def identity_format(item):
    return item


l_formatter = [
('Genotype': identity_format, 'genotype'),
('Sex': identity_format, 'sex'),
('Date Frozen', date_to_link, 'frozend'),
('Date RNA Extracted', date_to_link, 'rnad'),
'rnaconc': identity_format,
'dnad': date_to_link,
'indexnum': identity_format,
'sentd': date_to_link,
'sample': identity_format,
'berkid': identity_format,
'qubit': identity_format,
'bioan_pdf': bioanalyzer_pdf_link,
'seqd': date_to_link,
'thawed': identity_format
}

row = allrows[0]

for item, col in zip(row, colnames)

#[[attachment:RNASeq-Autism-BioanalyzerResults/20140218_RGSJ006H.pdf|ok]]
