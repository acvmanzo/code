-- SQL code used for manipulating and querying a database with information
-- about RNASeq samples.

--CREATE TABLE autin_bad
--(
  --genotype character varying(80) NOT NULL,
  --tube integer NOT NULL,
  --sex character varying(80) NOT NULL,
  --frozend date NOT NULL,
  --rnad date,
  --rnaconc real,
  --mrnad date,
  --cdnad date,
  --indexnum integer,
  --sample character varying(80),
  --seqd date,
  --thawed integer,
  --toseq boolean,
  --CONSTRAINT autin_bad_pkey PRIMARY KEY (genotype, tube, sex, frozend)
--);

----\copy (select * from autin order by rnad, genotype, sex) TO '/home/andrea/Documents/lab/postgres/2014-0401_autindb_copy.csv' csv;

--DROP TABLE autin;
--CREATE TABLE autin
--(
  --genotype character varying(80) NOT NULL,
  --tube integer NOT NULL,
  --sex character varying(80) NOT NULL,
  --frozend date NOT NULL,
  --rnad date,
  --rnaconc real,
  --mrnad date,
  --cdnad date,
  --indexnum integer,
  --sample character varying(80),
  --seqd date,
  --thawed integer,
  --toseq boolean,
  --samplenum int PRIMARY KEY,
  --berkid varchar(10),
  --sentd date,
  --qbitngul real,
  --qbitd date,
  --seq_received boolean,
  --use_seq boolean
  --UNIQUE (genotype, tube, sex, frozend)
--);

-- TO COPY TABLE TO A FILE
--\copy (select * from autin) TO '/home/andrea/Documents/lab/postgres/2014-0403_autindb_copy_nosn.csv' header csv;

-- TO COPY TABLE FROM A FILE
--\copy autin from '/home/andrea/Documents/lab/postgres/2014-0403_autindb_copy_newsn.csv' header csv;

-- TO ADD A COLUMN
--ALTER TABLE autin ADD COLUMN qubit_ng_uL real;
--ALTER TABLE autin ADD COLUMN qubitd date;

-- TO ADD A SEQUENCE FOR USE AS PRIMARY ID
--DROP SEQUENCE samplenum_seq;
--CREATE SEQUENCE samplenum_seq START 1042;
--ALTER TABLE autin ALTER samplenum SET DEFAULT NEXTVAL('samplenum_seq');


--
-- CREATE TABLE autberkeley
-- (
  -- berkid character varying(80),
  -- sample character varying(80),
  -- indexnum character varying(80),
  -- indexseq character varying(80),
  -- sentd date,
  -- CONSTRAINT autberkeley_pkey PRIMARY KEY (berkid)
-- );

--\copy autberkeley from '/home/andrea/Documents/lab/RNAseq/berkeley_orders/2014-0218_samples_date.csv' with csv header delimiter as ',';
--\copy autberkeley from '/home/andrea/Documents/lab/RNAseq/berkeley_orders/2014-0311_samples_date.csv' with csv header delimiter as ',';
--\copy autberkeley from '/home/andrea/Documents/lab/RNAseq/berkeley_orders/2014-0320_samples_date.csv' with csv header delimiter as ',';
--\copy autberkeley from '/home/andrea/Documents/lab/RNAseq/berkeley_samples_sent/2014-0403/2014-04-03_samples_to_send.csv' with csv header delimiter as ',';
-- \copy autberkeley from '/home/andrea/Documents/lab/RNAseq/berkeley_samples_sent/2014-0507/2014-05-07_RGAM_samples.csv' with csv header delimiter as ',';


--CREATE TABLE autqubit
--(
  --berkid character varying(80),
  --qubit real,
  --qubitd date,
  --CONSTRAINT autqubit_pkey PRIMARY KEY (berkid)
--);

--\copy autqubit from '/home/andrea/Documents/lab/RNAseq/qubit/2014-0317_qubit_date.csv' with csv header delimiter as ',';
--\copy autqubit from '/home/andrea/Documents/lab/RNAseq/qubit/2014-0324_qubit_date.csv' with csv header delimiter as ',';
--\copy autqubit from '/home/andrea/Documents/lab/RNAseq/qubit/2014-0324_qubit_date.csv' with csv header delimiter as ',';


-- CREATE TABLE index_numseq(
    -- indexnum int,
    -- indexseq varchar(40),
    -- CONSTRAINT index_numseq_pkey PRIMARY KEY (indexnum, indexseq)
-- );

-- \copy index_numseq from '/home/andrea/Documents/lab/RNAseq/misc/indexnum_indexseq.csv' csv;

-- TO DETERMINE WHICH INDEX NUMBERS AND SEQUENCES ARE USED IN SAMPLES YET TO BE SEQUENCED
-- SELECT berkid, sample, autin.indexnum, indexseq 
-- FROM autin
    -- left outer join index_numseq ON (autin.indexnum = index_numseq.indexnum)
    -- WHERE seqd is Null
    -- ORDER BY berkid;

--CREATE VIEW fullautdb AS
    --select autin.sample, autberkeley.berkid, genotype, sex, frozend, rnad, rnaconc, mrnad, cdnad, sentd, seqd, autin.indexnum, qubit, thawed
    --from autin 
        --left outer join autberkeley on (autin.sample = autberkeley.sample) 
        --left outer join autqubit on (autberkeley.berkid = autqubit.berkid)
    --order by rnad;

--CREATE OR REPLACE VIEW autdbwiki AS
    --select samplenum, genotype, sex, frozend, rnad, rnaconc, mrnad, cdnad, autin.indexnum, indexseq, sentd, autin.sample, autberkeley.berkid, qubit, qubitd, toseq, seqd, thawed
    --from autin 
        --left outer join autberkeley on (autin.sample = autberkeley.sample) 
        --left outer join autqubit on (autberkeley.berkid = autqubit.berkid)
    --order by rnad;

-- Without autberkeley

--CREATE OR REPLACE VIEW autdbwiki AS
    --select samplenum, genotype, sex, frozend, rnad, rnaconc, mrnad, cdnad, autin.indexnum, sentd, sample, autin.berkid, qubit, qubitd, toseq, seqd, thawed
    --from autin 
        --left outer join autqubit on (autin.berkid = autqubit.berkid)
    --order by rnad;


--\copy (select genotype, sex, frozend, rnad, rnaconc, mrnad, cdnad, indexnum, sentd, sample, berkid, qubit, seqd, thawed from autdbwiki) TO '/home/andrea/Documents/lab/postgres/20140321_autdb_wiki.csv' csv;



--CREATE TABLE index_numseq
--(
    --indexnum int PRIMARY KEY,
    --indexseq varchar(80),
--);

-- Creates a view with information for Berkeley.
-- CREATE VIEW berkeley_order AS
    -- select samplenum, sample, autin.indexnum, index_numseq.indexseq, cdnad
    -- from autin
        -- left outer join index_numseq on (autin.indexnum = index_numseq.indexnum)
    -- order by samplenum

-- Creates a view with information on sample and indexnum.
-- DROP VIEW berkindex;
-- CREATE VIEW berkindex AS
    -- select berkid, sample, frozend, mrnad, cdnad, autin.indexnum, index_numseq.indexseq, seqd 
    -- from autin
        -- left outer join index_numseq on (autin.indexnum = index_numseq.indexnum)


---- TRIGGER FUNCTION FOR UPDATING A VIEW
--CREATE OR REPLACE FUNCTION update_autdbwiki_view() RETURNS TRIGGER AS $$
    --BEGIN

        --IF (TG_OP = 'UPDATE') THEN
            --UPDATE autin SET sample = NEW.sample WHERE genotype=OLD.genotype AND tube=OLD.tube AND sex=OLD.sex AND frozend=OLD.frozend;
            --IF NOT FOUND THEN RETURN NULL; 
            --RETURN NEW;
            --END IF;
        --END IF; 
    --END;
--$$ LANGUAGE plpgsql;

--CREATE TRIGGER update_sample
--INSTEAD OF UPDATE ON autdbwiki
    --FOR EACH ROW EXECUTE PROCEDURE update_autdbwiki_view();



-- TO DECIDE WHAT FLIES TO EXTRACT RNA FROM NEXT:
-- select genotype, sex,  sample, frozend, tube, rnad, rnaconc, cdnad from autin where sex = 'F' ORDER BY genotype, sex, sample;


---- TO INSERT NEW SAMPLES INTO AUTIN AFTER RNA EXTRACTION:
-- INSERT INTO autin (genotype, tube, sex, frozend, rnad, rnaconc) VALUES
    -- ('NrxIV', '2', 'M', '2014-02-16', '2014-05-28', 72.6),
    -- ('CS', '1', 'M', '2014-02-28', '2014-05-28', 69.8),
    -- ('Nhe3', '1', 'M', '2014-03-04', '2014-05-28', 71.2),
    -- ('NrxI', '1', 'M', '2014-03-10', '2014-05-28', 73);
    -- ('NrxIV', '2', 'F', '2014-02-13', '2014-04-30', 96.1),
    -- ('Nhe3', '3', 'F', '2014-03-04', '2014-04-30', 126.1)
    -- ('NrxIV', '3', 'F', '2014-02-13', '2014-04-22', 79.5), 
    -- ('en', '1', 'F', '2014-02-20', '2014-04-22', 91.9), 
    -- ('Nhe3', '1', 'F', '2014-03-02', '2014-04-22', 127),
    -- ('pten', '5', 'M', '2013-09-24', '2014-04-22', 68.9);
    -- ('Nhe3', '2', 'M', '2014-03-04', '2014-06-16', 90.6),
    -- ('CS', '1', 'M', '2014-02-24', '2014-06-16', 95.1);


---- TO ADD MRNAD VALUES:
-- UPDATE autin SET mrnad = '2014-05-29' WHERE rnad = '2014-05-28';
-- UPDATE autin SET mrnad = '2014-04-23' where rnad = '2014-04-21' and (genotype = 'Betaintnu' or genotype = 'NrxI' or genotype = 'pten');
-- UPDATE autin SET mrnad = '2014-04-23' where rnad = '2014-04-22' and genotype = 'en';
-- UPDATE autin SET mrnad = '2014-06-17' where rnad = '2014-06-16' and (genotype = 'CS' or genotype = 'Nhe3');


---- TO ADD CDNAD VALUES
-- UPDATE autin SET cdnad = '2014-05-30' where mrnad = '2014-05-29';
-- UPDATE autin SET cdnad = '2014-06-18' where mrnad = '2014-06-17';



---- TO DECIDE WHICH INDICES TO USE:
-- select genotype, berkid, sample, sentd, cdnad, seqd, toseq, indexnum from autin where seqd IS Null order by sentd, indexnum;


---- TO ENTER INDEX NUMBERS:
-- select samplenum, genotype, sex, indexnum, mrnad, cdnad from autin where mrnad = '2014-04-23';
-- UPDATE autin SET indexnum = 48 WHERE samplenum = 1060 AND genotype = 'Nhe3' AND cdnad = '2014-06-18';
-- UPDATE autin SET indexnum = 44 WHERE samplenum = 1062 AND genotype = 'CS' AND cdnad = '2014-06-18';


---- TO ASSIGN SAMPLE NAMES:
-- select samplenum, sample, genotype, sex, indexnum, mrnad, cdnad, sentd from autdbwiki order by genotype, sex, sample;

-- UPDATE autin SET sample = 'NrxIV_MD' WHERE samplenum = 1056 AND genotype = 'NrxIV' AND cdnad = '2014-05-30';
-- UPDATE autin SET sample = 'Nhe3_MD'  WHERE samplenum = 1058 AND genotype = 'Nhe3' AND cdnad = '2014-05-30';
-- UPDATE autin SET sample = 'NrxI_ME' WHERE samplenum = 1059 AND genotype = 'NrxI' AND cdnad = '2014-05-30';
-- UPDATE autin SET sample = 'CS_MD' WHERE samplenum = 1057 AND genotype = 'CS' AND cdnad = '2014-05-30';
-- UPDATE autin SET sample = 'CS_ME' WHERE samplenum = 1062 AND genotype = 'CS' AND cdnad = '2014-06-18';
-- UPDATE autin SET sample = 'Nhe3_ME'  WHERE samplenum = 1060 AND genotype = 'Nhe3' AND cdnad = '2014-06-18';

-- TO COPY SAMPLE AND INDEX INTO A FILE FOR SENDING TO BERKELEY:
-- \copy (select sample, indexnum, indexseq from berkeley_order where cdnad = '2014-06-18' order by indexnum) TO '/home/andrea/Documents/lab/RNAseq/berkeley_samples_sent/2014-0619/2014-06-19_samples_to_send_info_noberkid.csv' header csv;

-- TO COPY BERKELEY ORDER FILES TO THE autberkeley TABLE
-- delete from autberkeley;
-- \copy autberkeley from '/home/andrea/Documents/lab/RNAseq/berkeley_samples_sent/2014-0619/2014-06-19_RGAM_samples.csv' with csv header delimiter as ',';


-- TO ADD INFO FROM BERKELEY ORDER FILES TO AUTIN
-- UPDATE autin SET berkid = autberkeley.berkid FROM autberkeley WHERE autin.sample = autberkeley.sample;
-- UPDATE autin SET sentd = autberkeley.sentd FROM autberkeley WHERE autin.sample = autberkeley.sample;


-- TO ADD INFO FROM BERKELEY QUBIT FILES TO AUTIN
-- \copy autqubit from '/home/andrea/Documents/lab/RNAseq/qubit/2014-0602_qubit_date.csv' with csv header delimiter as ',';
-- \copy autqubit from '/home/andrea/Documents/lab/RNAseq/qubit/2014-0624_qubit_date.csv' with csv header delimiter as ',';

-- UPDATE autin SET qbitngul = autqubit.qubit FROM autqubit WHERE autqubit.berkid = autin.berkid;
-- UPDATE autin SET qbitd = qubitd FROM autqubit WHERE autqubit.berkid = autin.berkid;



---- TO SET ALL 'toseq' VALUES TO 'True' AFTER LOOKING AT BIOANALYZER RESULTS
-- UPDATE autin SET toseq = True WHERE qbitd = '2014-04-09' or qbitd = '2014-04-25';
-- UPDATE autin SET toseq = True WHERE qbitd = '2014-06-02' AND qbitngul > 2;
-- UPDATE autin SET toseq = False WHERE qbitd = '2014-06-02' AND qbitngul < 2;
-- UPDATE autin SET toseq = True WHERE qbitd = '2014-06-24' AND qbitngul > 2;


-- TO ASSIST IN LABELING TUBES FOR BERKELEY:
-- \copy (select berkid, sample, cdnad, genotype, sex from autin where sentd = '2014-05-07' order by cdnad, genotype) TO '/home/andrea/Documents/lab/RNAseq/berkeley_samples_sent/2014-0507/2014-05-07_samples_to_send_info.csv' header csv;


--- TO ASSIST IN ORDERING SAMPLES INTO LANES FOR SEQUENCING:
--select sample, berkid, sentd, indexnum, qubit, toseq from autdbwiki where toseq=True and seqd is null order by indexnum;
--select sample, berkid, sentd, indexnum, qubit, toseq from autdbwiki where toseq=True and seqd is null order by berkid;

--\copy (select berkid, sample, indexnum, indexseq, sentd, toseq from autdbwiki where toseq=True and seqd is null order by berkid) TO '/home/andrea/Documents/lab/RNAseq/2014-0401_samples_to_seq_2.csv' csv;

--- TO SET SEQUENCE DATE
-- see ~/Documents/lab/code/autsql.py

---- TO UPDATE SEQ_RECEIVED WHEN SEQUENCES ARE RECEIVED ----
-- UPDATE autin SET seq_received = True where berkid = 'RGAM014F';
-- UPDATE autin SET seq_received = True where berkid = 'RGAM014A';
-- UPDATE autin SET seq_received = True where berkid = 'RGAM014C';

-- RANDOM COMMANDS
----SELECT genotype, sex,  sample, frozend, rnad, mrnad from autdbwiki where rnad = '2014-03-25'
----EXCEPT 
----SELECT genotype, sex,  sample, frozend, rnad, mrnad from autdbwiki where rnad = '2014-03-25' AND genotype = 'Betaintnu';

-- ADD A COLUMN TO SPECIFY IF I WANT TO USE THE DATA FOR ANALYSIS
-- alter table autin add column use_seq boolean;

-- select sample, berkid, toseq, seqd from autin where seq_received is True order by seqd;
-- update autin set use_seq = True where seq_received = True;
-- update autin set use_seq = False where sample = 'NrxIV_MB';
-- update autin set use_seq = False where sample = 'NrxI_MD';
-- update autin set use_seq = False where sample = 'Nhe3_MC';


