

-- Creating a foreign database wrapper so that I can access the data in the
-- autin table from the rnaseq database.

-- CREATE EXTENSION postgres_fdw;
-- create server andreaserver FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'andrea');
-- create user mapping for andrea server andreaserver options (user 'andrea');

-- -- Copied from the last dump.
-- CREATE FOREIGN TABLE autin (
    -- genotype character varying(80) NOT NULL,
    -- tube integer,
    -- sex character varying(80) NOT NULL,
    -- frozend date NOT NULL,
    -- rnad date,
    -- rnaconc real,
    -- mrnad date,
    -- cdnad date,
    -- indexnum integer,
    -- sample character varying(80),
    -- seqd date,
    -- thawed integer,
    -- toseq boolean,
    -- samplenum integer,
    -- berkid character varying(10),
    -- sentd date,
    -- qbitngul real,
    -- qbitd date
-- )
-- SERVER andreaserver;

-- -- To count the number of rows in a select query:
-- select count (*) from (select autin.berkid from cuff_genes_fpkm_rgam009b inner join autin on (autin.berkid = cuff_genes_fpkm_rgam009b.sample)) as foo;

-- To join tables for correlation tests.
SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status,
t1.berkid, t2.berkid, a1.sample, a2.sample
FROM 
    cuff_genes_fpkm_rgam009b as t1 INNER JOIN autin as a1 using (berkid)
    INNER JOIN 
    cuff_genes_fpkm_rgam010f as t2 INNER JOIN autin as a2 using (berkid)
    USING (tracking_id) 
WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' 
ORDER BY tracking_id;

-- To check the # of rows in the joined table.
select count (*) from (
SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status,
t1.berkid, t2.berkid, a1.sample, a2.sample
FROM 
    cuff_genes_fpkm_rgam009b as t1 INNER JOIN autin as a1 using (berkid)
    INNER JOIN 
    cuff_genes_fpkm_rgam010f as t2 INNER JOIN autin as a2 using (berkid)
    USING (tracking_id) 
WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' 
ORDER BY tracking_id) as foo;
