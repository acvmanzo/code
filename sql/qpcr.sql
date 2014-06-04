-- SQL code for manipulating/querying tables containing qRT-PCR data.

--drop table qpcr_primers;

--CREATE TABLE qpcr_primers
--(
  --gene character varying(80),
  --primer character varying(80),
  --database character varying(80),
  --primer_num character varying(80),
  --after_insert character varying(80),
  --results character varying(80),
  --goodmelt Boolean,
  --used_primer Boolean,
  --fwd_pr_seq character varying(80),
  --fwd_pr_tm real,
  --rev_pr_seq character varying(80),
  --rev_pr_tm real,
  --amplicon_len int,
  --isoforms character varying(80),
  --spans_exons Boolean,
  --FlyBase_release character varying(80),
  --amplicon_seq character varying(500),
  --CONSTRAINT qpcr_primers_pkey PRIMARY KEY (fwd_pr_seq, rev_pr_seq)
--);

--\copy qpcr_primers from '/home/andrea/Documents/lab/qRT-PCR/db_importing/all_primers_for_db.csv' with csv header delimiter as ',';






--drop table qpcr_experiments;

--CREATE TABLE qpcr_experiments
--(
  --exptd date,
  --bywho character varying(80),
  --filename character varying(80),
  --expt character varying(80),
  --primer character varying(80),
  --controls character varying(80),
  --usedata Boolean,
  --notes character varying(500),
  --CONSTRAINT qpcr_experiments_pkey PRIMARY KEY (filename, primer)
--);

--\copy qpcr_experiments from '/home/andrea/Documents/lab/qRT-PCR/db_importing/qrtpcr_expts_byprimer.csv' with csv header delimiter as ',';


--select gene, qpcr_primers.primer, exptd, filename, expt, bywho 
--from qpcr_primers
   --right outer join qpcr_experiments on (qpcr_primers.primer = qpcr_experiments.primer)
--where expt = 'sc' and usedata = 'True'
--order by gene, qpcr_primers.primer;

--INSERT INTO qpcr_experiments VALUES
    --('2014-03-28', 'Andrea', '2014-0328_testmut_bintnu_en_-RT_run_2', 'mut', 'Bintnu-GP1', 'NTC; NRT for each primer', True, 'Only data from wells A-D1 and F-H1 can be used at the moment because GAPDH showed 2 peaks.'),
    --('2014-03-28', 'Andrea', '2014-0328_testmut_bintnu_en_-RT_run_2', 'mut', 'Diana', 'NTC; NRT for each primer', True, 'GAPDH showed 2 peaks.'),
    --('2014-03-28', 'Andrea', '2014-0328_testmut_bintnu_en_-RT_run_2', 'mut', 'Dhruv', 'NTC; NRT for each primer', True, 'Fine'),
    --('2014-03-28', 'Andrea', '2014-0328_testmut_bintnu_en_-RT_run_2', 'mut', 'Ralph', 'NTC; NRT for each primer', True, 'No amplification');



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


-- SELECT target, cq, dataid, sample FROM qpcr_mut 
    -- WHERE exptd = '2013-10-29' AND target = 'GAPDH' AND dataid <1034 AND sample != 'NT' AND sample IS NOT NULL    
    -- ORDER BY sample;
