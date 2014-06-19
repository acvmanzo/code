-- SQL code for manipulating/testing tables in the rnaseq database.

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


-- To join tables for correlation tests (double join method)

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


-- Create one table to contain all the cufflinks mapping data
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

-- SELECT COUNT (*) FROM (
-- SELECT t0.tracking_id, t0.berkid, t0.fpkm, t0.fpkm_status, t1.berkid, t1.fpkm, t1.fpkm_status 
    -- FROM cufflinks_data as t0 
        -- FULL OUTER JOIN 
        -- cufflinks_data as t1 
            -- USING (tracking_id)
            -- WHERE t0.berkid = 'RGAM009B' AND t1.berkid = 'RGAM010F' 
            -- AND t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK' 
            -- ORDER BY tracking_id
            -- ) as foo
 --            ;


-- Create a table of protein-coding genes; output of QueryBuilder on Flybase where I selected genes
-- that matched the class 'protein_coding_genes'

-- CREATE TABLE prot_coding_genes (
    -- tracking_id character varying(20),
    -- gene_long_name character varying(100),
    -- gene_short_name character varying(100)
-- );

-- Copy into table.
-- \copy prot_coding_genes from '/home/andrea/rnaseqanalyze/references/protein_coding_genes/flybase_results_protein_coding_genes_dmel_symbol.txt';

-- create view test as select t0.tracking_id, t0.berkid as berkid0, t0.fpkm as fpkm0, t1.berkid as berkid1, t1.fpkm as fpkm1 from cufflinks_data as t0 full outer join cufflinks_data as t1 using (tracking_id) where t0.berkid = 'RGAM009G' and t1.berkid = 'RGAM011A' and t0.tracking_id != '' and t0.fpkm_status = 'OK' and t1.fpkm_status = 'OK' order by tracking_id;

-- Testing code for doing a join with the protein_coding_genes table
-- select count (*) from (
-- select t0.tracking_id, t0.berkid as berkid0, t0.fpkm as fpkm0, t1.berkid as berkid1, t1.fpkm as fpkm1 
    -- from 
        -- cufflinks_data as t0 
        -- full outer join 
        -- cufflinks_data as t1 
            -- using (tracking_id)
        -- inner join
        -- prot_coding_genes as t2 
            -- using (tracking_id)
        -- where t0.berkid = 'RGAM009G' and t1.berkid = 'RGAM011A' and t0.tracking_id != '' and t0.fpkm_status = 'OK' and t1.fpkm_status = 'OK' 
            -- order by tracking_id
-- ) as foo
-- ;


-- Create one table to contain all the cufflinks mapping data
-- CREATE TABLE clc_data (
    -- gene_short_name character varying(100),
    -- exp_vale double precision,
    -- trans_annot int,
    -- trans_detected int,
    -- exon_length int,
    -- unique_gene_reads int,
    -- tot_gene_reads int,
    -- unique_exon_reads int,
    -- tot_exon_reads int,
    -- ratio_exon_reads real,
    -- unique_exon_exon_reads int,
    -- total_exon_exon_reads int,
    -- unique_intron_exon_reads int,
    -- total_intron_exon_reads int,
    -- exons int,
    -- put_exons int,
    -- rpkm double precision,
    -- med_cov real,
    -- chrom varchar(200),
    -- chrom_start int,
    -- chrom_end int,
    -- berkid varchar(20)
-- );

-- Testing using htseq and SERE
-- CREATE TABLE htseq (
    -- gene_name varchar(100),
    -- counts int,
    -- berkid varchar(20)
-- );

-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGAM009H/tophat_out/htseq_results_edit_berkid.txt';
-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGAM009D/tophat_out/htseq_results_edit_berkid.txt';
-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ006H/tophat_out/htseq_results_edit_berkid.txt';
-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ007D/tophat_out/htseq_results_edit_berkid.txt';

-- select count (*) from (
-- \copy (select t0.gene_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq as t0 inner join htseq as t1 using (gene_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_name) TO '/home/andrea/bookmarks/analysis/cg34127m_htseq_test.txt';
-- ) as foo
-- ;

-- \copy prot_coding_genes  to '/home/andrea/bookmarks/analysis/test.txt';

-- DROP TABLE htseq_gene;
-- CREATE TABLE htseq_gene (
    -- gene_short_name varchar(100),
    -- counts int,
    -- berkid varchar(20)
-- );

-- \copy htseq_gene from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ007D/tophat_out/htseq_results_edit_gene_berkid.txt';
-- \copy htseq_gene from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ006H/tophat_out/htseq_results_edit_gene_berkid.txt';

-- \copy (select t0.gene_short_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq_gene as t0 inner join htseq_gene as t1 using (gene_short_name) inner join prot_coding_genes as t2 using (gene_short_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_short_name) TO '/home/andrea/bookmarks/analysis/cg34127m_htseq_test_pcg.txt';
-- select t0.gene_short_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq_gene as t0 inner join htseq_gene as t1 using (gene_short_name) inner join prot_coding_genes as t2 using (gene_short_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_short_name; 
-- select t0.gene_short_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq_gene as t0 inner join htseq_gene as t1 using (gene_short_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_short_name; 


-- Creates a table with the alignment stats from clc and tophat mapping; files used to populate the table are output by the script align_summary.py
-- DROP TABLE aligninfo;
-- CREATE TABLE aligninfo (
    -- berkid varchar(20),
    -- sample varchar(20),
    -- input int,
    -- mapped int,
    -- pmapped real,
    -- multimapped int,
    -- pmulti real,
    -- aligner varchar(40)
-- );

-- \copy aligninfo from '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat/tophat_all_align_summarywithal.txt';
-- \copy aligninfo from '/home/andrea/Documents/lab/RNAseq/analysis/CLC_results/clc_all_align_summarywithal.txt';

-- \copy (select t0.berkid, t0.sample, t1.input as total_sequenced_reads, t0.mapped as clc_mapped, t1.mapped as th_mapped, t1.mapped-t0.mapped as diff_thmap_clcmap, t0.pmapped as clc_percent_mapped, t1.pmapped as th_percent_mapped, t0.mapped-t0.multimapped as clc_unique, (t0.mapped-t0.multimapped)/t1.input::float as clc_ratio_totalseq_unique, t1.mapped-t1.multimapped as th_unique, (t1.mapped-t1.multimapped)/t1.input::float as th_ratio_totalseq_unique from aligninfo as t0 inner join aligninfo as t1 using (berkid) where t0.aligner = 'clc' and t1.aligner = 'tophat' order by sample) to 'clc_tophat_mapping.csv' csv header;


-- Creates a table for the DE gene data.
-- DROP TABLE degenes;
-- CREATE TABLE degenes (
    -- gene varchar(100),
    -- logfc double precision,
    -- logcpm double precision,
    -- pvalue double precision, 
    -- fdr double precision,
    -- tool varchar(40),
    -- group1 varchar(50),
    -- group2 varchar(50),
    -- UNIQUE (gene, group1, group2)
-- );

-- \copy (select * from degenes where group1 = 'lowagg' and group2 = 'normagg' and fdr < 0.05) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/lowagg_vs_normagg_CS/toptags_edgeR_fdr05.csv' csv header;
-- \copy (select * from degenes where group1 = 'CG34127_M' and group2 = 'CS_M' and fdr < 0.05) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/CG34127_M/toptags_edgeR_fdr05.csv' csv header;


-- select t0.gene, t0.group1, 2^t0.logfc as foldchange, t1.group1, 2^t1.logfc as foldchange
-- select t0.gene
    -- from degenes as t0 
        -- inner join 
        -- degenes as t1 
        -- using (gene)
        -- inner join
        -- degenes as t2
        -- using (gene) 
        -- inner join
        -- degenes as t3
        -- using (gene) 
    -- where 
    -- t0.group1 = 'en_M' and t1.group1 = 'CG34127_M' and t2.group1 = 'NrxI_M' and t3.group1 = 'pten_M' and
    -- t0.group1 = 'en_M' and t1.group1 = 'CG34127_M' and t2.group1 = 'NrxI_M' and t3.group1 = 'pten_M' and
    -- t0.fdr < 0.05 and t1.fdr < 0.05 and t2.fdr < 0.05 and t3.fdr < 0.05
    -- order by gene
-- ;

\copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'CG34127_M' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/CG34127_M/toptags_edgeR_fdr05_fc.csv' csv header ;
\copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'en_M' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/en_M/toptags_edgeR_fdr05_fc.csv' csv header ;
\copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'NrxI_M' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/NrxI_M/toptags_edgeR_fdr05_fc.csv' csv header ;
\copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'lowagg' and group2 = 'normagg' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/lowagg_vs_normagg_CS/toptags_edgeR_fdr05_fc.csv' csv header ;
