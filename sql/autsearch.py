import psycopg2
import numpy as np
import datetime

conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

cur.execute("select sample, indexnum from autin where cdnad = '2014-03-20';")
allrows = cur.fetchall()
print allrows

l_formatter = [
('genotype', identity_format, 'Genotype'),
('sex', identity_format, 'Sex'),
('frozend', date_to_link, 'Date Frozen'),
('rnad', date_to_link, 'Date RNA Extracted'),
('rnaconc', identity_format,'[RNA] ng/uL'),
('mrnad', date_to_link, 'Date mRNA Purified'),
('cdnad': date_to_link, 'Date cDNA Synthesized'),
('indexnum': identity_format, 'Index'),
('sentd': date_to_link, 'Date sent to Berkeley'),
('sample': identity_format, 'Sample ID'),
('berkid': identity_format, 'Berkeley ID'),
('qubit': identity_format, 'Qubit (ng/uL)'),
('bioan_pdf': bioanalyzer_pdf_link, 'Bioan pdf'),
('seqd': date_to_link, 
'thawed': identity_format
}
