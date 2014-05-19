

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
-- SELECT t1.tracking_id, t1.berkid, a1.sample, t1.fpkm, t1.fpkm_status, t2.berkid,
-- a2.sample, t2.fpkm, t2.fpkm_status
-- FROM 
    -- cuff_genes_fpkm_rgam009b as t1 INNER JOIN autin as a1 using (berkid)
    -- FULL OUTER JOIN
    -- cuff_genes_fpkm_rgam010f as t2 INNER JOIN autin as a2 using (berkid)
    -- USING (tracking_id) 
-- WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' 
-- ORDER BY tracking_id;

-- -- To check the # of rows in the joined table.
-- select count (*) from (
-- SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status,
-- t1.berkid, t2.berkid, a1.sample, a2.sample
-- FROM 
    -- cuff_genes_fpkm_rgam009b as t1 INNER JOIN autin as a1 using (berkid)
    -- FULL OUTER JOIN 
    -- cuff_genes_fpkm_rgam010f as t2 INNER JOIN autin as a2 using (berkid)
    -- USING (tracking_id) 
-- WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' 
-- ORDER BY tracking_id) as foo;

-- # of rows in the joined tables are different from the single tables because
-- not all the fpkms are 'OK'. Because I ran the function without looking for
-- novel transcripts and with reference to the genome, the number of rows in the
-- single tables are the same.


-- For looking at correlation between CLCBio and Tophat.
-- DROP TABLE clcbio_rgam009b;
-- CREATE TABLE clcbio_rgam009b (
    -- feature_id varchar(200),
    -- rpkm double precision
-- );

-- \copy clcbio_rgam010f from '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/clc_results/RGAM010F_RNA-Seq_rpkm.txt'; 

-- \copy clcbio_rgam009b from '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/clc_results/CS_MB_RGAM009B_RNA-Seq_rpkm.txt';

-- Notes:
-- Correlation between clc and th is off; th seems to assign higher fpkms than
-- clc. Doing it again excluding the samples where th gives an fpkm of 0 and clc
-- gives an fpkm of not 0. Saved results in folder 
-- savefigdir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations_clc_th_cond1'



-- CREATE TABLE cufflinks_data (
    -- tracking_id character varying(20),
    -- class_code character varying(2),
    -- nearest_ref_id character varying(2),
    -- gene_id character varying(20),
    -- gene_short_name character varying(100),
    -- tss_id character varying(2),
    -- locus character varying(100),
    -- length character varying(2),
    -- coverage character varying(2),
    -- FPKM double precision ,
    -- FPKM_conf_lo double precision,
    -- FPKM_conf_hi double precision,
    -- FPKM_status character varying(5),
    -- berkid character varying(20));

SELECT COUNT (*) FROM (
SELECT t0.tracking_id, t0.berkid, t0.fpkm, t0.fpkm_status, t1.berkid, t1.fpkm, t1.fpkm_status 
    FROM cufflinks_data as t0 
        FULL OUTER JOIN 
        cufflinks_data as t1 
            USING (tracking_id)
            WHERE t0.berkid = 'RGAM009B' AND t1.berkid = 'RGAM010F' 
            AND t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK' 
            ORDER BY tracking_id
            ) as foo
            ;