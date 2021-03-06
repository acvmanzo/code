# Combines qPCR data into one file and copies it into the SQL table qpcr_mut

import os
import psycopg2
from libs.qrtpcrlib import combinedata


DIRNAME = os.path.dirname(os.path.abspath('.')) + '/' 
GFILENAME =  '2014-0410_allmutdata_fmt.csv'
gname = DIRNAME + GFILENAME
combinedata(gname)

conn = psycopg2.connect("dbname=andrea user=andrea")
cur = conn.cursor()

cur.execute("DROP TABLE qpcr_mut; CREATE TABLE qpcr_mut (dataid int PRIMARY KEY, exptd date, exptid varchar (80), well character varying(80), target character varying(80), content character varying(80), sample character varying(80), cq real );")

cur.execute("\copy qpcr_mut from '{0}' with csv header delimiter as ',';".format(gname))
