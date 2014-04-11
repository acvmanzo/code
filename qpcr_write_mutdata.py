from libs.qrtpcrlib import batch_write_cqs

batch_write_cqs('.')

DROP TABLE qpcr_mut;

CREATE TABLE qpcr_mut
(  
dataid int PRIMARY KEY, 
exptd date,
exptid varchar (80),
well character varying(80),
target character varying(80),
content character varying(80),
sample character varying(80),
cq real
);


\copy qpcr_mut from '/home/andrea/Documents/lab/qRT-PCR/1_data/2014-0410_allmutdata_fmt.csv' with csv header delimiter as ',';
